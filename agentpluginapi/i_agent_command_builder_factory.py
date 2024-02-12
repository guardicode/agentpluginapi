from abc import ABC, abstractmethod

from .i_linux_agent_command_builder import ILinuxAgentCommandBuilder
from .i_windows_agent_command_builder import IWindowsAgentCommandBuilder


class IAgentCommandBuilderFactory(ABC):
    @abstractmethod
    def create_linux_agent_command_builder(
        self,
    ) -> ILinuxAgentCommandBuilder:
        """
        Builds an ILinuxAgentCommandBuilder that constructs the Agent command

        :return: An ILinuxAgentCommandBuilder instance
        """

    @abstractmethod
    def create_windows_agent_command_builder(
        self,
    ) -> IWindowsAgentCommandBuilder:
        """
        Builds an IWindowsAgentCommandBuilder that constructs the Agent command

        :return: An IWindowsAgentCommandBuilder instance
        """
