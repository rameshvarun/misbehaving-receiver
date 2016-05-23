#!/usr/bin/python
"""
This script creates the mininet topology, runs a version of the server and
client, and logs the packets passing through the switch.
"""

import argparse
import subprocess
import signal
import time
import os

from mininet.topo import Topo
from mininet.node import CPULimitedHost, UserSwitch
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.cli import CLI

parser = argparse.ArgumentParser(description="Create a network toplogy and test clients and servers.")
parser.add_argument('--delay', type=float, help="Link propagation delay (ms)", default=5)
parser.add_argument('--bandwith', type=float, help="Bandwidth of network links (Mb/s)", default=1000)
parser.add_argument('--queuesize', type=int, help="Max buffer size of network interface in packets", default=100)
args = parser.parse_args()

class ClientServerTopo(Topo):
    """A simple network topology that has one switch connection a client and
    a server"""
    def build(self, n=2):
        client, server = self.addHost('client'), self.addHost('server')
        switch = self.addSwitch('s0')

        self.addLink(client, switch, bw=args.bandwith, delay=(str(args.delay) + 'ms'), max_queue_size=args.queuesize)
        self.addLink(server, switch, bw=args.bandwith, delay=(str(args.delay) + 'ms'), max_queue_size=args.queuesize)

if __name__ == "__main__":
    os.system('mkdir -p captures')
    net = Mininet(topo=ClientServerTopo(), host=CPULimitedHost, link=TCLink)
    print "Starting mininet network..."
    net.start()
    net.pingAll()

    port = 8000
    tcpdump = net.get('client').popen('tcpdump -w captures/normal.pcap')
    server = net.get('server').popen('python server.py --port %d' % port)
    time.sleep(1.0) # Give a second for the server to start up.

    client = net.get('client').popen("telnet %s %d" % (net.get('server').IP(), port)) #client opens 
    
    time.sleep(5.0)

    print "Stopping mininet network..."
    tcpdump.send_signal(signal.SIGINT)
    server.send_signal(signal.SIGINT)
    client.send_signal(signal.SIGINT)

    net.stop()
