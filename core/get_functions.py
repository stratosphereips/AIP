"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from inspect import getmembers, isfunction
import main_modulev3

def list_method_A_functions():
    functions_list = [o[0] for o in getmembers(main_modulev3) if isfunction(o[1])]
    dictionary_of_options = {}
    running_total = 1
    for function in functions_list:
        if function[:21] == 'prioritize_consistent':
            print(running_total, ':', function)
            dictionary_of_options[running_total] = function
            running_total += 1
    return dictionary_of_options

def list_method_B_functions():
    functions_list = [o[0] for o in getmembers(main_modulev3) if isfunction(o[1])]
    running_total = 1
    dictionary_of_options = {}
    for function in functions_list:
        if function[:14] == 'prioritize_new':
            print(running_total, ':', function)
            dictionary_of_options[running_total] = function
            running_total += 1
    return dictionary_of_options

def list_method_C_functions():
    functions_list = [o[0] for o in getmembers(main_modulev3) if isfunction(o[1])]
    running_total = 1
    dictionary_of_options = {}
    for function in functions_list:
        if function[:15] == 'todays_ips_only':
            print(running_total, ':', function)
            dictionary_of_options[running_total] = function
            running_total += 1
    return dictionary_of_options
