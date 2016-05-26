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

    # OLD SERVER CODE...
    # port = 8000
    # tcpdump = net.get('client').popen('tcpdump -w captures/normal.pcap')
    # server = net.get('server').popen('python server.py --port %d' % port)

    # http://stackoverflow.com/questions/13045593/using-sudo-with-python-script

    # run_lwip_command = "/home/cs244/cs244assign/misbehaving-receiver/lwip-tap && ./lwip-tap  addr=172.16.0.2,netmask=255.255.255.0,gw=172.16.0.1"
    # #server = net.get('server').popen("sudo -S %s"%(run_lwip_command), 'w').write('cs244')
    # server = net.get('server').popen(run_lwip_command)

    time.sleep(1.0) # Give a second for the server to start up.

    # OLD CLIENT CODE
    # client = net.get('client').popen("telnet %s %d" % (net.get('server').IP(), port)) #client starts to ping. 

    #os.system("/home/cs244/cs244assn/misbehaving-receiver/lwip-tap/lwip-tap -i addr=172.16.0.2,netmask=255.255.255.0,gw=172.16.0.1")
    #client = net.get('client').popen("ping 172.16.0.2 > lwip-results/lwip_pingtest.txt") #client starts to ping. 

    os.system('mkdir -p lwip-results')
    command = "./lwip-tap"
    arg1 = "-i"
    arg2 = "addr=172.16.0.2,netmask=255.255.255.0,gw=172.16.0.1"
    server = net.get('server').popen([command, arg1,arg2], cwd="/home/cs244/cs244assign/misbehaving-receiver/lwip-tap/")
    client = net.get('client').popen("ping 172.16.0.2 > lwip-results/lwip_pingtest.txt")

    time.sleep(3)
 
    print "Stopping mininet network..."
    #tcpdump.send_signal(signal.SIGINT)
    server.send_signal(signal.SIGINT)
    client.send_signal(signal.SIGINT)

    net.stop()
