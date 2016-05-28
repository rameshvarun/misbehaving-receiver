# Attacks on Congestion Control by a Misbehaving TCP Receiver

## Replicating Results

Follow the instructions here to setup a virtual machine - https://web.stanford.edu/class/cs244/vbsetup.html. If you still have your virtual machine from PA1, then you should be able to use it without any problems. Once logged, in run the following comamnds.

```bash
git clone https://github.com/rameshvarun/misbehaving-receiver.git
cd misbehaving-receiver
sudo run-experiment.sh
```

## Files Breakdown
- [run-experiment.sh](./run-experiment.sh) - This file runs the entire experiement, generating all of the network traces and all of the graphs.
- [opt-ack-defense.diff](./opt-ack-defense.diff) - This is our defense against optimistic ACK attacks, displayed as a patch.
- [server.py](./server.py) - This is a simple TCP server. When a client makes a connection, the server immediately sends a large stream of data. Upon sending the data, the server closes the connection.
- [attackers/](./attackers) - This folder contains three scripts, each of which implments one of the attacks mentioned in the original paper.
- [runner.py](./runner.py) - This script creates the mininet topolgy and runs the client and server, logging packets.
- [create_graph.py](./create_graph.py) - This script creates the ACK and data segment graphs based off of the packet captures.
