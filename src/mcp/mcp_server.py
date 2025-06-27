from http.server import ThreadingHTTPServer
import threading
import time
import socket
from .mcp_handler import CalendarMCPHandler
import argparse

class CalendarMCPServer:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        if host == "localhost" or host == "127.0.0.1":
            self.server = ThreadingHTTPServer(("0.0.0.0", port), CalendarMCPHandler)
            print(f"⚠️ Note: Binding to all interfaces (0.0.0.0) on port {port} for better connectivity")
        else:
            self.server = ThreadingHTTPServer((host, port), CalendarMCPHandler)
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_thread = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        actual_host = "localhost" if self.host == "0.0.0.0" else self.host
        print(f"Calendar MCP Server running at http://{actual_host}:{self.port}/")
        print(f"SSE endpoint available at http://{actual_host}:{self.port}/sse")

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.server.shutdown()
        self.server_thread.join()
        print("Calendar MCP Server stopped")

def run_server(host=None, port=None):
    if host is None:
        host = "localhost"
    if port is None:
        port = 3000

    server = CalendarMCPServer(host, port)
    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()

def main(argv=None):
    parser = argparse.ArgumentParser(description="Google Calendar MCP Server")
    parser.add_argument('--host', default='localhost', help='Host to bind the server to.')
    parser.add_argument('--port', type=int, default=3000, help='Port to bind the server to.')
    args = parser.parse_args(argv)

    run_server(args.host, args.port)

if __name__ == '__main__':
    main() 