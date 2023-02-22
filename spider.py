#!/usr/bin/env python

import requests
import re
import urlparse
target_url="http://192.168.101.137/mutillidae/"
target_links=[]
def extract_link(url):
    response=requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawler(url):
    href_links=extract_link(url)
    for link in href_links:
        link = urlparse.urljoin(url,link)
        if '#' in link:
            link=link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawler(link)

crawler(target_url)

crawler(target_url)