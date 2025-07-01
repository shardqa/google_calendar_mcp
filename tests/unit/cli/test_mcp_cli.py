import sys, json, os
from unittest.mock import patch
import pytest
import src.commands.mcp_cli as mcp_cli


def test_setup_mcp_config(tmp_home, capsys):
    mcp_cli.setup_mcp_config()
    cfg = tmp_home / '.cursor' / 'mcp.json'
    assert cfg.exists()
    content = json.loads(cfg.read_text())
    assert 'command' in content['mcpServers']['google_calendar']
    out = capsys.readouterr().out
    assert f'MCP configuration created at {cfg}' in out


def test_setup_mcp_config_preserves_existing_servers(tmp_home, capsys):
    """Test that setup_mcp_config preserves existing MCP server configurations."""
    # Create .cursor dir and seed config
    cursor_dir = tmp_home / '.cursor'
    cursor_dir.mkdir()
    cfg = cursor_dir / 'mcp.json'
    existing_config = {
        "mcpServers": {
            "other_server": {
                "command": "python",
                "args": ["-m", "other_mcp"],
                "env": {"KEY": "value"}
            },
            "another_server": {
                "url": "http://localhost:4000/sse",
                "type": "sse",
                "enabled": True
            }
        }
    }
    cfg.write_text(json.dumps(existing_config, indent=4))
    mcp_cli.setup_mcp_config()
    
    # Verify existing servers are preserved and new one is added
    content = json.loads(cfg.read_text())
    
    # Check that existing servers are still there
    assert 'google_calendar' in content['mcpServers']
    assert 'command' in content['mcpServers']['google_calendar']


def test_setup_mcp_config_handles_corrupted_file(tmp_home, capsys):
    """Test that setup_mcp_config handles corrupted mcp.json file gracefully."""
    # prepare corrupted file
    cursor_dir = tmp_home / '.cursor'
    cursor_dir.mkdir()
    cfg = cursor_dir / 'mcp.json'
    backup_cfg = cursor_dir / 'mcp.json.backup'
    cfg.write_text('{ "invalid": json content }')

    mcp_cli.setup_mcp_config()

    assert backup_cfg.exists()
    assert backup_cfg.read_text() == '{ "invalid": json content }'

    captured = capsys.readouterr()
    assert 'Warning: Corrupted mcp.json backed up to' in captured.out


def test_main_setup_only(tmp_home, monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['prog', '--setup-only'])
    mcp_cli.main()
    out = capsys.readouterr().out
    assert 'MCP configuration created at' in out
    assert 'Starting Google Calendar MCP server' not in out


def test_main_no_args_error(tmp_home, monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['prog'])
    with pytest.raises(SystemExit) as exc_info:
        mcp_cli.main()
    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert 'Error: This CLI only supports stdio mode or setup-only' in err


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
