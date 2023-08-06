# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from pants.engine.rules import SubsystemRule

from toolchain.pants.buildsense.reporter import Reporter


def rules():
    return (SubsystemRule(Reporter),)
