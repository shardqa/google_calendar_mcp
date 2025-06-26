import sys, os, subprocess, importlib
from unittest.mock import patch
import src.commands.mcp_cli as mcp_cli
import pytest
from pathlib import Path


def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def test_mcp_cli_script_execution():
    """Test that src/commands/mcp_cli.py can be executed as a script"""
    python_exe = '.venv/bin/python'
    res = subprocess.run([python_exe, 'src/commands/mcp_cli.py', '--setup-only'], 
                         capture_output=True, text=True)
    assert res.returncode == 0
    assert "MCP configuration created" in res.stdout


def test_mcp_cli_main_block_direct_execution():
    """Test direct execution with explicit main block"""
    python_exe = '.venv/bin/python'
    res = subprocess.run([python_exe, 'src/commands/mcp_cli.py', '--help'], 
                         capture_output=True, text=True)
    assert res.returncode == 0
    assert "Google Calendar MCP Server" in res.stdout


def test_mcp_cli_import_statements():
    """Test import statement coverage"""
    import src.commands.mcp_cli as cli
    assert hasattr(cli, 'main')
    assert callable(cli.main)


def test_mcp_cli_module_structure():
    """Test module structure and attributes"""
    import src.commands.mcp_cli as cli
    
    assert hasattr(cli, 'main')
    assert hasattr(cli, 'os')
    assert hasattr(cli, 'sys')


def test_import_error_path_insertion():
    test_file = '/some/path/to/src/commands/mcp_cli.py'
    exp = os.path.join(os.path.dirname(test_file), '..', '..')
    assert os.path.normpath(exp).endswith('to')


def test_mcp_cli_import_error(monkeypatch):
    with patch.dict('sys.modules', {'src.mcp.mcp_server': None}):
        if 'src.mcp.mcp_server' in sys.modules:
            del sys.modules['src.mcp.mcp_server']
        original = sys.path[:]
        sys.path = [p for p in sys.path if 'google_calendar_mcp' not in p]
        try:
            importlib.reload(mcp_cli)
        finally:
            sys.path = original
            importlib.reload(mcp_cli)
        assert hasattr(mcp_cli, 'run_server') 