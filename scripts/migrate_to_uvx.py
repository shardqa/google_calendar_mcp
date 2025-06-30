#!/usr/bin/env python3
"""
Script to migrate MCP configurations from python direct execution to uvx.
Updates both Cursor and Gemini CLI configurations.
"""
import json
import os
import sys
from pathlib import Path
import shutil


def backup_file(file_path):
    """Create backup of existing file."""
    backup_path = file_path.with_suffix(f'{file_path.suffix}.backup-uvx')
    if file_path.exists():
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    return None


def migrate_cursor_config():
    """Migrate Cursor MCP configuration to use uvx."""
    cursor_dir = Path.home() / ".cursor"
    mcp_config_path = cursor_dir / "mcp.json"
    
    if not mcp_config_path.exists():
        print("ℹ️  No Cursor MCP config found, skipping...")
        return
    
    print(f"🔄 Migrating Cursor config: {mcp_config_path}")
    backup_file(mcp_config_path)
    
    try:
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)
        
        project_root = str(Path(__file__).parent.parent.absolute())
        
        # Update existing python-based config to uvx
        servers_updated = []
        for server_name, server_config in config.get("mcpServers", {}).items():
            if (isinstance(server_config, dict) and 
                server_config.get("command") == "python3" and
                "src.mcp.mcp_stdio_server" in server_config.get("args", [])):
                
                # Convert to uvx
                config["mcpServers"][server_name] = {
                    "command": "uvx",
                    "args": ["--from", project_root, "google-calendar-mcp"],
                    "timeout": server_config.get("timeout", 30000)
                }
                servers_updated.append(server_name)
        
        # Add new uvx config if no existing google_calendar configs
        if not any("google_calendar" in name.lower() for name in config.get("mcpServers", {})):
            config.setdefault("mcpServers", {})["google_calendar_uvx"] = {
                "command": "uvx",
                "args": ["--from", project_root, "google-calendar-mcp"],
                "timeout": 30000
            }
            servers_updated.append("google_calendar_uvx")
        
        with open(mcp_config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        if servers_updated:
            print(f"✅ Updated Cursor servers: {', '.join(servers_updated)}")
        else:
            print("ℹ️  No Cursor servers needed updating")
            
    except Exception as e:
        print(f"❌ Error migrating Cursor config: {e}")


def migrate_gemini_config():
    """Migrate Gemini CLI configuration to use uvx."""
    gemini_dir = Path.home() / ".gemini"
    settings_path = gemini_dir / "settings.json"
    
    if not settings_path.exists():
        print("ℹ️  No Gemini CLI config found, skipping...")
        return
    
    print(f"🔄 Migrating Gemini config: {settings_path}")
    backup_file(settings_path)
    
    try:
        with open(settings_path, 'r') as f:
            config = json.load(f)
        
        project_root = str(Path(__file__).parent.parent.absolute())
        
        # Update existing python-based config to uvx
        servers_updated = []
        for server_name, server_config in config.get("mcpServers", {}).items():
            if (isinstance(server_config, dict) and 
                server_config.get("command") == "python3" and
                "src.mcp.mcp_stdio_server" in server_config.get("args", [])):
                
                # Convert to uvx
                config["mcpServers"][server_name] = {
                    "command": "uvx",
                    "args": ["--from", project_root, "google-calendar-mcp"],
                    "timeout": server_config.get("timeout", 30000)
                }
                servers_updated.append(server_name)
        
        # Add new uvx config if no existing google_calendar configs
        if not any("google_calendar" in name.lower() for name in config.get("mcpServers", {})):
            config.setdefault("mcpServers", {})["google_calendar"] = {
                "command": "uvx", 
                "args": ["--from", project_root, "google-calendar-mcp"],
                "timeout": 30000
            }
            servers_updated.append("google_calendar")
        
        with open(settings_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        if servers_updated:
            print(f"✅ Updated Gemini servers: {', '.join(servers_updated)}")
        else:
            print("ℹ️  No Gemini servers needed updating")
            
    except Exception as e:
        print(f"❌ Error migrating Gemini config: {e}")


def check_uv_installation():
    """Check if uv is installed."""
    try:
        import subprocess
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ uv is installed but not working properly")
            return False
    except FileNotFoundError:
        print("❌ uv is not installed")
        print("📦 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def main():
    """Main migration function."""
    print("🚀 Google Calendar MCP: Migration to uvx")
    print("=" * 50)
    
    # Check prerequisites
    if not check_uv_installation():
        print("\n⚠️  Please install uv before continuing")
        sys.exit(1)
    
    print()
    
    # Migrate configurations
    migrate_cursor_config()
    print()
    migrate_gemini_config()
    
    print()
    print("🎉 Migration completed!")
    print()
    print("📝 Next steps:")
    print("1. Test the new uvx configuration")
    print("2. If working correctly, remove old python-based configs")
    print("3. Restart Cursor/Gemini CLI to load new configuration")
    print()
    print("🔍 Test command:")
    project_root = Path(__file__).parent.parent.absolute()
    print(f"   uvx --from {project_root} google-calendar-mcp")


if __name__ == "__main__":
    main() 