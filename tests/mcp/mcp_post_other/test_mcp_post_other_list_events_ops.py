import json
import pytest
import src.mcp_post_other_handler as mod
from unittest.mock import Mock

class DummyHandler:
    def __init__(self):
        self._status = None
        self._headers = {}
        self._response_data = b""
        self.wfile = self

    def send_response(self, status):
        self._status = status

    def send_header(self, key, value):
        self._headers[key] = value

    def end_headers(self):
        pass  # No-op for dummy

    def write(self, data):
        self._response_data += data

def parse_response(handler):
    return json.loads(handler._response_data.decode())

def test_list_events(monkeypatch):
    handler = DummyHandler()
    called = {}
    class FakeOps:
        def __init__(self, service):
            called['service'] = service
        def list_events(self, max_results=None, calendar_id='primary'):
            called['max_results'] = max_results
            called['cal'] = calendar_id
            return ['e1', 'e2']
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    monkeypatch.setattr(mod.calendar_ops, 'CalendarOperations', FakeOps)
    request = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"tool": "list_events", "args": {"max_results": 5, "calendar_id": "globalsys"}}}
    response = {"jsonrpc": "2.0", "id": 3}
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    assert body.get("result") == {'content': ['e1', 'e2']}
    assert called['cal'] == 'globalsys' 