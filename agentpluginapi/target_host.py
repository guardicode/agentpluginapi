import pprint
from collections import UserDict
from ipaddress import IPv4Address
from typing import Optional, Set

from monkeytypes import (
    MutableInfectionMonkeyBaseModel,
    NetworkPort,
    NetworkProtocol,
    NetworkService,
    OperatingSystem,
    PortStatus,
)
from pydantic import ConfigDict, Field, TypeAdapter, field_serializer

from .port_scan_data import PortScanData


class PortScanDataDict(UserDict[NetworkPort, PortScanData]):
    def __setitem__(self, key: NetworkPort, value: PortScanData):
        TypeAdapter(NetworkPort).validate_python(key)
        PortScanData.model_validate(value)
        super().__setitem__(key, value)

    @property
    def open(self) -> Set[NetworkPort]:
        return self._filter_ports_by_status(PortStatus.OPEN)

    @property
    def closed(self) -> Set[NetworkPort]:
        return self._filter_ports_by_status(PortStatus.CLOSED)

    def _filter_ports_by_status(self, status: PortStatus) -> Set[NetworkPort]:
        return {
            port for port, port_scan_data in self.data.items() if port_scan_data.status == status
        }

    def get_open_service_ports(self, service: NetworkService) -> Set[NetworkPort]:
        return {port for port in self.open if self[port].service == service}


class TargetHostPorts(MutableInfectionMonkeyBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tcp_ports: PortScanDataDict = Field(default_factory=PortScanDataDict)
    udp_ports: PortScanDataDict = Field(default_factory=PortScanDataDict)

    @field_serializer("tcp_ports", "udp_ports", when_used="json")
    def dump_ports(self, v):
        return dict(v)

    def __getitem__(self, protocol: NetworkProtocol):
        if protocol == NetworkProtocol.TCP:
            return self.tcp_ports
        elif protocol == NetworkProtocol.UDP:
            return self.udp_ports
        else:
            raise KeyError(f"Invalid protocol: {protocol}")


class TargetHost(MutableInfectionMonkeyBaseModel):
    ip: IPv4Address
    operating_system: Optional[OperatingSystem] = Field(default=None)
    icmp: bool = Field(default=False)
    ports_status: TargetHostPorts = Field(default_factory=TargetHostPorts)

    def __hash__(self):
        return hash(self.ip)

    def __str__(self):
        return pprint.pformat(self.to_json_dict())
