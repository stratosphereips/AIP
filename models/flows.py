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
from slips_aip_constants.enums import FlowKeys


@dataclass
class Flow(Base):
    """
    dataclass used to describe flows
    """
    src_address: str
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
    aged_score: float

    __slots__ = [name for name in dir(FlowKeys) if not name.startswith('_')]


    def __init__(self):
        """
        Default constructor
        """
        self.src_address = "1.0.0.1"
        self.float = Defaults.ZERO.value
        self.duration = Defaults.ZERO.value
        self.avg_duration = Defaults.ZERO.value
        self.bytes = Defaults.ZERO.value
        self.avg_bytes = Defaults.ZERO.value
        self.packets = Defaults.ZERO.value
        self.avg_packets = Defaults.ZERO.value
        self.first_event = Defaults.ZERO.value
        self.last_event = Defaults.ZERO.value
        self.avg_events = Defaults.ZERO.value
        self.aged_score = Defaults.ZERO.value

    @classmethod
    def from_line(cls, line):
        """
        Flow constructor from config dict
        """
        f = cls()
        f.src_address = str(line[0])
        f.events = float(line[1])
        f.duration = float(line[2])
        f.avg_duration = float(line[3])
        f.bytes = float(line[4])
        f.avg_bytes = float(line[5])
        f.packets = float(line[6])
        f.avg_packets = float(line[7])
        f.first_event = float(line[8])
        f.last_event = float(line[9])
        f.avg_events = float(line[10])

        return f

    @classmethod
    def from_dict(cls, config):
        """
        Flow constructor from config dict
        """
        f = cls()
        f.src_address = config.get('src_address')
        f.events = float(config.get('events'))
        f.duration = float(config.get('duration'))
        f.avg_duration = float(config.get('avg_duration'))
        f.bytes = float(config.get('bytes'))
        f.avg_bytes = float(config.get('avg_bytes'))
        f.packets = float(config.get('packets'))
        f.avg_packets = float(config.get('avg_packets'))
        f.first_event = float(config.get('first_event'))
        f.last_event = float(config.get('last_event'))
        f.avg_events = float(config.get('avg_events'))

        return f
