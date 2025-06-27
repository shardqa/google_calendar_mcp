import json
from src.mcp import mcp_post_other_handler as mod

class Dummy:
    def __init__(self):
        self._status=None
        self._headers={}
        self._data=b''
        self.wfile=self
    def send_response(self,s):
        self._status=s
    def send_header(self,k,v):
        self._headers[k]=v
    def end_headers(self):
        pass
    def write(self,d):
        self._data+=d

def body(h):
    return json.loads(h._data)

def test_register_alias_missing_args(monkeypatch):
    h=Dummy()
    req={"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"tool":"register_ics_calendar","args":{"ics_url":"http://ex.com"}}}
    mod.handle_post_other(h, req, {"jsonrpc":"2.0","id":6})
    res=body(h)
    assert res['error']['code']==-32602 