from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
import datetime
import socket
from . import calendar_ops, auth
from .mcp_schema import get_mcp_schema

connected_clients = set()

class CalendarMCPHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        print(f"GET request received at path: {self.path}")
        
        if self.path == '/sse':
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Send initial hello message
            schema = get_mcp_schema()
            supported_protocol_version = schema.get("protocol", "2025-03-26")
            hello = {
                "jsonrpc": "2.0",
                "method": "mcp/hello",
                "params": {
                    "serverInfo": {
                        "name": "google_calendar",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {}
                    },
                    "protocolVersion": supported_protocol_version
                }
            }
            
            hello_json = json.dumps(hello)
            print(f"Sending hello: {hello_json}")
            self.wfile.write(b"event: mcp/hello\n")
            self.wfile.write(f"data: {hello_json}\n\n".encode('utf-8'))
            self.wfile.flush()
            
            # Wait a moment to ensure hello is processed
            time.sleep(0.5)
            
            # Send tool list immediately after hello
            tools_list = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {
                    "tools": schema["tools"]
                }
            }
            
            tools_json = json.dumps(tools_list)
            print(f"Sending tools list (length: {len(tools_json)}): {tools_json[:250]}...")
            self.wfile.write(b"event: tools/list\n")
            self.wfile.write(f"data: {tools_json}\n\n".encode('utf-8'))
            self.wfile.flush()
            
            # Track this client
            client_id = id(self)
            connected_clients.add(client_id)
            print(f"Client {client_id} connected. Total clients: {len(connected_clients)}")
            
            # Keep connection open with more frequent heartbeats
            try:
                heartbeat_interval = 5  # Reduced from 10 seconds to 5 seconds
                while client_id in connected_clients:
                    time.sleep(heartbeat_interval)
                    self.wfile.write(b":\n\n")  # Comment line as heartbeat
                    self.wfile.flush()
            except Exception as e:
                print(f"SSE connection error: {str(e)}")
            finally:
                if client_id in connected_clients:
                    connected_clients.remove(client_id)
                print(f"Client {client_id} disconnected. Remaining clients: {len(connected_clients)}")
        
        elif self.path == '/' or self.path == '/schema':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            
            schema = get_mcp_schema()
            self.wfile.write(json.dumps(schema).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        print(f"POST request received at path: {self.path}")
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"Received POST data: {post_data}")
        
        try:
            request = json.loads(post_data)
            jsonrpc = request.get("jsonrpc", "2.0")
            request_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})
            
            response = {"jsonrpc": jsonrpc, "id": request_id}
            
            if self.path == '/sse':
                if method == "mcp/cancel" or method == "$/cancelRequest":
                    # Handle cancellation properly
                    cancel_id = params.get("id") if isinstance(params, dict) else None
                    print(f"Received cancellation request/notification with ID: {request_id}, for operation ID: {cancel_id}")
                    
                    if method == "mcp/cancel":
                        # Respond only to method calls with ID
                        response["result"] = {"cancelled": True}
                        print(f"Sending cancellation response: {json.dumps(response)}")
                    else:
                        # For $/cancelRequest, which is typically a notification, just acknowledge
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Connection', 'close')
                        self.end_headers()
                        self.wfile.write(b"{}")
                        return
                elif method == "notifications/cancelled":
                    # Handle new cancellation notification as per MCP 2025-03-26 spec
                    cancel_id = params.get("requestId") if isinstance(params, dict) else None
                    print(f"Received cancellation notification for operation ID: {cancel_id}")
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    return
                
                elif method == "$/toolList" or method == "tools/list":
                    schema = get_mcp_schema()
                    response["result"] = {"tools": schema["tools"]}
                    print(f"Sent tools list response: {json.dumps(response)[:100]}...")
                
                elif method == "initialize":
                    supported_protocol_version = get_mcp_schema().get("protocol", "2025-03-26") # Default fallback
                    response["result"] = {
                        "serverInfo": {
                            "name": "google_calendar",
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        },
                        "protocolVersion": supported_protocol_version
                    }
                    print(f"Sent initialize response: {json.dumps(response)}")
                
                elif method == "list_events":
                    service = auth.get_calendar_service()
                    max_results = params.get("max_results", 10)
                    ops = calendar_ops.CalendarOperations(service)
                    events = ops.list_events(max_results)
                    response["result"] = events
                
                elif method == "add_event":
                    service = auth.get_calendar_service()
                    summary = params.get("summary")
                    location = params.get("location")
                    description = params.get("description")
                    start_time = params.get("start_time")
                    end_time = params.get("end_time")
                    
                    if not all([summary, start_time, end_time]):
                        raise ValueError("Missing required event parameters")
                    
                    ops = calendar_ops.CalendarOperations(service)
                    event_data = {
                        "summary": summary,
                        "start": {"dateTime": start_time},
                        "end": {"dateTime": end_time}
                    }
                    if location:
                        event_data["location"] = location
                    if description:
                        event_data["description"] = description
                    result = ops.add_event(event_data)
                    response["result"] = result
                
                elif method == "remove_event":
                    service = auth.get_calendar_service()
                    event_id = params.get("event_id")
                    
                    if not event_id:
                        raise ValueError("Event ID is required")
                    
                    ops = calendar_ops.CalendarOperations(service)
                    success = ops.remove_event(event_id)
                    response["result"] = {"success": success}
                
                elif method == "simple_test_tool":
                    print("Executing simple_test_tool")
                    response["result"] = {"message": "simple_test_tool executed successfully"}
                
                elif method == "echo":
                    message = params.get("message", "No message provided")
                    print(f"Echoing message: {message}")
                    response["result"] = {"echo": message}
                
                else:
                    response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
            
            else:
                # Handle requests to other endpoints
                if method == "initialize":
                    supported_protocol_version = get_mcp_schema().get("protocol", "2025-03-26") # Default fallback
                    response["result"] = {
                        "serverInfo": {
                            "name": "google_calendar", 
                            "version": "1.0.0"
                        },
                        "capabilities": {
                            "tools": {}
                        },
                        "protocolVersion": supported_protocol_version
                    }
                else:
                    response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
            
            # Send the response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Connection', 'close')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
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
            
            error = {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": None}
            self.wfile.write(json.dumps(error).encode())

class CalendarMCPServer:
    def __init__(self, host="localhost", port=3000):
        self.host = host
        self.port = port
        
        # Ensure we're binding to all interfaces properly
        if host == "localhost" or host == "127.0.0.1":
            # For local development, bind to all interfaces to ensure proper connections
            self.server = ThreadingHTTPServer(("0.0.0.0", port), CalendarMCPHandler)
            print(f"⚠️ Note: Binding to all interfaces (0.0.0.0) on port {port} for better connectivity")
        else:
            self.server = ThreadingHTTPServer((host, port), CalendarMCPHandler)
        
        # Ensure server socket does not hold onto port when restarting
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
        
        # Display URLs for connecting
        actual_host = "localhost" if self.host == "0.0.0.0" else self.host
        print(f"Calendar MCP Server running at http://{actual_host}:{self.port}/")
        print(f"SSE endpoint available at http://{actual_host}:{self.port}/sse")
    
    def stop(self):
        if not self.running:
            return
        
        self.running = False
        self.server.shutdown()
        self.server_thread.join()
        connected_clients.clear()
        print("Calendar MCP Server stopped")

def run_server(host="localhost", port=3000):
    server = CalendarMCPServer(host, port)
    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    run_server() 