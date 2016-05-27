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

    # Test the Kernel TCP stack against a normal client, as well as the attackers.

    create_graph("Kernel TCP Stack - A Normal TCP Connection", "graphs/kernel-kernel.png", [("captures/kernel-kernel.pcap", 'ACKs', 'Data Segments')])

    create_graph("Kernel TCP Stack vs. Optimistic ACK Attacker", "graphs/kernel-opt-attack.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/opt-ack-kernel.pcap", 'ACKs (Optimistic Ack)', 'Data Segments (Optimistic Ack)')
        ])

    create_graph("Kernel TCP Stack vs. ACK Division Attacker", "graphs/kernel-ack-division.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/ack-division-kernel.pcap", 'ACKs (Ack Division)', 'Data Segments (Ack Division)')
        ])

    create_graph("Kernel TCP Stack vs. Duplicate ACK Attacker", "graphs/kernel-dup-ack.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/dup-ack-kernel.pcap", 'ACKs (Duplicate ACK)', 'Data Segments (Duplicate ACK)')
        ])
    
    # Test the LWIP stack against a normal client, as well as attackers.
    
    create_graph("LWIP with Normal TCP Client", "graphs/kernel-lwip.png", [("captures/kernel-lwip.pcap", 'ACKs', 'Data Segments')])

    create_graph("LWIP Stack vs. ACK Division Attacker", "graphs/lwip-ack-div.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/ack-division-lwip.pcap", 'ACKs (Ack Division)', 'Data Segments (Ack Division)')
        ])

    create_graph("LWIP Stack vs. Opt Ack Attacker", "graphs/lwip-opt-ack.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/opt-ack-lwip.pcap", 'ACKs (Optimistic Ack)', 'Data Segments (Optimistic Ack)')
        ])
    
    create_graph("LWIP Stack vs. Dup Ack Attacker", "graphs/lwip-dup-ack.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/dup-ack-lwip.pcap", 'ACKs (Duplicate Ack)', 'Data Segments (Duplicate Ack)')
        ])
    
