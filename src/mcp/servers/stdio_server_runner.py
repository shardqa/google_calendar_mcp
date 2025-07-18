#!/usr/bin/env python3
"""
MCP Stdio Server runner and entry point.
Contains the main execution function and CLI entry point.
"""
from .stdio_server_core import MCPStdioServer


def run_stdio_server():
    """Run the MCP server in stdio mode."""
    server = MCPStdioServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    run_stdio_server() 