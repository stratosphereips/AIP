"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from main.safelist import Safelist
from slips_aip_constants.defaults import DefaultSafelists


CURRENT_IP_SAFELIST_SIZE = 107
CURRENT_NET_SAFELIST_SIZE = 22
CURRENT_ORG_SAFELIST_SIZE = 8


@pytest.fixture
def safelist():
    """
    Fixture instance of Safelist
    """
    return Safelist()


def test_default_ip_safelist_success():
    """
    Verifies that DefaultSafelists.IP has correct values
    """
    default_ip_safelist = DefaultSafelists.IP.value
    assert isinstance(default_ip_safelist, set)
    assert len(default_ip_safelist) == CURRENT_IP_SAFELIST_SIZE
    assert '8.8.8.8' in default_ip_safelist
    assert '69.162.124.233' in default_ip_safelist
    assert '139.59.173.249' in default_ip_safelist
    assert '216.245.221.84' in default_ip_safelist
    assert '2607:ff68:107::21' in default_ip_safelist


def test_default_net_safelist_success():
    """
    Verifies that DefaultSafelists.NET has correct values
    """
    default_net_safelist = DefaultSafelists.NET.value
    assert isinstance(default_net_safelist, set)
    assert len(default_net_safelist) == CURRENT_NET_SAFELIST_SIZE
    assert '35.191.0.0/16' in default_net_safelist
    assert '72.14.192.0/18' in default_net_safelist
    assert '172.217.160.0/20' in default_net_safelist
    assert '209.85.128.0/17' in default_net_safelist
    assert '216.58.192.0/19' in default_net_safelist


def test_default_org_safelist_success():
    """
    Verifies that DefaultSafelists.ORG has correct values
    """
    default_org_safelist = DefaultSafelists.ORG.value
    assert isinstance(default_org_safelist, set)
    assert len(default_org_safelist) == CURRENT_ORG_SAFELIST_SIZE
    assert 'stratosphereips' in default_org_safelist


def test_safelist_instantiation_success(safelist):
    safelisted_ips, safelisted_nets, safelisted_orgs = safelist.load_safelists()
    assert len(safelisted_ips) == len(DefaultSafelists.IP.value)
    assert len(safelisted_nets) == len(DefaultSafelists.NET.value)
    assert len(safelisted_orgs) == len(DefaultSafelists.ORG.value)


def test_org_in_safelisted_orgs_success(safelist):
    is_org_safelisted, org_name = safelist.check_if_org_in_safelisted_orgs("25.224.186.35.bc.googleusercontent.com")
    assert is_org_safelisted
    assert org_name == "google"


def test_org_in_safelisted_orgs_failure(safelist):
    is_org_safelisted, org_name = safelist.check_if_org_in_safelisted_orgs("45.155.205.27.cdn.metadata.twitter.com")
    assert not is_org_safelisted
    assert not org_name


def test_ip_in_safelisted_nets_success(safelist):
    assert safelist.check_if_ip_in_safelisted_nets("172.217.147.174")


def test_ip_in_safelisted_nets_failure(safelist):
    assert not safelist.check_if_ip_in_safelisted_nets("123.8.185.32")


def test_ip_in_safelisted_ips_success(safelist):
    assert safelist.check_if_ip_in_safelisted_ips("216.245.221.84")


def test_ip_in_safelisted_ips_failure(safelist):
    assert not safelist.check_if_ip_in_safelisted_ips("37.224.56.175")
