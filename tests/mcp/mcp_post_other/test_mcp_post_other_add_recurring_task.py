import json
from unittest.mock import Mock
from src.mcp import mcp_post_other_handler as mod

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

def test_add_recurring_task_missing_params(monkeypatch):
    """Test add_recurring_task with missing required parameters."""
    mock_service = Mock()
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: mock_service)
    
    handler = DummyHandler()
    request = {
        "jsonrpc": "2.0", 
        "id": 8, 
        "method": "tools/call", 
        "params": {
            "tool": "add_recurring_task", 
            "args": {
                "summary": "Tomar remédio",
                "frequency": "daily"
                # Missing count, start_time, end_time
            }
        }
    }
    response = {"jsonrpc": "2.0", "id": 8}
    
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    
    assert body.get("error", {}).get("code") == -32602
    assert "Missing required recurring task parameters" in body.get("error", {}).get("message", "")

def test_add_recurring_task_success(monkeypatch):
    """Test successful add_recurring_task call."""
    handler = DummyHandler()
    called = {}
    
    def fake_add_recurring_event(service, **kwargs):
        called['service'] = service
        called['kwargs'] = kwargs
        return {
            'status': 'confirmed',
            'event': {
                'id': 'recurring_event_123',
                'summary': kwargs['summary']
            }
        }
    
    monkeypatch.setattr(mod.auth, 'get_calendar_service', lambda: 'mock_service')
    monkeypatch.setattr(mod, 'add_recurring_event', fake_add_recurring_event)
    
    request = {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "tool": "add_recurring_task",
            "args": {
                "summary": "Tomar remédio",
                "frequency": "daily",
                "count": 30,
                "start_time": "2024-03-20T08:00:00Z",
                "end_time": "2024-03-20T08:30:00Z",
                "location": "Casa",
                "description": "Remédio para pressão"
            }
        }
    }
    response = {"jsonrpc": "2.0", "id": 9}
    
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    
    # Verify successful response
    assert body['result']['content'].get("status") == "confirmed"
    assert "recurring_event_123" in str(body['result']['content'])
    
    # Verify method was called with correct parameters
    assert called['service'] == 'mock_service'
    assert called['kwargs']['summary'] == "Tomar remédio"
    assert called['kwargs']['frequency'] == "daily"
    assert called['kwargs']['count'] == 30
    assert called['kwargs']['location'] == "Casa"
    assert called['kwargs']['description'] == "Remédio para pressão" 