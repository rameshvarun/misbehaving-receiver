#!/usr/bin/env bash
ip tuntap add dev tap0 mode tap
ip link set dev tap0 up
ip addr add 172.16.0.1/24 dev tap0
./lwip-tap/lwip-tap -i name=tap0,addr=172.16.0.2,netmask=255.255.255.0,gw=172.16.0.1 -E
