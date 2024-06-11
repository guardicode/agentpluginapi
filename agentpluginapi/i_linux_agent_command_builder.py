import abc
from enum import Enum, auto
from pathlib import PurePosixPath
from typing import Optional

from monkeytypes import InfectionMonkeyBaseModel
from pydantic import Field, model_validator

from .dropper_execution_mode import DropperExecutionMode


class LinuxDownloadMethod(Enum):
    WGET = auto()
    CURL = auto()


class LinuxDownloadOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PurePosixPath
    download_method: LinuxDownloadMethod
    download_url: str


class LinuxSetPermissionsOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PurePosixPath
    permissions: int = Field(ge=0, le=0o777, default=0o700)


class LinuxRunOptions(InfectionMonkeyBaseModel):
    agent_destination_path: PurePosixPath
    dropper_execution_mode: DropperExecutionMode
    dropper_destination_path: Optional[PurePosixPath] = None

    @model_validator(mode="after")
    def check_dropper_execution(self) -> "LinuxRunOptions":
        if (
            self.dropper_destination_path is not None
            and self.dropper_execution_mode != DropperExecutionMode.DROPPER
        ):
            raise ValueError(
                "Dropper execution mode must be DropperExecutionMode.DROPPER if "
                "dropper_destination_path is not None"
            )
        return self


class ILinuxAgentCommandBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_download_command(self, download_options: LinuxDownloadOptions):
        """
        Build Agent's download command

        :param download_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_set_permissions_command(self, set_permissions_options: LinuxSetPermissionsOptions):
        """
        Build Agent's binary permission change command

        :param set_permissions_options: Options needed for the command to be built
        """

    @abc.abstractmethod
    def build_run_command(self, run_options: LinuxRunOptions):
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
