import io, json
from src.mcp.mcp_stdio_server import MCPStdioServer
from unittest.mock import patch

def test_send_response_and_error(monkeypatch, capsys):
    srv = MCPStdioServer()
    # normal response
    srv._send_response({"ok": True})
    out = capsys.readouterr().out.strip()
    assert json.loads(out)["ok"] is True
    # trigger internal error by passing non-serializable object
    class X: ...
    srv._send_response({"bad": X()})
    err_out = json.loads(capsys.readouterr().out.strip())
    assert err_out["error"]["code"] == -32603


def test_read_stdin_parse_error(monkeypatch, capsys):
    bad = "not json\n"
    good = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n"
    fake_in = io.StringIO(bad + good)
    monkeypatch.setattr("sys.stdin", fake_in)
    srv = MCPStdioServer()
    # Patch handler to return simple result to avoid deeper logic
    monkeypatch.setattr(srv, "handler", type("H", (), {"handle_request": lambda self, req: {"jsonrpc": "2.0", "id": req.get("id"), "result": "ok"}})())
    srv._read_stdin()
    captured = capsys.readouterr().out
    assert "Parse error" in captured 