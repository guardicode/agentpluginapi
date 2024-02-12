from pathlib import PurePosixPath

import pytest

from agentpluginapi import DropperExecutionMode, LinuxRunOptions


def test_linux_run_options():
    with pytest.raises(ValueError):
        LinuxRunOptions(
            agent_destination_path=PurePosixPath("/tmp/agent"),
            dropper_execution_mode=DropperExecutionMode.NONE,
            dropper_destination_path=PurePosixPath("/tmp/dropper"),
        )
