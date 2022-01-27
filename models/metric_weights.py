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

    These values define metric is the most important
    """
    total_events: float
    average_events: float
    total_duration: float
    average_duration: float
    total_bytes: float
    average_bytes: float
    total_packets: float
    average_packets: float

    __slots__ = ['total_events', 'average_events', 'total_duration', 'average_duration',
                 'total_bytes', 'average_bytes', 'total_packets', 'average_packets']
