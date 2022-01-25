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


@dataclass
class MetricWeights(Base):
    """
    dataclass used to describe metric weights
    """
    total_event: float
    average_event: float
    total_duration: float
    average_duration: float
    total_byte: float
    byte_average: float
    total_packets: float
    average_packet: float
