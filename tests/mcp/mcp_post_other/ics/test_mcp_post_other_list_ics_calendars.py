import json, sys
from src.mcp import mcp_post_other_handler as mod
from unittest.mock import Mock

class H:
    def __init__(self):
        self._status=None
        self._headers={}
        self._data=b''
        self.wfile=self
    def send_response(self,s): self._status=s
    def send_header(self,k,v): self._headers[k]=v
    def end_headers(self): pass
    def write(self,d): self._data+=d

def j(h): return json.loads(h._data)

def test_list_ics_calendars_other(monkeypatch):
    class FakeReg:
        @staticmethod
        def list_all():
            return {'a':'u'}
    monkeypatch.setitem(sys.modules,'src.core.ics_registry', FakeReg)
    h=H()
    req={"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"tool":"list_ics_calendars","args":{}}}
    mod.handle_post_other(h, req, {"jsonrpc":"2.0","id":7})
    assert j(h)['result']=={'calendars':{'a':'u'}} 