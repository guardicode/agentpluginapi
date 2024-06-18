from pathlib import PurePosixPath

import pytest

from agentpluginapi import DropperExecutionMode, LinuxRunOptions, LinuxSetPermissionsOptions


@pytest.mark.parametrize(
    "dropper_execution_mode", [DropperExecutionMode.NONE, DropperExecutionMode.SCRIPT]
)
def test_linux_run_options(dropper_execution_mode: DropperExecutionMode):
    with pytest.raises(ValueError):
        LinuxRunOptions(
            agent_destination_path=PurePosixPath("/tmp/agent"),
            dropper_execution_mode=dropper_execution_mode,
            dropper_destination_path=PurePosixPath("/tmp/dropper"),
        )


@pytest.mark.parametrize("permissions", [0o1000, -0o1])
def test_linux_permissions_options(permissions: int):
    with pytest.raises(ValueError):
        LinuxSetPermissionsOptions(
            agent_destination_path=PurePosixPath("/tmp/agent"),
            permissions=permissions,
        )


def test_linux_otp_present_for_dropper_script():
    with pytest.raises(ValueError):
        LinuxRunOptions(
            agent_destination_path=PurePosixPath("/tmp/agent"),
            dropper_execution_mode=DropperExecutionMode.SCRIPT,
            dropper_destination_path=PurePosixPath("/tmp/dropper"),
            include_otp=False,
        )
