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
from .stdio_handler import StdioRequestHandler


class MCPStdioServer:
    """MCP Server that communicates via stdin/stdout using JSON-RPC protocol."""
    
    def __init__(self):
        self.running = False
        self._setup_capabilities()
        self.handler = StdioRequestHandler(self.capabilities)
    
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
    
    def _read_stdin(self):
        """Read and process JSON-RPC requests from stdin."""
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handler.handle_request(request)
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
