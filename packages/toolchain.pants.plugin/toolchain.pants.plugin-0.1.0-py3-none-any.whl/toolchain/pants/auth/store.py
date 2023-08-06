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
from typing import Optional

from pants.option.global_options import GlobalOptions
from pants.option.subsystem import Subsystem

from toolchain.pants.auth.client import AuthClient, AuthError, AuthState, AuthToken
from toolchain.pants.common.toolchain_setup import ToolchainSetup

_logger = logging.getLogger(__name__)


def optional_file_option(fn: str) -> str:
    # Similar to Pant's file_option, but doesn't require the file to exist.
    return os.path.normpath(fn)


class AuthStore(Subsystem):
    """Setup for authentication with Toolchain."""

    options_scope = "auth"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_options = None
        self._access_token: Optional[AuthToken] = None

    @classmethod
    def subsystem_dependencies(cls):
        return super().subsystem_dependencies() + (GlobalOptions, ToolchainSetup)

    @classmethod
    def register_options(cls, register):
        register(
            "--auth-file",
            type=optional_file_option,
            help="Relative path (relative to the build root) for where to store and read the auth token",
        )
        register("--from-env-var", type=str, default=None, help="Loads the access token from an environment variable")
        register("--base-url", type=str, help="auth app base url", default="https://app.toolchain.com/api/v1")
        register("--ci-env-variables", type=list)
        register("--org", type=str, default=None, help="organization slug for public repo PRs")

    @property
    def _repo_slug(self) -> Optional[str]:
        if not self.options.org:
            return None
        repo = ToolchainSetup.global_instance().options.repo
        return f"{self.options.org}/{repo}"

    def get_auth_options(self, pants_bin_name: str) -> AuthClient:
        if self._auth_options is None:
            opts = self.options
            self._auth_options = AuthClient.create(
                pants_bin_name=pants_bin_name,
                base_url=opts.base_url,
                auth_file=opts.auth_file,
                env_var=opts.from_env_var,
                ci_env_vars=tuple(opts.ci_env_variables),
                repo_slug=self._repo_slug,
            )
        return self._auth_options

    def _get_access_token(self) -> AuthToken:
        pants_bin_name = GlobalOptions.global_instance().options.pants_bin_name
        auth_options = self.get_auth_options(pants_bin_name)
        access_token = self._access_token
        if access_token and not access_token.has_expired():
            return access_token
        self._access_token = auth_options.acquire_access_token()
        return self._access_token

    @classmethod
    def get_access_token(cls) -> AuthToken:
        instance: AuthStore = cls.global_instance()
        return instance._get_access_token()

    @classmethod
    def get_auth_state(cls) -> AuthState:
        try:
            cls.get_access_token()
        except AuthError as error:
            _logger.warning(f"Error loading access token: {error!r}")
            return error.get_state()
        return AuthState.OK
