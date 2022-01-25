"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from slips_aip_constants.defaults import DefaultSafelists


def test_default_ip_safelist():
    """
    Verifies that DefaultSafelists.IP has correct values
    """
    default_ip_safelist = DefaultSafelists.IP.value
    assert isinstance(default_ip_safelist, set)
    assert len(default_ip_safelist) == 107
    assert '8.8.8.8' in default_ip_safelist
    assert '69.162.124.233' in default_ip_safelist
    assert '139.59.173.249' in default_ip_safelist
    assert '216.245.221.84' in default_ip_safelist
    assert '2607:ff68:107::21' in default_ip_safelist

def test_default_net_safelist():
    """
    Verifies that DefaultSafelists.IP has correct values
    """
    default_net_safelist = DefaultSafelists.NET.value
    assert isinstance(default_net_safelist, set)
    assert len(default_net_safelist) == 22
    assert '35.191.0.0/16' in default_net_safelist
    assert '72.14.192.0/18' in default_net_safelist
    assert '172.217.160.0/20' in default_net_safelist
    assert '209.85.128.0/17' in default_net_safelist
    assert '216.58.192.0/19' in default_net_safelist
