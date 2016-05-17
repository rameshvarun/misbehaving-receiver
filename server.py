import SocketServer
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('port', type=int, help='The port to host the TCP server on.')
args = parser.parse_args()

DATA_LENGTH = 10000
DATA = "F" * DATA_LENGTH

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.sendall(DATA)

if __name__ == "__main__":
    server = SocketServer.TCPServer(('localhost', args.port), TCPHandler)
    try:
        print "Starting TCP server on port", args.port, "..."
        server.serve_forever()
    except KeyboardInterrupt as e: server.shutdown()
