import json
import pytest
import src.mcp_post_sse_handler as mod

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

def test_mcp_cancel_sets_result():
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":1,"method":"mcp/cancel","params":{"id":"op1"}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["result"] == {"cancelled":True}
    assert handler.headers[0] == ("Content-Type","application/json")
    assert ("Access-Control-Allow-Origin","*") in handler.headers
    assert ("Connection","close") in handler.headers

def test_cancel_request_writes_empty_json():
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":2,"method":"$/cancelRequest","params":{"id":"op2"}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    assert handler.status == 200
    assert handler.headers[0] == ("Content-Type","application/json")
    assert handler.wrote == b"{}"

def test_notifications_cancelled_only_headers():
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":3,"method":"notifications/cancelled","params":{"requestId":"r1"}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    assert handler.status == 200
    assert ("Content-Type","application/json") in handler.headers
    assert handler.wrote == b"" 