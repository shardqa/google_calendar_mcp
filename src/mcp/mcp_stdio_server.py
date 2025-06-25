#!/usr/bin/env python3
"""
MCP Server with stdio support for JSON-RPC communication.
This server reads JSON-RPC requests from stdin and writes responses to stdout.
"""
import json
import sys
import threading
from typing import Dict, Any, Optional
from .mcp_schema import get_mcp_schema
from .mcp_post_other_handler import handle_post_other


class MCPStdioServer:
    """MCP Server that communicates via stdin/stdout using JSON-RPC protocol."""
    
    def __init__(self):
        self.running = False
        self.capabilities = None
        self._setup_capabilities()
    
    def _setup_capabilities(self):
        """Setup server capabilities from schema."""
        schema = get_mcp_schema()
        self.capabilities = {
            "tools": {tool['name']: tool['inputSchema'] for tool in schema['tools']},
            "serverInfo": schema.get("serverInfo", {"name": "google_calendar", "version": "1.0.0"}),
            "protocolVersion": schema.get("protocol", "2025-03-26")
        }
    
    def _send_response(self, response: Dict[str, Any]) -> None:
        """Send JSON-RPC response to stdout."""
        try:
            response_json = json.dumps(response)
            print(response_json, flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": None
            }
            print(json.dumps(error_response), flush=True)
    
    def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "jsonrpc": request.get("jsonrpc", "2.0"),
            "id": request.get("id"),
            "result": {
                "serverInfo": self.capabilities["serverInfo"],
                "capabilities": {"tools": self.capabilities["tools"]},
                "protocolVersion": self.capabilities["protocolVersion"]
            }
        }
    
    def _handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request."""
        schema = get_mcp_schema()
        return {
            "jsonrpc": request.get("jsonrpc", "2.0"),
            "id": request.get("id"),
            "result": {
                "tools": schema['tools']
            }
        }
    
    def _handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request by delegating to existing handler."""
        # Create a mock handler object that captures the response
        class MockHandler:
            def __init__(self):
                self.response_data = None
                self.status_code = 200
                self.headers = []
            
            def send_response(self, code):
                self.status_code = code
            
            def send_header(self, key, value):
                self.headers.append((key, value))
            
            def end_headers(self):
                pass
            
            @property
            def wfile(self):
                class MockWFile:
                    def __init__(self, handler):
                        self.handler = handler
                    
                    def write(self, data):
                        if isinstance(data, bytes):
                            data = data.decode('utf-8')
                        try:
                            self.handler.response_data = json.loads(data)
                        except json.JSONDecodeError:
                            self.handler.response_data = {"error": "Invalid JSON response"}
                
                return MockWFile(self)
        
        # Create mock handler and response
        mock_handler = MockHandler()
        response = {
            "jsonrpc": request.get("jsonrpc", "2.0"),
            "id": request.get("id")
        }
        
        try:
            # Delegate to existing handler
            handle_post_other(mock_handler, request, response)
            
            # Return the response that was written to the mock handler
            if mock_handler.response_data:
                return mock_handler.response_data
            else:
                return response
                
        except Exception as e:
            return {
                "jsonrpc": request.get("jsonrpc", "2.0"),
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming JSON-RPC request."""
        method = request.get("method")
        
        if method == "initialize":
            return self._handle_initialize(request)
        elif method == "tools/list":
            return self._handle_tools_list(request)
        elif method == "tools/call":
            return self._handle_tools_call(request)
        else:
            return {
                "jsonrpc": request.get("jsonrpc", "2.0"),
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def _read_stdin(self):
        """Read and process JSON-RPC requests from stdin."""
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self._handle_request(request)
                    if response:
                        self._send_response(response)
                        
                except json.JSONDecodeError:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        },
                        "id": None
                    }
                    self._send_response(error_response)
                    
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        },
                        "id": None
                    }
                    self._send_response(error_response)
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
    
    def start(self):
        """Start the stdio server."""
        if self.running:
            return
        
        self.running = True
        
        # Send initial hello message to establish connection
        hello_message = {
            "jsonrpc": "2.0",
            "method": "mcp/hello",
            "params": {
                "serverInfo": self.capabilities["serverInfo"],
                "capabilities": {"tools": self.capabilities["tools"]},
                "protocolVersion": self.capabilities["protocolVersion"]
            }
        }
        self._send_response(hello_message)
        
        # Start reading from stdin
        try:
            self._read_stdin()
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Server error: {str(e)}"
                },
                "id": None
            }
            self._send_response(error_response)
    
    def stop(self):
        """Stop the stdio server."""
        self.running = False


def run_stdio_server():
    """Run the MCP server in stdio mode."""
    server = MCPStdioServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    run_stdio_server()
