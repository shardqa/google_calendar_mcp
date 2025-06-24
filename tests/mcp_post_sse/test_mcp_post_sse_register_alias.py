import json, sys
import src.mcp_post_sse_handler as mod
from unittest.mock import Mock

class DummyHandler:
    def __init__(self):
        self.status=None
        self.headers=[]
        self.wrote=b''
    def send_response(self, c):
        self.status=c
    def send_header(self,k,v):
        self.headers.append((k,v))
    def end_headers(self):
        pass
    @property
    def wfile(self):
        class W:
            def __init__(self, outer):
                self.outer=outer
            def write(self,d):
                self.outer.wrote+=d
        return W(self)

def pj(h):
    return json.loads(h.wrote.decode())

def test_register_and_list_alias_sse(monkeypatch):
    store={}
    class FakeReg:
        @staticmethod
        def register(a,u):
            store[a]=u
        @staticmethod
        def list_all():
            return store.copy()
    monkeypatch.setitem(sys.modules,'src.core.ics_registry',FakeReg)
    handler=DummyHandler()
    req={"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"tool":"register_ics_calendar","args":{"alias":"my","ics_url":"http://ex.com"}}}
    resp={}
    mod.handle_post_sse(handler,req,resp)
    res = pj(handler)['result']
    assert res['registered'] is True
    assert any("my" in item['text'] for item in res.get('content', []))
    handler2=DummyHandler()
    req2={"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"tool":"list_ics_calendars","args":{}}}
    mod.handle_post_sse(handler2,req2,resp)
    assert pj(handler2)['result']=={"calendars":{"my":"http://ex.com"}}

def test_register_ics_calendar_missing_params_sse():
    handler=DummyHandler()
    req={"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"tool":"register_ics_calendar","args":{"alias":"my"}}}
    resp={}
    mod.handle_post_sse(handler,req,resp)
    result = pj(handler)
    assert "error" in result
    assert result["error"]["code"] == -32602
    assert "alias and ics_url are required" in result["error"]["message"] 