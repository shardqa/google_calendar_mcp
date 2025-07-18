#!/usr/bin/env python3
"""
Core MCP Stdio Server class.
Contains the main server logic and capabilities setup.
"""
from typing import Dict, Any
from ..mcp_schema import get_mcp_schema
from ..handlers.stdio_handler import StdioRequestHandler


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
    
    def _send_response(self, response):
        """Send JSON-RPC response to stdout. Always include 'id' (string/number, never null)."""
        from .stdio_server_io import send_response
        send_response(response)
    
    def _read_stdin(self):
        """Read and process JSON-RPC requests from stdin."""
        from .stdio_server_io import read_stdin_loop
        read_stdin_loop(self)
    
    def start(self):
        """Start the stdio server."""
        if self.running:
            return
        
        self.running = True
        
        try:
            self._read_stdin()
        except Exception as e:
            from .stdio_server_io import create_error_response, send_response
            error_response = create_error_response(-32603, f"Server error: {str(e)}")
            send_response(error_response)
    
    def stop(self):
        """Stop the stdio server."""
        self.running = False 