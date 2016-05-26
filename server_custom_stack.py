#!/usr/bin/env python

import argparse
from threading import Thread
from Queue import Queue
from scapy.all import *

parser = argparse.ArgumentParser(description='Create a TCP server that is capable of being attacked by our three attacks.')
parser.add_argument('--port', default=8000, type=int, help='The port to host the server on.')
args = parser.parse_args()

SYN = 0x02
ACK = 0x10
FIN = 0x01

STATE_LISTENING = 0

class DataSender (Thread):
    def __init__(self, socket, queue):
        Thread.__init__(self)
        self.socket = socket
        self.queue = queue
        self.running = True
        self.state =

        pass
    def run(self):
        # In an infinite loop, process incoming packets and send outgoing packets.
        while self.running:
            while not self.queue.empty():
                packet = self.queue.get()
                self.handle_packet(packet)
    def handle_packet(self, ip_packet):
        packet = ip_packet.payload
        if packet.dport != args.port: return
        if packet.flags & SYN:
            print "SYN recieved. Creating connection."
            print packet.seq
            synack = IP(dst=ip_packet.src) / TCP(sport=args.port, dport=packet.sport, flags='SA', ack=(packet.seq + 1))
            self.socket.send(Ether() / synack)

        if packet.flags & ACK:
            print "ACk recieved."
    def stop(self):
        print "Stopping sender."
        self.running = False


socket = conf.L2socket(iface='server-eth0')
queue = Queue()

def handle_packet(data):
    queue.put(data.payload)

sender = DataSender(socket, queue)
sender.start()

sniff(iface='server-eth0', filter='tcp and ip', prn=handle_packet)
sender.stop()
