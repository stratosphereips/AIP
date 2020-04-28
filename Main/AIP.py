from inspect import getmembers, isfunction
import csv
import operator
from datetime import datetime
import shutil
import os
import main_modulev3
from get_functions import list_method_A_functions, list_method_B_functions, list_method_C_functions

startTime = datetime.now()

print('AIP started')

# Open the file that stored the selected modules, and store the selections in
# a list.
file_for_functions = os.environ['output_folder'] + '/Selected_modules.csv'
with open(file_for_functions, 'r') as file:
    list_of_functions_that_were_choosen = []
    for line in csv.reader(file):
        if not line:
            break
        else:
            list_of_functions_that_were_choosen.extend(line)

functions_list = [o for o in getmembers(main_modulev3) if isfunction(o[1])]


# >>>>>>>>> Needs to be here so it can be called immediately, fine what data
# files have not been processed.
def find_new_data_files(b, c):
    list_of_new_data_files = []
    list_of_data_files = os.listdir(b)
    dictionary_of_dates_on_files = {}
    with open(c, 'r') as record:
        list_of_processed_data_files = record.read().split('\n')
    for file in list_of_data_files:
        if file not in list_of_processed_data_files:
            list_of_new_data_files.extend([file])
            dictionary_of_dates_on_files[file[0:10]] = file
    for file12 in list_of_new_data_files:
        with open(c, 'a') as records_file1:
            records_file1.write(file12 + '\n')
    sorted_dates = sorted(dictionary_of_dates_on_files, key=lambda date: datetime.strptime(date, '%Y-%m-%d'))
    if len(sorted_dates) == 1:
        return list_of_new_data_files, sorted_dates[0]
    else:
        return list_of_new_data_files, sorted_dates[-1]

# Full path to directory where all the files will be stored
# (a)
AIPP_direcory = os.environ['output_folder']

# Full path to the  folder where the program will look for new data files. It will look in the file and only process the
# files it has not precessed yet. It will process every file it does not recognize.
# (b)
folder_path_for_raw_Splunk_data = AIPP_direcory + '/Input_Data'

# Full path to the file where the program will record the data files it processes
# (c)
record_file_path_for_processed_Splunk_files = AIPP_direcory + '/Processed_Splunk_Files.txt'

# A complete list of every IP seen by the program since it was started
# (d)
record_file_path_to_known_IPs = AIPP_direcory + '/Known_IPs.txt'

# Full path to the file where the data flows for each IP are stored. Includes all the data the program has received
# since it was started. This is NOT the file that contains the ratings.
# (e)
record_file_path_for_absolute_data = AIPP_direcory + '/Absolute_Data.csv'

# Full path to folder that wil contain the daily rating files. This is a FOLDER!!
# (f)
directory_path_historical_ratings = AIPP_direcory + '/Historical_Ratings'


# >>>>>>>>>>>>>>> Call the find new file function and define the time reference point for the aging function
new_data_files, date = find_new_data_files(folder_path_for_raw_Splunk_data, record_file_path_for_processed_Splunk_files)
print('There are ', len(new_data_files), ' new data files to process')
current_time = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), 1).timestamp()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Blacklist Files <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Path to the file that will contain top IPs from today's data only. Program will overwrite the previous days data.
# (g)
top_IPs_seen_today = directory_path_historical_ratings + '/Seen_today_Only/' + date + '_blacklist.csv'

# Path to file that will contain the top IPs from the data from all time. Program will overwrite the previous days data.
# (h)
top_IPs_for_all_time = directory_path_historical_ratings + '/Prioritize_Consistent/' + date + '_blacklist.csv'

# Path to file that will have the ratings that will prioritize the IPs that are newer over older ones based on
# all the data.
top_IPs_all_time_newer_prioritized = directory_path_historical_ratings + '/Prioritize_New/' + date + '_blacklist.csv'

# Path to file that will save the traditional blacklist
traditional_blacklist = directory_path_historical_ratings + '/Traditional/' + date + '_blacklist.csv'

# File that will be storing the run times for this script
time_file = AIPP_direcory + '/Times.csv'

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

list_of_known_data_flows, list_of_known_IPs_in_data = open_sort_abs_file(record_file_path_for_absolute_data)

list_of_new_data_flows, list_of_IPs_in_new_data = open_sort_new_file(folder_path_for_raw_Splunk_data, new_data_files)

unknown_IP_flows_from_new_data, unknown_IPs_from_new_data, known_IP_data_flows_from_new_data, known_IPs_from_new_data\
    = sort_IPs_from_data(list_of_known_IPs_in_data, list_of_new_data_flows)

write_unkown_IPs_to_data_file(unknown_IPs_from_new_data, record_file_path_to_known_IPs)

update_records_files(record_file_path_for_absolute_data, known_IP_data_flows_from_new_data, unknown_IP_flows_from_new_data)

new_absolute_file_data, new_IPs = open_sort_abs_file(record_file_path_for_absolute_data)


def create_final_blacklist(path_to_file, data_from_absolute_file, function_to_use):
    with open(path_to_file, 'w') as new_file2:
        write2 = csv.writer(new_file2, quoting=csv.QUOTE_ALL)
        # write2.writerow(('Top IPs from data gathered in last 24 hours only', date))
        # write2.writerow(('Number', 'IP address', 'Rating'))
        for x2, interesting_rating2 in enumerate(sort_data_decending(function_to_use(data_from_absolute_file, current_time))):
            if x2 <= 24999.0:
                new_list2 = []
                new_list2.append(list(interesting_rating2)[0])
                write2.writerow(new_list2)
            else:
                break


# Pull the three functions that were choosen by the user from the dictionary of functions.
print(list_of_functions_that_were_choosen)
PCF = getattr(main_modulev3, list_of_functions_that_were_choosen[0])
PNF = getattr(main_modulev3, list_of_functions_that_were_choosen[1])
OTF = getattr(main_modulev3, list_of_functions_that_were_choosen[2])

# Call the create blacklist function for each of the three user input functions
create_final_blacklist(top_IPs_for_all_time, new_absolute_file_data, PCF)
create_final_blacklist(top_IPs_all_time_newer_prioritized, new_absolute_file_data, PNF)
create_final_blacklist(top_IPs_seen_today, new_absolute_file_data, OTF)


shutil.copy2(record_file_path_to_known_IPs, traditional_blacklist)

# Append the time that it took to a file
with open(time_file, 'a') as new_file_another:
        wr2 = csv.writer(new_file_another, quoting=csv.QUOTE_ALL)
        list4 = []
        list4.append(date)
        list4.append(datetime.now() - startTime)
        wr2.writerow(list4)
