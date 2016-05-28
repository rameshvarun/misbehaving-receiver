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
parser.add_argument('--client', type=str, choices=['kernel', 'opt-ack', 'ack-division', 'dup-ack'], help='The client type to use.', default='kernel')
parser.add_argument('--server', type=str, choices=['kernel', 'lwip', 'lwip-defended'], help='The server type to use.', default='kernel')
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

    server_node = net.get('server')
    client_node = net.get('client')
   
    client_node.cmd("iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP")
    
    # For the LWIP stack, we use a fixed port and ip address for the server.
    port = random.randint(49152, 65535) if args.server == 'kernel' else 7
    server_ip = server_node.IP() if args.server == 'kernel' else '10.11.0.1'

    if not args.cli:
        tcpdump = net.get('client').popen('tcpdump -w captures/%s-%s.pcap' % (args.client, args.server))

        if args.server == 'kernel':
            server = server_node.popen('python server.py --port %d' % port)
        elif args.server == 'lwip':
            server = server_node.popen('sh lwip-server.sh')
        elif args.server == 'lwip-defended':
            server = server_node.popen('sh lwip-server-defended.sh')
        else:
            raise "Unkown server type %s." % args.server

        time.sleep(1.0) # Give a second for the server to start up.

        if args.client == 'kernel':
            client = client_node.popen("telnet %s %d" % (server_ip, port))
        elif args.client == 'opt-ack':
            client = client_node.popen("python attackers/opt_ack_attacker.py --host %s --dport %d" % (server_ip, port))
        elif args.client == 'ack-division':
            client = client_node.popen("python attackers/ack_division_attacker.py --host %s --dport %d" % (server_ip, port))
        elif args.client == 'dup-ack':
            client = client_node.popen("python attackers/dup_ack_attacker.py --host %s --dport %d" % (server_ip, port))
        else:
            raise "Unkown client type %s." % args.client

        time.sleep(5.0)

        print "Stopping mininet network..."
        tcpdump.send_signal(signal.SIGINT)
        server.send_signal(signal.SIGINT)
        client.send_signal(signal.SIGINT)
    else:
        CLI(net)

    net.stop()
