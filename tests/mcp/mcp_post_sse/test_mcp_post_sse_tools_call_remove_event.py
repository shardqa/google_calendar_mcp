import json
import pytest
import src.mcp.mcp_post_sse_handler as mod
from unittest.mock import patch

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

@patch('src.mcp.mcp_post_sse_handler.auth.get_calendar_service')
@patch('src.mcp.mcp_post_sse_handler.calendar_ops.CalendarOperations')
def test_tools_call_remove_event_missing(MockCalendarOperations, MockGetCalendarService):
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":11,"method":"tools/call","params":{"tool":"remove_event","args":{}}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["error"]["code"] == -32602

def test_tools_call_remove_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    class Fake:
        def __init__(self, svc):
            called["service"] = svc
        def remove_event(self, eid):
            called["eid"] = eid
            return False
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    request = {"jsonrpc":"2.0","id":12,"method":"tools/call","params":{"tool":"remove_event","args":{"event_id":"e1"}}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["result"] == {"success":False}
    assert called["eid"] == "e1" 