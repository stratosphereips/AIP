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
    Prioritizes 
    """

    # These values will define which of the four metrics are the most important
    original_weight = Weights.ORIGINAL.value
    total_event_weight = original_weight.total_event
    average_event_weight = original_weight.average_event
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_byte_weight = original_weight.total_byte
    byte_average_weight = original_weight.byte_average
    total_packets_weight = original_weight.total_packets
    average_packet_weight = original_weight.average_packet

    # Rating section
    list_of_raw_ratings = []

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
        event_score = (events * total_event_weight)
        average_events_score = (avg_events * average_event_weight)
        duration_score = (duration * total_duration_weight)
        average_duration_score = (avg_duration * average_duration_weight)
        bytes_score = (bytes * total_byte_weight)
        average_bytes_score = (avg_bytes * byte_average_weight)
        packets_score = (packets * total_packets_weight)
        average_packets_score = (avg_packets * average_packet_weight)

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
        all_scores = sum(event_score, average_events_score, duration_score,
                         average_duration_score, bytes_score, average_bytes_score,
                         packets_score, average_packets_score)
        total_score = math.sqrt(all_scores * time_modifier)
        current_rating = RawRating(flow.src_address, total_score)
        list_of_raw_ratings.append([current_rating])

    logger.info(f"")

    return list_of_raw_ratings


def todays_ips_only(flows: list[Flow], time) -> list[RawRating]:
    # These values will define which of the four metrics are the most important
    original_weight = Weights.ORIGINAL.value
    total_event_weight = original_weight.total_event
    average_event_weight = original_weight.average_event
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_byte_weight = original_weight.total_byte
    byte_average_weight = original_weight.byte_average
    total_packets_weight = original_weight.total_packets
    average_packet_weight = original_weight.average_packet

    # Rating section
    list_of_raw_ratings = []

    for flow in flows:
        events = flow.events
        duration = flow.duration
        average_duration = flow.avg_duration
        bytes = flow.bytes
        average_bytes = flow.avg_bytes
        packets = flow.packets
        average_packets = flow.average_packets
        average_events = flow.average_events

        # Calculate the scores
        event_score = (events * total_event_weight)
        average_events_score = (average_events * average_event_weight)
        duration_score = (duration * total_duration_weight)
        average_duration_score = (average_duration * average_duration_weight)
        bytes_score = (bytes * total_byte_weight)
        average_bytes_score = (average_bytes * byte_average_weight)
        packets_score = (packets * total_packets_weight)
        average_packets_score = (average_packets * average_packet_weight)

        all_scores = float(sum(event_score, average_events_score, duration_score,
                               average_duration_score, bytes_score, average_bytes_score,
                               packets_score, average_packets_score))
        total_score = math.sqrt(all_scores)
        current_rating = RawRating(flow.src_address, total_score)
        list_of_raw_ratings.append([current_rating])
    return list_of_raw_ratings


def prioritize_new_original(flows: list[Flow], data_newest_time) -> list[RawRating]:
    """
    Prioritizes new original flows

    :param flows: list of flows
    :param data_newest_time: datetime obje
    """

    # These values will define which of the four metrics are the most important
    original_weight = Weights.ORIGINAL.value
    total_event_weight = original_weight.total_event
    average_event_weight = original_weight.average_event
    total_duration_weight = original_weight.total_duration
    average_duration_weight = original_weight.average_duration
    total_byte_weight = original_weight.total_byte
    byte_average_weight = original_weight.byte_average
    total_packets_weight = original_weight.total_packets
    average_packet_weight = original_weight.average_packet

    # Rating section
    list_of_raw_ratings = []

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
        event_score = (events * total_event_weight)
        average_events_score = (avg_events * average_event_weight)
        duration_score = (duration * total_duration_weight)
        average_duration_score = (average_duration * average_duration_weight)
        bytes_score = (bytes * total_byte_weight)
        average_bytes_score = (avg_bytes * byte_average_weight)
        packets_score = (packets * total_packets_weight)
        average_packets_score = (avg_packets * average_packet_weight)

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
            time_modifier = unseen_days/(time_modifier_factor + unseen_days)
        all_scores = sum(event_score, average_events_score, duration_score,
                            average_duration_score, bytes_score, average_bytes_score,
                            packets_score, average_packets_score)
        total_score = math.sqrt(all_scores * time_modifier)
        list_of_raw_ratings.append([RawRating(flow.src_address, total_score)])
    
    return list_of_raw_ratings


def prioritize_consistent_normalized(flows: list[Flow],
                                     data_newest_time,
                                     path_to_aging_file) -> list[RawRating]:
    """
    """

    counter = 0
    aging_file_data = open_and_read_aging_file(path_to_aging_file)
    # These values will define which of the four metrics are the most important
    normalized_weight = Weights.NORMALIZED.value
    total_event_weight = normalized_weight.total_event
    average_event_weight = normalized_weight.average_event
    total_duration_weight = normalized_weight.total_duration
    average_duration_weight = normalized_weight.average_duration
    total_byte_weight = normalized_weight.total_byte
    byte_average_weight = normalized_weight.byte_average
    total_packets_weight = normalized_weight.total_packets
    average_packet_weight = normalized_weight.average_packet

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
    list_of_raw_ratings = []

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
        event_score = (diff_event / dh_event) * total_event_weight
        average_events_score = (diff_avg_event / dh_avg_event) * average_event_weight
        duration_score = (diff_duration / dh_duration) * total_duration_weight
        average_duration_score = (diff_avg_duration / dh_avg_duration) * average_duration_weight
        bytes_score = (diff_bytes / dh_bytes) * total_byte_weight
        average_bytes_score = (diff_avg_bytes / dh_avg_bytes) * byte_average_weight
        packets_score = (diff_packets / dh_packets) * total_packets_weight
        average_packets_score = (diff_avg_packets / dh_avg_packets) * average_packet_weight

        # This is the time modifier section. The longer an IP does not have any events, the lower its score will
        # be. An IP will lose .01 of its score per day that it is not active, thus taking 100 days to be reduced
        # to a score of zero.
        calculated_score = (event_score + average_events_score + duration_score + average_duration_score
                                      + bytes_score + average_bytes_score + packets_score + average_packets_score)
        time_delta = data_newest_time - last_event
        if time_delta < Defaults.MINUTES_A_DAY.value:
            if flow.aged_score in aging_file_data:
                aged_score = aging_file_data[flow.aged_score]
            else:
                aged_score = 0
        else:
            total_time_attacking = last_event - first_event
            percentage_drop = time_delta / (time_delta + total_time_attacking)
            aged_score = calculated_score * (1 - percentage_drop)
            if flow.aged_score in aging_file_data:
                updated_entry = {flow.aged_score: aged_score}
                aging_file_data.update(updated_entry)
            else:
                aging_file_data[flow.aged_score] = aged_score
        current_rating = RawRating(flow.aged_score, aged_score)
        list_of_raw_ratings.append([current_rating])
        counter += 1

    write_to_aging_file(path_to_aging_file, aging_file_data)

    return list_of_raw_ratings


def prioritize_new_normalized(flows: list[Flow], time_of_newest_data_file, path_to_aging_file):
    counter = 0
    aging_file_data = open_and_read_aging_file(path_to_aging_file)
    # These values will define which of the four metrics are the most important
    total_event_weight = 0.20
    average_event_weight = 0.05
    total_duration_weight = 0.20
    average_duration_weight = 0.05
    total_byte_weight = 0.20
    byte_average_weight = 0.05
    total_packets_weight = 0.20
    average_packet_weight = 0.05

    # List of Mins and Max's each of the data types.
    min_event = float("inf")
    max_event = - float("inf")
    min_dur = float("inf")
    max_dur = - float("inf")
    min_av_dur = float("inf")
    max_av_dur = - float("inf")
    min_byte = float("inf")
    max_byte = - float("inf")
    min_av_byte = float("inf")
    max_av_byte = - float("inf")
    min_packet = float("inf")
    max_packet = - float("inf")
    min_av_packet = float("inf")
    max_av_packet = - float("inf")
    min_av_event = float("inf")
    max_av_event = - float("inf")

    for flow in flows:
        if float(flow[1]) > max_event:
            max_event = float(flow[1])
        if float(flow[1]) < min_event:
            min_event = float(flow[1])
        if float(flow[2]) > max_dur:
            max_dur = float(flow[2])
        if float(flow[2]) < min_dur:
            min_dur = float(flow[2])
        if float(flow[3]) > max_av_dur:
            max_av_dur = float(flow[3])
        if float(flow[3]) < min_av_dur:
            min_av_dur = float(flow[3])
        if float(flow[4]) > max_byte:
            max_byte = float(flow[4])
        if float(flow[4]) < min_byte:
            min_byte = float(flow[4])
        if float(flow[5]) > max_av_byte:
            max_av_byte = float(flow[5])
        if float(flow[5]) < min_av_byte:
            min_av_byte = float(flow[5])
        if float(flow[6]) > max_packet:
            max_packet = float(flow[6])
        if float(flow[6]) < min_packet:
            min_packet = float(flow[6])
        if float(flow[7]) > max_av_packet:
            max_av_packet = float(flow[7])
        if float(flow[7]) < min_av_packet:
            min_av_packet = float(flow[7])
        if float(flow[10]) > max_av_event:
            max_av_event = float(flow[10])
        if float(flow[10]) < min_av_event:
            min_av_event = float(flow[10])

    # The actual rating section
    list_of_raw_ratings = []
    for flow in flows:
        # Convert all strings to float
        events = float(flow[1])
        duration = float(flow[2])
        average_duration = float(flow[3])
        bytes = float(flow[4])
        average_bytes = float(flow[5])
        packets = float(flow[6])
        average_packets = float(flow[7])
        last_event = float(flow[9])
        average_events = float(flow[10])

        # Calculate the scores
        event_score = (((events - min_event) / (max_event - min_event)) * total_event_weight)
        average_events_score = (
                    ((average_events - min_av_event) / (max_av_event - min_av_event)) * average_event_weight)
        duration_score = ((duration - min_dur) / (max_dur - min_dur)) * total_duration_weight
        average_duration_score = (
                    ((average_duration - min_av_dur) / (max_av_dur - min_av_dur)) * average_duration_weight)
        bytes_score = (((bytes - min_byte) / (max_byte - min_byte)) * total_byte_weight)
        average_bytes_score = (((average_bytes - min_av_byte) / (max_av_byte - min_av_byte)) * byte_average_weight)
        packets_score = (((packets - min_packet) / (max_packet - min_packet)) * total_packets_weight)
        average_packets_score = (
                    ((average_packets - min_av_packet) / (max_av_packet - min_av_packet)) * average_packet_weight)

        calculated_score = (event_score + average_events_score + duration_score + average_duration_score
                            + bytes_score + average_bytes_score + packets_score + average_packets_score)
        if (time_of_newest_data_file - last_event) < 86400:
            if flow[0] in aging_file_data:
                aged_score = float(aging_file_data[flow[0]])
            else:
                aged_score = 0
        else:
            time_modifier_factor = (time_of_newest_data_file - last_event) // 86400
            aged_score = calculated_score * (2 / (time_modifier_factor + 2))
            if flow[0] in aging_file_data:
                updated_entry = {flow[0]: aged_score}
                aging_file_data.update(updated_entry)
            else:
                aging_file_data[flow[0]] = aged_score
        total_score = aged_score
        list_of_raw_ratings.append([flow[0], total_score])
        counter += 1
    write_to_aging_file(path_to_aging_file, aging_file_data)
    return list_of_raw_ratings

def todays_ips_only_normalized(flows: list[Flow], time_of_newest_data_file, path_to_aging_file):
    # These values will define which of the four metrics are the most important
    total_event_weight = 0.05
    average_event_weight = 0.20
    total_duration_weight = 0.05
    average_duration_weight = 0.20
    total_byte_weight = 0.05
    byte_average_weight = 0.20
    total_packets_weight = 0.05
    average_packet_weight = 0.20

    # List of Mins and Max's each of the data types.
    min_event = float("inf")
    max_event = - float("inf")
    min_dur = float("inf")
    max_dur = - float("inf")
    min_av_dur = float("inf")
    max_av_dur = - float("inf")
    min_byte = float("inf")
    max_byte = - float("inf")
    min_av_byte = float("inf")
    max_av_byte = - float("inf")
    min_packet = float("inf")
    max_packet = - float("inf")
    min_av_packet = float("inf")
    max_av_packet = - float("inf")
    min_av_event = float("inf")
    max_av_event = - float("inf")

    for flow in flows:
        if float(flow[1]) > max_event:
            max_event = float(flow[1])
        if float(flow[1]) < min_event:
            min_event = float(flow[1])
        if float(flow[2]) > max_dur:
            max_dur = float(flow[2])
        if float(flow[2]) < min_dur:
            min_dur = float(flow[2])
        if float(flow[3]) > max_av_dur:
            max_av_dur = float(flow[3])
        if float(flow[3]) < min_av_dur:
            min_av_dur = float(flow[3])
        if float(flow[4]) > max_byte:
            max_byte = float(flow[4])
        if float(flow[4]) < min_byte:
            min_byte = float(flow[4])
        if float(flow[5]) > max_av_byte:
            max_av_byte = float(flow[5])
        if float(flow[5]) < min_av_byte:
            min_av_byte = float(flow[5])
        if float(flow[6]) > max_packet:
            max_packet = float(flow[6])
        if float(flow[6]) < min_packet:
            min_packet = float(flow[6])
        if float(flow[7]) > max_av_packet:
            max_av_packet = float(flow[7])
        if float(flow[7]) < min_av_packet:
            min_av_packet = float(flow[7])
        if float(flow[10]) > max_av_event:
            max_av_event = float(flow[10])
        if float(flow[10]) < min_av_event:
            min_av_event = float(flow[10])

    # The actual rating section
    list_of_raw_ratings = []
    for flow in flows:
        # Convert all strings to float
        events = float(flow[1])
        duration = float(flow[2])
        average_duration = float(flow[3])
        bytes = float(flow[4])
        average_bytes = float(flow[5])
        packets = float(flow[6])
        average_packets = float(flow[7])
        last_event = float(flow[9])
        average_events = float(flow[10])

        # Calculate the scores
        event_score = (((events - min_event) / (max_event - min_event)) * total_event_weight)
        average_events_score = (
                    ((average_events - min_av_event) / (max_av_event - min_av_event)) * average_event_weight)
        duration_score = ((duration - min_dur) / (max_dur - min_dur)) * total_duration_weight
        average_duration_score = (
                    ((average_duration - min_av_dur) / (max_av_dur - min_av_dur)) * average_duration_weight)
        bytes_score = (((bytes - min_byte) / (max_byte - min_byte)) * total_byte_weight)
        average_bytes_score = (((average_bytes - min_av_byte) / (max_av_byte - min_av_byte)) * byte_average_weight)
        packets_score = (((packets - min_packet) / (max_packet - min_packet)) * total_packets_weight)
        average_packets_score = (
                    ((average_packets - min_av_packet) / (max_av_packet - min_av_packet)) * average_packet_weight)


        total_score = math.sqrt((event_score + average_events_score + duration_score + average_duration_score
                                 + bytes_score + average_bytes_score + packets_score + average_packets_score))
        list_of_raw_ratings.append([flow.src_address, total_score])
    return list_of_raw_ratings

def open_and_read_aging_file(self, path_to_aging_file):
    """
    """
    dictionary = {}
    with open(path_to_aging_file, 'r') as file:
        for line in csv.reader(file):
            dictionary[line[0]] = line[1]
    return dictionary

def write_to_aging_file(self, path_to_aging_file, data):
    with open(path_to_aging_file, 'w') as file:
        csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for ip, age in data.items():
            list = [ip, age]
            csv_writer.writerow(list)
