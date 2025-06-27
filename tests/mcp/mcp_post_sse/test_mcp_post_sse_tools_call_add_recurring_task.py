import json
from unittest.mock import Mock
from src.mcp import mcp_post_sse_handler as mod

class DummyHandler:
    def __init__(self):
        self.response_data = []
        self.wfile = self
        
    def send_response(self, code):
        self.response_code = code
        
    def send_header(self, name, value):
        pass
        
    def end_headers(self):
        pass
        
    def write(self, data):
        self.response_data.append(data)

def parse_response(handler):
    if handler.response_data:
        return json.loads(handler.response_data[-1].decode())
    return {}

def test_add_recurring_task_success(monkeypatch):
    """Test successful add_recurring_task via SSE handler."""
    mock_service = Mock()
    mock_recurring_result = {
        'status': 'confirmed',
        'event': {'id': 'recurring_123', 'summary': 'Daily Medicine'}
    }
    mock_add_recurring_event = Mock(return_value=mock_recurring_result)
    
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)
    monkeypatch.setattr(mod.calendar, 'add_recurring_event', mock_add_recurring_event)
    
    handler = DummyHandler()
    request = {
        "method": "tools/call",
        "params": {
            "tool": "add_recurring_task",
            "args": {
                "summary": "Take Medicine",
                "frequency": "daily",
                "count": 30,
                "start_time": "2024-03-20T08:00:00Z",
                "end_time": "2024-03-20T08:30:00Z",
                "location": "Home",
                "description": "Daily medication reminder"
            }
        }
    }
    response = {"id": 1}
    
    mod.handle_post_sse(handler, request, response)
    
    response_data = parse_response(handler)
    assert "result" in response_data
    assert response_data["result"]["status"] == "confirmed"
    mock_add_recurring_event.assert_called_once_with(
        mock_service,
        summary="Take Medicine",
        frequency="daily", 
        count=30,
        start_time="2024-03-20T08:00:00Z",
        end_time="2024-03-20T08:30:00Z",
        location="Home",
        description="Daily medication reminder"
    )

def test_add_recurring_task_missing_params(monkeypatch):
    """Test add_recurring_task with missing required parameters."""
    mock_service = Mock()
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)
    
    handler = DummyHandler()
    request = {
        "method": "tools/call",
        "params": {
            "tool": "add_recurring_task",
            "args": {
                "summary": "Take Medicine"
                # Missing required parameters: frequency, count, start_time, end_time
            }
        }
    }
    response = {"id": 1}
    
    mod.handle_post_sse(handler, request, response)
    
    response_data = parse_response(handler)
    assert "error" in response_data
    assert response_data["error"]["code"] == -32602
    assert "Missing required recurring task parameters" in response_data["error"]["message"]

def test_add_recurring_task_minimal_params(monkeypatch):
    """Test add_recurring_task with only required parameters."""
    mock_service = Mock()
    mock_recurring_result = {
        'status': 'confirmed',
        'event': {'id': 'recurring_456', 'summary': 'Weekly Task'}
    }
    mock_add_recurring_event = Mock(return_value=mock_recurring_result)
    
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)
    monkeypatch.setattr(mod.calendar, 'add_recurring_event', mock_add_recurring_event)
    
    handler = DummyHandler()
    request = {
        "method": "tools/call",
        "params": {
            "tool": "add_recurring_task",
            "args": {
                "summary": "Weekly Meeting",
                "frequency": "weekly",
                "count": 10,
                "start_time": "2024-03-20T14:00:00Z",
                "end_time": "2024-03-20T15:00:00Z"
                # No location or description
            }
        }
    }
    response = {"id": 1}
    
    mod.handle_post_sse(handler, request, response)
    
    response_data = parse_response(handler)
    assert "result" in response_data
    assert response_data["result"]["status"] == "confirmed"
    mock_add_recurring_event.assert_called_once_with(
        mock_service,
        summary="Weekly Meeting",
        frequency="weekly",
        count=10,
        start_time="2024-03-20T14:00:00Z",
        end_time="2024-03-20T15:00:00Z",
        location=None,
        description=None
    ) 