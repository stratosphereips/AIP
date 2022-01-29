"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from main.methodology import Methodology


def test_functions_for_method_A():
    """
    Verifies that Method A has the correct functions
    """
    method_a_functions = Methodology.get_functions_for_method_A()
    assert method_a_functions.get('1') == 'prioritize_consistent_normalized_ips'
    assert method_a_functions.get('2') == 'prioritize_consistent_original_ips'


def test_functions_for_method_B():
    """
    Verifies that Method B has the correct functions
    """
    method_b_functions = Methodology.get_functions_for_method_B()
    assert method_b_functions.get('1') == 'prioritize_new_normalized_ips'
    assert method_b_functions.get('2') == 'prioritize_new_original_ips'


def test_functions_for_method_C():
    """
    Verifies that Method C has the correct functions
    """
    method_c_functions = Methodology.get_functions_for_method_C()
    assert method_c_functions.get('1') == 'prioritize_only_normalized_today_ips'
    assert method_c_functions.get('2') == 'prioritize_only_today_ips'
