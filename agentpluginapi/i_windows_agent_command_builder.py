import abc
from enum import Enum, auto
from pathlib import PureWindowsPath
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel
from pydantic import model_validator

from .dropper_execution_mode import DropperExecutionMode


class WindowsDownloadMethod(Enum):
    WEB_REQUEST = auto()
    WEB_CLIENT = auto()


class WindowsShell(Enum):
    CMD = auto()
    POWERSHELL = auto()


class WindowsDownloadOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PureWindowsPath
    download_method: WindowsDownloadMethod
    download_url: str


class WindowsRunOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PureWindowsPath
    dropper_execution_mode: DropperExecutionMode
    shell: WindowsShell
    dropper_destination_path: Optional[PureWindowsPath] = None
    include_otp: bool = True

    @model_validator(mode="after")
    def check_dropper_execution(self) -> "WindowsRunOptions":
        if (
            self.dropper_destination_path is not None
            and self.dropper_execution_mode != DropperExecutionMode.DROPPER
        ):
            raise ValueError(
                "Dropper execution mode must be DropperExecutionMode.DROPPER if "
                "dropper_destination_path is None"
            )
        return self

    @model_validator(mode="after")
    def check_otp(self) -> "WindowsRunOptions":
        if not self.include_otp and self.dropper_execution_mode == DropperExecutionMode.SCRIPT:
            raise ValueError(
                "OTP must be passed when running the dropper script, because "
                "there's no other secure way to pass it"
            )
        return self


class IWindowsAgentCommandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_download_command(self, download_options: WindowsDownloadOptions):
        """
        Build Agent's download command

        :param download_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_run_command(self, run_options: WindowsRunOptions):
        """
        Builds Agent's run command

        :param run_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def get_command(self) -> str:
        """
        Gets the resulting command
        """

    @abc.abstractmethod
    def reset_command(self):
        """
        Resets the command
        """
