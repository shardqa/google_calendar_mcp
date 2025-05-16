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

def test_unknown_method_fails():
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":13,"method":"foo","params":{}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["error"]["code"] == -32601 