import json
import pytest
import src.mcp_post_other_handler as mod
from src.mcp_schema import get_mcp_schema

class DummyHandler:
    def __init__(self):
        self.status = None
        self.headers = []
        self.wrote = b''
    def send_response(self, code):
        self.status = code
    def send_header(self, key, value):
        self.headers.append((key, value))
    def end_headers(self):
        pass
    @property
    def wfile(self):
        class W:
            def __init__(self, outer):
                self.outer = outer
            def write(self, data):
                self.outer.wrote += data
        return W(self)


def parse_response(handler):
    assert handler.status == 200
    return json.loads(handler.wrote.decode())


def test_initialize():
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    response = {"jsonrpc": "2.0", "id": 1}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    schema = get_mcp_schema()
    expected = {
        "serverInfo": schema["serverInfo"],
        "capabilities": {"tools": {t["name"]: t["inputSchema"] for t in schema["tools"]}},
        "protocolVersion": schema["protocol"]
    }
    assert body.get("result") == expected
    assert "error" not in body 