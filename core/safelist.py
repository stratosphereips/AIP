"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import logging
import os
import re

from netaddr import IPAddress, IPNetwork
import maxminddb

from slips_aip_constants.defaults import DefaultSafelists

logger = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))


def load_safelist():
    """
    Loads into list our defaults safelists
    """
    list_of_safelisted_nets = list({*DefaultSafelists.NET.value}) 
    list_of_safelisted_ips = list({*DefaultSafelists.IP.value})

    return list_of_safelisted_nets, list_of_safelisted_ips

def check_if_ip_is_in_safelisted_nets(ip, list_of_safelisted_nets):
    """
    Validates if ip belongs to the list_of_safelisted_nets

    :param ip: string with source address
    :param list_of_safelisted_nets: list with safelisted nets

    :return: bool. True for belonging. False, otherwise.
    """
    is_net_safelisted = any(entry for entry in list_of_safelisted_nets
                            if IPAddress(ip) in IPNetwork(entry))
    return is_net_safelisted

def check_if_ip_is_in_safelisted_ips(ip, list_of_safelisted_ips):
    """
    Validates if ip belongs to the list_of_safelisted_ips

    :param ip: string with source address
    :param list_of_safelisted_ips: list with safelisted nets

    :return: bool. True for belonging. False, otherwise.
    """
    is_ip_safelisted = any(entry for entry in list_of_safelisted_ips
                           if ip == entry)
    return is_ip_safelisted


def get_ASN_data(asn_database, list_of_ips):
    """
    Validates if ip belongs to the list_of_safelisted_ips

    :param ip: string with source address
    :param list_of_safelisted_ips: list with safelisted nets

    :return: bool. True for belonging. False, otherwise.
    """
    reader = maxminddb.open_database(asn_database)
    dictionary = {}
    for ip in list_of_ips:
        data = reader.get(ip[0])
        if data:
            try:
                organization = data['autonomous_system_organization']
            except KeyError as e:
                logger.exception(f"'autonomous_system_organization' key not found in data")
                organization = ' '
        else:
            organization = ' '
        dictionary[ip[0]] = organization
    return dictionary


def check_organization_strings(org, list_of_good_organizations):
    """
    Validates if org belongs to the list_of_good_organizations

    :param org: string with organization name
    :param list_of_good_organizations: list of good organizations

    :return: bool. True for belonging. False, otherwise.
    """
    is_a_good_organization = False
    filler = None
    for ENTRY in list_of_good_organizations:
        expression = re.compile(ENTRY[0], re.IGNORECASE)
        if expression.search(org):
            is_a_good_organization = True
            return is_a_good_organization, ENTRY[0]
        else:
            continue
    return is_a_good_organization, filler

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
