#!/usr/bin/env python3
import argparse
import os
import json
import sys
from pathlib import Path
import shutil

def setup_mcp_config():
    """Setup MCP configuration in user's Cursor directory"""
    try:
        cursor_dir = Path.home() / ".cursor"
        cursor_dir.mkdir(exist_ok=True)
        
        mcp_config_path = cursor_dir / "mcp.json"
        
        # If config file exists, try to parse it. If corrupted, create backup
        existing_config = {}
        if mcp_config_path.exists():
            try:
                with open(mcp_config_path, "r") as f:
                    existing_config = json.load(f)
            except json.JSONDecodeError:
                # Create backup of corrupted file
                backup_path = cursor_dir / "mcp.json.backup"
                shutil.copy2(mcp_config_path, backup_path)
                print(f"Warning: Corrupted mcp.json backed up to {backup_path}")
                existing_config = {}
        
        # Preserve existing mcpServers if they exist and file was valid
        config = {"mcpServers": existing_config.get("mcpServers", {})}
        
        # Add/update the google_calendar server configuration
        uvx_cmd = shutil.which("uvx") or "uvx"
        project_root = Path(__file__).parent.parent.parent.resolve()
        config["mcpServers"]["google_calendar"] = {
            "command": uvx_cmd,
            "args": [
                "--from",
                str(project_root),
                "google-calendar-mcp"
            ],
            "timeout": 60000,
            "description": "Google Calendar Integration (uvx)"
        }
        
        # Write the updated config
        with open(mcp_config_path, "w") as f:
            json.dump(config, f, indent=4)
        
        print(f"MCP configuration created at {mcp_config_path}")
        print(f"Google Calendar MCP server configured for uvx usage")
    except (OSError, FileExistsError) as e:
        print(f"Error: Could not write MCP configuration to {cursor_dir}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Google Calendar MCP Server")
    parser.add_argument(
        "--setup-only", 
        action="store_true", 
        help="Only setup MCP configuration without starting the server"
    )
    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run server in stdio mode (default: False)"
    )
    args = parser.parse_args()
    
    # Only set up configuration when explicitly requested via --setup-only
    if args.setup_only:
        setup_mcp_config()
        return
    
    if args.stdio:
        print(f"Starting Google Calendar MCP server in stdio mode.", file=sys.stderr)
        try:
            from ..mcp.mcp_stdio_server import run_stdio_server
        except ImportError:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from src.mcp.servers.mcp_stdio_server import run_stdio_server
        run_stdio_server()
    else:
        print("Error: This CLI only supports stdio mode or setup-only.", file=sys.stderr)
        print("Use --stdio to run in stdio mode or --setup-only to configure MCP.", file=sys.stderr)
        print("For regular usage, use: uvx --from . google-calendar-mcp", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 