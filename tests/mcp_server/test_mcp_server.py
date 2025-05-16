import threading
import time
import pytest
from src.mcp_server import CalendarMCPServer, run_server
import src.mcp_server as mcp_server_module

class DummySocket:
    def setsockopt(self, *args):
        pass

class DummyServer:
    def __init__(self, server_address, RequestHandlerClass):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass
        self.socket = DummySocket()
        self.shutdown_requested = False
        self.serve_forever_called = False
    def serve_forever(self):
        self.serve_forever_called = True
        try:
            while not self.shutdown_requested:
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
    def shutdown(self):
        self.shutdown_requested = True

@pytest.fixture(autouse=True)
def patch_http_server(monkeypatch):
    monkeypatch.setattr(mcp_server_module, 'ThreadingHTTPServer', DummyServer)

def test_init_binding(capsys):
    server = CalendarMCPServer()
    captured = capsys.readouterr()
    assert 'Binding to all interfaces (0.0.0.0) on port 3000' in captured.out
    assert server.server.server_address == ('0.0.0.0', 3000)

def test_custom_host_no_binding(capsys):
    server = CalendarMCPServer(host='example.com', port=1234)
    captured = capsys.readouterr()
    assert 'Binding to all interfaces' not in captured.out
    assert server.server.server_address == ('example.com', 1234)

def test_start_and_stop(capsys):
    server = CalendarMCPServer(host='0.0.0.0', port=5000)
    capsys.readouterr()
    server.start()
    time.sleep(0.05)
    captured = capsys.readouterr()
    assert 'Calendar MCP Server running at http://localhost:5000/' in captured.out
    assert 'SSE endpoint available at http://localhost:5000/sse' in captured.out
    assert server.running
    assert isinstance(server.server_thread, threading.Thread)
    assert server.server.serve_forever_called
    server.stop()
    captured = capsys.readouterr()
    assert 'Calendar MCP Server stopped' in captured.out
    assert not server.running

def test_run_server(monkeypatch, capsys):
    def fake_sleep(x):
        raise KeyboardInterrupt
    monkeypatch.setattr(mcp_server_module.time, 'sleep', fake_sleep)
    run_server(host='0.0.0.0', port=8000)
    captured = capsys.readouterr()
    assert 'Calendar MCP Server running at http://localhost:8000/' in captured.out
    assert 'Calendar MCP Server stopped' in captured.out 