#!/usr/bin/env bash
sysctl net.ipv4.ip_forward=1
sysctl net.ipv4.conf.all.proxy_arp=1
route add default gw 10.11.0.1

ip tuntap add dev tap0 mode tap
ip link set dev tap0 up
ip addr add 10.11.0.2/16 dev tap0
./lwip-tap-defended/lwip-tap -i name=tap0,addr=10.11.0.1,netmask=255.255.0.0,gw=10.11.0.2 -E
