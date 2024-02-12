from pathlib import PurePosixPath

import pytest

from agentpluginapi import DropperExecutionMode, LinuxRunOptions


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
