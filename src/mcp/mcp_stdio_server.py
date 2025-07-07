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
        """Send JSON-RPC response to stdout. Always include 'id' (string/number, never null)."""
        # Always include 'id' field, and never set it to null (Zod expects string/number).
        if "id" not in response or response["id"] is None:
            response["id"] = ""
        try:
            response_json = json.dumps(response)
            print(response_json, flush=True)
        except Exception as e:
            # In case serialization itself fails, fall back to a minimal error message.
            fallback_error = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": ""
            }
            print(json.dumps(fallback_error), flush=True)
    
    def _read_stdin(self):
        """Read and process JSON-RPC requests from stdin."""
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                try:
                    request = json.loads(line)
                    # If this is a notification (no id), do not send any response
                    if "id" not in request or request["id"] is None:
                        continue
                    response = self.handler.handle_request(request)
                    if response:
                        self._send_response(response)

                except json.JSONDecodeError:
                    # Parse errors are always responded to, as per JSON-RPC spec
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        },
                        "id": ""
                    }
                    self._send_response(error_response)
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        },
                        "id": ""
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
        
        # Start reading from stdin and respond to client requests
        try:
            self._read_stdin()
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Server error: {str(e)}"
                },
                "id": ""
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
