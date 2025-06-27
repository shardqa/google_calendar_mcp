import importlib
import json
import os
import pathlib
import sys
import tempfile
import types
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "src.commands.mcp_cli"

def test_mcp_cli_setup_only(monkeypatch, capsys):
    """Test that --setup-only creates the config and exits."""
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(pathlib.Path, "home", lambda: pathlib.Path(tmp))
        monkeypatch.setattr(sys, "argv", ["mcp_cli", "--port", "4321", "--setup-only"])
        
        # Ensure module is fresh for argv patching
        mod = importlib.reload(importlib.import_module(MODULE_PATH))
        mod.main()

        captured = capsys.readouterr()
        cfg_path = pathlib.Path(tmp) / ".cursor" / "mcp.json"
        assert cfg_path.exists()
        data = json.loads(cfg_path.read_text())
        assert data["mcpServers"]["google_calendar"]["url"].endswith(":4321/sse")
        assert "MCP configuration created" in captured.out

def test_mcp_cli_stdio_entry(monkeypatch, capsys):
    """Test that --stdio starts the stdio server."""
    mock_run_stdio = MagicMock()
    monkeypatch.setattr("src.mcp.mcp_stdio_server.run_stdio_server", mock_run_stdio)
    monkeypatch.setattr(sys, "argv", ["mcp_cli", "--stdio"])
    
    mod = importlib.reload(importlib.import_module(MODULE_PATH))
    mod.main()
    
    mock_run_stdio.assert_called_once()
    captured = capsys.readouterr()
    assert "Starting Google Calendar MCP server in stdio mode" in captured.err

def test_import_error_fallback(monkeypatch):
    """Test the sys.path modification when src is not in the path."""
    original_path = list(sys.path)
    # Simulate 'src' not being in the path
    sys.path = [p for p in sys.path if 'src' not in p]
    
    # The module must be removed from cache to force reload with the new path
    if MODULE_PATH in sys.modules:
        del sys.modules[MODULE_PATH]
    if 'src.mcp' in sys.modules:
        del sys.modules['src.mcp']
        
    # Check that it runs without error
    importlib.import_module(MODULE_PATH)
    
    # Restore the original path
    sys.path = original_path

def test_setup_config_os_error(monkeypatch, tmp_path):
    """Test that file permission errors are handled during config write."""
    # Make the target directory read-only to trigger an OSError
    config_dir = tmp_path / ".cursor"
    config_dir.mkdir(parents=True)
    os.chmod(config_dir, 0o400)  # Read-only

    monkeypatch.setattr(pathlib.Path, 'home', lambda: tmp_path)

    with pytest.raises(SystemExit) as excinfo:
        mod = importlib.reload(importlib.import_module(MODULE_PATH))
        mod.setup_mcp_config(9999)

    assert excinfo.value.code == 1

def test_setup_config_mkdir_error(monkeypatch, tmp_path):
    """Test that errors during directory creation are handled."""
    # Create a file where the directory should be, causing mkdir to fail
    config_file_path = tmp_path / ".cursor"
    config_file_path.touch()

    monkeypatch.setattr(pathlib.Path, 'home', lambda: tmp_path)

    with pytest.raises(SystemExit) as excinfo:
        mod = importlib.reload(importlib.import_module(MODULE_PATH))
        mod.setup_mcp_config(9999)
    
    assert excinfo.value.code == 1 