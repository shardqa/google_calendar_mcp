import json
import pytest
from src.mcp import mcp_post_other_handler as mod
from unittest.mock import Mock, patch
import sys

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
    monkeypatch.setattr(mod.auth, 'get_calendar_service', Mock())
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"tool": "add_event", "args": {"start_time": "s", "end_time": "e"}}}
    response = {"jsonrpc": "2.0", "id": 4}

    with patch('src.mcp.mcp_post_other_handler.add_event') as mock_add_event:
        mod.handle_post_other(handler, request, response)
        body = parse_response(handler)
        assert body.get("error", {}).get("code") == -32602
        mock_add_event.assert_not_called()

def test_add_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    def fake_add_event(service, event_data):
        called['service'] = service
        called['event_data'] = event_data
        return {'status': 'confirmed', 'event': {'summary': 'Test Event', 'start': {'dateTime': '2024-01-01T10:00:00'}, 'end': {'dateTime': '2024-01-01T11:00:00'}}}

    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc2')
    monkeypatch.setattr(mod, 'add_event', fake_add_event)
    args = {"summary": "t", "start_time": "s", "end_time": "e", "location": "loc", "description": "desc"}
    request = {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"tool": "add_event", "args": args}}
    response = {"jsonrpc": "2.0", "id": 5}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body['result']['content']['status'] == 'confirmed'
    assert called['service'] == 'svc2'
    assert called['event_data']["summary"] == "t"
    assert called['event_data']["location"] == "loc"
    assert called['event_data']["description"] == "desc"

def test_add_event_with_location_coverage(monkeypatch):
    """Test to cover location and description in body"""
    handler = DummyHandler()
    called = {}
    def fake_add_event(service, event_data):
        called['service'] = service
        called['event_data'] = event_data
        return {'status': 'confirmed', 'event': {'summary': 'Test Event', 'start': {'dateTime': '2024-01-01T10:00:00'}, 'end': {'dateTime': '2024-01-01T11:00:00'}, 'location': 'Test Location'}}

    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc2')
    monkeypatch.setattr(mod, 'add_event', fake_add_event)
    args = {"summary": "Test Event", "start_time": "2024-01-01T10:00:00", "end_time": "2024-01-01T11:00:00", "location": "Test Location", "description": "desc"}
    request = {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"tool": "add_event", "args": args}}
    response = {"jsonrpc": "2.0", "id": 5}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body['result']['content']['event']['location'] == 'Test Location'
    assert called['event_data']['location'] == 'Test Location'
    assert called['event_data']['description'] == 'desc'


def test_add_event_error_coverage(monkeypatch):
    """Test for add_event failure"""
    handler = DummyHandler()
    called = {}
    def fake_add_event(service, event_data):
        called['service'] = service
        called['event_data'] = event_data
        return {'status': 'error', 'message': 'Test error message'}

    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc2')
    monkeypatch.setattr(mod, 'add_event', fake_add_event)
    args = {"summary": "Test Event", "start_time": "2024-01-01T10:00:00", "end_time": "2024-01-01T11:00:00"}
    request = {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"tool": "add_event", "args": args}}
    response = {"jsonrpc": "2.0", "id": 5}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body['result']['content']['status'] == 'error' 