#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

echo "Building LWIP stacks."
(cd lwip-tap; ./configure; make)
(cd lwip-tap-defended; ./configure; make)

echo "Destroying existing mininet topology..."
mn -c

echo "Generating network traces..."

# Run the kernel server against various attackers.
python runner.py --server=kernel --client=kernel
python runner.py --server=kernel --client=opt-ack
python runner.py --server=kernel --client=dup-ack
python runner.py --server=kernel --client=ack-division

# Run the vanilla LWIP server against various attackers.
python runner.py --server=lwip --client=kernel
python runner.py --server=lwip --client=opt-ack
python runner.py --server=lwip --client=dup-ack
python runner.py --server=lwip --client=ack-division

# Run the defended LWIP server against the attackers.
python runner.py --server=lwip-defended --client=kernel
python runner.py --server=lwip-defended --client=opt-ack
python runner.py --server=lwip-defended --client=ack-division
python runner.py --server=lwip-defended --client=dup-ack

echo "Creating graphs..."
python create_graphs.py
