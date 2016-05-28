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

# Bitmasks for checking the flags of a TCP packet.
SYN = 0x02
ACK = 0x10
FIN = 0x01

def load_pcap(filename):
    """Loads in a pcap file and returns a pair of lists - one of acks and one of data packets.
    Each of these lists contains pairs of the format (time, segment number). The lists are
    normalized to the smallest time and the initial sequence number."""
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

    # Remove retransmits for a cleaner graph.
    seen_seqnos, deduped_data = set(), []
    for (time, seqno) in data:
        if seqno in seen_seqnos: continue
        seen_seqnos.add(seqno)
        deduped_data.append((time, seqno))

    return acks, deduped_data

def create_graph(title, output, graphs):
    """Helper function for creating a graph."""
    colors = [('red', 'blue'), ('green', 'yellow')]

    plt.figure(figsize=(8, 8))
    plt.title(title)

    for i, (filename, ack_label, data_label) in enumerate(graphs):
        acks, data = load_pcap(filename)
        plt.scatter(map(itemgetter(0), acks), map(itemgetter(1), acks), c=colors[i][0], marker='x', label=ack_label)
        plt.scatter(map(itemgetter(0), data), map(itemgetter(1), data), c=colors[i][1], label=data_label)
    
    plt.xlabel("Time (sec)")
    plt.ylabel("Sequence Number (bytes)")
    plt.legend(loc='lower right', fontsize=10)
    
    plt.savefig(output)

if __name__ == "__main__":
    os.system("mkdir -p graphs")

    # Test the Kernel TCP stack against a normal client, as well as the attackers.
    create_graph("Kernel TCP Stack - A Normal TCP Connection", "graphs/kernel-kernel.png",
        [("captures/kernel-kernel.pcap", 'ACKs', 'Data Segments')])

    create_graph("Kernel TCP Stack vs. Optimistic ACK Attacker", "graphs/opt-attack-kernel.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/opt-ack-kernel.pcap", 'ACKs (Optimistic Ack)', 'Data Segments (Optimistic Ack)')
        ])

    create_graph("Kernel TCP Stack vs. ACK Division Attacker", "graphs/ack-division-kernel.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/ack-division-kernel.pcap", 'ACKs (Ack Division)', 'Data Segments (Ack Division)')
        ])

    create_graph("Kernel TCP Stack vs. Duplicate ACK Attacker", "graphs/dup-ack-kernel.png", [
        ("captures/kernel-kernel.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/dup-ack-kernel.pcap", 'ACKs (Duplicate ACK)', 'Data Segments (Duplicate ACK)')
        ])
    
    # Test the LWIP stack against a normal client, as well as attackers.

    create_graph("LWIP with Normal TCP Client", "graphs/kernel-lwip.png",
        [("captures/kernel-lwip.pcap", 'ACKs', 'Data Segments')])

    create_graph("LWIP Stack vs. ACK Division Attacker", "graphs/ack-division-lwip.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/ack-division-lwip.pcap", 'ACKs (Ack Division)', 'Data Segments (Ack Division)')
        ])

    create_graph("LWIP Stack vs. Opt Ack Attacker", "graphs/opt-ack-lwip.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/opt-ack-lwip.pcap", 'ACKs (Optimistic Ack)', 'Data Segments (Optimistic Ack)')
        ])
    
    create_graph("LWIP Stack vs. Dup Ack Attacker", "graphs/dup-ack-lwip.png", [
        ("captures/kernel-lwip.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/dup-ack-lwip.pcap", 'ACKs (Duplicate Ack)', 'Data Segments (Duplicate Ack)')
        ])
    
    # Test our defended LWIP stack against various clients.

    create_graph("Defended LWIP Stack with Normal (Kernel) TCP Client", "graphs/kernel-lwip-defended.png",
        [("captures/kernel-lwip-defended.pcap", 'ACKs', 'Data Segments')])

    create_graph("Defended LWIP Stack vs. ACK Division Attacker", "graphs/ack-division-lwip-defended.png", [
        ("captures/kernel-lwip-defended.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/ack-division-lwip-defended.pcap", 'ACKs (Ack Division)', 'Data Segments (Ack Division)')
        ])

    create_graph("Defended LWIP Stack vs. Opt Ack Attacker", "graphs/opt-ack-lwip-defended.png", [
        ("captures/kernel-lwip-defended.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/opt-ack-lwip-defended.pcap", 'ACKs (Optimistic Ack)', 'Data Segments (Optimistic Ack)')
        ])

    create_graph("Defended LWIP Stack vs. Duplicate ACK Attacker", "graphs/dup-ack-lwip-defended.png", [
        ("captures/kernel-lwip-defended.pcap", 'ACKs (Normal)', 'Data Segments (Normal)'),
        ("captures/dup-ack-lwip-defended.pcap", 'ACKs (Duplicate ACK)', 'Data Segments (Duplicate ACK)')
        ])
