import io
import json
import pytest
from src.mcp import mcp_get_handler as handler_module

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


def test_sse_handler_exception_handling(monkeypatch):
    schema = {'protocol': '2025-03-26', 'tools': [{'name': 'tool1', 'inputSchema': {'x': 'y'}}]}
    monkeypatch.setattr(handler_module, 'get_mcp_schema', lambda: schema)
    
    class ExceptionWriter:
        def __init__(self):
            self.write_count = 0
            
        def write(self, data):
            self.write_count += 1
            if self.write_count > 6:  # Let initial writes succeed, then fail
                raise Exception('Write error')
            return len(data)
            
        def flush(self):
            pass
            
        def getvalue(self):
            return b''
    
    handler = DummyHandler('/sse')
    handler.wfile = ExceptionWriter()
    handler_id = id(handler)
    
    # Mock sleep to control loop execution  
    def fake_sleep(seconds):
        if seconds > 1:  # This is the heartbeat sleep
            raise Exception('Simulated write error')
    
    monkeypatch.setattr(handler_module.time, 'sleep', fake_sleep)
    
    # Run the handler - it should handle the exception gracefully
    handler_module.handle_get(handler)
    
    # Verify client was removed from connected_clients
    assert handler_id not in handler_module.connected_clients


def test_sse_handler_client_disconnect(monkeypatch):
    schema = {'protocol': '2025-03-26', 'tools': [{'name': 'tool1', 'inputSchema': {'x': 'y'}}]}
    monkeypatch.setattr(handler_module, 'get_mcp_schema', lambda: schema)
    
    handler = DummyHandler('/sse')
    handler_id = id(handler)
    
    # Mock sleep to simulate client disconnect
    sleep_count = 0
    def fake_sleep(seconds):
        nonlocal sleep_count
        sleep_count += 1
        if seconds > 1 and sleep_count > 1:  # Second heartbeat sleep
            handler_module.connected_clients.discard(handler_id)  # Simulate disconnect
    
    monkeypatch.setattr(handler_module.time, 'sleep', fake_sleep)
    
    handler_module.handle_get(handler)
    
    # Verify client was properly removed
    assert handler_id not in handler_module.connected_clients 