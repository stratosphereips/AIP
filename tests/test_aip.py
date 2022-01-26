"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from aip import AIP


def test_aip_instantiation():
    """
    Verifies that AIP has correct values
    """
    current_aip = AIP()
    assert current_aip
