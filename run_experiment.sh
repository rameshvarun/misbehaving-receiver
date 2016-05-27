#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

echo "Destroying existing mininet topology..."
mn -c

echo "Generating network traces..."
python runner.py --server=kernel --client=kernel
python runner.py --server=kernel --client=opt-ack
python runner.py --server=kernel --client=dup-ack
python runner.py --server=kernel --client=ack-division

python runner.py --server=lwip --client=kernel
python runner.py --server=lwip --client=opt-ack
python runner.py --server=lwip --client=dup-ack
python runner.py --server=lwip --client=ack-division

echo "Creating graphs..."
python create_graphs.py
