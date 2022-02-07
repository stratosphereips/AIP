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

from methodology import Methodology


FILE_FOR_FUNCTIONS = os.environ['output_folder'] + '/selected_modules.csv'

manual = 0
automatic = 1

NOT_AN_OPTION = 'Not an option, please select one from list: '
CHOOSE_A_FUNCTION = 'Which function to use: '


if manual == 1:

    # Models available to prioritize CONSISTENT IPs
    possible_options_A = Methodology.get_functions_for_method_A()
    option_A_choice = input(CHOOSE_A_FUNCTION)
    while int(option_A_choice) not in possible_options_A:
        option_A_choice = input(NOT_AN_OPTION)
    print('You chose ', option_A_choice)
    print('............................')

    # Models available to prioritize NEW IPs
    possible_options_B = Methodology.get_functions_for_method_B()
    option_B_choice = input(CHOOSE_A_FUNCTION)
    while int(option_B_choice) not in possible_options_B:
        option_B_choice = input(NOT_AN_OPTION)
    print('You chose ', option_B_choice)
    print('............................')

    # Models available to prioritize only TODAY IPs
    possible_options_C = Methodology.get_functions_for_method_C()
    option_C_choice = input(CHOOSE_A_FUNCTION)
    while int(option_C_choice) not in possible_options_C:
        option_C_choice = input(NOT_AN_OPTION)
    print('You choose ', option_C_choice)
    print('............................')

    list_of_functions_that_were_choosen = [
        possible_options_A.get(int(option_A_choice)),
        possible_options_B.get(int(option_B_choice)),
        possible_options_C.get(int(option_C_choice))
    ]

else:

    list_of_functions_that_were_choosen = [
        'prioritize_consistent_normalized_ips',
        'prioritize_new_normalized_ips',
        'prioritize_only_normalized_today_ips'
    ]

with open(FILE_FOR_FUNCTIONS, "w", encoding="utf-8") as file:
        csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for module in list_of_functions_that_were_choosen:
            csv_writer.writerow([module])
