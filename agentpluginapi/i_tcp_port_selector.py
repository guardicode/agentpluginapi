import abc
from typing import Optional, Sequence

from monkeytypes import NetworkPort


class ITCPPortSelector(metaclass=abc.ABCMeta):
    """
    An interface for components to select an available TCP port
    that a new server can listen on.
    """

    @abc.abstractmethod
    def get_free_tcp_port(
        self,
        min_range: int = 1024,
        max_range: int = 65535,
        lease_time_sec: float = 30,
        preferred_ports: Sequence[NetworkPort] = [],
    ) -> Optional[NetworkPort]:
        """
        Get a free TCP port that a new server can listen on

        :param min_range: The smallest port number a random port can be chosen from, defaults to
                          1024
        :param max_range: The largest port number a random port can be chosen from, defaults to
                          65535
        :param lease_time_sec: The amount of time a port should be reserved for if the OS does not
                               report it as in use, defaults to 30 seconds
        :param preferred_ports: A sequence of ports that should be tried first
        :return: The selected port, or None if no ports are available
        """
