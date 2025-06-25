import json, sys
import src.mcp_post_sse_handler as mod
from unittest.mock import Mock

class DummyHandler:
    def __init__(self):
        self.status=None
        self.headers=[]
        self.wrote=b''
    def send_response(self,c):
        self.status=c
    def send_header(self,k,v):
        self.headers.append((k,v))
    def end_headers(self):
        pass
    @property
    def wfile(self):
        class W:
            def __init__(self,o):
                self.o=o
            def write(self,d):
                self.o.wrote+=d
        return W(self)

def pj(h):
    return json.loads(h.wrote.decode())

def test_list_events_with_alias(monkeypatch):
    class FakeReg:
        @staticmethod
        def get(alias):
            return 'http://ex.com/b.ics' if alias=='work' else ''
    class FakeICSOps:
        def list_events(self, url, max_results):
            assert url=='http://ex.com/b.ics'
            assert max_results==3
            return ['x']
    monkeypatch.setitem(sys.modules,'src.core.ics_registry', FakeReg)
    monkeypatch.setitem(sys.modules,'src.core.ics_ops', Mock(ICSOperations=FakeICSOps))
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'svc')
    monkeypatch.setattr(mod, 'calendar_ops', Mock())
    h=DummyHandler()
    req={"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"tool":"list_events","args":{"ics_alias":"work","max_results":3}}}
    mod.handle_post_sse(h, req, {})
    assert pj(h)['result']=={'content':['x']} 