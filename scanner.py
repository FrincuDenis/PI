#!/usr/bin/env python

import requests
import re
import urlparse
from BeautifulSoup import BeautifulSoup


class scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_link(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawler(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_link(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)
            if '#' in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print(link)
                self.crawler(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        parse_html = BeautifulSoup(response.content)
        return parse_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        method = form.get("method")
        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scan(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_vul_xss=self.xss_in_form(form,link)
                if is_vul_xss:
                    print("\n\n[****] XSS discovered in " + link + " in the following form")
                    print(form)
            if "=" in link:
                print("\n\n[+] Testing " + link)
                is_vul_xss= self.xss_in_link(link)
                if is_vul_xss:
                    print("[***]Discovered XSS in " + link)

    def xss_in_form(self, form, url):
        xss_script = "<sCript>alert('test')<scriPt>"
        response = self.submit_form(form, xss_script, url)
        return xss_script in response.content

    def xss_in_link(self, url):
        xss_script = "<sCript>alert('test')<scriPt>"
        url = url.replace("=", "=" + xss_script)
        response = self.session.get(url)
        return xss_script in response.content
