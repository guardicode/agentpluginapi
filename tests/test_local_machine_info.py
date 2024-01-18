from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path
from types import MappingProxyType
from typing import Final

import pytest
from monkeytypes import OperatingSystem

from agentpluginapi.local_machine_info import LocalMachineInfo

INTERFACES: Final = (
    IPv4Interface("192.168.1.0/24"),
    IPv4Interface("192.168.2.2/32"),
    IPv4Interface("10.0.0.0/16"),
)

LOCAL_MACHINE_INFO_OBJECT: Final = LocalMachineInfo(
    operating_system=OperatingSystem.WINDOWS,
    temporary_directory=Path("temp"),
    network_interfaces=frozenset(INTERFACES),
)

LOCAL_MACHINE_INFO_DICT: Final = {
    "operating_system": "windows",
    "temporary_directory": "temp",
    "network_interfaces": sorted([str(i) for i in INTERFACES]),
}

INCLUDED_IPS: Final = MappingProxyType(
    {
        IPv4Address("192.168.1.10"): INTERFACES[0],
        IPv4Address("192.168.1.254"): INTERFACES[0],
        IPv4Address("192.168.2.2"): INTERFACES[1],
        IPv4Address("10.0.254.5"): INTERFACES[2],
        IPv4Address("10.0.0.1"): INTERFACES[2],
        IPv4Address("10.0.16.123"): INTERFACES[2],
    }
)

EXCLUDED_IPS: Final = (
    IPv4Address("192.168.2.10"),
    IPv4Address("192.168.2.3"),
    IPv4Address("192.168.3.4"),
    IPv4Address("172.1.2.3"),
    IPv4Address("10.1.254.5"),
    IPv4Address("10.2.0.1"),
    IPv4Address("10.3.16.123"),
)


def test_local_machine_info__serialization():
    serialized_lmi = LOCAL_MACHINE_INFO_OBJECT.to_json_dict()
    serialized_lmi["network_interfaces"].sort()

    assert serialized_lmi == LOCAL_MACHINE_INFO_DICT


def test_local_machine_info__deserialization():
    assert LocalMachineInfo(**LOCAL_MACHINE_INFO_DICT) == LOCAL_MACHINE_INFO_OBJECT


def test_empty_interfaces(monkeypatch):
    monkeypatch.setattr(
        "agentpluginapi.LocalMachineInfo._empirical_get_interface_to_target",
        lambda *args, **kwargs: None,
    )
    lmio = LocalMachineInfo(
        operating_system=LOCAL_MACHINE_INFO_OBJECT.operating_system,
        temporary_directory=LOCAL_MACHINE_INFO_OBJECT.temporary_directory,
        network_interfaces=[],
    )
    assert lmio.get_interface_to_target(IPv4Address("192.168.1.10")) is None


@pytest.mark.parametrize("ip", INCLUDED_IPS.keys())
def test_target_reachable(ip):
    assert LOCAL_MACHINE_INFO_OBJECT.get_interface_to_target(ip) == INCLUDED_IPS[ip]


@pytest.mark.parametrize("ip", EXCLUDED_IPS)
def test_target_unreachable(ip, monkeypatch):
    monkeypatch.setattr(
        "agentpluginapi.LocalMachineInfo._empirical_get_interface_to_target",
        lambda *args, **kwargs: None,
    )
    assert LOCAL_MACHINE_INFO_OBJECT.get_interface_to_target(ip) is None


@pytest.mark.parametrize("ip", EXCLUDED_IPS)
def test_empirical_fallback(monkeypatch, ip):
    monkeypatch.setattr(
        "agentpluginapi.LocalMachineInfo._empirical_get_interface_to_target",
        lambda *args, **kwargs: INTERFACES[2].ip,
    )
    assert LOCAL_MACHINE_INFO_OBJECT.get_interface_to_target(ip) == INTERFACES[2]
