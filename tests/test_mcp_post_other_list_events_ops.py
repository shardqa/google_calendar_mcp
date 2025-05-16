import json
import pytest
import src.mcp_post_other_handler as mod

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

def test_list_events(monkeypatch):
    handler = DummyHandler()
    called = {}
    class FakeOps:
        def __init__(self, service):
            called['service'] = service
        def list_events(self, max_results=None):
            called['max_results'] = max_results
            return ['e1', 'e2']
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    monkeypatch.setattr(mod.calendar_ops, 'CalendarOperations', FakeOps)
    request = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"tool": "list_events", "args": {"max_results": 5}}}
    response = {"jsonrpc": "2.0", "id": 3}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("result") == ['e1', 'e2']
    assert called['service'] == 'svc'
    assert called['max_results'] == 5 