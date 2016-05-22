#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo!"
  exit
fi

echo "Destroying existing mininet topology..."
mn -c

echo "Generating network traces..."
python runner.py
python runner.py --client=modified

echo "Creating graphs..."
python create_graphs.py
