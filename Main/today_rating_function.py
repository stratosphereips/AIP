import math

# The only thing that makes that makes this function different is that is does not have a time modifier since it is only
# dealing with the IPs seen today.

def rate_IPs_today(list_of_flows):
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
            average_events = float(flow[1])

            # Calculate the scores
            event_score = (events * total_event_weight)
            average_events_score = (average_events * average_event_weight)
            duration_score = (duration * total_duration_weight)
            average_duration_score = (average_duration * average_duration_weight)
            bytes_score = (bytes * total_byte_weight)
            average_bytes_score = (average_bytes * byte_average_weight)
            packets_score = (packets * total_packets_weight)
            average_packets_score = (average_packets * average_packet_weight)

            total_score = math.sqrt(event_score + average_events_score + duration_score + average_duration_score
                                     + bytes_score + average_bytes_score + packets_score + average_packets_score)

            list_of_raw_ratings.append([flow[0], total_score])
        return list_of_raw_ratings