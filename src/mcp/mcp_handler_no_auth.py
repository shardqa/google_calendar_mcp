import json
import urllib.parse
from http.server import BaseHTTPRequestHandler
from .mcp_schema import get_mcp_schema
from .mcp_post_sse_handler import handle_post_sse
from .mcp_get_handler import handle_get

class CalendarMCPHandlerNoAuth(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
    
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        
        if path == "/sse":
            self.handle_sse_connection()
        elif path == "/":
            self.handle_root()
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        
        if path == "/sse":
            self.handle_sse_post()
        else:
            self.send_error(404, "Not found")
    
    def handle_sse_connection(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        hello_data = {
            "jsonrpc": "2.0",
            "method": "mcp/hello",
            "params": {
                "serverInfo": {"name": "google_calendar", "version": "1.0.0"},
                "capabilities": {"tools": {tool["name"]: tool["inputSchema"] for tool in get_mcp_schema()["tools"]}},
                "protocolVersion": "2025-03-26"
            }
        }
        
        self.wfile.write(f"event: message\n".encode())
        self.wfile.write(f"data: {json.dumps(hello_data)}\n\n".encode())
        self.wfile.flush()
    
    def handle_sse_post(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
                request = json.loads(post_data)
            else:
                request = {}
                
            response = {"jsonrpc": "2.0", "id": request.get("id")}
            handle_post_sse(self, request, response)
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": None
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def handle_root(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        info = {
            "name": "Google Calendar MCP Server",
            "version": "1.0.0",
            "endpoints": {
                "sse": "/sse",
                "schema": "/schema"
            },
            "status": "running"
        }
        self.wfile.write(json.dumps(info, indent=2).encode()) 