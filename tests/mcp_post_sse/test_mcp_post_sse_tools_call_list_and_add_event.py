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

def test_tools_call_add_event_missing(monkeypatch):
    # Mock the calendar service to prevent file access
    mock_service = Mock()
    mock_service.events.return_value.insert.return_value.execute.return_value = {'status': 'confirmed', 'event': {'id': 'mocked_event_id'}}
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)

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
            return {'status': 'confirmed', 'event': {'summary': 'Test Event', 'start': {'dateTime': '2024-01-01T10:00:00'}, 'end': {'dateTime': '2024-01-01T11:00:00'}}}
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    args = {"summary":"t","start_time":"s","end_time":"e"}
    request = {"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"tool":"add_event","args":args}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    assert "✅ Evento criado com sucesso!" in body["result"]["content"][0]["text"]
    assert "start" in called["data"] and "end" in called["data"]

def test_tools_call_add_event_with_location_coverage(monkeypatch):
    """Test to cover line 77 - if location: condition in SSE handler"""
    handler = DummyHandler()
    called = {}
    class Fake:
        def __init__(self, svc):
            called["service"] = svc
        def add_event(self, data):
            called["data"] = data
            return {'status': 'confirmed', 'event': {'summary': 'Test Event', 'start': {'dateTime': '2024-01-01T10:00:00'}, 'end': {'dateTime': '2024-01-01T11:00:00'}, 'location': 'Test Location'}}
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    args = {"summary":"Test Event","start_time":"2024-01-01T10:00:00","end_time":"2024-01-01T11:00:00","location":"Test Location"}
    request = {"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"tool":"add_event","args":args}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    result_text = body["result"]["content"][0]["text"]
    assert "✅ Evento criado com sucesso!" in result_text
    assert "📍 Test Location" in result_text

def test_tools_call_add_event_error_coverage(monkeypatch):
    """Test to cover line 81 - else: condition when add_event fails in SSE handler"""
    handler = DummyHandler()
    called = {}
    class Fake:
        def __init__(self, svc):
            called["service"] = svc
        def add_event(self, data):
            called["data"] = data
            return {'status': 'error', 'message': 'Test error from SSE'}
    monkeypatch.setattr(mod.auth, "get_calendar_service", lambda: "svc")
    monkeypatch.setattr(mod.calendar_ops, "CalendarOperations", Fake)
    args = {"summary":"Test Event","start_time":"2024-01-01T10:00:00","end_time":"2024-01-01T11:00:00"}
    request = {"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"tool":"add_event","args":args}}
    response = {}
    mod.handle_post_sse(handler, request, response)
    body = parse_json(handler)
    result_text = body["result"]["content"][0]["text"]
    assert "❌ Erro ao criar evento: Test error from SSE" in result_text 