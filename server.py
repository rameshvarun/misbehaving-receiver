#!/usr/bin/env python

"""
This file starts a simple TCP server that listens for connections. When a
connection is established, the server sends a bunch of data through tha
connection. After sending the data, it closes the connection.
"""

import SocketServer
import argparse

parser = argparse.ArgumentParser(description='Start a TCP server.')
parser.add_argument('--port', default=8000, type=int,
                    help='The port on which to listen.')
parser.add_argument('--length', default=100000, type=int,
                    help='The size of the data to send over the connection.')
args = parser.parse_args()

DATA = "F" * args.length

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print "Connection opened from %s:%d. Sending data." % self.client_address
        self.request.sendall(DATA)
        print "Data sent. Closing connection to %s:%d." % self.client_address

if __name__ == "__main__":
    server = SocketServer.TCPServer(('0.0.0.0', args.port), TCPHandler)
    try:
        print "Starting TCP server on port", args.port, "..."
        server.serve_forever()
    except KeyboardInterrupt as e: server.shutdown()
