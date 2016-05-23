#!/usr/bin/env python
"""
This file implements the Optimal Ack attacker.
"""

from scapy.all import *
from argparse import ArgumentParser

parser = ArgumentParser(
    description='Attack a TCP server with the optimistic ack attack.')
parser.add_argument('--dport', default=8000, type=int,
                    help='The port to attack.')
parser.add_argument('--sport', default=8080, type=int,
                    help='The port to send the TCP packats from.')
parser.add_argument('--host', default='127.0.0.1', type=str,
                    help='The ip address to attack.')
args = parser.parse_args()

packet = IP(dst=args.host) / TCP(sport=args.sport, dport=args.dport,
                                 flags='S', seq=12345)
send(packet)


# Get the receiver to ACK more stuff... and it's not gonna be some vanilla TCP receiver that's TelNET... how to do?
# no display name and no $DISPLAY environment variable error when runnnig the graph python module. 