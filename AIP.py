"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import csv
import operator
import os
import shutil
from datetime import datetime
from inspect import getmembers, isfunction
from typing import IO

from netaddr import IPAddress, IPNetwork

from core.safelist import *
import core.main_modulev3 as modules
from models.flows import Flow
from slips_aip_constants.defaults import Defaults

# Full path to directory where all the files will be stored
# (a)
AIPP_directory = os.environ['output_folder']

startTime = datetime.utcnow()

# Open the file that stored the selected modules, and store the selections in
# a list.
file_for_functions = AIPP_directory + '/Selected_modules.csv'

with open(file_for_functions, 'r') as file:
    list_of_functions_that_were_choosen = [line for line in csv.reader(file) if line]

functions_list = [o for o in getmembers(modules) if isfunction(o[1])]


# >>>>>>>>> Needs to be here so it can be called immediately, fine what data
# files have not been processed.
def find_new_data_files(raw_data_dir_path, processed_files_filepath):
    """
    Finds which data files have not been processed yet

    :param raw_data_dir_path: stirng with data dir path
    :param processed_files_filepath: string with filepath for processed files

    :return: tuple[list, list]. new data files
    """
    list_of_data_files = os.listdir(raw_data_dir_path)
    
    new_data_files_list = []
    dictionary_of_dates_on_files = {}

    with open(processed_files_filepath, 'r') as record:
        list_of_processed_data_files = record.read().split('\n')

    for file in list_of_data_files:
        if file not in list_of_processed_data_files:
            new_data_files_list.extend([file])
            dictionary_of_dates_on_files[file[0:10]] = file

    for new_file in new_data_files_list:
        with open(processed_files_filepath, 'a') as records_file:
            records_file.write(new_file + '\n')

    sorted_dates = sorted(dictionary_of_dates_on_files,
                          key=lambda date: datetime.strptime(date, Defaults.DATE_FORMAT.value),
                          reverse=True)

    with open(AIPP_directory + "log.txt", "a") as myfile:
        myfile.write(str(sorted_dates) + "\n")

    return new_data_files_list, sorted_dates[0]

current_directory = os.getcwd()

FP_log_file = AIPP_directory + '/FP_log_file.csv'

# Full path to the  folder where the program will look for new data files. It will look in the file and only process the
# files it has not precessed yet. It will process every file it does not recognize.
# (b)
raw_splunk_data_filepath = AIPP_directory + '/Input_Data'

# Full path to the file where the program will record the data files it processes
# (c)
splunk_processed_files_filepath = AIPP_directory + '/Processed_Splunk_Files.txt'

# A complete list of every IP seen by the program since it was started
# (d)
known_ips_filepath = AIPP_directory + '/Known_IPs.txt'

# Full path to the file where the data flows for each IP are stored. Includes all the data the program has received
# since it was started. This is NOT the file that contains the ratings.
# (e)
absolute_data_path = AIPP_directory + '/Absolute_Data.csv'

# Full path to folder that wil contain the daily rating files. This is a FOLDER!!
# (f)
historical_ratings_path = AIPP_directory + '/Historical_Ratings'


# >>>>>>>>>>>>>>> Call the find new file function and define the time reference point for the aging function
new_data_files, reference_date = find_new_data_files(raw_splunk_data_filepath, splunk_processed_files_filepath)

with open(AIPP_directory + "/log.txt", "a") as myfile:
    myfile.write('There are ' + str(len(new_data_files)) + ' new data files to process' + "\n")
    myfile.write('Files are ' + str(new_data_files) + "\n")
current_time = datetime(int(reference_date[0:4]), int(reference_date[5:7]), int(reference_date[8:10]), 1).timestamp()

with open(AIPP_directory + "/log.txt", "a") as myfile:
    myfile.write(str(startTime) + "\n")
    myfile.write("AIP started" + "\n")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Blacklist Files <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Path to the file that will contain top IPs from today's data only. Program will overwrite the previous days data.
# (g)
top_IPs_seen_today = historical_ratings_path + '/Seen_today_Only/' + reference_date + '_new_blacklist.csv'

# Path to file that will contain the top IPs from the data from all time. Program will overwrite the previous days data.
# (h)
top_IPs_for_all_time = historical_ratings_path + '/Prioritize_Consistent/' + reference_date + '_pc_blacklist.csv'

# Path to file that will have the ratings that will prioritize the IPs that are newer over older ones based on
# all the data.
top_IPs_all_time_newer_prioritized = historical_ratings_path + '/Prioritize_New/' + reference_date + '_pn_blacklist.csv'

# Path to file that will save the traditional blacklist
traditional_blacklist = historical_ratings_path + '/Traditional/' + reference_date + '_trad_blacklist.csv'

# File that will be storing the run times for this script
time_file = AIPP_directory + '/Times.csv'

# Files for keeping track of aging modifiers
path_aging_modifier_pc = AIPP_directory + '/Aging-modifiers-pc.csv'
path_aging_modifier_pn = AIPP_directory + '/Aging-modifiers-pn.csv'

def open_sort_new_file(b, list_of_new_files):
    """
    """
    list_of_new_data_flows = []
    list_of_new_ips = []
    for file in list_of_new_files:
        with open(b + '/' + file, 'r') as csvfile:
            for line in csv.reader(csvfile):
                if line[0] != 'SrcAddr':
                    list_of_new_data_flows.append(Flow(line))
                    list_of_new_ips.append(line[0])
    return list_of_new_data_flows, list_of_new_ips


def open_sort_abs_file(e):
    """
    """
    ip_flows = []
    ips_in_absolute_file = []
    with open(e, 'r') as csv_file:
        for line in csv.reader(csv_file):
            if line:
                ip_flows.append(Flow(line))
                ips_in_absolute_file.append(line[0])
    return ip_flows, ips_in_absolute_file


def get_updated_flows(absolute_data_filepath) -> list:
    """
    """
    try:
        with open(absolute_data_filepath, 'r') as csv_file:
            ip_flows = [Flow(line) for line in csv.reader(csv_file)
                        if line]
    except IOError as e:
        logger.error(f"Unable to open {absolute_data_filepath} file: {e}")
        return []
    return ip_flows


def sort_ips_from_data(ips_from_absolute_data, ip_flows_from_todays_data):
    """
    """
    unknown_ip_flows = []
    unknown_ips = []
    known_ips = []
    known_ip_data_flows = []
    for ip_flow in ip_flows_from_todays_data:
        if ip_flow.src_address in ips_from_absolute_data:
            known_ip_data_flows.append(ip_flow)
            known_ips.append(ip_flow.src_address)
        else:
            unknown_ip_flows.append(ip_flow)
            unknown_ips.append(ip_flow.src_address)
    return unknown_ip_flows, unknown_ips, known_ip_data_flows, known_ips


def write_unkown_ips_to_data_file(list_of_unknown_ips, known_ips_filepath) -> None:
    try:
        with open(known_ips_filepath, 'a') as data_file:
            for flow in list_of_unknown_ips:
                data_file.write(flow + '\n')
    except IOError as e:
        logger.error(f"Unable to append data to {known_ips_filepath} file: {e}")


def update_records_files(e, list_of_known_new_IP_data, unknown_ip_flows):
    absolute_data, IPs_in_abs_file = open_sort_abs_file(e)
    new_absolute_file_flows = []
    new_absolute_file_flows += absolute_data
    new_unknown_ip_flows = []
    for new_flow2 in unknown_ip_flows:
        new_flow2.extend([new_flow2[1]])
        new_unknown_ip_flows.append(new_flow2)

    new_absolute_file_flows.extend(new_unknown_ip_flows)

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

    safelist = Safelist()
    asn_info = safelist.get_ASN_data(current_directory + '/Main/ASN/GeoLite2-ASN.mmdb',
                                     new_absolute_file_flows)
    safelisted_nets, safelisted_ips, safelisted_orgs = safelist.load_safelists()
    list_of_FPs = []
    for index, flow in enumerate(new_absolute_file_flows):
        first_judgement = safelist.check_if_ip_in_safelisted_nets(flow.src_address, safelisted_nets)
        second_judgement = safelist.check_if_ip_in_safelisted_ips(flow.src_address, safelisted_ips)
        third_judgement, entry = safelist.check_organization_alignment(asn_info[flow.src_address], safelisted_orgs)

        if first_judgement:
            list_of_FPs.append(flow)
            del new_absolute_file_flows[index]
            with open(AIPP_directory + "/log.txt", "a") as myfile:
                myfile.write('Found ' + flow.src_address + ' in Safelisted Nets. Deleting entry...' + "\n")
        elif second_judgement:
            list_of_FPs.append(flow)
            del new_absolute_file_flows[index]
            with open(AIPP_directory + "/log.txt", "a") as myfile:
                myfile.write('Found ' + flow.src_address + ' in Safelisted IPs. Deleting entry...' + "\n")
        elif third_judgement:
            list_of_FPs.append(flow)
            del new_absolute_file_flows[index]
            with open(AIPP_directory + "/log.txt", "a") as myfile:
                myfile.write('Found ' + flow.src_address + ' ASN matches organization ' + str(entry) + ' Deleting entry...' + "\n")
        else:
            continue

    with open(FP_log_file, 'a') as FP_file:
        csvwriter = csv.writer(FP_file)
        csvwriter.writerows(list_of_FPs)

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

list_of_known_data_flows, list_of_known_IPs_in_data = open_sort_abs_file(absolute_data_path)
list_of_new_data_flows, list_of_IPs_in_new_data = open_sort_new_file(raw_splunk_data_filepath, new_data_files)

unknown_IP_flows_from_new_data, unknown_IPs_from_new_data, known_IP_data_flows_from_new_data, known_IPs_from_new_data\
    = sort_ips_from_data(list_of_known_IPs_in_data, list_of_new_data_flows)

write_unkown_ips_to_data_file(unknown_IPs_from_new_data, known_ips_filepath)

update_records_files(absolute_data_path, known_IP_data_flows_from_new_data, unknown_IP_flows_from_new_data)

number_of_lines = len(open(absolute_data_path).readlines())
with open(AIPP_directory + "/log.txt", "a") as myfile:
    myfile.write('Number of lines in absolute data' + str(number_of_lines) + "\n")

def create_final_blacklist(path_to_file, data_from_absolute_file, function_to_use):
    with open(path_to_file, 'wt', newline ='') as new_file2:
        writer = csv.DictWriter(new_file2, fieldnames=['# Top IPs from data gathered in last 24 hours only', reference_date])
        writer.writeheader()
        writer1 = csv.DictWriter(new_file2, fieldnames=['# Number', 'IP address', 'Rating'])
        writer1.writeheader()
        if function_to_use == getattr(modules, list_of_functions_that_were_choosen[1]):
            with open(AIPP_directory + "log.txt", "a") as myfile:
                myfile.write('Using Prioritize New Function')
            for x2, interesting_rating2 in enumerate(sort_data_decending(function_to_use(data_from_absolute_file, current_time, path_aging_modifier_pn))):
                if float(interesting_rating2[1]) >= 0.002:
                    new_entry = {'# Number': x2, 'IP address': list(interesting_rating2)[0], 'Rating': interesting_rating2[1]}
                    writer1.writerows([new_entry])
                else:
                    break
        elif function_to_use == getattr(modules, list_of_functions_that_were_choosen[0]):
            with open(AIPP_directory + "log.txt", "a") as myfile:
                myfile.write('Using Prioritize Consistent Function')
            for x2, interesting_rating2 in enumerate(sort_data_decending(function_to_use(data_from_absolute_file, current_time, path_aging_modifier_pc))):
                if float(interesting_rating2[1]) >= 0.057:
                    new_entry = {'# Number': x2, 'IP address': list(interesting_rating2)[0],
                                 'Rating': interesting_rating2[1]}
                    writer1.writerows([new_entry])
                else:
                    break
        else:
            with open(AIPP_directory + "log.txt", "a") as myfile:
                myfile.write('Using Only New IPs Function')
            for x2, interesting_rating2 in enumerate(sort_data_decending(function_to_use(data_from_absolute_file, current_time, path_aging_modifier_pc))):
                new_entry = {'# Number': x2, 'IP address': list(interesting_rating2)[0],
                             'Rating': interesting_rating2[1]}
                writer1.writerows([new_entry])



# Pull the three functions that were choosen by the user from the dictionary of functions.
# print(list_of_functions_that_were_choosen)

PCF = getattr(modules, list_of_functions_that_were_choosen[0])
PNF = getattr(modules, list_of_functions_that_were_choosen[1])
OTF = getattr(modules, list_of_functions_that_were_choosen[2])

# Call the create blacklist function for each of the three user input functions
create_final_blacklist(top_IPs_for_all_time, get_updated_flows(absolute_data_filepath), PCF)
create_final_blacklist(top_IPs_all_time_newer_prioritized, get_updated_flows(absolute_data_filepath), PNF)
create_final_blacklist(top_IPs_seen_today, unknown_IP_flows_from_new_data, OTF)


shutil.copy2(known_ips_filepath, traditional_blacklist)

with open(AIPP_directory + "/log.txt", "a") as log_file:
    myfile.write('Total Runtime' + str(datetime.utcnow() - startTime) + "\n")
    myfile.write('---------------- AIP run complete ----------------' + "\n")

# Append the time that it took to a file
with open(time_file, 'a') as new_file_another:
        wr2 = csv.writer(new_file_another, quoting=csv.QUOTE_ALL)
        list4 = [reference_date, datetime.utcnow() - startTime]
        wr2.writerow(list4)
