import json
from http.server import BaseHTTPRequestHandler
from .mcp_get_handler import handle_get
from .mcp_post_handler import handle_post

class CalendarMCPHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        handle_get(self)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            request = json.loads(post_data)
            response = {"jsonrpc": request.get("jsonrpc", "2.0"), "id": request.get("id")}
            handle_post(self, request, response)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            error = {"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}
            self.wfile.write(json.dumps(error).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            error = {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": request.get("id")}
            self.wfile.write(json.dumps(error).encode()) 