import csv
import operator
import time
import datetime
import os
from today_rating_function import rate_IPs_today
from all_time_rating_function import rate_IPs_all_time
from new_IPs_prioritized_function import rate_IPs_all_time_new_important

current_time = time.time()
today = datetime.date.today()

# Full path to directory where all the files will be stored
# (a)
AIP_direcory = '/path/to/install/file'

# Full path to the  folder where the program will look for new data files. It will look in the file and only process the
# files it has not precessed yet. It will process every file it does not recognize.
# (b)
folder_path_for_raw_network_csv_data = AIP_direcory + '/Data'

# Full path to the file where the program will record the data files it processes
# (c)
record_file_path_for_processed_data_files = AIP_direcory + '/Processed_Data_Files.txt'

# A complete list of every IP seen by the program since it was started
# (d)
record_file_path_to_known_IPs = AIP_direcory + '/Known_IPs.txt'

# Full path to the file where the data flows for each IP are stored. Includes all the data the program has received
# since it was started. This is NOT the file that contains the ratings.
# (e)
record_file_path_for_absolute_data = AIP_direcory + '/Absolute_Data.csv'

# Full path to folder that wil contain the daily rating files. This is a FOLDER!!
# (f)
directory_path_historical_ratings = AIP_direcory + '/Historical_Ratings'

# Path to the file that will contain top 1000 IPs from todays data only. Program will overwrite the previous days data.
# (g)
top_IPs_seen_today = AIP_direcory + '/Today-Top-IPs.csv'

# Full path to file that will contain the top 1000 IPs from the data from all time. Program will overwrite the previous
# days data.
# (h)
top_IPs_for_all_time = AIP_direcory + '/All-Time-Top-IPs.csv'

# Full path to file that will contain all the IPs and their ratings, not just the top IPs
all_IPs_seen_today = AIP_direcory + '/Today-All-IPs.csv'

all_IPs_from_all_time = AIP_direcory + '/All-Time-All-IPs.csv'

# Full path to the file that will have the ratings that will prioritize the IPs that are newer over older ones based on
# all the data.
top_IPs_all_time_newer_prioritized = AIP_direcory + '/all_time_NEW_IPS_Prioritized.csv'


def find_new_data_files(b, c):
    list_of_new_data_files = []
    list_of_data_files = os.listdir(b)
    with open(c, 'r') as record:
        list_of_processed_data_files = record.read().split('\n')
    for file in list_of_data_files:
        if file not in list_of_processed_data_files:
            list_of_new_data_files.extend([file])
    for file12 in list_of_new_data_files:
        with open(c, 'a') as records_file1:
            records_file1.write(file12 + '\n')
    return list_of_new_data_files


def open_sort_new_file(b, list_of_new_files):
    list_of_new_data_flows = []
    list_of_IPs_in_new_data = []
    for file in list_of_new_files:
        with open(b + '/' + file, 'r') as csvfile:
            for line in csv.reader(csvfile):
                if line[0] != 'SrcAddr':
                    list_of_new_data_flows.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]])
                    list_of_IPs_in_new_data.append(line[0])
                else:
                    continue
    return list_of_new_data_flows, list_of_IPs_in_new_data


def open_sort_abs_file(e):
    IP_flows = []
    IPs_in_absolute_file = []
    with open(e, 'r') as csvfile:
        for line in csv.reader(csvfile):
            if not line:
                break
            else:
                IP_flows.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]])
                IPs_in_absolute_file.append(line[0])
    return IP_flows, IPs_in_absolute_file


def sort_IPs_from_data(IPs_from_absolute_data, IP_flows_from_todays_data):
    unknown_IP_flows = []
    unknown_IPs = []
    known_IPs = []
    known_IP_data_flows = []
    for IP in IP_flows_from_todays_data:
        if IP[0] in IPs_from_absolute_data:
            known_IP_data_flows.append(IP)
            known_IPs.append(IP[0])
        elif IP[0] not in IPs_from_absolute_data:
            unknown_IP_flows.append(IP)
            unknown_IPs.append(IP[0])
    return unknown_IP_flows, unknown_IPs, known_IP_data_flows, known_IPs


def write_unkown_IPs_to_data_file(list_of_unknown_IPs, d):
    with open(d, 'a') as data_file:
        for flow in list_of_unknown_IPs:
            data_file.write(flow + '\n')


def update_records_files(e, list_of_known_new_IP_data, unknown_IP_flows):
    absolute_data, IPs_in_abs_file = open_sort_abs_file(e)
    new_absolute_file_flows = []
    new_absolute_file_flows += absolute_data
    unknown_IP_flows_new = []
    for new_flow2 in unknown_IP_flows:
        new_flow2.extend([new_flow2[1]])
        unknown_IP_flows_new.append(new_flow2)
    new_absolute_file_flows.extend(unknown_IP_flows_new)

    if not list_of_known_new_IP_data:
        pass

    else:
        for x1, new_flow in enumerate(list_of_known_new_IP_data):
            for x2, absolute_flow in enumerate(new_absolute_file_flows):
                if absolute_flow[0] == new_flow[0]:
                    days_since_first_seen = (current_time - float(absolute_flow[9])) // 86400.0
                    if days_since_first_seen != 0:
                        updated_event_average = ((float(absolute_flow[10])) * (days_since_first_seen - 1) + float(
                            new_flow[1])) / days_since_first_seen
                    else:
                        updated_event_average = ((float(absolute_flow[10])) * (days_since_first_seen - 1) + float(
                            new_flow[1])) / 1
                    # if absolute_flow[8] == '0':
                    #     updated_SD = (((float(absolute_flow[1]) - updated_event_average) ** 2 + (
                    #             float(new_flow[1]) - updated_event_average) ** 2) / 2.0) ** .5
                    # else:
                    #     updated_SD = ((((float(absolute_flow[8])) ** 2) * (days_since_first_seen - 1) + (
                    #             float(new_flow[1]) - updated_event_average) ** 2) / days_since_first_seen) ** .5

                    updated_total_events = float(new_flow[1]) + float(absolute_flow[1])
                    updated_total_duration = float(absolute_flow[2]) + float(new_flow[2])
                    updated_average_duration = (float(absolute_flow[3]) + float(new_flow[3])) / 2.0
                    updated_total_bytes = float(absolute_flow[4]) + float(new_flow[4])
                    updated_average_bytes = (float(absolute_flow[5]) + float(new_flow[5])) / 2.0
                    updated_total_packets = float(absolute_flow[6]) + float(new_flow[6])
                    updated_average_packets = (float(absolute_flow[7]) + float(new_flow[7])) / 2.0
                    updated_last_event = new_flow[9]

                    updated_entry = [new_flow[0], updated_total_events, updated_total_duration,
                                     updated_average_duration,
                                     updated_total_bytes, updated_average_bytes, updated_total_packets,
                                     updated_average_packets,
                                     absolute_flow[8], updated_last_event, updated_event_average]
                    new_absolute_file_flows[x2] = updated_entry
                    break
                else:
                    continue

    with open(e, 'w') as new_file_another:
        wr2 = csv.writer(new_file_another, quoting=csv.QUOTE_ALL)
        for y in new_absolute_file_flows:
            wr2.writerow(y)


def sort_data_decending(data):
    list_as_dictionary = {}
    for entry in data:
        list_as_dictionary[entry[0]] = entry[1]
    return sorted(list_as_dictionary.items(), key=operator.itemgetter(1), reverse=True)


# Now call all the functions on the data

new_data_files = find_new_data_files(folder_path_for_raw_network_csv_data, record_file_path_for_processed_data_files)

list_of_known_data_flows, list_of_known_IPs_in_data = open_sort_abs_file(record_file_path_for_absolute_data)

list_of_new_data_flows, list_of_IPs_in_new_data = open_sort_new_file(folder_path_for_raw_network_csv_data, new_data_files)

unknown_IP_flows_from_new_data, unknown_IPs_from_new_data, known_IP_data_flows_from_new_data, known_IPs_from_new_data\
    = sort_IPs_from_data(list_of_known_IPs_in_data, list_of_new_data_flows)

write_unkown_IPs_to_data_file(unknown_IPs_from_new_data, record_file_path_to_known_IPs)

update_records_files(record_file_path_for_absolute_data, known_IP_data_flows_from_new_data, unknown_IP_flows_from_new_data)

new_absolute_file_data, new_IPs = open_sort_abs_file(record_file_path_for_absolute_data)


with open(top_IPs_seen_today, 'w') as new_file2:
    write2 = csv.writer(new_file2, quoting=csv.QUOTE_ALL)
    write2.writerow(('Top 5000 IPs from data gathered in last 24 hours only', str(today)))
    write2.writerow(('Number', 'IP address', 'Rating'))
    for x2, interesting_rating2 in enumerate(sort_data_decending(rate_IPs_today(unknown_IP_flows_from_new_data))):
        if x2 <= 4999.0:
            new_list2 = []
            new_list2.append(x2)
            new_list_interesting_rating2 = list(interesting_rating2)
            new_list2.extend(new_list_interesting_rating2)
            write2.writerow(new_list2)
        elif x2 > 4999.0:
            if float(list(interesting_rating2)[1]) >= 20.0:
                new_list2 = []
                new_list2.append(x2)
                new_list_interesting_rating2 = list(interesting_rating2)
                new_list2.extend(new_list_interesting_rating2)
                write2.writerow(new_list2)

with open(top_IPs_for_all_time, 'w') as new_file1:
    write1 = csv.writer(new_file1, quoting=csv.QUOTE_ALL)
    write1.writerow(('Top 5000 IPs based on the accumulated data gathered since AIP started', str(today)))
    write1.writerow(('Number', 'IP address', 'Rating'))
    for x1, interesting_rating1 in enumerate(
            sort_data_decending(
                rate_IPs_all_time(new_absolute_file_data))):
        if x1 <= 4999.0:
            new_list1 = []
            new_list1.append(x1)
            new_list_interesting_rating1 = list(interesting_rating1)
            new_list1.extend(new_list_interesting_rating1)
            write1.writerow(new_list1)
        elif x1 > 4999.0:
            if float(list(interesting_rating1)[1]) >= 20.0:
                new_list1 = []
                new_list1.append(x1)
                new_list_interesting_rating1 = list(interesting_rating1)
                new_list1.extend(new_list_interesting_rating1)
                write1.writerow(new_list1)

with open(all_IPs_from_all_time, 'w') as new_file3:
    write1 = csv.writer(new_file3, quoting=csv.QUOTE_ALL)
    write1.writerow(('Ratings for all IPs from data gathered since AIP started', str(today)))
    write1.writerow(('Number', 'IP address', 'Rating'))
    for x1, interesting_rating1 in enumerate(sort_data_decending(rate_IPs_all_time(new_absolute_file_data))):
        new_list1 = []
        new_list1.append(x1)
        new_list_interesting_rating1 = list(interesting_rating1)
        new_list1.extend(new_list_interesting_rating1)
        write1.writerow(new_list1)

with open(all_IPs_seen_today, 'w') as new_file4:
    write2 = csv.writer(new_file4, quoting=csv.QUOTE_ALL)
    write2.writerow(('Ratings for all IPs from data gathered in last 24 hours only', str(today)))
    write2.writerow(('Number', 'IP address', 'Rating'))
    for x2, interesting_rating2 in enumerate(sort_data_decending(rate_IPs_today(unknown_IP_flows_from_new_data))):
        new_list2 = []
        new_list2.append(x2)
        new_list_interesting_rating2 = list(interesting_rating2)
        new_list2.extend(new_list_interesting_rating2)
        write2.writerow(new_list2)

with open(top_IPs_all_time_newer_prioritized, 'w') as new_file5:
    write1 = csv.writer(new_file5, quoting=csv.QUOTE_ALL)
    write1.writerow(('Top 5000 IPs based on all data, but NEW IPs are prioritized', str(today)))
    write1.writerow(('Number', 'IP address', 'Rating'))
    for x1, interesting_rating1 in enumerate(sort_data_decending(rate_IPs_all_time_new_important(new_absolute_file_data))):
        if x1 <= 4999.0:
            new_list1 = []
            new_list1.append(x1)
            new_list_interesting_rating1 = list(interesting_rating1)
            new_list1.extend(new_list_interesting_rating1)
            write1.writerow(new_list1)
        elif x1 > 4999.0:
            if float(list(interesting_rating1)[1]) >= 20.0:
                new_list1 = []
                new_list1.append(x1)
                new_list_interesting_rating1 = list(interesting_rating1)
                new_list1.extend(new_list_interesting_rating1)
                write1.writerow(new_list1)
