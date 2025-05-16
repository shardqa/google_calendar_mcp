import json
import pytest
import src.mcp_post_sse_handler as mod

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


def parse_json(handler):
    assert handler.status == 200
    return json.loads(handler.wrote.decode())

def test_initialize(monkeypatch):
    handler = DummyHandler()
    fake = {"protocol":"v1","tools":[{"name":"a","inputSchema":{"y":2}}]}
    monkeypatch.setattr(mod, "get_mcp_schema", lambda: fake)
    request = {"jsonrpc":"2.0","id":5,"method":"initialize","params":{}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    expected = {"serverInfo":{"name":"google_calendar","version":"1.0.0"},"capabilities":{"tools":{"a":{"y":2}}},"protocolVersion":"v1"}
    assert body["result"] == expected 