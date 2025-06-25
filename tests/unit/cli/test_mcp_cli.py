import sys, json, os
from unittest.mock import patch
import src.commands.mcp_cli as mcp_cli


def test_setup_mcp_config(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    port = 12345
    mcp_cli.setup_mcp_config(port)
    cfg = tmp_path / '.cursor' / 'mcp.json'
    assert cfg.exists()
    content = json.loads(cfg.read_text())
    assert content['mcpServers']['google_calendar']['url'] == f'http://localhost:{port}/sse'
    out = capsys.readouterr().out
    assert f'MCP configuration created at {cfg}' in out


def test_main_setup_only(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda h, p: calls.append((h, p)))
    monkeypatch.setattr(sys, 'argv', ['prog', '--port', '5555', '--host', 'testhost', '--setup-only'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert 'MCP configuration created at' in out
    assert 'Starting Google Calendar MCP server' not in out
    assert calls == []


def test_main_start_server(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda h, p: calls.append((h, p)))
    monkeypatch.setattr(sys, 'argv', ['prog', '--port', '8888', '--host', 'myhost'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert 'http://myhost:8888/' in out
    assert calls == [('myhost', 8888)]


def test_main_stdio_mode(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(sys, 'argv', ['prog', '--stdio'])
    with patch('src.mcp.mcp_stdio_server.run_stdio_server', lambda: calls.append('stdio')):
        with patch('builtins.print') as mock_print:
            mcp_cli.main()
        mock_print.assert_any_call('Starting Google Calendar MCP server in stdio mode.', file=sys.stderr)
    assert calls == ['stdio']


def test_main_stdio_mode_import_error(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(sys, 'argv', ['prog', '--stdio'])
    
    # Mock import to trigger ImportError and fallback path
    original_import = __builtins__['__import__']
    def mock_import(name, *args, **kwargs):
        if name == 'src.mcp.mcp_stdio_server' and 'run_stdio_server' in str(args):
            raise ImportError("Mocked import error")
        return original_import(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=mock_import):
        with patch('src.mcp.mcp_stdio_server.run_stdio_server', lambda: calls.append('stdio')):
            with patch('builtins.print') as mock_print:
                mcp_cli.main()
            mock_print.assert_any_call('Starting Google Calendar MCP server in stdio mode.', file=sys.stderr)
    assert calls == ['stdio']


def test_main_with_default_args(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('HOME', str(tmp_path))
    calls = []
    monkeypatch.setattr(mcp_cli, 'run_server', lambda h, p: calls.append((h, p)))
    monkeypatch.setattr(sys, 'argv', ['prog'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert 'http://localhost:3000/' in out
    assert calls == [('localhost', 3000)]
