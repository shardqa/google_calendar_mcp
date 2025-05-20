import json
import pytest
import time

# Assuming mod is imported elsewhere, e.g., from .. import mcp_post_sse_handler as mod
from src.mcp import mcp_post_sse_handler as mod # Adjust import if necessary
from unittest.mock import Mock

# Dummy handler class to capture SSE events
class DummyHandler:
    def __init__(self):
        self._status = None
        self._headers = {}
        self._response_data = b""
        self.wfile = self

    def send_response(self, status):
        self._status = status

    def send_header(self, key, value):
        self._headers[key] = value

    def end_headers(self):
        pass  # No-op for dummy

    def write(self, data):
        self._response_data += data

def parse_json(handler):
    # Assuming the last part written is the final JSON response
    # In a real SSE scenario, this would be more complex
    parts = handler._response_data.split(b'\r\n\r\n')
    if parts and parts[-1]:
        try:
            return json.loads(parts[-1].decode())
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from: {parts[-1]}")
            return None
    return None

def test_tools_call_list_events(monkeypatch):
    handler = DummyHandler()
    called = {}
    class Fake:
        def __init__(self, svc):
            called["service"] = svc
        def list_events(self, max_results=None):
            called["max_results"] = max_results
            return ["e"]
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    request = {"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"tool":"list_events","args":{"max_results":3}}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["result"] == {"content": ["e"]} # Update assertion to expect {"content": [...]}
    assert called["service"] == "svc"
    assert called["max_results"] == 3

def test_tools_call_add_event_missing():
    handler = DummyHandler()
    request = {"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"tool":"add_event","args":{"start_time":"s","end_time":"e"}}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["error"]["code"] == -32602

def test_tools_call_add_event_success(monkeypatch):
    handler = DummyHandler()
    called = {}
    class Fake:
        def __init__(self, svc):
            called["service"] = svc
        def add_event(self, data):
            called["data"] = data
            return {"ok":True}
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    args = {"summary":"t","start_time":"s","end_time":"e"}
    request = {"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"tool":"add_event","args":args}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert body["result"] == {"ok":True}
    assert "start" in called["data"] and "end" in called["data"] 