"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

from enum import Enum


class Defaults(Enum):
    """
    Default values
    """
    MINUTES_AN_HOUR = (60**2)
    MINUTES_A_DAY = 24*MINUTES_AN_HOUR
    ZERO = 0.0
    UNSEEN_DAYS = 6
    POS_INFINITY = float("inf")
    NEG_INFINITY = - float("inf")
    DATE_FORMAT = '%Y-%m-%d'
    SPLUNK_DATE_FORMAT = '%Y/%m/%d %H:%M:%S.%f'

IP_SAFELIST = {
    '1.0.0.1',
    '1.1.1.1',
    '8.8.4.4',
    '8.8.8.8',
    '17.57.146.20',
    '18.221.56.27',
    '34.233.66.117',
    '35.186.224.25',
    '46.101.250.135',
    '46.137.190.132',
    '52.113.194.132',
    '52.60.129.180',
    '54.64.67.106',
    '54.67.10.127',
    '54.79.28.129',
    '54.94.142.218',
    '63.143.42.242',
    '63.143.42.243',
    '63.143.42.244',
    '63.143.42.245',
    '63.143.42.246',
    '63.143.42.247',
    '63.143.42.248',
    '63.143.42.249',
    '63.143.42.250',
    '63.143.42.251',
    '63.143.42.252',
    '63.143.42.253',
    '69.162.124.226',
    '69.162.124.227',
    '69.162.124.228',
    '69.162.124.229',
    '69.162.124.230',
    '69.162.124.231',
    '69.162.124.232',
    '69.162.124.233',
    '69.162.124.234',
    '69.162.124.235',
    '69.162.124.236',
    '69.162.124.237',
    '74.125.34.46',
    '89.221.214.130',
    '104.131.107.63',
    '122.248.234.23',
    '128.199.195.156',
    '138.197.150.151',
    '139.59.173.249',
    '142.250.102.188',
    '142.250.27.188',
    '146.185.143.14',
    '147.231.100.5',
    '159.203.30.41',
    '159.89.8.111',
    '165.227.83.148',
    '178.62.52.237',
    '188.226.183.141',
    '195.113.20.2',
    '198.49.23.145',
    '216.144.250.150',
    '216.245.221.82',
    '216.245.221.83',
    '216.245.221.84',
    '216.245.221.85',
    '216.245.221.86',
    '216.245.221.87',
    '216.245.221.88',
    '216.245.221.89',
    '216.245.221.90',
    '216.245.221.91',
    '216.245.221.92',
    '216.245.221.93',
    '2607:ff68:107::3',
    '2607:ff68:107::4',
    '2607:ff68:107::5',
    '2607:ff68:107::6',
    '2607:ff68:107::7',
    '2607:ff68:107::8',
    '2607:ff68:107::9',
    '2607:ff68:107::10',
    '2607:ff68:107::11',
    '2607:ff68:107::12',
    '2607:ff68:107::13',
    '2607:ff68:107::14',
    '2607:ff68:107::15',
    '2607:ff68:107::16',
    '2607:ff68:107::17',
    '2607:ff68:107::18',
    '2607:ff68:107::19',
    '2607:ff68:107::20',
    '2607:ff68:107::21',
    '2607:ff68:107::22',
    '2607:ff68:107::23',
    '2607:ff68:107::24',
    '2607:ff68:107::25',
    '2607:ff68:107::26',
    '2607:ff68:107::27',
    '2607:ff68:107::28',
    '2607:ff68:107::29',
    '2607:ff68:107::30',
    '2607:ff68:107::31',
    '2607:ff68:107::32',
    '2607:ff68:107::33',
    '2607:ff68:107::34',
    '2607:ff68:107::35',
    '2607:ff68:107::36',
    '2607:ff68:107::37',
    '2607:ff68:107::38'
}

CIDR_BLOCK_SAFELIST = {
    '35.190.247.0/24',
    '35.191.0.0/16',
    '64.18.0.0/16',
    '64.233.160.0/19',
    '66.102.0.0/20',
    '66.249.80.0/20',
    '72.14.192.0/18',
    '74.125.0.0/16',
    '108.177.8.0/21',
    '108.177.96.0/19',
    '130.211.0.0/22',
    '172.217.0.0/19',
    '172.217.128.0/19',
    '172.217.160.0/20',
    '172.217.192.0/19',
    '172.217.32.0/20',
    '172.253.112.0/20',
    '172.253.56.0/21',
    '173.194.0.0/16',
    '209.85.128.0/17',
    '216.239.32.0/19',
    '216.58.192.0/19'
}

ORG_SAFELIST = {
    'apple',
    'facebook',
    'google',
    'telegram',
    'microsoft',
    'spotify',
    'stratosphereips',
    'wikipedia'
}

class DefaultSafelists(Enum):
    """
    Default safelists
    """
    IP = IP_SAFELIST
    NET = CIDR_BLOCK_SAFELIST
    ORG = ORG_SAFELIST
