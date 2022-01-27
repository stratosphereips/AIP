"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import logging
import re

from netaddr import IPAddress, IPNetwork
import maxminddb

from slips_aip_constants.defaults import DefaultSafelists

logger = logging.getLogger(__name__)


class Safelist:
    """
    Class to handle all safelisting operations
    """

    __slots__ = ['ips_safelist', 'nets_safelist', 'orgs_safelist']

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
        safelisted_ips_list = list({*self.ips_safelist})
        safelisted_nets_list = list({*self.nets_safelist})
        safelisted_orgs_list = list({*self.orgs_safelist})

        return safelisted_ips_list, safelisted_nets_list, safelisted_orgs_list


    def check_if_ip_in_safelisted_nets(self, ip) -> bool:
        """
        Validates if ip belongs to the list_of_safelisted_nets

        :param ip: string with source address
        :param list_of_safelisted_nets: list with safelisted nets

        :return: bool. True for belonging. False, otherwise.
        """
        safelisted_nets_list = list({*self.nets_safelist})
        is_net_safelisted = any(safelisted_net for safelisted_net in safelisted_nets_list
                                if IPAddress(ip) in IPNetwork(safelisted_net))
        return is_net_safelisted


    def check_if_ip_in_safelisted_ips(self, ip) -> bool:
        """
        Validates if ip belongs to the list_of_safelisted_ips

        :param ip: string with source address
        :param list_of_safelisted_ips: list with safelisted nets

        :return: bool. True for belonging. False, otherwise.
        """
        safelisted_ips_list = list({*self.ips_safelist})
        is_ip_safelisted = any(safelisted_ip for safelisted_ip in safelisted_ips_list
                               if ip == safelisted_ip)
        return is_ip_safelisted


    def check_if_org_in_safelisted_orgs(self, org) -> tuple:
        """
        Validates if org belongs to the safelisted_organizations

        :param org: string with organization name
        :param safelisted_organizations: list of safelisted organizations

        :return: tuple(bool,str): belonging, safelisted_org
        """
        safelisted_orgs_list = list({*self.orgs_safelist})
        is_safelisted_organization = False
        filler = None

        for safelisted_org in safelisted_orgs_list:
            expression = re.compile(safelisted_org, re.IGNORECASE)
            if expression.search(org):
                is_safelisted_organization = True
                return is_safelisted_organization, safelisted_org

        return is_safelisted_organization, filler


    def get_asn_data(self, asn_database, list_of_ips) -> dict:
        """
        Validates if ip belongs to the list_of_safelisted_ips

        :param ip: string with source address
        :param list_of_safelisted_ips: list with safelisted nets

        :return: dict. True for belonging. False, otherwise.
        """
        reader = maxminddb.open_database(asn_database)
        dictionary = {}
        for ip in list_of_ips:
            data = reader.get(ip.src_address)
            if data:
                org_key = 'autonomous_system_organization'
                try:
                    organization = data.get(org_key)
                except KeyError as e:
                    logger.exception(f"{org_key} key not found in data")
                    organization = ' '
            else:
                organization = ' '
            dictionary[ip.src_address] = organization
        return dictionary
