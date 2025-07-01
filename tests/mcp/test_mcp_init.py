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
        # Test that we can import tool_calendar
        tool_calendar = mcp_module.__getattr__("tool_calendar")
        assert tool_calendar is not None
        
        # Test that we can import tool_ics
        tool_ics = mcp_module.__getattr__("tool_ics")
        assert tool_ics is not None
    
    def test_server_name_import(self):
        """Test importing server modules by name."""
        # Test a few server name imports
        mcp_server = mcp_module.__getattr__("mcp_server")
        assert mcp_server is not None
        
        stdio_handler = mcp_module.__getattr__("stdio_handler")
        assert stdio_handler is not None
    
    def test_invalid_name_raises_error(self):
        """Test that invalid attribute names raise AttributeError."""
        with pytest.raises(AttributeError):
            mcp_module.__getattr__("nonexistent_module")
    
    def test_all_tool_names_importable(self):
        """Test that all defined tool names can be imported."""
        # Test that all tools in _TOOL_NAMES can be imported
        tool_names = ["tool_calendar", "tool_ics"]
        for tool_name in tool_names:
            tool_module = mcp_module.__getattr__(tool_name)
            assert tool_module is not None
    
    def test_tool_calendar_has_handle_function(self):
        tool_calendar = mcp_module.__getattr__("tool_calendar")
        assert hasattr(tool_calendar, "handle")
        assert callable(tool_calendar.handle)
    
    def test_tool_ics_has_handle_function(self):
        tool_ics = mcp_module.__getattr__("tool_ics")
        assert hasattr(tool_ics, "handle")
        assert callable(tool_ics.handle)
