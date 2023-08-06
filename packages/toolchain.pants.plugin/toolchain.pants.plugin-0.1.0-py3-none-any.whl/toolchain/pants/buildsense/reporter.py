# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import logging
import os
import re
import socket
import time
from enum import Enum, unique
from pathlib import Path
from threading import Thread
from typing import Dict, Optional

from pants.base.build_environment import get_git
from pants.goal.run_tracker import RunTracker
from pants.option.subsystem import Subsystem

from toolchain.base.datetime_tools import utcnow
from toolchain.pants.auth.store import AuthStore
from toolchain.pants.buildsense.client import BuildSenseClient, WorkUnits
from toolchain.pants.buildsense.common import RunTrackerBuildInfo
from toolchain.pants.buildsense.state import BuildState
from toolchain.pants.common.toolchain_setup import ToolchainSetup

logger = logging.getLogger(__name__)


_CI_MAP = {
    "CIRCLECI": re.compile(r"^CIRCLE.*"),
    "TRAVIS": re.compile(r"^TRAVIS.*"),
    "GITHUB_ACTION": re.compile(r"^GITHUB.*"),
}


@unique
class ReporterState(Enum):
    UNKNOWN = "unknown"
    ENABLED = "enabled"
    DISABLED = "disabled"

    @property
    def is_determined(self) -> bool:
        return self != self.UNKNOWN

    @property
    def is_enabled(self) -> bool:
        return self == self.ENABLED

    @property
    def is_disabled(self) -> bool:
        return self == self.DISABLED


def optional_dir_option(dn: str) -> str:
    # Similar to Pant's dir_option, but doesn't require the directory to exist.
    return os.path.normpath(dn)


class Reporter(Subsystem):
    """Configuration for Toolchain's BuildSense reporting."""

    options_scope = "buildsense"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repo = ToolchainSetup.global_instance().get_repo_name(raise_error=False)
        if not self._repo:
            logger.warning("Couldn't determine repo name. Plugin will be disabled.")
            self._state = ReporterState.DISABLED
            return
        self._state = ReporterState.UNKNOWN
        self._call_count = 0
        self._build_state = None
        self._reporter_thread = ReportThread(self._get_state)

    def _get_state(self) -> ReporterState:
        return self._state

    @classmethod
    def subsystem_dependencies(cls):
        return super().subsystem_dependencies() + (RunTracker, AuthStore, ToolchainSetup)

    @classmethod
    def register_options(cls, register):
        register(
            "--base-url",
            type=str,
            default="https://app.toolchain.com/api/v1/repos/",
            help="Where to make HTTP requests to",
        )
        register(
            "--timeout",
            advanced=True,
            type=int,
            default=5,
            help="Wait at most this many seconds for network calls to complete.",
        )
        register("--dry-run", type=bool, help="Go thru the motions w/o making network calls", default=False)
        register(
            "--local-build-store",
            advanced=True,
            type=bool,
            default=True,
            help="Store failed uploads and try to upload later.",
        )
        register(
            "--local-store-base",
            advanced=True,
            type=optional_dir_option,
            default=".pants.d/toolchain/buildsense/",
            help="Base direcory for storing buildsense data locally",
        )
        register(
            "--max-batch-size-mb",
            advanced=True,
            type=int,
            default=20,
            help="Maximum batch size to try and upload (uncompressed).",
        )
        register(
            "--ci-env-var-pattern",
            advanced=True,
            type=str,
            default=None,
            help="CI Environment variables regex pattern.",
        )

    @classmethod
    def is_active(cls) -> bool:
        return True

    def _lazy_init(self) -> bool:
        if self._state.is_determined:
            return self._state.is_enabled
        if not AuthStore.get_auth_state().is_ok:
            logger.warning("Auth failed - BuildSense plugin is disabled.")
            self._state = ReporterState.DISABLED
            return self._state.is_enabled
        options = self.options
        client = BuildSenseClient.from_options(
            client_options=options, get_access_token_callback=AuthStore.get_access_token, repo=self._repo
        )
        # set self._build_state *before* changing the state.
        self._build_state = BuildState(
            client,
            local_store_base_path=Path(options.local_store_base),
            max_batch_size_mb=options.max_batch_size_mb,
            local_store_enabled=options.local_build_store,
        )
        self._reporter_thread.set_build_state(self._build_state)
        self._state = ReporterState.ENABLED
        self._ci_regex_pattern = re.compile(options.ci_env_var_pattern) if options.ci_env_var_pattern else None
        logger.debug("BuildSense Plugin enabled")
        return self._state.is_enabled

    def handle_workunits(
        self, *, completed_workunits: WorkUnits, started_workunits: WorkUnits, context, finished=False, **kwargs
    ) -> None:
        work_units_map = {wu["span_id"]: wu for wu in (started_workunits or [])}
        work_units_map.update({wu["span_id"]: wu for wu in (completed_workunits or [])})
        if not self._lazy_init():
            return
        self._build_state.set_context(context)
        if self._call_count == 0:
            self._enqueue_initial_report()
        if work_units_map:
            logger.debug(
                f"handle_workunits total={len(work_units_map)} completed={len(completed_workunits)} started={len(started_workunits)} finished={finished}"
            )
            self._build_state.queue_workunits(self._call_count, work_units_map, int(utcnow().timestamp()))
        if finished:
            self._on_finish()
        self._call_count += 1

    def _enqueue_initial_report(self) -> None:
        run_tracker_info = self._get_run_tracker_info()
        logger.debug(f"enqueue_initial_report {run_tracker_info.run_id}")
        self._build_state.queue_initial_report(run_tracker_info)

    def _on_finish(self):
        self._build_state.submit_final_report(self._get_run_tracker_info(), self._call_count)
        self._reporter_thread.stop_thread()

    def _get_run_tracker_info(self) -> RunTrackerBuildInfo:
        run_tracker = RunTracker.global_instance()
        # based on https://github.com/pantsbuild/pants/blob/master/src/python/pants/goal/run_tracker.py#L452
        has_ended = run_tracker.has_ended()
        run_info = run_tracker.run_information()
        _update_run_info(run_info)
        if not has_ended:
            run_info["outcome"] = "NOT_AVAILABLE"
            log_file = None
        else:
            log_file = run_tracker.run_logs_file
        if "parent_build_id" in run_info:
            del run_info["parent_build_id"]
        v2_goals = run_tracker.v2_goals_rule_names

        if v2_goals:
            # We already have this in the service side, maybe migrate it to use a better name. but the name is internal anyway right now.
            run_info["computed_goals"] = list(v2_goals)
        options = run_tracker.get_options_to_record()
        build_stats = {
            "run_info": run_info,
            "recorded_options": options,
        }
        ci_env = _capture_ci_env(os.environ, self._ci_regex_pattern)  # type: ignore[arg-type]
        if ci_env:
            build_stats["ci_env"] = ci_env
        if has_ended:
            build_stats.update(
                {
                    "pantsd_stats": run_tracker.pantsd_scheduler_metrics,
                    "cumulative_timings": run_tracker.cumulative_timings.get_all(),
                }
            )
        return RunTrackerBuildInfo(
            has_ended=has_ended, build_stats=build_stats, log_file=Path(log_file) if log_file else None
        )


class ReportThread:
    def __init__(self, get_state_callback):
        self._build_state = None
        self._get_state_callback = get_state_callback
        self._terminate = False
        self._reporter_thread = Thread(target=self._report_loop, name="buildsense-reporter", daemon=True)
        self._reporter_thread.start()

    def set_build_state(self, build_state: BuildState) -> None:
        self._build_state = build_state

    def stop_thread(self):
        self._terminate = True
        self._reporter_thread.join()

    def _report_loop(self):
        while not self._terminate:
            state = self._get_state_callback()
            if state.is_disabled:
                return
            if state.is_enabled and self._build_state.send_report():
                # If we send something in this call, then we don't need to sleep.
                continue
            time.sleep(0.05)
        self._build_state.send_final_report()


def _get_pattern(env: Dict[str, str]) -> Optional[re.Pattern]:
    for ci_name, capture_expression in _CI_MAP.items():
        if ci_name in env:
            return capture_expression
    return None


def _capture_ci_env(env: Dict[str, str], pattern: Optional[re.Pattern]) -> Optional[Dict[str, str]]:
    pattern = pattern or _get_pattern(env)
    if not pattern:
        return None
    return {key: value for key, value in env.items() if pattern.match(key)}


def _is_docker() -> bool:
    # Based on https://github.com/jaraco/jaraco.docker/blob/master/jaraco/docker.py
    # https://stackoverflow.com/a/49944991/38265
    cgroup = Path("/proc/self/cgroup")
    return Path("/.dockerenv").exists() or (cgroup.exists() and "docker" in cgroup.read_text("utf-8"))


def _update_run_info(run_info: dict) -> None:
    scm = get_git()
    revision = scm.commit_id
    host = socket.gethostname()
    machine = f"{host} [docker]" if _is_docker() else host
    run_info.update(machine=machine, revision=scm.commit_id, branch=scm.branch_name or revision)
