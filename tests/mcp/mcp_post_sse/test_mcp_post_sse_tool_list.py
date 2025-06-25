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

@pytest.mark.parametrize("method", ["$/toolList", "tools/list"]
)
def test_tool_list(method, monkeypatch):
    handler = DummyHandler()
    fake = {"tools":[{"name":"t","inputSchema":{"x":1}}]}
    monkeypatch.setattr(mod, "get_mcp_schema", lambda: fake)
    request = {"jsonrpc":"2.0","id":4,"method":method,"params":{}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["result"] == {"tools": fake["tools"]} 