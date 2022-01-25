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


class Safelist:
    """
    Class to handle all safelisting operations
    """

    def __init__(self):
        """
        Safelist default constructor
        """
        self.ips_safelist = DefaultSafelists.IP.value
        self.nets_safelist = DefaultSafelists.NET.value
        self.orgs_safelist = DefaultSafelists.ORG.value


    def load_safelists(self) -> tuple:
        """
        Loads into list our defaults safelists
        """
        safelisted_nets_list = list({*self.nets_safelist}) 
        safelisted_ips_list = list({*self.nets_safelist})
        safelisted_orgs_list = list({*self.orgs_safelist})

        return safelisted_nets_list, safelisted_ips_list, safelisted_orgs_list


    def check_if_ip_in_safelisted_nets(ip, list_of_safelisted_nets) -> bool:
        """
        Validates if ip belongs to the list_of_safelisted_nets

        :param ip: string with source address
        :param list_of_safelisted_nets: list with safelisted nets

        :return: bool. True for belonging. False, otherwise.
        """
        is_net_safelisted = any(entry for entry in list_of_safelisted_nets
                                if IPAddress(ip) in IPNetwork(entry))
        return is_net_safelisted


    def check_if_ip_in_safelisted_ips(ip, list_of_safelisted_ips) -> bool:
        """
        Validates if ip belongs to the list_of_safelisted_ips

        :param ip: string with source address
        :param list_of_safelisted_ips: list with safelisted nets

        :return: bool. True for belonging. False, otherwise.
        """
        is_ip_safelisted = any(entry for entry in list_of_safelisted_ips
                            if ip == entry)
        return is_ip_safelisted


    def get_ASN_data(asn_database, list_of_ips) -> dict:
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


    def check_organization_alignment(org, safelisted_organizations) -> tuple:
        """
        Validates if org belongs to the safelisted_organizations

        :param org: string with organization name
        :param safelisted_organizations: list of safelisted organizations

        :return: tuple(bool,str): belonging, safelisted_org_name
        """
        is_safelisted_organization = False
        filler = None
        for safelisted_org in safelisted_organizations:
            expression = re.compile(safelisted_org, re.IGNORECASE)
            if expression.search(org):
                is_safelisted_organization = True
                return is_safelisted_organization, safelisted_org

        return is_safelisted_organization, filler
