import sys
import subprocess
from unittest.mock import patch
import runpy

@patch('src.mcp.mcp_server.main')
def test_mcp_main_entrypoint(mock_main):
    """
    Tests the `if __name__ == '__main__'` block in src/mcp/__main__.py
    by using runpy and patching the downstream main function.
    """
    runpy.run_module("src.mcp", run_name="__main__")
    mock_main.assert_called_once()