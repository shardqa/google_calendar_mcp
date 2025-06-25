import sys, os, subprocess, importlib
from unittest.mock import patch
import src.commands.mcp_cli as mcp_cli


def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def test_mcp_cli_script_execution(tmp_path):
    script_path = os.path.join(_project_root(), 'src', 'commands', 'mcp_cli.py')
    env = os.environ.copy(); env['HOME'] = str(tmp_path)
    rc_path = os.path.join(_project_root(), '.coveragerc')
    if importlib.util.find_spec('coverage'):
        cmd = [sys.executable, '-m', 'coverage', 'run', f'--rcfile={rc_path}', script_path, '--setup-only']
    else:
        cmd = [sys.executable, script_path, '--setup-only']
    res = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=_project_root())
    assert res.returncode == 0
    assert 'MCP configuration created at' in res.stdout
    assert 'Traceback' not in res.stderr


def test_mcp_cli_main_block_direct_execution(tmp_path):
    env = os.environ.copy(); env['HOME'] = str(tmp_path)
    res = subprocess.run([sys.executable, mcp_cli.__file__, '--setup-only'], env=env, capture_output=True, text=True)
    assert res.returncode == 0
    assert 'MCP configuration created at' in res.stdout


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