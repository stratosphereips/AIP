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
from logging import getLogger

from main.methodology import Methodology
from main.safelist import Safelist
from models.flows import Flow
from constants.defaults import (Blocklists,
    BlocklistConfig,
    BlocklistTypes,
    Defaults,
    DirPaths,
    EnvVars,
    FilePaths)
from utils.utils import Utils


logger = getLogger(__name__)


class AIP:
    """
    Generates IPv4 address blocklists

    Stratosphere IPS | Attacker IP Prioritizer (AIP)
    """
    
    def __init__(self, start_time):
        """
        AIP class default constructor
        """
        # Datetime when AIP started (a)
        self.start_time = start_time
        # Directory path where all the files will be stored to (b)
        self.aipp_directory = os.environ[EnvVars.OUTPUT_FOLDER.value]
        # Filepath with stored selected modules (c)
        self.functions_filepath = f"{self.aipp_directory}{FilePaths.SELECTED_MODULES.value}"
        # Filepath where FPs will be stored (d)
        self.fp_log_filepath = f"{self.aipp_directory}{FilePaths.FP_LOG.value}"
        # Directory path where AIP will look for new data files (e)
        self.raw_data_dirpath = f"{self.aipp_directory}{DirPaths.INPUT_DATA.value}"
        # Filepath where AIP will save files it processes (f)
        self.processed_files_filepath = f"{self.aipp_directory}{FilePaths.PROCESSED_FILES.value}"
        # Filepath with complete list of IPs seen since AIP started (g)
        self.known_ips_filepath = f"{self.aipp_directory}{FilePaths.KNOWN_IPS.value}"
        # Filepath where all IP data flows are stored since AIP started (h)
        self.absolute_data_filepath = f"{self.aipp_directory}{FilePaths.ABSOLUTE_DATA.value}"
        # Directory path which will contain daily rating files (i)
        self.historical_ratings_dirpath = f"{self.aipp_directory}{DirPaths.HISTORICAL_RATINGS.value}"
        # Filepath which will store run times for AIP (j)
        self.times_filepath = f"{self.aipp_directory}{FilePaths.TIMES.value}"
        # Filepath which will keep track of PC aging modifiers (k)
        self.aging_modifier_pc_filepath = f"{self.aipp_directory}{FilePaths.AGING_PC_MODS.value}"
        # Filepath which will keep track of PN aging modifiers (l)
        self.aging_modifier_pn_filepath = f"{self.aipp_directory}{FilePaths.AGING_PN_MODS.value}"


    def find_new_data_files(self, raw_data_dir_path, processed_files_filepath) -> tuple:
        """
        Finds which data files have not been processed yet

        :param raw_data_dir_path: stirng with data dir path
        :param processed_files_filepath: string with filepath for processed files

        :return: tuple(list, datetime). new_data_files_list, reference_date
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


    def open_sort_new_file(self, raw_data_dir_path, new_files) -> tuple:
        """
        Provides a tuple(list, list) with new IPs flow and IPs from input
        raw data dir

        :param raw_data_dir_path: dir path of input data
        :param new_files: list of unprocessed new data files

        :return: tuple(list, list) new_ip_flows, new_ips
        """
        new_ip_flows = []
        new_ips = []
        for file in new_files:
            with open(f"{raw_data_dir_path}/{file}", 'r') as csv_file:
                for line in csv.reader(csv_file):
                    if line[0] != 'SrcAddr':
                        new_ip_flows.append(Flow.from_line(line))
                        new_ips.append(line[0])

        return new_ip_flows, new_ips


    def open_sort_abs_file(self, absolute_data_path) -> tuple:
        """
        Provides a tuple(list, list) with IPs flow and IPs from the main
        data file

        :param absolute_data_path: filepath where all IPs flows are stored

        :return: tuple(list, list) ip_flows, ips
        """
        ip_flows = []
        ips_in_absolute_file = []
        with open(absolute_data_path, "r", encoding="utf-8") as csv_file:
            for line in csv.reader(csv_file):
                if line:
                    ip_flows.append(Flow.from_line(line))
                    ips_in_absolute_file.append(line[0])

        return ip_flows, ips_in_absolute_file


    def get_updated_flows(self, absolute_data_path) -> list:
        """
        Returns a list of the updated IP flows from absolute data file

        :param absolute_data_path: filepath where all IPs flows are stored

        :return: list of all IP flows
        """
        try:
            with open(absolute_data_path, "r", encoding="utf-8") as csv_file:
                ip_flows = [Flow.from_line(line) for line in csv.reader(csv_file)
                            if line]
        except IOError as e:
            logger.exception(f"Unable to open {absolute_data_path} file: {e}")
            return []

        logger.debug(f"Updated flows successfully: {ip_flows}")

        return ip_flows


    def sort_ips_from_data(self, ips_from_absolute_data, ip_flows_from_today) -> tuple:
        """
        Provides tuple with known|unknown IP flows and IPs

        :param ips_from_absolute_data: list of known IPs
        :param ip_flows_from_today: list of new IP flows

        :return: tuple(list, list, list, list) unknown|known IP flows and their IPs
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

        logger.debug(f"Sorted known|unknown IP flows and IPs successfully")

        return unknown_ip_flows, unknown_ips, known_ip_flows, known_ips


    def write_unkown_ips_to_data_file(self, unknown_ips, known_ips_filepath) -> None:
        """
        Updates record files for unknown IP

        :param unknown_ips: list of unknown IPs to be saved
        :param known_ips_filepath: filepath of known IPs
        """
        try:
            with open(known_ips_filepath, "a", encoding="utf-8") as data_file:
                for flow in unknown_ips:
                    data_file.write(flow + '\n')
        except IOError as e:
            logger.exception(f"Unable to append data to {known_ips_filepath} file: {e}")

        logger.debug("Updated record files for unknown IP successfully\n")


    def update_records_files(self,
                             absolute_data_path,
                             new_known_ip_flows,
                             unknown_ip_flows,
                             current_time) -> None:
        """
        Updates record files for IP flows and filter those which are safelisted

        :param absolute_data_path: filepath where all IPs flows are stored
        :param new_known_ip_flows: list of new known IP flows
        :param unknown_ip_flows: list of unknown IP flows
        :param current_time: datetime object
        """
        known_ip_flows, ips_in_abs_file = self.open_sort_abs_file(absolute_data_path)
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

        current_directory = os.getcwd()
        safelist = Safelist()
        asn_db_path = f"{current_directory}{DirPaths.ASN.value}{FilePaths.ASN_DB.value}"
        asn_info = safelist.get_asn_data(asn_db_path, new_absolute_flows)
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

        try:
            with open(self.fp_log_filepath, "a", encoding="utf-8") as FP_file:
                csv_writer = csv.writer(FP_file)
                csv_writer.writerows(list_of_FPs)
        except IOError as e:
            logger.exception(f"Unable to append data to {self.fp_log_filepath} file: {e}\n")
            raise e

        try:
            with open(absolute_data_path, "w", encoding="utf-8") as csv_file:
                    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                    for new_flow in new_absolute_flows:
                        csv_writer.writerow(new_flow)
        except IOError as e:
            logger.exception(f"Unable to save {absolute_data_path} file: {e}\n")
            raise e

        logger.debug("Updated record files for IP flows successfully\n")


    def sort_data_descending(self, raw_ratings):
        """
        Returns raw_ratings in descending order

        :param raw_ratings: list of RawRating objects

        :return: list of RawRating objects
        """
        return sorted(raw_ratings, key=lambda x: x.total_score, reverse=True)


    def create_final_blocklist(self, blocklist_config) -> None:
        """
        Creates final blocklist

        :param path_to_file: filepath to save the results blocklist
        :param data_from_absolute_file: filepath
        :param chosen_function: method from Methodology
        :param current_time: datetime object
        """
        chosen_functions = self.get_chosen_functions()

        blocklist_filepath = blocklist_config.get(BlocklistConfig.OUTPUT_FILEPATH.value)
        data_from_absolute_file = blocklist_config.get(BlocklistConfig.INPUT_FILEPATH.value)
        chosen_function = blocklist_config.get(BlocklistConfig.CHOSEN_FUNCTION.value)
        current_time = blocklist_config.get(BlocklistConfig.CURRENT_TIME.value)
        reference_date = blocklist_config.get(BlocklistConfig.REFERENCE_DATE.value)

        header_fieldnames = ['# Top IPs from data gathered in last 24 hours only', reference_date] 
        row_fieldnames = ('# Number', 'IP address', 'Rating')

        try:
            with open(blocklist_filepath, 'wt', newline ='') as blocklist_file:
                header_writer = csv.DictWriter(blocklist_file, fieldnames=header_fieldnames)
                header_writer.writeheader()
                csv_writer = csv.DictWriter(blocklist_file, fieldnames=row_fieldnames)
                csv_writer.writeheader()

                if chosen_function == getattr(Methodology, chosen_functions[0]):
                    logger.info("Using Prioritize Consistent IPs Function\n")
                    new_ratings = chosen_function(data_from_absolute_file,
                                                current_time,
                                                self.aging_modifier_pc_filepath)
                    for idx2, rating in enumerate(self.sort_data_descending(new_ratings)):
                        if rating.total_score >= 0.057: # What does this value mean???
                            new_entry = {'number': idx2,
                                        'ip_address': rating.src_address,
                                        'rating': rating.total_score}
                            csv_writer.writerows([new_entry])
                        else:
                            break
                elif chosen_function == getattr(Methodology, chosen_functions[1]):
                    logger.info("Using Prioritize New IPs Function\n")
                    new_ratings = chosen_function(data_from_absolute_file,
                                                current_time,
                                                self.aging_modifier_pn_filepath)
                    for idx2, rating in enumerate(self.sort_data_descending(new_ratings)):
                        if rating.total_score >= 0.002: # What does this value mean???
                            new_entry = {'number': idx2,
                                        'ip_address': rating.src_address,
                                        'rating': rating.total_score}
                            csv_writer.writerows([new_entry])
                        else:
                            break
                else:
                    logger.info("Using Prioritize Only Today IPs Function\n")
                    new_ratings = chosen_function(data_from_absolute_file,
                                                current_time,
                                                self.aging_modifier_pc_filepath)
                    for idx2, rating in enumerate(self.sort_data_descending(new_ratings)):
                        new_entry = {'number': idx2,
                                    'ip_address': rating.src_address,
                                    'rating': rating.total_score}
                        csv_writer.writerows([new_entry])
        except Exception as e:
            logger.exception(f"Unable to create blocklist {blocklist_filepath}: {e}\n")
            raise e

        logger.debug(f"Created blocklist {blocklist_filepath} successfully\n")


    def get_blocklists_filenames(self, reference_date) -> str:
        """
        Returns the blocklists filenames

        :param reference_date: datetime with reference date

        :return: dict with four (4) known blocklists filenames
        """
        today_dir = f"{self.historical_ratings_dirpath}{DirPaths.PRIORITIZE_TODAY_ONLY.value}"
        consistent_dir = f"{self.historical_ratings_dirpath}{DirPaths.PRIORITIZE_CONSISTENT.value}"
        new_dir = f"{self.historical_ratings_dirpath}{DirPaths.PRIORITIZE_NEW.value}"
        traditional_dir = f"{self.historical_ratings_dirpath}{DirPaths.TRADITIONAL.value}"

        # Filepath to save top IPs only from today
        top_ips_seen_today = f"{today_dir}{reference_date}{BlocklistTypes.NEW.value}"

        # Filepath to save top IPs for all time
        top_ips_for_all_time = f"{consistent_dir}{reference_date}{BlocklistTypes.PC.value}"

        # Filepath to save IPs that are newer
        top_ips_all_time_newer_prioritized = f"{new_dir}{reference_date}{BlocklistTypes.PN.value}"

        # Filepath to save the traditional blocklist
        traditional_blocklist = f"{traditional_dir}{reference_date}{BlocklistTypes.TRADITIONAL.value}"

        blocklists_filenames = {
            Blocklists.NEW_BLOCKLIST.value: top_ips_seen_today,
            Blocklists.PC_BLOCKLIST.value: top_ips_for_all_time,
            Blocklists.PN_BLOCKLIST.value: top_ips_all_time_newer_prioritized,
            Blocklists.TRADITIONAL_BLOCKLIST.value: traditional_blocklist
        }

        return blocklists_filenames


    def get_chosen_functions(self) -> list:
        """
        Gets chosen user's input functions

        :return: list of Methodology functions
        """
        chosen_functions = []
        try:
            with open(self.functions_filepath, 'r') as csv_file:
                for line in csv.reader(csv_file):
                    if line:
                        chosen_functions.extend(line)
        except IOError as e:
            logger.exception(f"Unable to open {self.functions_filepath} file\n")
            raise e

        logger.debug(f"User's chosen functions: {chosen_functions}\n")

        return chosen_functions


    def create_all_final_blocklists(self):
        """
        Creates all final blcklists with chosen user's input functions
        """
        new_data_files, reference_date = self.find_new_data_files(self.raw_data_dirpath,
                                                                  self.processed_files_filepath)

        current_reference_date = reference_date.strftime(Defaults.DATE_FORMAT.value)
        current_year = int(current_reference_date[0:4])
        current_month = int(current_reference_date[5:7])
        current_day = int(current_reference_date[8:10])
        current_time = datetime(current_year, current_month, current_day, 1).timestamp()

        chosen_functions = self.get_chosen_functions()

        known_data_flows, known_ips = self.open_sort_abs_file(self.absolute_data_filepath)
        new_ip_flows, new_ips = self.open_sort_new_file(self.raw_data_dirpath,
                                                        new_data_files)
        new_unknown_ip_flows, unknown_ips, known_ip_flows, new_known_ips = self.sort_ips_from_data(known_ips, 
                                                                                                   new_ip_flows)

        self.write_unkown_ips_to_data_file(unknown_ips, self.known_ips_filepath)
        self.update_records_files(self.absolute_data_filepath,
                                  known_ip_flows,
                                  new_unknown_ip_flows,
                                  current_time)

        try:
            with open(self.absolute_data_filepath, "r", encoding="utf-8") as abs_data:
                number_of_lines = len(abs_data.readlines())
            logger.debug(f"Number of lines in absolute data {number_of_lines}\n")
        except IOError as e:
            logger.exception(f"Unknown number of lines for {self.absolute_data_filepath}: {e}\n")
            raise e

        # Get blocklists methods
        PCF = getattr(Methodology, chosen_functions[0])
        PNF = getattr(Methodology, chosen_functions[1])
        OTF = getattr(Methodology, chosen_functions[2])

        # Get blocklists filenames
        blocklists_filenames = self.get_blocklists_filenames(reference_date)
        top_ips_seen_today = blocklists_filenames.get(Blocklists.NEW_BLOCKLIST.value)
        top_ips_for_all_time = blocklists_filenames.get(Blocklists.PC_BLOCKLIST.value)
        top_ips_all_time_newer_prioritized = blocklists_filenames.get(Blocklists.PN_BLOCKLIST.value)
        traditional_blocklist = blocklists_filenames.get(Blocklists.TRADITIONAL_BLOCKLIST.value)

        # Create final blocklist for each of the user's chosen functions
        consistent_blocklist_config = {
            BlocklistConfig.OUTPUT_FILEPATH.value: top_ips_for_all_time,
            BlocklistConfig.INPUT_FILEPATH.value: self.get_updated_flows(self.absolute_data_filepath),
            BlocklistConfig.CHOSEN_FUNCTION.value: PCF,
            BlocklistConfig.CURRENT_TIME.value: current_time,
            BlocklistConfig.REFERENCE_DATE.value: reference_date
        }
        self.create_final_blocklist(consistent_blocklist_config)

        new_blocklist_config = {
            BlocklistConfig.OUTPUT_FILEPATH.value: top_ips_all_time_newer_prioritized,
            BlocklistConfig.INPUT_FILEPATH.value: self.get_updated_flows(self.absolute_data_filepath),
            BlocklistConfig.CHOSEN_FUNCTION.value: PNF,
            BlocklistConfig.CURRENT_TIME.value: current_time,
            BlocklistConfig.REFERENCE_DATE.value: reference_date
        }
        self.create_final_blocklist(new_blocklist_config)

        today_blocklist_config = {
            BlocklistConfig.OUTPUT_FILEPATH.value: top_ips_seen_today,
            BlocklistConfig.INPUT_FILEPATH.value: new_unknown_ip_flows,
            BlocklistConfig.CHOSEN_FUNCTION.value: OTF,
            BlocklistConfig.CURRENT_TIME.value: current_time,
            BlocklistConfig.REFERENCE_DATE.value: reference_date
        }
        self.create_final_blocklist(today_blocklist_config)

        # Copy known IPs as the traditional blocklist
        shutil.copy2(self.known_ips_filepath, traditional_blocklist)

        try:
            with open(self.times_filepath, "a", encoding="utf-8") as csv_time_file:
                csv_writer = csv.writer(csv_time_file, quoting=csv.QUOTE_ALL)
                csv_writer.writerow([reference_date, Utils.now() - self.start_time])
        except IOError as e:
            logger.exception(f"Unable to append data to {self.times_filepath} file: {e}\n")
            raise e

        logger.debug(f"Created all blocklists successfully\n")


if __name__ == "__main__":
    """
    Generates IPv4 address blocklists
    """
    logger.info("---- Stratosphere IPS | Attacker IP Prioritizer (AIP) ----\n")
    start_time = Utils.now()
    logger.info(f"AIP start time {start_time}\n")
    aip = AIP(start_time)
    logger.info("-------------------- AIP STARTED ----------------\n")
    aip.create_all_final_blocklists()
    logger.info("-------------------- AIP FINISHED ----------------\n")
    finish_time = Utils.now()
    logger.info(f"AIP finish time {finish_time}\n")
    logger.info(f"Total runtime: {finish_time - start_time}\n")
