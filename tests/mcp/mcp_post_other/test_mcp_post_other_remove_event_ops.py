import json
import pytest
from src.mcp import mcp_post_other_handler as mod
from unittest.mock import Mock, patch

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
    monkeypatch.setattr(mod.auth, 'get_calendar_service', Mock())
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"tool": "remove_event", "args": {}}}
    response = {"jsonrpc": "2.0", "id": 6}
    with patch('src.mcp.mcp_post_other_handler.remove_event') as mock_remove_event:
        mod.handle_post_other(handler, request, response)
        body = parse_response(handler)
        assert body.get("error", {}).get("code") == -32602
        mock_remove_event.assert_not_called()

def test_remove_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    def fake_remove_event(service, event_id):
        called['service'] = service
        called['event_id'] = event_id
        return True
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc3')
    monkeypatch.setattr(mod, 'remove_event', fake_remove_event)
    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"tool": "remove_event", "args": {"event_id": "id1"}}}
    response = {"jsonrpc": "2.0", "id": 7}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    txt = body['result']['content'][0]['text']
    assert '✅' in txt
    assert called['event_id'] == 'id1'

def test_remove_event_failure(monkeypatch):
    handler = DummyHandler()
    called = {}
    def fake_remove_event(service, event_id):
        called['service'] = service
        called['event_id'] = event_id
        return False
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc4')
    monkeypatch.setattr(mod, 'remove_event', fake_remove_event)
    request = {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"tool": "remove_event", "args": {"event_id": "id_fail"}}}
    response = {"jsonrpc": "2.0", "id": 8}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    txt = body['result']['content'][0]['text']
    assert '❌' in txt
    assert called['event_id'] == 'id_fail' 