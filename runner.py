#!/usr/bin/python
"""
This script creates the mininet topology, runs a version of the server and
client, and logs the packets passing through the switch.
"""

import argparse
from mininet.topo import Topo

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
        switch = self.addSwitch('switch')

        self.addLink(client, switch, bw=args.bandwith, delay=(str(args.delay) + 'ms'), max_queue_size=args.queuesize)
        self.addLink(server, switch, bw=args.bandwith, delay=(str(args.delay) + 'ms'), max_queue_size=args.queuesize)

if __name__ == "__main__":
    pass
