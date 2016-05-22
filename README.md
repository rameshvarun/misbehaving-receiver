# Attacks on Congestion Control by a Misbehaving TCP Receiver
- [server.py](./server.py) - This is a simple TCP server. When a client makes a connection, the server immediately sends a large stream of data. Upon sending the data, the server closes the connection.
- [opt_ack_attacker.py](./opt_ack_attacker.py) (WIP) - This script implements a malicious client that executes the Optimal Acking attack against a server.
- [runner.py](./runner.py) - This script creates the mininet topolgy and runs the client and server, logging packets.
- [create_graph.py](./create_graph.py) - This script creates the ACK and data segment graphs based off of the packet captures.
