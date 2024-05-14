from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from monkeytypes import Event, OperatingSystem

ReservationID: TypeAlias = UUID


@dataclass(frozen=True)
class AgentBinaryDownloadReservation:
    id: ReservationID
    operating_system: OperatingSystem
    agent_binary_template: bytes | None
    download_url: str
    download_completed: Event


@dataclass(frozen=True)
class AgentBinaryDownloadTicket:
    id: ReservationID
    download_url: str
    download_completed: Event
