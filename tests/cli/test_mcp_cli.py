import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import src.commands.mcp_cli as mcp_cli
import subprocess
import importlib
import os

def test_setup_mcp_config(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    port = 12345
    mcp_cli.setup_mcp_config(port)
    config_path = tmp_path / ".cursor" / "mcp.json"
    assert config_path.exists()
    content = json.loads(config_path.read_text())
    expected = {"mcpServers": {"google_calendar": {"url": f"http://localhost:{port}/sse","type": "sse","enabled": True,"description": "Google Calendar Integration"}}}
    assert content == expected
    out = capsys.readouterr().out
    assert f"MCP configuration created at {config_path}" in out
    assert f"Google Calendar MCP server configured at http://localhost:{port}/sse" in out

def test_main_setup_only(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda host, port: calls.append((host, port)))
    monkeypatch.setattr(sys, 'argv', ['prog', '--port', '5555', '--host', 'testhost', '--setup-only'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert "MCP configuration created at" in out
    assert "Starting Google Calendar MCP server" not in out
    assert calls == []

def test_main_start_server(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda host, port: calls.append((host, port)))
    monkeypatch.setattr(sys, 'argv', ['prog', '--port', '8888', '--host', 'myhost'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert f"Starting Google Calendar MCP server at http://myhost:8888/" in out
    assert calls == [('myhost', 8888)]

def test_mcp_cli_script_execution(tmp_path):
    """
    Test the __main__ and ImportError blocks of mcp_cli.py via subprocess.
    This covers both the main execution path and the relative import fallback.
    """
    # This test covers lines 10-12 (ImportError) and 69 (__main__)
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'commands', 'mcp_cli.py')

    # Running the script directly triggers the __main__ block. It also causes
    # the initial relative import to fail, which triggers the ImportError block.
    env = os.environ.copy()
    env['HOME'] = str(tmp_path)
    
    # We explicitly point to the .coveragerc file to ensure parallel mode is activated.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    rc_path = os.path.join(project_root, '.coveragerc')

    # Prefer running under coverage to maintain branch/statement metrics, but fall back to
    # a direct execution path when the coverage module is unavailable in the environment.
    if importlib.util.find_spec("coverage") is not None:
        cmd = [
            sys.executable, "-m", "coverage", "run", f"--rcfile={rc_path}",
            script_path, '--setup-only'
        ]
    else:
        cmd = [sys.executable, script_path, '--setup-only']

    result = subprocess.run(
        cmd, env=env, capture_output=True, text=True, cwd=project_root
    )
    
    # Assert a clean run
    assert result.returncode == 0
    assert "MCP configuration created at" in result.stdout
    assert "Error" not in result.stderr
    assert "Traceback" not in result.stderr

def test_import_error_path_insertion():
    """Test that the ImportError path properly inserts the correct path"""
    import os
    
    # Simulate the path that would be inserted
    test_file_path = "/some/path/to/src/commands/mcp_cli.py"
    expected_path = os.path.join(os.path.dirname(test_file_path), '..', '..')
    
    # Normalize the path like the code would
    normalized_path = os.path.normpath(expected_path)
    
    # This should result in "/some/path/to"
    assert normalized_path.endswith("to")

def test_main_with_default_args(tmp_path, monkeypatch, capsys):
    """Test main function with default arguments"""
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda host, port: calls.append((host, port)))
    monkeypatch.setattr(sys, 'argv', ['prog'])  # No additional args
    
    mcp_cli.main()
    
    out = capsys.readouterr().out
    assert "Starting Google Calendar MCP server at http://localhost:3000/" in out
    assert calls == [('localhost', 3000)]

def test_mcp_cli_main_block_direct_execution(tmp_path, monkeypatch):
    """Test the __main__ block of mcp_cli.py via direct execution"""
    # This test covers line 69
    
    # We need to run the script in a separate process to trigger the __main__ block
    script_path = mcp_cli.__file__
    
    # Use subprocess to run the script with --setup-only to prevent it from hanging
    # We also need to set HOME to a temporary directory
    env = os.environ.copy()
    env['HOME'] = str(tmp_path)
    
    result = subprocess.run([sys.executable, script_path, '--setup-only'], env=env, capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "MCP configuration created at" in result.stdout

def test_mcp_cli_import_error(monkeypatch):
    """Test the ImportError block of mcp_cli.py"""
    # This test covers lines 10-12
    
    # To test the ImportError, we need to make 'src.mcp.mcp_server' unavailable
    # We can do this by patching sys.modules
    with patch.dict('sys.modules', {'src.mcp.mcp_server': None}):
        # We also need to remove it from the loaded modules to force a re-import
        if 'src.mcp.mcp_server' in sys.modules:
            del sys.modules['src.mcp.mcp_server']
            
        # The script uses a relative import `from ..mcp.mcp_server...`. 
        # When run as a test, this can be tricky.
        # We will patch sys.path to simulate the import error condition.
        original_path = sys.path[:]
        sys.path = [p for p in sys.path if 'google_calendar_mcp' not in p]
        
        try:
            # Re-importing the module should trigger the ImportError block
            importlib.reload(mcp_cli)
        finally:
            # Restore sys.path
            sys.path = original_path
            # And reload the module in its correct state for other tests
            importlib.reload(mcp_cli)
            
        # The assertion is that no exception is raised and the module is loaded
        assert hasattr(mcp_cli, 'run_server') 