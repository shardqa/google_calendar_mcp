#!/usr/bin/env python3
"""
MCP Server with stdio support for JSON-RPC communication.
This server reads JSON-RPC requests from stdin and writes responses to stdout.
"""
from .stdio_server_core import MCPStdioServer
from .stdio_server_runner import run_stdio_server

__all__ = ['MCPStdioServer', 'run_stdio_server']
