"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from enum import Enum

from models.metric_weights import MetricWeights


class BlocklistSTypes(Enum):
    """
    Parameterized file paths
    """
    NEW_BLOCKLIST = '_new_blocklist.csv'
    PC_BLOCKLIST = '_pc_blocklist.csv'
    PN_BLOCKLIST = '_pn_blocklist.csv'
    TRAD_BLOCKLIST = '_trad_blocklist.csv'

class FlowKeys(Enum):
    """
    Parameterized keys for Flow
    """
    SRC_ADDRESS = 'src_address'
    EVENTS = 'events'
    DURATION = 'duration'
    AVG_DURATION = 'avg_duration'
    BYTES = 'bytes'
    AVG_BYTES = 'avg_bytes'
    PACKETS = 'packets'
    AVG_PACKETS = 'avg_packets'
    FIRST_EVENT = 'first_event'
    LAST_EVENT = 'last_event'
    AVG_EVENTS = 'avg_events'
    AGED_SCORE = 'aged_score'

class Normalized(MetricWeights):
    """
    Weights used to ponder normalized data
    """
    def __init__(self):
        self.total_events = 0.05
        self.average_events = 0.20
        self.total_duration = 0.05
        self.average_duration = 0.20
        self.total_bytes = 0.05
        self.average_bytes = 0.20
        self.total_packets = 0.05
        self.average_packets = 0.20

class Original(MetricWeights):
    """
    Weights used to ponder original data
    """
    def __init__(self):
        self.total_events = 0.20
        self.average_events = 0.10
        self.total_duration = 0.10
        self.average_duration = 0.10
        self.total_bytes = 0.20
        self.average_bytes = 0.10
        self.total_packets = 0.10
        self.average_packets = 0.10

class Paths(Enum):
    """
    Parameterized file paths
    """
    ABSOLUTE_DATA = '/absolute_data.csv'
    AGING_PC_MODS = '/aging_modifiers_pc.csv'
    AGING_PN_MODS = '/Aging_modifiers_pn.csv'
    KNOWN_IPS = '/known_ips.txt'
    PROCESSED_SPLUNK_FILES = '/processed_splunk_files.txt'
    SELECTED_MODULES = '/selected_modules.csv'
    TIMES = '/times.csv'

class Weights(Enum):
    """
    Parameterized MetricWeights
    """
    NORMALIZED = Normalized()
    ORIGINAL = Original()
