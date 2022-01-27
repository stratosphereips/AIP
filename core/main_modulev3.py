"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

# What makes this function unique is that I have changed two things, the scoring weights and the time modifier. Since
# this function is supposed to look at historical data and prioritize aggressive IPs, I have put more importance
# on the the daily averages over the total stats. This way, IPs that have been super active consistently will grow
# faster than ones who have been active for only a day. I have also altered the time modifier so that instead of using
# the first time seen, it uses the last time the IP is seen. That way, if an IP is consistent every day, its score will
# not decrease, while IPs that are active for only a day will decrease faster.

import csv
import math
from logging import getLogger

from models.flows import Flow
from models.raw_ratings import RawRating
from slips_aip_constants.defaults import Defaults
from slips_aip_constants.enums import Weights


logger = getLogger(__name__)


def prioritize_consistent_original(flows: list[Flow],
                                   data_newest_time) -> list[RawRating]:
    """
    Prioritizes original consistent flows

    :param flows: list of flows
    :param data_newest_time: datetime object

    :return: list of RawRating objects
    """
    original_weight = Weights.ORIGINAL.value
    total_events_weight = original_weight.total_events
    average_events_weight = original_weight.average_events
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_bytes_weight = original_weight.total_bytes
    average_bytes_weight = original_weight.average_bytes
    total_packets_weight = original_weight.total_packets
    average_packets_weight = original_weight.average_packets

    # Rating section
    raw_ratings = []

    for flow in flows:
        events = flow.events
        duration = flow.duration
        avg_duration = flow.avg_duration
        bytes = flow.bytes
        avg_bytes = flow.avg_bytes
        packets = flow.packets
        avg_packets = flow.avg_packets
        last_event = flow.last_event
        avg_events = flow.avg_events

        # Calculate the scores
        events_score = (events * total_events_weight)
        avg_events_score = (avg_events * average_events_weight)
        duration_score = (duration * total_duration_weight)
        avg_duration_score = (avg_duration * average_duration_weight)
        bytes_score = (bytes * total_bytes_weight)
        avg_bytes_score = (avg_bytes * average_bytes_weight)
        packets_score = (packets * total_packets_weight)
        avg_packets_score = (avg_packets * average_packets_weight)

        # This is the time modifier section. The longer an IP does not have
        # events, the lower its score will be. An IP will lose .01 of its
        # score per day of inactivity, thus taking 100 days to score zero (0).
        time_delta = data_newest_time - last_event
        if time_delta < Defaults.MINUTES_A_DAY.value:
            time_modifier = 1
        else:
            time_modifier_factor = time_delta // Defaults.MINUTES_A_DAY.value
            # We are using the general function y = x/(x + 10), where x is the
            # number of days an IP is not seen. Hence, the amount by which a
            # score will decrease will increase to about 50% in about 30 days,
            # and will infinities approach 100% after that.
            unseen_days = Defaults.UNSEEN_DAYS.value
            time_modifier = unseen_days / (time_modifier_factor + unseen_days)

        all_scores = sum(events_score, avg_events_score, duration_score,
                         avg_duration_score, bytes_score, avg_bytes_score,
                         packets_score, avg_packets_score)
        total_score = math.sqrt(all_scores * time_modifier)
        raw_ratings.append([RawRating(flow.src_address, total_score)])

    logger.info(f"Raw ratings for PCF: {raw_ratings}")

    return raw_ratings


def todays_ips_only(flows: list[Flow], data_newest_time) -> list[RawRating]:
    """
    Prioritizes only today's flows

    :param flows: list of flows
    :param data_newest_time: datetime object

    :return: list of RawRating objects
    """
    original_weight = Weights.ORIGINAL.value
    total_events_weight = original_weight.total_events
    average_events_weight = original_weight.average_events
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_bytes_weight = original_weight.total_bytes
    average_bytes_weight = original_weight.average_bytes
    total_packets_weight = original_weight.total_packets
    average_packets_weight = original_weight.average_packets

    # Rating section
    raw_ratings = []

    for flow in flows:
        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        average_bytes = flow.avg_bytes
        packets = flow.packets
        average_packets = flow.avg_packets
        average_events = flow.avg_events

        # Calculate the scores
        events_score = (events * total_events_weight)
        avg_events_score = (average_events * average_events_weight)
        duration_score = (duration * total_duration_weight)
        avg_duration_score = (average_duration * average_duration_weight)
        bytes_score = (bytes * total_bytes_weight)
        avg_bytes_score = (average_bytes * average_bytes_weight)
        packets_score = (packets * total_packets_weight)
        avg_packets_score = (average_packets * average_packets_weight)

        all_scores = sum(events_score, avg_events_score, duration_score,
                         avg_duration_score, bytes_score, avg_bytes_score,
                         packets_score, avg_packets_score)
        total_score = math.sqrt(all_scores)
        raw_ratings.append([RawRating(flow.src_address, total_score)])

    logger.info(f"Raw ratings for OTF: {raw_ratings}")

    return raw_ratings


def prioritize_new_original(flows: list[Flow], data_newest_time) -> list[RawRating]:
    """
    Prioritizes new original flows

    :param flows: list of flows
    :param data_newest_time: datetime object

    :return: list of RawRating objects
    """
    original_weight = Weights.ORIGINAL.value
    total_events_weight = original_weight.total_events
    average_events_weight = original_weight.average_events
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_bytes_weight = original_weight.total_bytes
    average_bytes_weight = original_weight.average_bytes
    total_packets_weight = original_weight.total_packets
    average_packets_weight = original_weight.average_packets

    # Rating section
    raw_ratings = []

    for flow in flows:
        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        avg_bytes = flow.avg_bytes
        packets = flow.packets
        avg_packets = flow.avg_packets
        last_event = flow.last_event
        avg_events = flow.avg_events

        # Calculate the scores
        events_score = (events * total_events_weight)
        avg_events_score = (avg_events * average_events_weight)
        duration_score = (duration * total_duration_weight)
        avg_duration_score = (average_duration * average_duration_weight)
        bytes_score = (bytes * total_bytes_weight)
        avg_bytes_score = (avg_bytes * average_bytes_weight)
        packets_score = (packets * total_packets_weight)
        avg_packets_score = (avg_packets * average_packets_weight)

        # This is the time modifier section. The longer an IP does not have events,
        # the lower its score will be. An IP will lose .01 of its score per day of
        # inactivity, thus taking 100 days to score zero (0).
        time_delta = data_newest_time - last_event
        if time_delta < Defaults.MINUTES_A_DAY.value:
            time_modifier = 1
        else:
            time_modifier_factor = time_delta // Defaults.MINUTES_A_DAY.value
            # I am using the general function y = x/(x + 10), where x is the
            # number of days an IP is not seen. Hence, the amount by which a
            # score will decrease will increase to about 50% in about 30 days,
            # and will infinities approach 100% after that.
            unseen_days = Defaults.UNSEEN_DAYS.value
            time_modifier = unseen_days / (time_modifier_factor + unseen_days)

        all_scores = sum(events_score, avg_events_score, duration_score,
                            avg_duration_score, bytes_score, avg_bytes_score,
                            packets_score, avg_packets_score)
        total_score = math.sqrt(all_scores * time_modifier)
        raw_ratings.append([RawRating(flow.src_address, total_score)])

    logger.info(f"Raw ratings for PNF: {raw_ratings}")
    
    return raw_ratings


def prioritize_consistent_normalized(flows: list[Flow],
                                     data_newest_time,
                                     path_to_aging_file) -> list[RawRating]:
    """
    Prioritizes normalized consistent flows

    :param flows: list of flows
    :param data_newest_time: datetime object
    :param path_to_aging_file: path of aging file

    :return: list of RawRating objects
    """
    aging_file_data = open_and_read_aging_file(path_to_aging_file)

    normalized_weight = Weights.NORMALIZED.value
    total_events_weight = normalized_weight.total_events
    average_events_weight = normalized_weight.average_events
    total_duration_weight = normalized_weight.total_duration
    average_duration_weight = normalized_weight.average_duration
    total_bytes_weight = normalized_weight.total_bytes
    average_bytes_weight = normalized_weight.average_bytes
    total_packets_weight = normalized_weight.total_packets
    average_packets_weight = normalized_weight.average_packets

    # List of Mins and Max's each of the data types.
    min_event = Defaults.POS_INFINITY.value
    max_event = Defaults.NEG_INFINITY.value
    min_dur = Defaults.POS_INFINITY.value
    max_dur = Defaults.NEG_INFINITY.value
    min_av_dur = Defaults.POS_INFINITY.value
    max_av_dur = Defaults.NEG_INFINITY.value
    min_byte = Defaults.POS_INFINITY.value
    max_byte = Defaults.NEG_INFINITY.value
    min_av_byte = Defaults.POS_INFINITY.value
    max_av_byte = Defaults.NEG_INFINITY.value
    min_packet = Defaults.POS_INFINITY.value
    max_packet = Defaults.NEG_INFINITY.value
    min_av_packet = Defaults.POS_INFINITY.value
    max_av_packet = Defaults.NEG_INFINITY.value
    min_av_event = Defaults.POS_INFINITY.value
    max_av_event = Defaults.NEG_INFINITY.value

    # Rating section
    raw_ratings = []

    for flow in flows:
        if flow.events > max_event:
            max_event = flow.events
        if flow.events < min_event:
            min_event = flow.events
        if flow.duration > max_dur:
            max_dur = flow.duration
        if flow.duration < min_dur:
            min_dur = flow.duration
        if flow.avg_duration > max_av_dur:
            max_av_dur = flow.avg_duration
        if flow.avg_duration < min_av_dur:
            min_av_dur = flow.avg_duration
        if flow.bytes > max_byte:
            max_byte = flow.bytes
        if flow.bytes < min_byte:
            min_byte = flow.bytes
        if flow.avg_bytes > max_av_byte:
            max_av_byte = flow.avg_bytes
        if flow.avg_bytes < min_av_byte:
            min_av_byte = flow.avg_bytes
        if flow.packets > max_packet:
            max_packet = flow.packets
        if flow.packets < min_packet:
            min_packet = flow.packets
        if flow.avg_packets > max_av_packet:
            max_av_packet = flow.avg_packets
        if flow.avg_packets < min_av_packet:
            min_av_packet = flow.avg_packets
        if flow.avg_events > max_av_event:
            max_av_event = flow.avg_events
        if flow.avg_events < min_av_event:
            min_av_event = flow.avg_events
        
        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        average_bytes = flow.avg_bytes
        packets = flow.packets
        average_packets = flow.avg_packets
        first_event = flow.first_event
        last_event = flow.last_event
        average_events = flow.avg_events

        # Deltas
        dh_event = max_event - min_event
        dh_avg_event = max_av_event - min_av_event
        dh_duration = max_dur - min_dur
        dh_avg_duration = max_av_dur - min_av_dur
        dh_bytes = max_byte - min_byte
        dh_avg_bytes = max_av_byte - min_av_byte
        dh_packets = max_packet - min_packet
        dh_avg_packets = max_av_packet - min_av_packet

        # Differentials
        diff_event = events - min_event
        diff_avg_event = average_events - min_av_event
        diff_duration = duration - min_dur
        diff_avg_duration = average_duration - min_av_dur
        diff_bytes = bytes - min_byte
        diff_avg_bytes = average_bytes - min_av_byte
        diff_packets = packets - min_packet
        diff_avg_packets = average_packets - min_av_packet

        # Scores
        events_score = (diff_event / dh_event) * total_events_weight
        avg_events_score = (diff_avg_event / dh_avg_event) * average_events_weight
        duration_score = (diff_duration / dh_duration) * total_duration_weight
        avg_duration_score = (diff_avg_duration / dh_avg_duration) * average_duration_weight
        bytes_score = (diff_bytes / dh_bytes) * total_bytes_weight
        avg_bytes_score = (diff_avg_bytes / dh_avg_bytes) * average_bytes_weight
        packets_score = (diff_packets / dh_packets) * total_packets_weight
        avg_packets_score = (diff_avg_packets / dh_avg_packets) * average_packets_weight

        # This is the time modifier section. The longer an IP does not have events,
        # the lower its score will be. An IP will lose .01 of its score per day of
        # inactivity, thus taking 100 days to score zero (0).
        all_scores = sum(events_score, avg_events_score, duration_score,
                         avg_duration_score, bytes_score, avg_bytes_score,
                         packets_score, avg_packets_score)

        time_delta = data_newest_time - last_event
        if time_delta < Defaults.MINUTES_A_DAY.value:
            if flow.src_address in aging_file_data:
                aged_score = float(aging_file_data[flow.src_address])
            else:
                aged_score = 0
        else:
            total_time_attacking = last_event - first_event
            percentage_drop = time_delta / (time_delta + total_time_attacking)
            aged_score = all_scores * (1 - percentage_drop)
            aging_file_data.update({flow.src_address: aged_score})

        total_score = aged_score
        raw_ratings.append([RawRating(flow.src_address, total_score)])

    write_to_aging_file(path_to_aging_file, aging_file_data)

    logger.info(f"Raw ratings for PNCF: {raw_ratings}")

    return raw_ratings


def prioritize_new_normalized(flows: list[Flow],
                              data_newest_time,
                              path_to_aging_file) -> list[RawRating]:
    """
    Prioritizes normalized consistent flows

    :param flows: list of flows
    :param data_newest_time: datetime object
    :param path_to_aging_file: path of aging file

    :return: list of RawRating objects
    """
    aging_file_data = open_and_read_aging_file(path_to_aging_file)
    
    normalized_weight = Weights.NORMALIZED.value
    total_events_weight = normalized_weight.total_events
    average_events_weight = normalized_weight.average_events
    total_duration_weight = normalized_weight.total_duration
    average_duration_weight = normalized_weight.average_duration
    total_bytes_weight = normalized_weight.total_bytes
    average_bytes_weight = normalized_weight.average_bytes
    total_packets_weight = normalized_weight.total_packets
    average_packets_weight = normalized_weight.average_packets

    # List of Mins and Max's each of the data types.
    min_event = Defaults.POS_INFINITY.value
    max_event = Defaults.NEG_INFINITY.value
    min_dur = Defaults.POS_INFINITY.value
    max_dur = Defaults.NEG_INFINITY.value
    min_av_dur = Defaults.POS_INFINITY.value
    max_av_dur = Defaults.NEG_INFINITY.value
    min_byte = Defaults.POS_INFINITY.value
    max_byte = Defaults.NEG_INFINITY.value
    min_av_byte = Defaults.POS_INFINITY.value
    max_av_byte = Defaults.NEG_INFINITY.value
    min_packet = Defaults.POS_INFINITY.value
    max_packet = Defaults.NEG_INFINITY.value
    min_av_packet = Defaults.POS_INFINITY.value
    max_av_packet = Defaults.NEG_INFINITY.value
    min_av_event = Defaults.POS_INFINITY.value
    max_av_event = Defaults.NEG_INFINITY.value

    # Rating section
    raw_ratings = []

    for flow in flows:        
        if flow.events > max_event:
            max_event = flow.events
        if flow.events < min_event:
            min_event = flow.events
        if flow.duration > max_dur:
            max_dur = flow.duration
        if flow.duration < min_dur:
            min_dur = flow.duration
        if flow.avg_duration > max_av_dur:
            max_av_dur = flow.avg_duration
        if flow.avg_duration < min_av_dur:
            min_av_dur = flow.avg_duration
        if flow.bytes > max_byte:
            max_byte = flow.bytes
        if flow.bytes < min_byte:
            min_byte = flow.bytes
        if flow.avg_bytes > max_av_byte:
            max_av_byte = flow.avg_bytes
        if flow.avg_bytes < min_av_byte:
            min_av_byte = flow.avg_bytes
        if flow.packets > max_packet:
            max_packet = flow.packets
        if flow.packets < min_packet:
            min_packet = flow.packets
        if flow.avg_packets > max_av_packet:
            max_av_packet = flow.avg_packets
        if flow.avg_packets < min_av_packet:
            min_av_packet = flow.avg_packets
        if flow.avg_events > max_av_event:
            max_av_event = flow.avg_events
        if flow.avg_events < min_av_event:
            min_av_event = flow.avg_events

        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        average_bytes = flow.avg_bytes
        packets = flow.packets
        average_packets = flow.avg_packets
        last_event = flow.last_event
        average_events = flow.avg_events

        # Deltas
        dh_event = max_event - min_event
        dh_avg_event = max_av_event - min_av_event
        dh_duration = max_dur - min_dur
        dh_avg_duration = max_av_dur - min_av_dur
        dh_bytes = max_byte - min_byte
        dh_avg_bytes = max_av_byte - min_av_byte
        dh_packets = max_packet - min_packet
        dh_avg_packets = max_av_packet - min_av_packet

        # Differentials
        diff_event = events - min_event
        diff_avg_event = average_events - min_av_event
        diff_duration = duration - min_dur
        diff_avg_duration = average_duration - min_av_dur
        diff_bytes = bytes - min_byte
        diff_avg_bytes = average_bytes - min_av_byte
        diff_packets = packets - min_packet
        diff_avg_packets = average_packets - min_av_packet

        # Scores
        events_score = (diff_event / dh_event) * total_events_weight
        avg_events_score = (diff_avg_event / dh_avg_event) * average_events_weight
        duration_score = (diff_duration / dh_duration) * total_duration_weight
        avg_duration_score = (diff_avg_duration / dh_avg_duration) * average_duration_weight
        bytes_score = (diff_bytes / dh_bytes) * total_bytes_weight
        avg_bytes_score = (diff_avg_bytes / dh_avg_bytes) * average_bytes_weight
        packets_score = (diff_packets / dh_packets) * total_packets_weight
        avg_packets_score = (diff_avg_packets / dh_avg_packets) * average_packets_weight

        all_scores = sum(events_score, avg_events_score, duration_score,
                         avg_duration_score, bytes_score, avg_bytes_score,
                         packets_score, avg_packets_score)

        time_delta = (data_newest_time - last_event)
        if time_delta < Defaults.MINUTES_A_DAY.value:
            if flow.src_address in aging_file_data:
                aged_score = float(aging_file_data[flow.src_address])
            else:
                aged_score = 0
        else:
            time_modifier_factor = time_delta // Defaults.MINUTES_A_DAY.value
            aged_score = all_scores * (2 / (time_modifier_factor + 2))
            aging_file_data.update({flow.src_address: aged_score})

        total_score = aged_score
        raw_ratings.append([RawRating(flow.src_address, total_score)])

    write_to_aging_file(path_to_aging_file, aging_file_data)

    logger.info(f"Raw ratings for PNNF: {raw_ratings}")

    return raw_ratings


def todays_ips_only_normalized(flows: list[Flow],
                               data_newest_time,
                               path_to_aging_file) -> list[RawRating]:
    """
    Prioritizes only normalized today's flows

    :param flows: list of flows
    :param data_newest_time: datetime object
    :param path_to_aging_file: path of aging file

    :return: list of RawRating objects
    """
    normalized_weight = Weights.NORMALIZED.value
    total_events_weight = normalized_weight.total_events
    average_events_weight = normalized_weight.average_events
    total_duration_weight = normalized_weight.total_duration
    average_duration_weight = normalized_weight.average_duration
    total_bytes_weight = normalized_weight.total_bytes
    average_bytes_weight = normalized_weight.average_bytes
    total_packets_weight = normalized_weight.total_packets
    average_packets_weight = normalized_weight.average_packets

    # List of Mins and Max's each of the data types.
    min_event = Defaults.POS_INFINITY.value
    max_event = Defaults.NEG_INFINITY.value
    min_dur = Defaults.POS_INFINITY.value
    max_dur = Defaults.NEG_INFINITY.value
    min_av_dur = Defaults.POS_INFINITY.value
    max_av_dur = Defaults.NEG_INFINITY.value
    min_byte = Defaults.POS_INFINITY.value
    max_byte = Defaults.NEG_INFINITY.value
    min_av_byte = Defaults.POS_INFINITY.value
    max_av_byte = Defaults.NEG_INFINITY.value
    min_packet = Defaults.POS_INFINITY.value
    max_packet = Defaults.NEG_INFINITY.value
    min_av_packet = Defaults.POS_INFINITY.value
    max_av_packet = Defaults.NEG_INFINITY.value
    min_av_event = Defaults.POS_INFINITY.value
    max_av_event = Defaults.NEG_INFINITY.value

    # The actual rating section
    raw_ratings = []

    for flow in flows:
        if flow.events > max_event:
            max_event = flow.events
        if flow.events < min_event:
            min_event = flow.events
        if flow.duration > max_dur:
            max_dur = flow.duration
        if flow.duration < min_dur:
            min_dur = flow.duration
        if flow.avg_duration > max_av_dur:
            max_av_dur = flow.avg_duration
        if flow.avg_duration < min_av_dur:
            min_av_dur = flow.avg_duration
        if flow.bytes > max_byte:
            max_byte = flow.bytes
        if flow.bytes < min_byte:
            min_byte = flow.bytes
        if flow.avg_bytes > max_av_byte:
            max_av_byte = flow.avg_bytes
        if flow.avg_bytes < min_av_byte:
            min_av_byte = flow.avg_bytes
        if flow.packets > max_packet:
            max_packet = flow.packets
        if flow.packets < min_packet:
            min_packet = flow.packets
        if flow.avg_packets > max_av_packet:
            max_av_packet = flow.avg_packets
        if flow.avg_packets < min_av_packet:
            min_av_packet = flow.avg_packets
        if flow.avg_events > max_av_event:
            max_av_event = flow.avg_events
        if flow.avg_events < min_av_event:
            min_av_event = flow.avg_events

        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        average_bytes = flow.avg_bytes
        packets = flow.packets
        average_packets = flow.avg_packets
        average_events = flow.avg_events

        # Deltas
        dh_event = max_event - min_event
        dh_avg_event = max_av_event - min_av_event
        dh_duration = max_dur - min_dur
        dh_avg_duration = max_av_dur - min_av_dur
        dh_bytes = max_byte - min_byte
        dh_avg_bytes = max_av_byte - min_av_byte
        dh_packets = max_packet - min_packet
        dh_avg_packets = max_av_packet - min_av_packet

        # Differentials
        diff_event = events - min_event
        diff_avg_event = average_events - min_av_event
        diff_duration = duration - min_dur
        diff_avg_duration = average_duration - min_av_dur
        diff_bytes = bytes - min_byte
        diff_avg_bytes = average_bytes - min_av_byte
        diff_packets = packets - min_packet
        diff_avg_packets = average_packets - min_av_packet

        # Scores
        events_score = (diff_event / dh_event) * total_events_weight
        avg_events_score = (diff_avg_event / dh_avg_event) * average_events_weight
        duration_score = (diff_duration / dh_duration) * total_duration_weight
        avg_duration_score = (diff_avg_duration / dh_avg_duration) * average_duration_weight
        bytes_score = (diff_bytes / dh_bytes) * total_bytes_weight
        avg_bytes_score = (diff_avg_bytes / dh_avg_bytes) * average_bytes_weight
        packets_score = (diff_packets / dh_packets) * total_packets_weight
        avg_packets_score = (diff_avg_packets / dh_avg_packets) * average_packets_weight

        calculated_score = sum(events_score, avg_events_score, duration_score,
                               avg_duration_score, bytes_score, avg_bytes_score,
                               packets_score, avg_packets_score)
        total_score = math.sqrt(calculated_score)
        raw_ratings.append([RawRating(flow.src_address, total_score)])
    
    logger.info(f"Raw ratings for OTNF: {raw_ratings}")

    return raw_ratings


def open_and_read_aging_file(self, path_to_aging_file):
    """
    """
    with open(path_to_aging_file, 'r') as csv_file:
        aged_scores_dict = {line[0]:float(line[1]) for line in csv.reader(csv_file)}
    return aged_scores_dict


def write_to_aging_file(self, path_to_aging_file, aged_scores_dict):
    """
    """
    with open(path_to_aging_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for ip, age in aged_scores_dict.items():
            csv_writer.writerow([ip, age])
