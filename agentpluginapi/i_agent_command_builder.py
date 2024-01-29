import abc
from pathlib import PurePath
from typing import Sequence

from . import TargetHost


class IAgentCommandBuilder(metaclass=abc.ABCMeta):
    """
    IAgentCommandLineBuilder provides an interface for other components to build Agent command-line
    strings.
    Notably, this is used by the exploiters during propagation to get command line arguments that
    will run the Agent on a victim machine.
    """

    def build_download_command(
        target_host: TargetHost, url: str, destination_path: PurePath
    ) -> str:
        """
        Builds the download part of the command for specific TargetHost.
        By default: Wget is used for Linux OS and WebRequest for Windows OS.

        :param target_host: The host for which we build the download command
        :param url: The URL where the Agent is hosted
        :param destination_path: The destination path where the Agent will be downloaded to
        """

    def build_download_command_linux_wget(url: str, destination_path: PurePath) -> str:
        """
        Builds the download part of the command for Linux using Wget.

        :param url: The URL where the Agent is hosted
        :param destination_path: The destination path where the Agent will be downloaded to
        """

    def build_download_command_linux_curl(url: str, destination_path: PurePath) -> str:
        """
        Builds the download part of the command for Linux using cURL.

        :param url: The URL where the Agent is hosted
        :param destination_path: The destination path where the Agent will be downloaded to
        """

    def build_download_command_windows_powershell_webclient(
        url: str, destination_path: PurePath
    ) -> str:
        """
        Builds the download part of the command for Windows using PowerShell WebClient.

        :param url: The URL where the Agent is hosted
        :param destination_path: The destination path where the Agent will be downloaded to
        """

    def build_download_command_windows_powershell_webrequest(
        url: str, destination_path: PurePath
    ) -> str:
        """
        Builds the download part of the command for Windows using PowerShell WebRequest.

        :param url: The URL where the Agent is hosted
        :param destination_path: The destination path where the Agent will be downloaded to
        """

    def build_run_command(
        target_host: TargetHost,
        agent_otp_environment_variable: str,
        destination_path: PurePath,
        arguments: Sequence[str],
    ) -> str:
        """
        Builds the run part of the command for specific TargetHost.

        :param target_host: The host for which we build the run command
        :param agent_otp_environment_variable: Name for the Agent OTP Environment variable
        :param destination_path: The destination path where the Agent will be downloaded to
        :param arguments: The command line arguments for the Agent
        """

    def build_agent_command_line() -> str:
        """
        Builds the Agent command line arguments string.
        """

    def build_agent_command_line_arguments() -> list[str]:
        """
        Builds the Agent command line arguments list.
        """

    def build_agent_deploy_command(
        target_host: TargetHost,
        url: str,
        agent_otp_environment_variable: str,
        arguments: Sequence[str],
    ) -> str:
        """
        Builds the complete Agent deployment command

        :param target_host: The host for which we build the deployment command
        :param agent_otp_environment_variable: Name for the Agent OTP Environment variable
        :param destination_path: The destination path where the Agent will be downloaded to
        :param arguments: The command line arguments for the Agent
        """

    def build_dropper_deploy_command(
        target_host: TargetHost,
        url: str,
        agent_otp_environment_variable: str,
        arguments: Sequence[str],
    ) -> str:
        """
        Builds the complete Dropper deployment command

        :param target_host: The host for which we build the deployment command
        :param agent_otp_environment_variable: Name for the Agent OTP Environment variable
        :param destination_path: The destination path where the Agent will be downloaded to
        :param arguments: The command line arguments for the Agent
        """
