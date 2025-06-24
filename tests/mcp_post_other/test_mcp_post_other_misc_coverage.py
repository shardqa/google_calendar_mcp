import json, sys
from unittest.mock import patch, MagicMock

import src.mcp.mcp_post_other_handler as mod

class Dummy:
    def __init__(self):
        self._data = b""
        self.wfile = self
    def send_response(self, *_):
        pass
    def send_header(self, *_):
        pass
    def end_headers(self):
        pass
    def write(self, d):
        self._data += d

def parsed(handler):
    return json.loads(handler._data or b"{}")

def test_unknown_tool_error():
    h = Dummy()
    req = {"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"tool":"nonexistent","args":{}}}
    mod.handle_post_other(h, req, {"jsonrpc":"2.0","id":1})
    body = parsed(h)
    assert body["error"]["code"] == -32601

@patch("src.mcp.mcp_post_other_handler.calendar_ops.CalendarOperations")
@patch("src.mcp.mcp_post_other_handler.auth.get_calendar_service")
def test_add_recurring_task_success(mock_get_service, mock_cal_ops):
    mock_get_service.return_value = "svc"
    mock_inst = MagicMock()
    mock_inst.add_recurring_event.return_value = {"status":"confirmed"}
    mock_cal_ops.return_value = mock_inst
    h = Dummy()
    args = {
        "summary":"Daily standup",
        "frequency":"daily",
        "count":5,
        "start_time":"2024-04-01T09:00:00",
        "end_time":"2024-04-01T09:15:00"
    }
    req = {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"tool":"add_recurring_task","args":args}}
    mod.handle_post_other(h, req, {"jsonrpc":"2.0","id":2})
    body = parsed(h)
    assert body.get("result") == {"status":"confirmed"} 