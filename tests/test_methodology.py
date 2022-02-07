"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest
from inspect import isfunction

from main.methodology import Methodology
from slips_aip_constants.defaults import Functions


def test_get_functions_for_method_A():
    """
    Verifies that Method A has the correct functions
    """
    method_a_functions = Methodology.get_functions_for_method_A()
    assert method_a_functions[1] == Functions.PCN.value
    assert method_a_functions[2] == Functions.PCO.value


def test_get_functions_for_method_B():
    """
    Verifies that Method B has the correct functions
    """
    method_b_functions = Methodology.get_functions_for_method_B()
    assert method_b_functions[1] == Functions.PNN.value
    assert method_b_functions[2] == Functions.PNO.value


def test_get_functions_for_method_C():
    """
    Verifies that Method C has the correct functions
    """
    method_c_functions = Methodology.get_functions_for_method_C()
    assert method_c_functions[1] == Functions.POTN.value
    assert method_c_functions[2] == Functions.POT.value


def test_get_methodology_functions_by_name():
    """
    Verifies that when get Methodology functions by name they are callable
    """
    pcnf = getattr(Methodology, Functions.PCN.value)
    pcof = getattr(Methodology, Functions.PCO.value)
    pnnf = getattr(Methodology, Functions.PNN.value)
    pnof = getattr(Methodology, Functions.PNO.value)
    potnf = getattr(Methodology, Functions.POTN.value)
    potf = getattr(Methodology, Functions.POT.value)
    assert isfunction(pcnf)
    assert isfunction(pcof)
    assert isfunction(pnnf)
    assert isfunction(pnof)
    assert isfunction(potnf)
    assert isfunction(potf)
