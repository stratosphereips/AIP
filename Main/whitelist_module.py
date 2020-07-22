from netaddr import IPAddress, IPNetwork
import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))

def load_whitelist():
    path_to_nets = dir_path + '/net-whitelist.csv'
    path_to_ips = dir_path + '/ip-whitelist.csv'
    with open(path_to_nets, 'r') as record:
        list_of_whitelisted_nets = []
        for line in csv.reader(record):
            if not line:
                break
            else:
                list_of_whitelisted_nets.extend(line)
    with open(path_to_ips, 'r') as record2:
        list_of_whitelisted_ips = []
        for line in csv.reader(record2):
            if not line:
                break
            else:
                list_of_whitelisted_ips.extend(line)
    return list_of_whitelisted_nets, list_of_whitelisted_ips

def check_if_ip_is_in_whitelisted_nets(ip, list_of_whitelist_nets):
    for entry in list_of_whitelist_nets:
        if IPAddress(ip) in IPNetwork(entry):
            return True
        else:
            continue

def check_if_ip_is_in_whitelisted_ips(ip, list_of_whitelist_ips):
    for entry in list_of_whitelist_ips:
        if ip == entry:
            return True
        else:
            continue



#----------------Debugging--------------------


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
#print(check_if_ip_is_in_whitelisted_nets(sample[0][0], load_whitelist()[0]))

# for ip in open_sort_abs_file()[1]:
#     check_if_ip_is_in_whitelisted_nets(ip, nets)
#     check_if_ip_is_in_whitelisted_ips(ip, ips)
