import json
import sys
import src.mcp_post_sse_handler as mod
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


def parse_json(handler):
    assert handler.status == 200
    return json.loads(handler.wrote.decode())


def test_tools_call_list_ics_events(monkeypatch):
    sample = ['e1', 'e2']
    class FakeICSOps:
        def list_events(self, ics_url, max_results):
            assert ics_url == 'http://example.com/calendar.ics'
            assert max_results == 7
            return sample
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    monkeypatch.setattr(mod, 'calendar_ops', Mock())
    monkeypatch.setitem(sys.modules, 'src.core.ics_ops', Mock(ICSOperations=FakeICSOps))

    handler = DummyHandler()
    request = {"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": {"tool": "list_events", "args": {"ics_url": "http://example.com/calendar.ics", "max_results": 7}}}
    response = {}
    mod.handle_post_sse(handler, request, response)

    body = parse_json(handler)
    assert body.get("result") == {'content': sample} 