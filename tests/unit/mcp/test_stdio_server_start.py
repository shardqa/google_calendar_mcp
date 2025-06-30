from src.mcp.mcp_stdio_server import MCPStdioServer
import builtins

def test_stdio_server_start(monkeypatch):
    srv = MCPStdioServer()
    # Patch _read_stdin so start returns immediately
    monkeypatch.setattr(srv, "_read_stdin", lambda: setattr(srv, 'running', False))
    srv.start()
    assert srv.running is False 