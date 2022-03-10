"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import os
import pytest
from datetime import datetime

from aip import AIP
from constants.defaults import Blocklists, Defaults, EnvVars, Functions


MOCK_DATA_DIR = "/tests/mock_data/"

os.environ[EnvVars.OUTPUT_FOLDER.value] = MOCK_DATA_DIR

MOCKED_START_TIME = "2022-01-31"
EXPECTED_NEW_BL_FILENAME = f"{MOCK_DATA_DIR}historical_ratings/prioritize_today_only/2022-01-31_new_blocklist.csv"
EXPECTED_PC_BL_FILENAME = f"{MOCK_DATA_DIR}historical_ratings/prioritize_consistent/2022-01-31_pc_blocklist.csv"
EXPECTED_PN_BL_FILENAME = f"{MOCK_DATA_DIR}historical_ratings/prioritize_new/2022-01-31_pn_blocklist.csv"
EXPECTED_TRAD_BL_FILENAME = f"{MOCK_DATA_DIR}historical_ratings/traditional/2022-01-31_trad_blocklist.csv"


def get_number_of_ips(filepath):
    number_of_lines = 0
    try:
        with open(filepath, "r", encoding="utf-8") as abs_data:
            number_of_lines = len(abs_data.readlines())
        print(f"Number of lines in absolute data {number_of_lines}\n")
    except IOError as e:
        print(f"Unknown number of lines for {filepath}: {e}\n")

    return number_of_lines


@pytest.fixture
def my_aip():
    """
    Fixture instance of AIP
    """
    mocked_start_time = datetime.strptime(MOCKED_START_TIME, Defaults.DATE_FORMAT.value)
    return AIP(mocked_start_time)


def test_aip_instantiation_success(my_aip):
    """
    Verifies that AIP instantiation succeeds with start_time
    """
    assert isinstance(my_aip, AIP)


def test_aip_instantiation_failure():
    """
    Verifies that AIP instantiation fails without a start_time
    """
    with pytest.raises(TypeError) as e:
        return AIP()


def test_aip_instantiation_paths_success(my_aip):
    """
    Verifies that AIP instantiation successfully generates the required paths
    """
    expected_start_time = datetime.strptime(MOCKED_START_TIME, Defaults.DATE_FORMAT.value)
    expected_aipp_dir = MOCK_DATA_DIR
    expected_historical_ratings_dirpath = f"{MOCK_DATA_DIR}historical_ratings/"
    expected_raw_data_dirpath = f"{MOCK_DATA_DIR}input_data/"
    expected_absolute_data_filepath = f"{MOCK_DATA_DIR}absolute_data.csv"
    expected_aging_modifier_pc_filepath = f"{MOCK_DATA_DIR}aging_modifiers_pc.csv"
    expected_aging_modifier_pn_filepath = f"{MOCK_DATA_DIR}aging_modifiers_pn.csv"
    expected_fp_log_filepath = f"{MOCK_DATA_DIR}fp_log_file.csv"
    expected_functions_filepath = f"{MOCK_DATA_DIR}selected_modules.csv"
    expected_known_ips_filepath = f"{MOCK_DATA_DIR}known_ips.txt"
    expected_processed_files_filepath = f"{MOCK_DATA_DIR}processed_splunk_files.txt"
    expected_times_filepath = f"{MOCK_DATA_DIR}times.csv"
    
    assert my_aip.start_time == expected_start_time
    assert my_aip.aipp_directory == expected_aipp_dir
    assert my_aip.historical_ratings_dirpath == expected_historical_ratings_dirpath
    assert my_aip.raw_data_dirpath == expected_raw_data_dirpath
    assert my_aip.absolute_data_filepath == expected_absolute_data_filepath
    assert my_aip.aging_modifier_pc_filepath == expected_aging_modifier_pc_filepath
    assert my_aip.aging_modifier_pn_filepath == expected_aging_modifier_pn_filepath
    assert my_aip.fp_log_filepath == expected_fp_log_filepath
    assert my_aip.functions_filepath == expected_functions_filepath
    assert my_aip.known_ips_filepath == expected_known_ips_filepath
    assert my_aip.processed_files_filepath == expected_processed_files_filepath
    assert my_aip.times_filepath == expected_times_filepath


def test_get_blocklists_filenames_success(my_aip):
    """
    Verifies that AIP successfully generates the correct filenames for each blocklist
    """
    reference_date = my_aip.start_time.strftime(Defaults.DATE_FORMAT.value)
    blockslists_filenames = my_aip.get_blocklists_filenames(reference_date)
    current_new_bl_filename = blockslists_filenames.get(Blocklists.NEW_BLOCKLIST.value)
    current_pc_bl_filename = blockslists_filenames.get(Blocklists.PC_BLOCKLIST.value)
    current_pn_bl_filename = blockslists_filenames.get(Blocklists.PN_BLOCKLIST.value)
    current_trad_bl_filename = blockslists_filenames.get(Blocklists.TRADITIONAL_BLOCKLIST.value)

    assert current_new_bl_filename == EXPECTED_NEW_BL_FILENAME
    assert current_pc_bl_filename == EXPECTED_PC_BL_FILENAME
    assert current_pn_bl_filename == EXPECTED_PN_BL_FILENAME
    assert current_trad_bl_filename == EXPECTED_TRAD_BL_FILENAME


def test_get_chosen_functions_success(my_aip):
    """
    Verifies that AIP successfully gets the user's chosen functions
    """
    current_directory = os.getcwd()
    current_functions_full_path = f"{current_directory}{my_aip.functions_filepath}"
    my_aip.functions_filepath = current_functions_full_path 
    chosen_functions = my_aip.get_chosen_functions()

    assert isinstance(chosen_functions, list)
    assert chosen_functions[0] == Functions.PCN.value
    assert chosen_functions[1] == Functions.PNO.value
    assert chosen_functions[2] == Functions.POTN.value


@pytest.mark.skip(reason="Currently unable to test this without mocked input files")
def test_create_all_final_blocklists_success(my_aip):
    """
    Verifies that AIP su
    """
    my_aip.create_all_final_blocklists()

    assert get_number_of_ips(EXPECTED_NEW_BL_FILENAME)
    assert get_number_of_ips(EXPECTED_PC_BL_FILENAME)
    assert get_number_of_ips(EXPECTED_PN_BL_FILENAME)
    assert get_number_of_ips(EXPECTED_TRAD_BL_FILENAME)
