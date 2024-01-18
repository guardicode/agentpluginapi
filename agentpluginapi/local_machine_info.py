import logging
import socket
import struct
import sys
from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path
from typing import Final, List, Optional, Tuple

from monkeytoolbox import get_os
from monkeytypes import InfectionMonkeyBaseModel, OperatingSystem

if get_os() == OperatingSystem.LINUX:
    from fcntl import ioctl

logger = logging.getLogger(__name__)

# Timeout for monkey connections
LOOPBACK_NAME: Final = b"lo"
SIOCGIFADDR: Final = 0x8915  # get PA address
SIOCGIFNETMASK: Final = 0x891B  # get network PA mask
RTF_UP: Final = 0x0001  # Route usable
RTF_REJECT: Final = 0x0200


class LocalMachineInfo(InfectionMonkeyBaseModel):
    """
    Contains information about the local machine

    :param operating_system: Operating system of the local machine
    :param temporary_directory: Path to a temporary directory on the local machine
                                to store artifacts
    :param network_interfaces: Network interfaces on the local machine
    """

    operating_system: OperatingSystem
    temporary_directory: Path
    network_interfaces: frozenset[IPv4Interface]

    def get_interface_to_target(self, target: IPv4Address) -> Optional[IPv4Interface]:
        """
        Gets an interface on the local machine that can be reached by the target machine

        This function attempts to find the interface that can connect to the target. It first
        attempts to do this rationally by examining network membership. If that fails, it attempts
        to do this empirically by opening sockets and examining routes.

        :param interfaces: An iterable of interfaces
        :param target: The IP address of the target
        :return: The network interface that can connect to the target, or None if no such interface
                 could be found
        """

        interface_to_target = self._rational_get_interface_to_target(target)

        if interface_to_target is not None:
            return interface_to_target

        interface_ip_to_target = LocalMachineInfo._empirical_get_interface_to_target(target)

        if interface_ip_to_target is None:
            return None

        for i in self.network_interfaces:
            if i.ip == interface_ip_to_target:
                return i

        return None

    def _rational_get_interface_to_target(self, target: IPv4Address) -> Optional[IPv4Interface]:
        """

        :param interfaces: An iterable of interfaces
        :param target: The IP address of the target
        :return: The network interface that can connect to the target, or None if no such interface
                 could be found
        """
        for i in self.network_interfaces:
            if target in i.network:
                return i

        return None

    @staticmethod
    def _empirical_get_interface_to_target(target_ip: IPv4Address) -> Optional[IPv4Address]:
        """
        This function attempts to find the interface that can connect to the target by opening a
        socket

        :param target_ip: The destination IP address
        :return: IP address string of an interface that can connect to the target, or None if no
                 such interface could be found
        """
        target = str(target_ip)
        if sys.platform == "win32":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect((target, 1))
                ip_to_dst = s.getsockname()[0]
            except KeyError:
                logger.debug(
                    "Couldn't get an interface to the target, presuming that target is localhost."
                )
                ip_to_dst = "127.0.0.1"
            finally:
                s.close()
            return IPv4Address(ip_to_dst)
        else:
            # based on scapy implementation

            def atol(x):
                ip = socket.inet_aton(x)
                return struct.unpack("!I", ip)[0]

            routes = LocalMachineInfo.get_routes()
            target_long = atol(target)
            paths: list[tuple[int, tuple[bytes | str, str, str]]] = []
            for d, m, gw, i, a in routes:
                aa = atol(a)
                if aa == target_long:
                    paths.append((0xFFFFFFFF, ("lo", a, "0.0.0.0")))
                if (target_long & m) == (d & m):
                    paths.append((m, (i, a, gw)))
            if not paths:
                return None
            paths.sort()
            ret = paths[-1][1]
            return IPv4Address(ret[1])

    @staticmethod
    def get_routes() -> List[Tuple[int, int, str, bytes, str]]:
        if get_os() == OperatingSystem.WINDOWS:
            raise NotImplementedError()

        routes = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for line in LocalMachineInfo._read_route_file():
            dst: bytes
            msk: bytes
            iff, dst, gw, flags, msk = LocalMachineInfo._extract_network_info(line)
            if flags & RTF_UP == 0:
                continue
            if flags & RTF_REJECT:
                continue
            ifaddr: Optional[str] = LocalMachineInfo._get_interface_address(s, iff)
            if ifaddr is None:
                continue
            routes.append(
                (
                    socket.htonl(int(dst, 16)) & 0xFFFFFFFF,
                    socket.htonl(int(msk, 16)) & 0xFFFFFFFF,
                    socket.inet_ntoa(struct.pack("I", int(gw, 16))),
                    iff,
                    ifaddr,
                )
            )

        ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", LOOPBACK_NAME))
        addrfamily = struct.unpack("h", ifreq[16:18])[0]
        if addrfamily == socket.AF_INET:
            ifreq2 = ioctl(s, SIOCGIFNETMASK, struct.pack("16s16x", LOOPBACK_NAME))
            mask = socket.ntohl(struct.unpack("I", ifreq2[20:24])[0])
            destination = socket.ntohl(struct.unpack("I", ifreq[20:24])[0]) & mask
            ifaddress = socket.inet_ntoa(ifreq[20:24])
            routes.append((destination, mask, "0.0.0.0", LOOPBACK_NAME, ifaddress))

        return routes

    @staticmethod
    def _read_route_file() -> List[str]:
        try:
            with open("/proc/net/route", "r") as f:
                return f.readlines()[1:]
        except IOError:
            return []

    @staticmethod
    def _extract_network_info(line: str) -> Tuple[bytes, bytes, bytes, int, bytes]:
        values = [var.encode() for var in line.split()]
        iff: bytes = values[0]
        dst: bytes = values[1]
        gw: bytes = values[2]
        flags: int = int(values[3], 16)
        msk: bytes = values[7]
        return iff, dst, gw, flags, msk

    @staticmethod
    def _get_interface_address(s: socket.socket, iff: bytes) -> Optional[str]:
        try:
            ifreq = ioctl(s, SIOCGIFADDR, struct.pack("16s16x", iff))
        except IOError:
            return "0.0.0.0"
        addrfamily = struct.unpack("h", ifreq[16:18])[0]
        if addrfamily == socket.AF_INET:
            return socket.inet_ntoa(ifreq[20:24])
        return None
