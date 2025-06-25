from src.mcp import tool_calendar as tc
import importlib
import types

def test_list_events_merges_ics(monkeypatch):
    # Stub calendar service
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: "svc")

    class FakeCalOps:
        def __init__(self, svc):
            pass
        def list_events(self, max_results=None, calendar_id="primary"):
            return ["g1"]

    monkeypatch.setattr(tc, "_cal_ops", lambda: types.SimpleNamespace(CalendarOperations=FakeCalOps))

    # Stub ICS registry
    registry = importlib.import_module("src.core.ics_registry")
    monkeypatch.setattr(registry, "list_all", lambda: {"work": "http://example.com/work.ics"})

    # Stub ICS operations
    ics_mod = importlib.import_module("src.core.ics_ops")
    class FakeICS:
        def list_events(self, url, max_results):
            assert url == "http://example.com/work.ics"
            return ["i1"]
    monkeypatch.setattr(ics_mod, "ICSOperations", lambda: FakeICS())

    res = tc._list_events({"with_ics": True})
    assert res["result"]["content"] == ["g1", "i1"] 