import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import src.mcp as mcp_module


class TestMCPInit:
    """Test the MCP module's __getattr__ functionality."""
    
    def test_tool_name_import(self):
        """Test importing tool modules by name."""
        # Test importing a tool module
        tool_echo = mcp_module.__getattr__("tool_echo")
        assert tool_echo is not None
        # Check for the actual function that exists in tool_echo module
        assert hasattr(tool_echo, 'handle')
        
        # Test that it's cached in globals
        assert "tool_echo" in mcp_module.__dict__
    
    def test_server_name_import(self):
        """Test importing server modules by name."""
        # Test importing a server module
        mcp_server = mcp_module.__getattr__("mcp_server")
        assert mcp_server is not None
        assert hasattr(mcp_server, 'run_server')
        
        # Test stdio server
        mcp_stdio_server = mcp_module.__getattr__("mcp_stdio_server")
        assert mcp_stdio_server is not None
        assert hasattr(mcp_stdio_server, 'run_stdio_server')
        
        # Test that they're cached in globals
        assert "mcp_server" in mcp_module.__dict__
        assert "mcp_stdio_server" in mcp_module.__dict__
    
    def test_invalid_attribute_raises_error(self):
        """Test that invalid attribute names raise AttributeError."""
        with pytest.raises(AttributeError) as exc_info:
            mcp_module.__getattr__("invalid_module_name")
        
        assert str(exc_info.value) == "invalid_module_name"
    
    def test_all_tool_names_importable(self):
        """Test that all defined tool names can be imported."""
        tool_names = {"tool_calendar", "tool_tasks", "tool_echo", "tool_ics"}
        
        for tool_name in tool_names:
            tool_module = mcp_module.__getattr__(tool_name)
            assert tool_module is not None
            # Each tool should be cached after import
            assert tool_name in mcp_module.__dict__
    
    def test_all_server_names_importable(self):
        """Test that all defined server names can be imported."""
        server_names = {"mcp_server", "mcp_stdio_server"}
        
        for server_name in server_names:
            server_module = mcp_module.__getattr__(server_name)
            assert server_module is not None
            # Each server should be cached after import
            assert server_name in mcp_module.__dict__
