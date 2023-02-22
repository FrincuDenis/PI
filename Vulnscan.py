#!/usr/bin/env python

import scanner
import argparse
import optparse


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



#target="http://192.168.81.133/dvwa/"

links_to_ignore = ["http://192.168.81.133/dvwa/logout.php"]
data_dict = {"username": "admin", "password": "password", "Login": "submit"}
options = get_arguments()
target = options.target

vuln_scanner = scanner.scanner(target, links_to_ignore)
vuln_scanner.session.post("http://192.168.81.133/dvwa/login.php", data=data_dict)

vuln_scanner.crawler()
vuln_scanner.run_scan()
