import json
from src.mcp.handlers.stdio_handler import StdioRequestHandler

def test_tools_call_error(mock_credentials):
    caps = {"tools": {}, "serverInfo": {}, "protocolVersion": "v"}
    h = StdioRequestHandler(caps)
    # tools/call with unknown tool triggers error -32601 from inner process
    req = {"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"tool": "unknown", "args": {}}}
    res = h.handle_request(req)
    assert res["error"]["code"] == -32601


def test_bad_jsonrpc():
    caps = {"tools": {}, "serverInfo": {}, "protocolVersion": "v"}
    h = StdioRequestHandler(caps)
    # Missing method field
    req = {"jsonrpc": "2.0", "id": 1}
    res = h.handle_request(req)
    assert res["error"]["code"] == -32601 