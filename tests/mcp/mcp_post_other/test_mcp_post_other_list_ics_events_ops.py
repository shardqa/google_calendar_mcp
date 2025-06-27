import json
import sys
from src.mcp import mcp_post_other_handler as mod
from unittest.mock import Mock, patch

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
        pass

    def write(self, data):
        self._response_data += data


def parse_response(handler):
    return json.loads(handler._response_data.decode())


def test_list_ics_events(monkeypatch):
    handler = DummyHandler()

    sample_events = ['e1', 'e2']

    class FakeICSOps:
        def __init__(self):
            pass
        def list_events(self, ics_url, max_results):
            assert ics_url == 'http://example.com/calendar.ics'
            assert max_results == 5
            return sample_events

    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    # The handler now imports ICSOperations via importlib from src.core.ics_ops
    # So we need to patch 'src.core.ics_ops.ICSOperations'
    with patch('src.core.ics_ops.ICSOperations', return_value=FakeICSOps()) as mock_ics_ops:
        request = {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"tool": "list_events", "args": {"ics_url": "http://example.com/calendar.ics", "max_results": 5}}}
        response = {"jsonrpc": "2.0", "id": 10}
        mod.handle_post_other(handler, request, response)

        body = parse_response(handler)
        assert body.get("result") == {'content': sample_events}
        mock_ics_ops.assert_called_once() 