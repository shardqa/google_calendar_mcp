import json
import pytest
import src.mcp_post_other_handler as mod
from unittest.mock import Mock

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

def test_remove_event_missing(monkeypatch):
    # Mock the calendar service to prevent file access
    mock_service = Mock()
    mock_service.events.return_value.delete.return_value.execute.return_value = None # Mock successful deletion
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)

    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"tool": "remove_event", "args": {}}}
    response = {"jsonrpc": "2.0", "id": 6}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("error", {}).get("code") == -32602

def test_remove_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    class FakeOps:
        def __init__(self, service):
            called['service'] = service
        def remove_event(self, event_id):
            called['event_id'] = event_id
            return True
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc3')
    monkeypatch.setattr(mod.calendar_ops, 'CalendarOperations', FakeOps)
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"tool": "remove_event", "args": {"event_id": "id1"}}}
    response = {"jsonrpc": "2.0", "id": 7}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("result") == {'success': True}
    assert called['event_id'] == 'id1' 