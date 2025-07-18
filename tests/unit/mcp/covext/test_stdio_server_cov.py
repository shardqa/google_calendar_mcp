from io import StringIO
import json, sys
from src.mcp.servers.mcp_stdio_server import MCPStdioServer


def test_stdio_loop(monkeypatch):
    srv = MCPStdioServer()

    class H:
        def handle_request(self, req):
            if req.get("method") == "err":
                raise ValueError()
            return {"jsonrpc": "2.0", "id": req.get("id"), "result": "ok"}

    srv.handler = H()
    inp = "\n".join([
        json.dumps({"jsonrpc": "2.0", "method": "a", "id": 1}),
        json.dumps({"jsonrpc": "2.0", "method": "err", "id": 2}),
        "{bad",
    ])
    monkeypatch.setattr(sys, "stdin", StringIO(inp))
    out = StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    srv._read_stdin()
    lines = [json.loads(l) for l in out.getvalue().strip().splitlines()]
    assert lines[0]["result"] == "ok"
    assert lines[1]["error"]["code"] == -32603
    assert lines[2]["error"]["code"] == -32700 