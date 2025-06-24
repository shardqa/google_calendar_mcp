#!/usr/bin/env python3
import argparse
import os
import json
import sys
from pathlib import Path

try:
    from ..mcp.mcp_server import run_server
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.mcp.mcp_server import run_server

def setup_mcp_config(port):
    """Setup MCP configuration in user's Cursor directory"""
    cursor_dir = Path.home() / ".cursor"
    cursor_dir.mkdir(exist_ok=True)
    
    mcp_config_path = cursor_dir / "mcp.json"
    
    # Create a new MCP config (overwrite instead of update)
    config = {
        "mcpServers": {
            "google_calendar": {
                "url": f"http://localhost:{port}/sse",
                "type": "sse",
                "enabled": True,
                "description": "Google Calendar Integration"
            }
        }
    }
    
    # Write the config
    with open(mcp_config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"MCP configuration created at {mcp_config_path}")
    print(f"Google Calendar MCP server configured at http://localhost:{port}/sse")

def main():
    parser = argparse.ArgumentParser(description="Google Calendar MCP Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=3000, 
        help="Port to run the server on (default: 3000)"
    )
    parser.add_argument(
        "--host", 
        default="localhost", 
        help="Host to bind the server to (default: localhost)"
    )
    parser.add_argument(
        "--setup-only", 
        action="store_true", 
        help="Only setup MCP configuration without starting the server"
    )
    
    args = parser.parse_args()
    
    # Only set up configuration when explicitly requested via --setup-only
    if args.setup_only:
        setup_mcp_config(args.port)
    
    if not args.setup_only:
        print(f"Starting Google Calendar MCP server at http://{args.host}:{args.port}/")
        run_server(args.host, args.port)

if __name__ == "__main__":
    main() 