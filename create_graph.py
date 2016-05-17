#!/usr/bin/python

"""
This script is used to create the graphs of data packets and their corresponding ACKs. 
"""

import os
from operator import itemgetter
from scapy.all import * # Scapy is used for reading packets.
import matplotlib.pyplot as plt # Matplotlib is used for graphing.

SYN = 0x02
ACK = 0x10
FIN = 0x01

cap = rdpcap("captures/normal.pcap")
os.system("mkdir -p graphs")

# This is the data that we need to extract from our packets
acks, data, inital_seqno = [], [], None

for packet in cap:
    if not isinstance(packet, Ether): continue
    if not isinstance(packet.payload, IP): continue
    if not isinstance(packet.payload.payload, TCP): continue
    tcp = packet.payload.payload

    if tcp.flags & SYN and tcp.flags & ACK: inital_seqno = tcp.seq
    if not tcp.payload and tcp.flags & ACK and not tcp.flags & SYN and not tcp.flags & FIN:
        acks.append((packet.time, tcp.ack))
    if tcp.payload:
        data.append((packet.time, tcp.seq + len(tcp.payload)))

min_time = min(min(ack[0] for ack in acks), min(d[0] for d in data))
acks = [(time - min_time, num - inital_seqno - 1) for (time, num) in acks]
data = [(time - min_time, num - inital_seqno - 1) for (time, num) in data]

plt.figure()
plt.title("A Normal TCP Connection")
plt.scatter(map(itemgetter(0), acks), map(itemgetter(1), acks), c='red', marker='x', label="ACKs")
plt.scatter(map(itemgetter(0), data), map(itemgetter(1), data), c='blue', label="Data Segments")

plt.xlabel("Time (sec)")
plt.ylabel("Sequence Number (bytes)")
plt.legend(loc='lower right')

plt.savefig("graphs/normal.png")
