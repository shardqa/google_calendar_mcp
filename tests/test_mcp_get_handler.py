import io
import json
import pytest
from src import mcp_get_handler as handler_module

class DummyHandler:
    def __init__(self, path):
        self.path = path
        self.wfile = io.BytesIO()
        self.headers_sent = []
        self.status_code = None

    def send_response(self, code):
        self.status_code = code

    def send_header(self, k, v):
        self.headers_sent.append((k, v))

    def end_headers(self):
        pass

def test_sse_handler(monkeypatch):
    schema = {'protocol': '2025-03-26', 'tools': [{'name': 'tool1', 'inputSchema': {'x': 'y'}}]}
    monkeypatch.setattr(handler_module, 'get_mcp_schema', lambda: schema)
    handler = DummyHandler('/sse')
    handler_id = id(handler)
    def fake_sleep(seconds):
        if seconds > 1:
            handler_module.connected_clients.discard(handler_id)
    monkeypatch.setattr(handler_module.time, 'sleep', fake_sleep)
    handler_module.handle_get(handler)
    data = handler.wfile.getvalue().decode('utf-8')
    assert 'event: mcp/hello' in data
    assert '"method": "mcp/hello"' in data
    assert 'event: tools/list' in data
    assert '"method": "tools/list"' in data
    assert ":\n\n" in data

def test_schema_handler(monkeypatch):
    schema = {'a': 1}
    monkeypatch.setattr(handler_module, 'get_mcp_schema', lambda: schema)
    handler = DummyHandler('/schema')
    handler_module.handle_get(handler)
    assert handler.status_code == 200
    assert ('Content-Type', 'application/json') in handler.headers_sent
    assert handler.wfile.getvalue() == json.dumps(schema).encode()

def test_root_handler(monkeypatch):
    schema = {'b': 2}
    monkeypatch.setattr(handler_module, 'get_mcp_schema', lambda: schema)
    handler = DummyHandler('/')
    handler_module.handle_get(handler)
    assert handler.status_code == 200
    assert ('Content-Type', 'application/json') in handler.headers_sent
    assert handler.wfile.getvalue() == json.dumps(schema).encode()

def test_not_found_handler():
    handler = DummyHandler('/other')
    handler_module.handle_get(handler)
    assert handler.status_code == 404
    assert handler.wfile.getvalue() == b'' 