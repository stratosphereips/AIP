from inspect import getmembers, isfunction
from datetime import datetime
import main_modulev3
from get_functions import list_method_A_functions, list_method_B_functions, list_method_C_functions
import os
import csv

startTime = datetime.now()
manual = 0
automatic = 1

file_for_functions = os.environ['output_folder'] + '/Selected_modules.csv'

if manual == 1:
    # Put the options for modules in a dictionary, so user can pick which one they want
    functions_list = [o for o in getmembers(main_modulev3) if isfunction(o[1])]
    # print(functions_list)

    dictionary_of_functions = {}
    for function in functions_list:
        dictionary_of_functions[function[0]] = function[1]

    # Call the methods listing functions to list the possible choices for each function.
    # Models available for prioritize CONSISTENT function.
    possible_options_A = list_method_A_functions()
    option_A_choice = input('Which function to use: ')
    while int(option_A_choice) not in possible_options_A:
        option_A_choice = input('Not an option, please select one from list: ')
    print('You choose ', option_A_choice)
    print('............................')

    # Models available for prioritize NEW function.
    possible_options_B = list_method_B_functions()
    option_B_choice = input('Which function to use: ')
    while int(option_B_choice) not in possible_options_B:
        option_B_choice = input('Not an option, please select one from list: ')
    print('You choose ', option_B_choice)
    print('............................')

    # Models available for only today function.
    possible_options_C = list_method_C_functions()
    option_C_choice = input('Which function to use: ')
    while int(option_C_choice) not in possible_options_C:
        option_C_choice = input('Not an option, please select one from list: ')
    print('You choose ', option_C_choice)
    print('............................')

    list_of_functions_that_were_choosen = []
    for function in functions_list:
        if function[0] == possible_options_A[int(option_A_choice)]:
            list_of_functions_that_were_choosen.append(function[0])
        elif function[0] == possible_options_B[int(option_B_choice)]:
            list_of_functions_that_were_choosen.append(function[0])
        elif function[0] == possible_options_C[int(option_C_choice)]:
            list_of_functions_that_were_choosen.append(function[0])

    with open(file_for_functions, 'w') as file:
        write2 = csv.writer(file, quoting=csv.QUOTE_ALL)
        for module in list_of_functions_that_were_choosen:
            new_list2 = []
            new_list2.append(module)
            write2.writerow(new_list2)

elif automatic == 1:
    list_of_functions_that_were_choosen = ['prioritize_consistent_normalized', 'prioritize_new_normalized', 'todays_ips_only_normalized']
    with open(file_for_functions, 'w') as file:
        write2 = csv.writer(file, quoting=csv.QUOTE_ALL)
        for module in list_of_functions_that_were_choosen:
            new_list2 = []
            new_list2.append(module)
            write2.writerow(new_list2)