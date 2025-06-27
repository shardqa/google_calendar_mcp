import json
from src.mcp import mcp_post_sse_handler as mod

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


def test_tools_call_list_calendars(monkeypatch):
    handler = DummyHandler()

    def fake_list_calendars(service):
        assert service == 'svc'
        return ['c1', 'c2']

    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    monkeypatch.setattr(mod.calendar, 'list_calendars', fake_list_calendars)

    request = {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"tool": "list_calendars", "args": {}}}
    response = {}
    mod.handle_post_sse(handler, request, response)

    body = parse_json(handler)
    assert body.get("result") == {'content': ['c1', 'c2']} 