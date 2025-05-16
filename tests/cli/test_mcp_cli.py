import sys
import json
from pathlib import Path
import src.commands.mcp_cli as mcp_cli

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