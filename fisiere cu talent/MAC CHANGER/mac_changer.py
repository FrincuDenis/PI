#!/usr/bin/env python
import re
import subprocess
import os
import random
import argparse

def get_arguments():
    # This will give user a neat CLI
    parser = argparse.ArgumentParser()
    # We need the interface name
    parser.add_argument("-i", "--interface",
                dest="interface",
                help="Name of the interface. "
                "Type ifconfig for more details.")
    options = parser.parse_args()
    # Check if interface was given
    if options.interface:
        return options.interface
    else:
        parser.error("[!] Invalid Syntax. "
                     "Use --help for more details.")

def get_random_mac_address():
    characters = "0123456789abcdef"
    random_mac_address = "00"
    for i in range(5):
        random_mac_address += ":" + \
                              random.choice(characters) \
                              + random.choice(characters)
    return random_mac_address

def get_current_mac(stat):
    print("Current MAC=" + get_mac())
    if not stat:
        f = open("or.txt", "w")
        f.write(get_mac())
        f.close()
def file_exist():
    path = 'or.txt'
    stat = os.path.exists(path)
    return stat
def meniu(stat):
    if not stat:
        print("1.Change MAC")
        print("3.Exit")
    else:
        print("1.Change MAC")
        print("2.Original Mac")
        print("3.Exit")
def get_original_mac():
	f=open("or.txt","r")
	macc=f.read()
	f.close()
	return macc
def get_mac ():
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_disp = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    return mac_disp.group(0)

def change_mac(interface,new_mac):
    print("[+] Changing MAC address for "+interface+" to " + new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def inputuser(user):
	match user:
    		case '1':
        		mac_disp = get_mac()
        		if (mac_disp):
            			get_current_mac(file_exist())
            			change_mac(interface,get_random_mac_address())
            			print("[+]MAC Address changed succesfully")

        		else:
            			print("[-] Could not read MAC address")
    		case '2':
        		change_mac(interface, get_original_mac())
        		print("[+]MAC Address changed succesfully")
interface =get_arguments()
#get_arguments()
meniu(file_exist())
user=input()
inputuser(user)
