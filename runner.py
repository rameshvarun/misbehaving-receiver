#!/usr/bin/python
"""
This script creates the mininet topology, runs a version of the server and
client, and logs the packets passing through the switch.
"""

import argparse
import random
import subprocess
import signal
import time
import sys
import os

from mininet.topo import Topo
from mininet.node import CPULimitedHost, UserSwitch
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.cli import CLI

# Check for root permissions.
if os.geteuid() != 0:
    sys.stderr.write('This script must be run with sudo.\n')
    sys.exit(1)

# Argument parsing.
parser = argparse.ArgumentParser(description="Create a network toplogy and test clients and servers.")
parser.add_argument('--delay', type=float, help="Link propagation delay (ms)", default=50)
parser.add_argument('--bandwith', type=float, help="Bandwidth of network links (Mb/s)", default=1000)
parser.add_argument('--queuesize', type=int, help="Max buffer size of network interface in packets", default=100)
parser.add_argument('--client', type=str, choices=['normal', 'modified'], help='The client type to use.', default='normal')
parser.add_argument('--server', type=str, choices=['normal', 'modified'], help='The server type to use.', default='normal')
parser.add_argument('--cli', help='Instead of running the server and client, open a Mininet CLI.', action='store_true')
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

    port = random.randint(49152, 65535) if args.server == 'normal' else 7
    server_ip = net.get('server').IP() if args.server == 'normal' else '10.11.0.1'

    if not args.cli:
        tcpdump = net.get('client').popen('tcpdump -w captures/%s-%s.pcap' % (args.client, args.server))

        if args.server == 'normal':
            server = net.get('server').popen('python server.py --port %d' % port)
        else: 
            server = net.get('server').popen('sh lwip-server.sh')

        time.sleep(1.0) # Give a second for the server to start up.

        if args.client == 'normal':
            client = net.get('client').popen("telnet %s %d" % (server_ip, port))
        elif args.client == 'modified':
            client = net.get('client').popen("python attackers/opt_ack_attacker.py --host %s --dport %d" % (server_ip, port))
        
        time.sleep(5.0)

        print "Stopping mininet network..."
        tcpdump.send_signal(signal.SIGINT)
        server.send_signal(signal.SIGINT)
        client.send_signal(signal.SIGINT)
    else:
        CLI(net)

    net.stop()
