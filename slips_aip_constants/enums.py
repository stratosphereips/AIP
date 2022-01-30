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
from defaults import Defaults


class BlocklistTypes(Enum):
    """
    Parameterized file paths
    """
    NEW_BLOCKLIST = "_new_blocklist.csv"
    PC_BLOCKLIST = "_pc_blocklist.csv"
    PN_BLOCKLIST = "_pn_blocklist.csv"
    TRAD_BLOCKLIST = "_trad_blocklist.csv"

class DirPaths(Enum):
    """
    Parameterized directories paths
    """
    ASN = "core/asn/"
    HISTORICAL_RATINGS = "historical_ratings/"
    INPUT_DATA = "input_data/"
    PRIORITIZE_CONSISTENT = "prioritize_consistent/"
    PRIORITIZE_NEW = "prioritize_new/"
    PRIORITIZE_TODAY_ONLY = "prioritize_today_only/"
    TRADITIONAL = "traditional/"

class EnvVars(Enum):
    """
    Parameterized environment variables
    """
    OUTPUT_FOLDER = "output_folder"
    OUTPUT_DATA_FOLDER = "output_data_folder"
    RESULTS_FILE ="results_file"

class FilePaths(Enum):
    """
    Parameterized file paths
    """
    ASN_DB = "asn.mmdb"
    ABSOLUTE_DATA = '/absolute_data.csv'
    AGING_PC_MODS = '/aging_modifiers_pc.csv'
    AGING_PN_MODS = '/aging_modifiers_pn.csv'
    FP_LOG = '/fp_log_file.csv'
    KNOWN_IPS = '/known_ips.txt'
    PROCESSED_FILES = '/processed_splunk_files.txt'
    SELECTED_MODULES = '/selected_modules.csv'
    TIMES = '/times.csv'

class FlowKeys(Enum):
    """
    Parameterized keys for Flow
    """
    SRC_ADDRESS = "src_address"
    EVENTS = "events"
    DURATION = "duration"
    AVG_DURATION = "avg_duration"
    BYTES = "bytes"
    AVG_BYTES = "avg_bytes"
    PACKETS = "packets"
    AVG_PACKETS = "avg_packets"
    FIRST_EVENT = "first_event"
    LAST_EVENT = "last_event"
    AVG_EVENTS = "avg_events"
    AGED_SCORE = "aged_score"

class Normalized(MetricWeights):
    """
    Weights used to ponder normalized data
    """
    def __init__(self):
        self.total_events = Defaults.FIVE_PERCENTAGE.value
        self.average_events = Defaults.TWENTY_PERCENTAGE.value
        self.total_duration = Defaults.FIVE_PERCENTAGE.value
        self.average_duration = Defaults.TWENTY_PERCENTAGE.value
        self.total_bytes = Defaults.FIVE_PERCENTAGE.value
        self.average_bytes = Defaults.TWENTY_PERCENTAGE.value
        self.total_packets = Defaults.FIVE_PERCENTAGE.value
        self.average_packets = Defaults.TWENTY_PERCENTAGE.value

class Original(MetricWeights):
    """
    Weights used to ponder original data
    """
    def __init__(self):
        self.total_events = Defaults.TWENTY_PERCENTAGE.value
        self.average_events = Defaults.TEN_PERCENTAGE.value
        self.total_duration = Defaults.TEN_PERCENTAGE.value
        self.average_duration = Defaults.TEN_PERCENTAGE.value
        self.total_bytes = Defaults.TWENTY_PERCENTAGE.value
        self.average_bytes = Defaults.TEN_PERCENTAGE.value
        self.total_packets = Defaults.TEN_PERCENTAGE.value
        self.average_packets = Defaults.TEN_PERCENTAGE.value

class Weights(Enum):
    """
    Parameterized MetricWeights
    """
    NORMALIZED = Normalized()
    ORIGINAL = Original()
