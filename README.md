# Attacks on Congestion Control by a Misbehaving TCP Receiver

<img src="http://i.imgur.com/bnzyV8S.png" width="500px" height="500px" />

The repository contains scripts for replicating the results in the paper ["Attacks on Congestion Control by a Misbehaving TCP Receiver"](https://cseweb.ucsd.edu/~savage/papers/CCR99.pdf) by Savage Cardwell et. al. This project was done for the [CS244](https://web.stanford.edu/class/cs244/) (Advanced Topics in Networking) class at Stanford. The associated writeup is [here](https://reproducingnetworkresearch.wordpress.com/2016/05/30/cs244-16-tcp-congestion-control-with-a-misbehaving-receiver/).

## Replicating Results

The results here can either be replicated on an EC2 instance or in VirtualBox. To setup an EC2 machine, use the instructions here - https://web.stanford.edu/class/cs244/ec2setup.html. Follow the instructions here to setup a local virtual machine in VirtualBox - https://web.stanford.edu/class/cs244/vbsetup.html. If you still have your virtual machine from PA1, then you should be able to use it without any problems (though the EC2 instance usually provides cleaner results). Note that when you SSH into your machine, you probably want to use the `-Y` flag (and have an X server running), in order to view the generated graphs. Once logged in, run the following commands.

```bash
git clone https://github.com/rameshvarun/misbehaving-receiver.git
cd misbehaving-receiver
sudo ./run-experiment.sh
```

The graphs should now be in the `graphs/` folder. The images that appear in our report are `graphs/opt-ack-lwip.png`, `graphs/opt-ack-lwip-defended.png`, and `graphs/opt-ack-kernel.png`. If you have X11 forwarding working, just use `xdg-open`. Otherwise, you should `scp -r` the folder.

## Files Breakdown
- [run-experiment.sh](./run-experiment.sh) - This file runs the entire experiement, generating all of the network traces and all of the graphs.
- [opt-ack-defense.diff](./opt-ack-defense.diff) - This is our defense against optimistic ACK attacks, displayed as a patch.
- [server.py](./server.py) - This is a simple TCP server. When a client makes a connection, the server immediately sends a large stream of data. Upon sending the data, the server closes the connection.
- [attackers/](./attackers) - This folder contains three scripts, each of which implments one of the attacks mentioned in the original paper.
- [runner.py](./runner.py) - This script creates the mininet topolgy and runs the client and server, logging packets.
- [create_graph.py](./create_graph.py) - This script creates the ACK and data segment graphs based off of the packet captures.
