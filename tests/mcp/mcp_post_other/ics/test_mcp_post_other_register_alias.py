import json, sys
from src.mcp import mcp_post_other_handler as mod
from unittest.mock import Mock, patch

class DummyHandler:
    def __init__(self):
        self._status = None
        self._headers = {}
        self._response_data = b''
        self.wfile = self
    def send_response(self, status):
        self._status = status
    def send_header(self, k, v):
        self._headers[k] = v
    def end_headers(self):
        pass
    def write(self, d):
        self._response_data += d

def parse(h):
    return json.loads(h._response_data.decode())

def test_register_and_use_alias(monkeypatch):
    handler = DummyHandler()
    # patch registry to memory dict
    store = {}
    class FakeReg:
        @staticmethod
        def register(alias,url):
            store[alias]=url
        @staticmethod
        def get(alias):
            return store.get(alias)
        @staticmethod
        def list_all():
            return store.copy()
    monkeypatch.setitem(sys.modules,'src.core.ics_registry', FakeReg)
    # register tool
    req = {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"tool":"register_ics_calendar","args":{"alias":"work","ics_url":"http://ex.com/a.ics"}}}
    resp = {"jsonrpc":"2.0","id":1}
    mod.handle_post_other(handler, req, resp)
    res = parse(handler)['result']
    assert res['registered'] is True
    assert any("work" in item['text'] for item in res.get('content', []))
    # reset handler
    handler2 = DummyHandler()
    class FakeICSOps:
        def list_events(self, url, max_results):
            assert url=="http://ex.com/a.ics"
            return ['ok']
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    with patch('src.core.ics_ops.ICSOperations', return_value=FakeICSOps()):
        req2 = {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"tool":"list_events","args":{"ics_alias":"work","max_results":5}}}
        resp2 = {"jsonrpc":"2.0","id":2}
        mod.handle_post_other(handler2, req2, resp2)
        assert parse(handler2)['result']=={'content':['ok']} 