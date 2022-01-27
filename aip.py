"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import csv
import os
import shutil
from datetime import datetime
from inspect import getmembers, isfunction
from logging import getLogger

from core.safelist import Safelist
import core.main_modulev3 as modules
from models.flows import Flow
from models.raw_ratings import RawRating
from slips_aip_constants.defaults import Defaults


logger = getLogger(__name__)


class AIP:
    """
    Generates IPv4 address blocklists

    Stratosphere IPS | Attacker IP Prioritizer (AIP)
    """
    
    def __init__(self):
        """
        TODO: Update function specs
        """
        pass


    def find_new_data_files(self, raw_data_dir_path, processed_files_filepath) -> tuple:
        """
        Finds which data files have not been processed yet

        :param raw_data_dir_path: stirng with data dir path
        :param processed_files_filepath: string with filepath for processed files

        :return: tuple[list, list]. new_data_files_list, reference_date
        """
        pass

    def open_sort_new_file(raw_data_dir_path, new_files) -> tuple:
        """
        TODO: Update function specs
        """
        pass


    def open_sort_abs_file(absolute_data_path) -> tuple:
        """
        TODO: Update function specs
        """
        pass


    def get_updated_flows(absolute_data_path) -> list:
        """
        TODO: Update function specs
        """
        pass


    def sort_ips_from_data(ips_from_absolute_data, ip_flows_from_today: list[Flow]) -> tuple:
        """
        TODO: Update function specs
        """
        pass


    def write_unkown_ips_to_data_file(unknown_ips, known_ips_filepath) -> None:
        """
        TODO: Update function specs
        """
        pass


    def update_records_files(absolute_data_path: str,
                            new_known_ip_flows: list[Flow],
                            unknown_ip_flows: list[Flow]) -> None:
        """
        TODO: Update function specs
        """
        pass


    def sort_data_descending(raw_ratings: list[RawRating]) -> list[RawRating]:
        """
        TODO: Update function specs
        """
        pass


    def create_final_blacklist(path_to_file, data_from_absolute_file, chosen_fn) -> None:
        """
        Creates final blacklists
        """
        pass


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


def find_new_data_files(self, raw_data_dir_path, processed_files_filepath) -> tuple:
    """
    Finds which data files have not been processed yet

    :param raw_data_dir_path: stirng with data dir path
    :param processed_files_filepath: string with filepath for processed files

    :return: tuple[list, list]. new_data_files_list, reference_date
    """
    list_of_data_files = os.listdir(raw_data_dir_path)    
    new_data_files = []
    files_dates = {}

    try:
        with open(processed_files_filepath, 'r') as records_file:
            processed_files = records_file.read().split('\n')
    except IOError as e:
        logger.error(f"Unable to open {processed_files_filepath} file: {e}")
        processed_files = []

    for file in list_of_data_files:
        if file not in processed_files:
            new_data_files.extend([file])
            files_dates[file[0:10]] = file

    try:
        for new_file in new_data_files:
            with open(processed_files_filepath, 'a') as records_file:
                records_file.write(new_file + '\n')
    except (IOError, ValueError) as e:
        logger.error(f"Unable to update {processed_files_filepath} file: {e}")

    sorted_dates = sorted(files_dates,
                          key=lambda date: datetime.strptime(date, Defaults.DATE_FORMAT.value),
                          reverse=True)

    logger.info(f"{__name__} sorted dates: {sorted_dates}\n")

    return new_data_files, sorted_dates[0]

current_directory = os.getcwd()

FP_log_file = AIPP_directory + '/FP_log_file.csv'

# Full path to the  folder where the program will look for new data files. It will look in the file and only process the
# files it has not precessed yet. It will process every file it does not recognize.
# (b)
splunk_raw_data_path = AIPP_directory + '/Input_Data'

# Full path to the file where the program will record the data files it processes
# (c)
splunk_processed_files_path = AIPP_directory + '/Processed_Splunk_Files.txt'

# A complete list of every IP seen by the program since it was started
# (d)
known_ips_path = AIPP_directory + '/Known_IPs.txt'

# Full path to the file where the data flows for each IP are stored. Includes all the data the program has received
# since it was started. This is NOT the file that contains the ratings.
# (e)
absolute_data_path = AIPP_directory + '/Absolute_Data.csv'

# Full path to folder that wil contain the daily rating files. This is a FOLDER!!
# (f)
historical_ratings_path = AIPP_directory + '/Historical_Ratings'


# >>>>>>>>>>>>>>> Call the find new file function and define the time reference point for the aging function
new_data_files, reference_date = find_new_data_files(splunk_raw_data_path, splunk_processed_files_path)

logger.info(f"{__name__} there are ({len(new_data_files)}) new data files to process\n")
logger.info(f"{__name__} files are {new_data_files}\n")

current_time = datetime(int(reference_date[0:4]), int(reference_date[5:7]), int(reference_date[8:10]), 1).timestamp()

logger.info(f"{__name__} start time {startTime}\n")
logger.info(f"{__name__} started\n")


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Blacklist Files <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Path to the file that will contain top IPs from today's data only. Program will overwrite the previous days data.
# (g)
top_ips_seen_today = historical_ratings_path + '/Seen_today_Only/' + reference_date + '_new_blacklist.csv'

# Path to file that will contain the top IPs from the data from all time. Program will overwrite the previous days data.
# (h)
top_ips_for_all_time = historical_ratings_path + '/Prioritize_Consistent/' + reference_date + '_pc_blacklist.csv'

# Path to file that will have the ratings that will prioritize the IPs that are newer over older ones based on
# all the data.
top_ips_all_time_newer_prioritized = historical_ratings_path + '/Prioritize_New/' + reference_date + '_pn_blacklist.csv'

# Path to file that will save the traditional blacklist
traditional_blacklist = historical_ratings_path + '/Traditional/' + reference_date + '_trad_blacklist.csv'

# File that will be storing the run times for this script
time_file = AIPP_directory + '/Times.csv'

# Files for keeping track of aging modifiers
path_aging_modifier_pc = AIPP_directory + '/Aging-modifiers-pc.csv'
path_aging_modifier_pn = AIPP_directory + '/Aging-modifiers-pn.csv'

def open_sort_new_file(raw_data_dir_path, new_files):
    """
    TODO: Update function specs
    """
    new_ip_flows = []
    new_ips = []
    for file in new_files:
        with open(f"{raw_data_dir_path}/{file}", 'r') as csv_file:
            for line in csv.reader(csv_file):
                if line[0] != 'SrcAddr':
                    new_ip_flows.append(Flow(line))
                    new_ips.append(line[0])

    return new_ip_flows, new_ips


def open_sort_abs_file(absolute_data_path) -> tuple:
    """
    TODO: Update function specs
    """
    ip_flows = []
    ips_in_absolute_file = []
    with open(absolute_data_path, 'r') as csv_file:
        for line in csv.reader(csv_file):
            if line:
                ip_flows.append(Flow(line=line))
                ips_in_absolute_file.append(line[0])

    return ip_flows, ips_in_absolute_file


def get_updated_flows(absolute_data_filepath) -> list:
    """
    TODO: Update function specs
    """
    try:
        with open(absolute_data_filepath, 'r') as csv_file:
            ip_flows = [Flow(line) for line in csv.reader(csv_file)
                        if line]
    except IOError as e:
        logger.error(f"Unable to open {absolute_data_filepath} file: {e}")
        return []

    return ip_flows


def sort_ips_from_data(ips_from_absolute_data, ip_flows_from_today: list[Flow]) -> tuple:
    """
    TODO: Update function specs
    """
    unknown_ip_flows = []
    unknown_ips = []
    known_ips = []
    known_ip_flows = []
    for ip_flow in ip_flows_from_today:
        if ip_flow.src_address in ips_from_absolute_data:
            known_ip_flows.append(ip_flow)
            known_ips.append(ip_flow.src_address)
        else:
            unknown_ip_flows.append(ip_flow)
            unknown_ips.append(ip_flow.src_address)

    return unknown_ip_flows, unknown_ips, known_ip_flows, known_ips


def write_unkown_ips_to_data_file(unknown_ips, known_ips_filepath) -> None:
    """
    TODO: Update function specs
    """
    try:
        with open(known_ips_filepath, 'a') as data_file:
            for flow in unknown_ips:
                data_file.write(flow + '\n')
    except IOError as e:
        logger.error(f"Unable to append data to {known_ips_filepath} file: {e}")


def update_records_files(absolute_data_path: str,
                         new_known_ip_flows: list[Flow],
                         unknown_ip_flows: list[Flow]) -> None:
    """
    TODO: Update function specs
    """
    known_ip_flows, ips_in_abs_file = open_sort_abs_file(absolute_data_path)
    new_absolute_flows = []
    new_absolute_flows.extend(known_ip_flows)
    new_unknown_ip_flows = [unknown_ip_flow for unknown_ip_flow in unknown_ip_flows]
    new_absolute_flows.extend(new_unknown_ip_flows)

    if new_known_ip_flows:
        for idx1, new_flow in enumerate(new_known_ip_flows):
            for idx2, absolute_flow in enumerate(new_absolute_flows):
                if absolute_flow.src_address == new_flow.src_address:
                    days_since_first_seen = (current_time - absolute_flow.last_event) // Defaults.MINUTES_A_DAY.value
                    dh_events = (absolute_flow.avg_events * (days_since_first_seen - 1)) + new_flow.events

                    if days_since_first_seen != 0:
                        updated_events_average = dh_events / days_since_first_seen
                    else:
                        updated_events_average = dh_events

                    updated_flow = Flow()
                    updated_flow.src_address = new_flow.src_address
                    updated_flow.events = absolute_flow.events + new_flow.events
                    updated_flow.duration = absolute_flow.duration + new_flow.duration
                    updated_flow.avg_duration = (absolute_flow.avg_duration + new_flow.avg_duration) / 2.0
                    updated_flow.bytes = absolute_flow.bytes + new_flow.bytes
                    updated_flow.avg_bytes = (absolute_flow.avg_bytes + new_flow.avg_bytes) / 2.0
                    updated_flow.packets = absolute_flow.packets + new_flow.packets
                    updated_flow.avg_packets = (absolute_flow.avg_packets + new_flow.avg_packets) / 2.0
                    updated_flow.first_event = absolute_flow.first_event
                    updated_flow.last_event = new_flow.last_event
                    updated_flow.avg_events = updated_events_average

                    new_absolute_flows[idx2] = updated_flow

    safelist = Safelist()
    asn_info = safelist.get_asn_data(f"{current_directory}/core/asn/GeoLite2-ASN.mmdb",
                                     new_absolute_flows)
    list_of_FPs = [] # What does FPs stand for?
    for index, flow in enumerate(new_absolute_flows):
        first_judgement = safelist.check_if_ip_in_safelisted_nets(flow.src_address)
        second_judgement = safelist.check_if_ip_in_safelisted_ips(flow.src_address)
        third_judgement, org_name = safelist.check_if_org_in_safelisted_orgs(asn_info[flow.src_address])

        if first_judgement:
            list_of_FPs.append(flow)
            del new_absolute_flows[index]
            logger.info(f"Found {flow.src_address} in safelisted Nets. Deleting entry...\n")
        elif second_judgement:
            list_of_FPs.append(flow)
            del new_absolute_flows[index]
            logger.info(f"Found {flow.src_address} in safelisted IPs. Deleting entry...\n")
        elif third_judgement:
            list_of_FPs.append(flow)
            del new_absolute_flows[index]
            logger.info(f"Found {flow.src_address} ASN matches organization {org_name} Deleting entry...\n")

    with open(FP_log_file, 'a') as FP_file:
        csv_writer = csv.writer(FP_file)
        csv_writer.writerows(list_of_FPs)

    with open(absolute_data_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            for y in new_absolute_flows:
                csv_writer.writerow(y)


def sort_data_descending(raw_ratings: list[RawRating]) -> list[RawRating]:
    """
    TODO: Update function specs
    """
    return sorted(raw_ratings, key=lambda x: x.total_score, reverse=True)

# Now call all the functions on the data

known_data_flows, known_ips = open_sort_abs_file(absolute_data_path)
new_ip_flows, new_ips = open_sort_new_file(splunk_raw_data_path, new_data_files)
new_unknown_ip_flows, unknown_ips, known_ip_flows, new_known_ips = sort_ips_from_data(known_ips, new_ip_flows)

write_unkown_ips_to_data_file(unknown_ips, known_ips_path)
update_records_files(absolute_data_path, known_ip_flows, new_unknown_ip_flows)

number_of_lines = len(open(absolute_data_path).readlines())

logger.info(f"Number of lines in absolute data {number_of_lines}\n")


def create_final_blacklist(path_to_file, data_from_absolute_file, chosen_fn):
    """
    Creates final blacklists
    """
    with open(path_to_file, 'wt', newline ='') as blocklist_file:
        header_writer = csv.DictWriter(blocklist_file, fieldnames=['# Top IPs from data gathered in last 24 hours only', reference_date])
        header_writer.writeheader()
        csv_writer = csv.DictWriter(blocklist_file, fieldnames=['# Number', 'IP address', 'Rating'])
        csv_writer.writeheader()
        if chosen_fn == getattr(modules, list_of_functions_that_were_choosen[1]):
            logger.info("Using Prioritize New Function")
            new_ratings = chosen_fn(data_from_absolute_file, current_time, path_aging_modifier_pn)
            for idx2, rating in enumerate(sort_data_descending(new_ratings)):
                if rating.total_score >= 0.002: # What does this value mean???
                    new_entry = {'number': idx2,
                                 'ip_address': rating.src_address,
                                 'rating': rating.total_score}
                    csv_writer.writerows([new_entry])
                else:
                    break
        elif chosen_fn == getattr(modules, list_of_functions_that_were_choosen[0]):
            logger.info("Using Prioritize Consistent Function")
            new_ratings = chosen_fn(data_from_absolute_file, current_time, path_aging_modifier_pc)
            for idx2, rating in enumerate(sort_data_descending(new_ratings)):
                if rating.total_score >= 0.057: # What does this value mean???
                    new_entry = {'number': idx2,
                                 'ip_address': rating.src_address,
                                 'rating': rating.total_score}
                    csv_writer.writerows([new_entry])
                else:
                    break
        else:
            logger.info("Using Only New IPs Function")
            new_ratings = chosen_fn(data_from_absolute_file, current_time, path_aging_modifier_pc)
            for idx2, rating in enumerate(sort_data_descending(new_ratings)):
                new_entry = {'number': idx2,
                             'ip_address': rating.src_address,
                             'rating': rating.total_score}
                csv_writer.writerows([new_entry])


# Pull the three functions that were choosen by the user from the dictionary of functions.
# print(list_of_functions_that_were_choosen)

PCF = getattr(modules, list_of_functions_that_were_choosen[0])
PNF = getattr(modules, list_of_functions_that_were_choosen[1])
OTF = getattr(modules, list_of_functions_that_were_choosen[2])

# Call the create blacklist function for each of the three user input functions
create_final_blacklist(top_ips_for_all_time, get_updated_flows(absolute_data_path), PCF)
create_final_blacklist(top_ips_all_time_newer_prioritized, get_updated_flows(absolute_data_path), PNF)
create_final_blacklist(top_ips_seen_today, new_unknown_ip_flows, OTF)

shutil.copy2(known_ips_path, traditional_blacklist)

logger.info(f"Total runtime: {datetime.utcnow() - startTime}\n")
logger.info("---------------- AIP run complete ----------------\n")

# Append the time that it took to a file
with open(time_file, 'a') as csv_time_file:
    csv_writer = csv.writer(csv_time_file, quoting=csv.QUOTE_ALL)
    csv_writer.writerow([reference_date, datetime.utcnow() - startTime])
