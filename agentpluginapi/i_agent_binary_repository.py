import abc
import io

from monkeytypes import OperatingSystem

# TODO: The Island also has an IAgentBinaryRepository with a totally different interface. At the
#       moment, the Island and Agent have different needs, but at some point we should unify these.
#       UPDATE: Since this is now in a separate package with a clear and focused purpose, unifying
#       this interface and the one in the Island may be unnecessary. The Agent and the Island have
#       different needs.


class RetrievalError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to retrieve data
    """


class IAgentBinaryRepository(metaclass=abc.ABCMeta):
    """
    IAgentBinaryRepository provides an interface for other components to access agent binaries.
    Notably, this is used by exploiters during propagation to retrieve the appropriate agent binary
    so that it can be uploaded to a victim and executed.
    """

    @abc.abstractmethod
    def get_agent_binary(self, operating_system: OperatingSystem) -> io.BytesIO:
        """
        Retrieve the appropriate agent binary from the repository.
        :param operating_system: The name of the operating system on which the agent binary will run
        :return: A file-like object for the requested agent binary
        :raises RetrievalError: If an error occurs when retrieving the agent binary
        """
