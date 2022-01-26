"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from dataclasses import dataclass
from typing import overload

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
    avg_duration: float
    bytes: float
    avg_bytes: float
    packets: float
    avg_packets: float
    first_event: float
    last_event: float
    avg_events: float

    @overload
    def __init__(self, line=None) -> None:
        """
        Flow constructor from CSV line
        """
        self.src_address = str(line[0]) if line[0] else "1.0.0.1"
        self.events = float(line[1]) if line[1] else Defaults.ZERO.value
        self.duration = float(line[2]) if line[2] else Defaults.ZERO.value
        self.avg_duration = float(line[3]) if line[3] else Defaults.ZERO.value
        self.bytes = float(line[4]) if line[4] else Defaults.ZERO.value
        self.avg_bytes = float(line[5]) if line[5] else Defaults.ZERO.value
        self.packets = float(line[6]) if line[6] else Defaults.ZERO.value
        self.avg_packets = float(line[7]) if line[7] else Defaults.ZERO.value
        self.first_event = float(line[8]) if line[8] else Defaults.ZERO.value
        self.last_event = float(line[9]) if line[9] else Defaults.ZERO.value
        self.avg_events = float(line[10]) if line[10] else Defaults.ZERO.value
        self.aged_score = Defaults.ZERO.value

    @overload
    def __init__(self, config=None) -> None:
        """
        Flow constructor from config dict
        """
        self.src_address = config.get('src_address', '1.0.0.1')
        self.events = config.get('events', Defaults.ZERO.value)
        self.duration = config.get('duration', Defaults.ZERO.value)
        self.avg_duration = config.get('avg_duration', Defaults.ZERO.value)
        self.bytes = config.get('bytes', Defaults.ZERO.value)
        self.avg_bytes = config.get('avg_bytes', Defaults.ZERO.value)
        self.packets = config.get('packets', Defaults.ZERO.value)
        self.avg_packets = config.get('avg_packets', Defaults.ZERO.value)
        self.first_event = config.get('first_event', Defaults.ZERO.value)
        self.last_event = config.get('last_event', Defaults.ZERO.value)
        self.avg_events = config.get('avg_events', Defaults.ZERO.value)
        self.aged_score = config.get('aged_score', Defaults.ZERO.value)
