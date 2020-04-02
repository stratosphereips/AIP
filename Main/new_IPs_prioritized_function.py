import math

# What makes this function unique is that I have changed two things, the scoring weights and the time modifier. Since
# this function is supposed to look at historical data and prioritize new IPs over old ones, I have put more importance
# on the the total stats as opposed to the averages. This way, IPs that have been super active for only a day will grow
# faster than ones who have good daily averages. I have also altered the time modifier so that instead of taking into
# account the last time the IP was seen, it uses the first time it was seen. That way even if an IP is super active, it
# will still lose points the older it gets, and the ones that are newer will get higher scores.


def rate_IPs_all_time_new_important(list_of_flows, time_of_newest_data_file):

        # These values will define which of the four metrics are the most important
        total_event_weight = 0.20
        average_event_weight = 0.10
        total_duration_weight = 0.10
        average_duration_weight = 0.10
        total_byte_weight = 0.20
        byte_average_weight = 0.10
        total_packets_weight = 0.10
        average_packet_weight = 0.10

        # The actual rating section
        list_of_raw_ratings = []
        for flow in list_of_flows:
            # Convert all strings to float
            events = float(flow[1])
            duration = float(flow[2])
            average_duration = float(flow[3])
            bytes = float(flow[4])
            average_bytes = float(flow[5])
            packets = float(flow[6])
            average_packets = float(flow[7])
            first_event = float(flow[8])
            last_event = float(flow[9])
            average_events = float(flow[10])

            # Calculate the scores
            event_score = (events * total_event_weight)
            average_events_score = (average_events * average_event_weight)
            duration_score = (duration * total_duration_weight)
            average_duration_score = (average_duration * average_duration_weight)
            bytes_score = (bytes * total_byte_weight)
            average_bytes_score = (average_bytes * byte_average_weight)
            packets_score = (packets * total_packets_weight)
            average_packets_score = (average_packets * average_packet_weight)

            # This is the time modifier section. The longer an IP does not have any events, the lower its score will
            # be. An IP will lose .01 of its score per day that it is not active, thus taking 100 days to be reduced
            # to a score of zero.
            if (time_of_newest_data_file - last_event) < 86400:
                time_modifier = 1
            else:
                time_modifier_factor = (time_of_newest_data_file - last_event) // 86400
                # I am using the general function y = x/(x + 10), where x is the number of days an IP is not seen.
                # In this way, the amount by which a score will decrease will increase to about 50% in about 30 days,
                # and will infinities approach 100% after that.
                time_modifier = 6/(time_modifier_factor+6)
            total_score = math.sqrt((event_score + average_events_score + duration_score + average_duration_score
                                     + bytes_score + average_bytes_score + packets_score + average_packets_score) * time_modifier)
            list_of_raw_ratings.append([flow[0], total_score])
        return list_of_raw_ratings

