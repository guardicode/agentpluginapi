import abc
from ipaddress import IPv4Address

from monkeytypes import OperatingSystem

from .agent_binary_request import AgentBinaryDownloadTicket, ReservationID


class IHTTPAgentBinaryServerRegistrar(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def reserve_download(
        self,
        operating_system: OperatingSystem,
        requestor_ip: IPv4Address,
        agent_binary_wrapper_template: bytes | None,
    ) -> AgentBinaryDownloadTicket:
        """
        Register to download an Agent over HTTP

        :param operating_system: The operating system for the Agent binary to serve
        :param requestor_ip: The IP address of the client that will download the Agent binary
        :param agent_binary_wrapper_template: A bytes template that the bytes from the Agent binary
            will be inserted into. This may be used to, e.g., convert the Agent binary into a
            self-extracting shell script. This template should include the string
            "$(agent_binary)b", which will be replaced by the bytes of the Agent binary.
            Defaults to None.
        :raises RuntimeError: If the binary could not be served
        :returns: A ticket to download the Agent binary
        """

    @abc.abstractmethod
    def clear_reservation(self, reservation_id: ReservationID):
        """
        Deregister a AgentBinaryDownloadReservation from the registrar

        :param reservation_id: The ID of the reservation to be deregistered
        :raises KeyError: If the reservation ID is not registered
        """
