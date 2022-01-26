"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import pytest

from core.safelist import Safelist
from slips_aip_constants.defaults import DefaultSafelists

CURRENT_IP_SAFELIST_SIZE = 107
CURRENT_NET_SAFELIST_SIZE = 22
CURRENT_ORG_SAFELIST_SIZE = 8


def test_default_ip_safelist():
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


def test_default_net_safelist():
    """
    Verifies that DefaultSafelists.IP has correct values
    """
    default_net_safelist = DefaultSafelists.NET.value
    assert isinstance(default_net_safelist, set)
    assert len(default_net_safelist) == CURRENT_NET_SAFELIST_SIZE
    assert '35.191.0.0/16' in default_net_safelist
    assert '72.14.192.0/18' in default_net_safelist
    assert '172.217.160.0/20' in default_net_safelist
    assert '209.85.128.0/17' in default_net_safelist
    assert '216.58.192.0/19' in default_net_safelist


def test_default_org_safelist():
    """
    Verifies that DefaultSafelists.ORG has correct values
    """
    default_org_safelist = DefaultSafelists.ORG.value
    assert isinstance(default_org_safelist, set)
    assert len(default_org_safelist) == CURRENT_ORG_SAFELIST_SIZE
    assert 'stratosphereips' in default_org_safelist


def test_safelist_instantiation():
    safelist = Safelist()
    safelisted_ips, safelisted_nets, safelisted_orgs = safelist.load_safelists()
    assert len(safelisted_ips) == len(DefaultSafelists.IP.value)
    assert len(safelisted_nets) == len(DefaultSafelists.NET.value)
    assert len(safelisted_orgs) == len(DefaultSafelists.ORG.value)


#----------------Debugging--------------------

# print(os.getcwd())
# get_ASN_data('/home/parthurnax/Documents/Programming/Git-Repos/AIP-Blacklist-Algorithm/Main/ASN/GeoLite2-ASN.mmdb', ['8.8.8.8'])
#
# print(check_organization_strings('25.224.186.35.bc.googleusercontent.com', ['google', 'facebook', 'spotify']))

# def open_sort_abs_file(e):
#     IP_flows = []
#     IPs_in_absolute_file = []
#     with open(e, 'r') as csvfile:
#         for line in csv.reader(csvfile):
#             if not line:
#                 break
#             else:
#                 IP_flows.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]])
#                 IPs_in_absolute_file.append(line[0])
#     return IP_flows, IPs_in_absolute_file


# nets, ips = load_whitelist()
# sample = [['37.224.56.175', '2540', '113336.535485', '44.620683261811024', '2541520', '1000.5984251968504', '22465', '8.844488188976378', '1583329869.013408', '1583276400.000000', '2540'], ['216.245.221.83', '73661.0', '1901426.3529939998', '27.09860137111148', '51295053.0', '699.2566959798728', '713881.0', '9.722731569894593', '1583359165.069386', '1591308125.085197', '842.7511052482093']]
# print(load_whitelist())
#print(check_if_ip_is_in_safelisted_nets(sample[0][0], load_whitelist()[0]))

# for ip in open_sort_abs_file()[1]:
#     check_if_ip_is_in_safelisted_nets(ip, nets)
#     check_if_ip_is_in_safelisted_ips(ip, ips)
