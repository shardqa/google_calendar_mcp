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

def test_add_event_missing(monkeypatch):
    # Mock the calendar service to prevent file access
    mock_service = Mock()
    mock_service.events.return_value.insert.return_value.execute.return_value = {'status': 'confirmed', 'event': {'id': 'mocked_event_id'}}
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)

    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"tool": "add_event", "args": {"start_time": "s", "end_time": "e"}}}
    response = {"jsonrpc": "2.0", "id": 4}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("error", {}).get("code") == -32602

def test_add_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    class FakeOps:
        def __init__(self, service):
            called['service'] = service
        def add_event(self, event_data):
            called['event_data'] = event_data
            return {'status': 'ok'}
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc2')
    monkeypatch.setattr(mod.calendar_ops, 'CalendarOperations', FakeOps)
    args = {"summary": "t", "start_time": "s", "end_time": "e", "location": "loc", "description": "desc"}
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"tool": "add_event", "args": args}}
    response = {"jsonrpc": "2.0", "id": 5}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("result") == {'status': 'ok'}
    assert called['service'] == 'svc2'
    assert called['event_data']["summary"] == "t" 