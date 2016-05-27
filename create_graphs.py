#!/usr/bin/python

"""
This script is used to create the graphs of data packets and their corresponding ACKs. 
"""

import os
import argparse

from operator import itemgetter
from scapy.all import * # Scapy is used for reading packets.

import matplotlib; matplotlib.use('Agg') # Use a backend that doesn't require a display.
import matplotlib.pyplot as plt # Use the pyplot interface of matplotlib.

SYN = 0x02
ACK = 0x10
FIN = 0x01

def load_pcap(filename):
    cap = rdpcap(filename)

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

    return acks, data

def create_graph(title, output, graphs):
    colors = [('red', 'blue'), ('green', 'yellow')]

    plt.figure()
    plt.title(title)

    for i, (filename, ack_label, data_label) in enumerate(graphs):
        acks, data = load_pcap(filename)
        plt.scatter(map(itemgetter(0), acks), map(itemgetter(1), acks), c=colors[i][0], marker='x', label="ACKs")
        plt.scatter(map(itemgetter(0), data), map(itemgetter(1), data), c=colors[i][1], label="Data Segments")
    
    plt.xlabel("Time (sec)")
    plt.ylabel("Sequence Number (bytes)")
    plt.legend(loc='lower right')
    
    plt.savefig(output)

if __name__ == "__main__":
    os.system("mkdir -p graphs")

    create_graph("Kernel TCP Stack - A Normal TCP Connection", "graphs/normal-kernel.png", [("captures/normal-normal.pcap", 'ACKs', 'Data Segments')])


    '''attack_acks, attack_data = load_pcap("captures/modified-normal.pcap")

    plt.figure()
    plt.title("Kernel TCP Stack vs. Optimistic ACK Attacker")
    plt.scatter(map(itemgetter(0), normal_acks), map(itemgetter(1), normal_acks), c='red', marker='x', label="ACKs (Normal)")
    plt.scatter(map(itemgetter(0), normal_data), map(itemgetter(1), normal_data), c='blue', label="Data Segments (Normal)")


    plt.scatter(map(itemgetter(0), attack_acks), map(itemgetter(1), attack_acks), c='green', marker='x', label="ACKs (Attack)")
    plt.scatter(map(itemgetter(0), attack_data), map(itemgetter(1), attack_data), c='yellow', label="Data Segments (Attack)")
    
    plt.xlabel("Time (sec)")
    plt.ylabel("Sequence Number (bytes)")
    plt.legend(loc='upper left')

    plt.savefig("graphs/kernel-opt-attack.png")'''

    create_graph("LWIP with Normal TCP Client", "graphs/normal-lwip-unmodified.png", [("captures/normal-modified.pcap", 'ACKs', 'Data Segments')])
