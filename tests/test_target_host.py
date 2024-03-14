from typing import Any

import pytest
from monkeytypes import NetworkPort, NetworkProtocol, NetworkService, PortStatus

from agentpluginapi import PortScanData, PortScanDataDict, TargetHost, TargetHostPorts


def test_port_scan_data_dict__constructor():
    input_dict = {
        NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
        NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
        NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
    }
    expected_port_scan_data_dict = {
        1: PortScanData(port=1, status=PortStatus.OPEN),
        2: PortScanData(port=2, status=PortStatus.CLOSED),
        3: PortScanData(port=3, status=PortStatus.OPEN),
    }

    port_scan_data_dict: PortScanDataDict = PortScanDataDict(input_dict)

    assert port_scan_data_dict == expected_port_scan_data_dict


def test_port_scan_data_dict__set():
    expected_port_scan_data_dict = {
        1: PortScanData(port=1, status=PortStatus.OPEN),
        2: PortScanData(port=2, status=PortStatus.CLOSED),
    }

    port_scan_data_dict = PortScanDataDict()
    port_scan_data_dict[1] = PortScanData(port=1, status=PortStatus.OPEN)
    port_scan_data_dict[2] = PortScanData(port=2, status=PortStatus.CLOSED)

    assert port_scan_data_dict == expected_port_scan_data_dict


INVALID_PORTS = (-1, 65536, "string", None, "22.2")
VALID_PORT_SCAN_DATA = PortScanData(port=1, status=PortStatus.OPEN)


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_constructor__invalid_port(invalid_port):
    with pytest.raises((ValueError, TypeError)):
        PortScanDataDict({invalid_port: VALID_PORT_SCAN_DATA})


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_update__invalid_port(invalid_port):
    port_scan_data_dict = PortScanDataDict()
    with pytest.raises((ValueError, TypeError)):
        port_scan_data_dict.update({invalid_port: VALID_PORT_SCAN_DATA})


@pytest.mark.parametrize("invalid_port", INVALID_PORTS)
def test_port_scan_data_dict_set__invalid_port(invalid_port):
    port_scan_data_dict = PortScanDataDict()
    with pytest.raises((ValueError, TypeError)):
        port_scan_data_dict[invalid_port] = VALID_PORT_SCAN_DATA


def test_closed_tcp_ports():
    expected_closed_ports = {2, 4}
    tcp_ports = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
            NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
            NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
            NetworkPort(4): PortScanData(port=4, status=PortStatus.CLOSED),
        }
    )

    assert tcp_ports.closed == expected_closed_ports


def test_open_tcp_ports():
    expected_open_ports = {1, 3}
    tcp_ports = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
            NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
            NetworkPort(3): PortScanData(port=3, status=PortStatus.OPEN),
            NetworkPort(4): PortScanData(port=4, status=PortStatus.CLOSED),
        }
    )

    assert tcp_ports.open == expected_open_ports


def test_target_host_hash():
    t1 = TargetHost(ip="10.0.0.1", icmp=False)
    t2 = TargetHost(ip="10.0.0.1", icmp=True)

    assert hash(t1) == hash(t2)


def test_target_host_ports__getitem():
    tcp_ports = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(port=1, status=PortStatus.OPEN),
        }
    )
    udp_ports = PortScanDataDict(
        {
            NetworkPort(2): PortScanData(port=2, status=PortStatus.CLOSED),
        }
    )

    thp = TargetHostPorts(tcp_ports=tcp_ports, udp_ports=udp_ports)

    assert thp[NetworkProtocol.TCP] == tcp_ports
    assert thp[NetworkProtocol.UDP] == udp_ports


@pytest.mark.parametrize("protocol", [None, "string", 1, NetworkProtocol.ICMP])
def test_target_host_ports__getitem__keyerror(protocol: Any):
    thp = TargetHostPorts(tcp_ports=PortScanDataDict(), udp_ports=PortScanDataDict())

    with pytest.raises(KeyError):
        thp[protocol]


@pytest.mark.parametrize(
    "service, expected_port", ((NetworkService.HTTP, 1), (NetworkService.SSH, 3))
)
def test_get_open_service_ports(service: NetworkService, expected_port: int):
    psdd = PortScanDataDict(
        {
            NetworkPort(1): PortScanData(
                port=1, status=PortStatus.OPEN, service=NetworkService.HTTP
            ),
            NetworkPort(2): PortScanData(
                port=2, status=PortStatus.CLOSED, service=NetworkService.HTTP
            ),
            NetworkPort(3): PortScanData(
                port=3, status=PortStatus.OPEN, service=NetworkService.SSH
            ),
        }
    )

    open_service_ports = psdd.get_open_service_ports(service)

    assert len(open_service_ports) == 1
    assert open_service_ports == {NetworkPort(expected_port)}


def create_target_host(ip, port_scan_data: list[PortScanData]):
    target_host = TargetHost(ip=ip)
    for psd in port_scan_data:
        target_host.ports_status.tcp_ports[psd.port] = psd
    return target_host


def test_target_host__constructor_not_altered_when_setting_ports():
    host = create_target_host("10.0.0.1", [VALID_PORT_SCAN_DATA])
    assert len(host.ports_status.tcp_ports) == 1

    other_host = create_target_host("10.0.0.2", [])
    assert len(other_host.ports_status.tcp_ports) == 0

