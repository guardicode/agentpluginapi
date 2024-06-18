from pathlib import PureWindowsPath

import pytest

from agentpluginapi import DropperExecutionMode, WindowsRunOptions, WindowsShell


@pytest.mark.parametrize(
    "dropper_execution_mode", [DropperExecutionMode.NONE, DropperExecutionMode.SCRIPT]
)
def test_windows_run_options(dropper_execution_mode: DropperExecutionMode):
    with pytest.raises(ValueError):
        WindowsRunOptions(
            agent_destination_path=PureWindowsPath("C:\\agent.exe"),
            dropper_execution_mode=dropper_execution_mode,
            shell=WindowsShell.CMD,
            dropper_destination_path=PureWindowsPath("C:\\Windows\\dropper.exe"),
        )


def test_windows_otp_present_for_dropper_script():
    with pytest.raises(ValueError):
        WindowsRunOptions(
            agent_destination_path=PureWindowsPath("C:\\agent.exe"),
            dropper_execution_mode=DropperExecutionMode.SCRIPT,
            shell=WindowsShell.CMD,
            dropper_destination_path=PureWindowsPath("C:\\Windows\\dropper.exe"),
            add_otp=False,
        )
