#!/usr/bin/env python3
"""
Wrapper script to run the MCP server with correct module path.
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the MCP server
from src.mcp.mcp_stdio_server import run_stdio_server

if __name__ == "__main__":
    run_stdio_server()