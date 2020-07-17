from netaddr import IPAddress, IPNetwork
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def load_whitelist():
    path_to_nets = dir_path + '/whitelist-nets.txt'
    path_to_ips = dir_path + '/whitelist-ips.txt'
    with open(path_to_nets, 'r') as record:
        list_of_whitelisted_nets = record.read().split('\n')
    with open(path_to_ips, 'r') as record2:
        list_of_whitelisted_ips = record2.read().split('\n')
    return list_of_whitelisted_nets, list_of_whitelisted_ips

def check_if_ip_is_in_whitelisted_nets(ip, list_of_whitelist_nets):
    for entry in list_of_whitelist_nets:
        if IPAddress(ip) in IPNetwork(entry):
            print('Yay', entry, ip)
            return True
        else:
            continue
    return False

def check_if_ip_is_in_whitelisted_ips(ip, list_of_whitelist_ips):
    for entry in list_of_whitelist_ips:
        if ip == entry:
            print('Yay', entry, ip)
            return True
        else:
            continue
    return False

check_if_ip_is_in_whitelisted_ips('216.245.221.87', load_whitelist()[1])