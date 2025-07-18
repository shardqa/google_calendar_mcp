from src.mcp import tool_calendar as tc
import importlib
from unittest.mock import patch


def test_list_events_with_ics_exception(monkeypatch):
    # Mock the Google Calendar list_events function to return ["g"]
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: "svc")
    
    # Mock the calendar.list_events function to return ["g"]
    monkeypatch.setattr("src.mcp.tools.tool_calendar.list_events", lambda svc, mr, cid: ["g"])
    
    # Make registry throw an exception when listing ICS calendars
    registry = importlib.import_module("src.core.ics_registry")
    monkeypatch.setattr(registry, "list_all", lambda: (_ for _ in ()).throw(RuntimeError("boom")))

    res = tc._list_events({"with_ics": True})
    assert res["result"]["content"] == ["g"] 