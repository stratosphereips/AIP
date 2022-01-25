"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from dataclasses import dataclass

from models.base import Base
from slips_aip_constants.defaults import Defaults


@dataclass
class Flow(Base):
    """
    dataclass used to describe flows
    """
    src_address: str
    aged_score: float
    events: float
    duration: float
    average_duration: float
    bytes: float
    average_bytes: float
    packets: float
    average_packets: float
    first_event: float
    last_event: float
    average_events: float

    def __init__(self, line: tuple) -> None:
        """
        Flow constructor from CSV line
        """
        self.src_address = line[0]
        self.aged_score = line[0] if line[0] else Defaults.ZERO.value
        self.events = line[1] if line[1] else Defaults.ZERO.value
        self.duration = line[2] if line[2] else Defaults.ZERO.value
        self.average_duration = line[3] if line[3] else Defaults.ZERO.value
        self.bytes = line[4] if line[4] else Defaults.ZERO.value
        self.average_bytes = line[5] if line[5] else Defaults.ZERO.value
        self.packets = line[6] if line[6] else Defaults.ZERO.value
        self.average_packets = line[7] if line[7] else Defaults.ZERO.value
        self.first_event = line[8] if line[8] else Defaults.ZERO.value
        self.last_event = line[9] if line[9] else Defaults.ZERO.value
        self.average_events = line[10] if line[10] else Defaults.ZERO.value
