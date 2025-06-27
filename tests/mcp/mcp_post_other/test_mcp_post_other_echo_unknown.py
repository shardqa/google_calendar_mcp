import json
import pytest
from src.mcp import mcp_post_other_handler as mod

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


def test_echo():
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"tool": "echo", "args": {"message": "hello"}}}
    response = {"jsonrpc": "2.0", "id": 2}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("result") == {"content": [{"type": "text", "text": "🔊 Echo: hello"}]}


def test_unknown_tool():
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"tool": "unknown", "args": {}}}
    response = {"jsonrpc": "2.0", "id": 8}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("error", {}).get("code") == -32601


def test_unknown_method():
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 9, "method": "foo", "params": {}}
    response = {"jsonrpc": "2.0", "id": 9}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("error", {}).get("code") == -32601 