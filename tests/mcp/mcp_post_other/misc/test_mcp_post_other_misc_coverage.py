import json, sys
from unittest.mock import patch, MagicMock

from src.mcp import mcp_post_other_handler as mod

class Dummy:
    def __init__(self):
        self._data = b""
        self.wfile = self
    def send_response(self, *_):
        pass
    def send_header(self, *_):
        pass
    def end_headers(self):
        pass
    def write(self, d):
        self._data += d

def parsed(handler):
    return json.loads(handler._data or b"{}")

@patch("src.mcp.mcp_post_other_handler.auth.get_calendar_service", MagicMock())
def test_unknown_tool_error():
    h = Dummy()
    req = {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"tool":"nonexistent","args":{}}}
    mod.handle_post_other(h, req, {"jsonrpc":"2.0","id":1})
    body = parsed(h)
    assert body["error"]["code"] == -32601 