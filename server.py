"""
This file starts a simple TCP server that listens for connections. When a
connection is established, the server sends a bunch of data through tha
connection. After sending the data, it closes the connection.
"""

import SocketServer
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', default=8000, type=int,
                    help='The port on which to listen.')
parser.add_argument('--length', default=100000, type=int,
                    help='The size of the data to send over the connection.')
args = parser.parse_args()

DATA = "F" * args.length

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self): self.request.sendall(DATA)

if __name__ == "__main__":
    server = SocketServer.TCPServer(('localhost', args.port), TCPHandler)
    try:
        print "Starting TCP server on port", args.port, "..."
        server.serve_forever()
    except KeyboardInterrupt as e: server.shutdown()
