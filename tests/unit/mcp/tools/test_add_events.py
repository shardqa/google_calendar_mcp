import pytest
from src.mcp.tools.tool_calendar import handle

def test_add_events_basic():
    args = {
        "events": [
            {
                "summary": "Test Event 1",
                "start_time": "2025-01-01T10:00:00",
                "end_time": "2025-01-01T11:00:00"
            }
        ]
    }
    result = handle("add_events", args)
    assert result is not None
    assert "result" in result
    assert "content" in result["result"]
    assert "1 eventos criados com sucesso, 0 falharam" in result["result"]["content"][0]["text"]  # Expected summary format

def test_add_events_multiple():
    args = {
        "events": [
            {
                "summary": "Test Event 1",
                "start_time": "2025-01-01T10:00:00",
                "end_time": "2025-01-01T11:00:00"
            },
            {
                "summary": "Test Event 2",
                "start_time": "2025-01-01T12:00:00",
                "end_time": "2025-01-01T13:00:00"
            }
        ]
    }
    result = handle("add_events", args)
    assert result is not None
    assert "result" in result
    assert "content" in result["result"]
    assert "2 eventos criados com sucesso, 0 falharam" in result["result"]["content"][0]["text"]

def test_add_events_with_failure():
    args = {
        "events": [
            {
                "summary": "Valid Event",
                "start_time": "2025-01-01T10:00:00",
                "end_time": "2025-01-01T11:00:00"
            },
            {
                "summary": "Invalid Event",  # Missing required fields for failure simulation
                "start_time": "invalid_time"
            }
        ]
    }
    result = handle("add_events", args)
    assert result is not None
    assert "result" in result
    assert "content" in result["result"]
    assert "1 eventos criados com sucesso, 1 falharam" in result["result"]["content"][0]["text"]
