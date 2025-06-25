from src.mcp import tool_calendar as tc
import importlib, types


def test_list_events_with_ics_exception(monkeypatch):
    # Stub calendar ops
    class FakeCalOps:
        def __init__(self, svc):
            pass
        def list_events(self, max_results=None, calendar_id="primary"):
            return ["g"]
    monkeypatch.setattr(tc, "_cal_ops", lambda: types.SimpleNamespace(CalendarOperations=FakeCalOps))
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: "svc")

    # Make registry throw
    registry = importlib.import_module("src.core.ics_registry")
    monkeypatch.setattr(registry, "list_all", lambda: (_ for _ in ()).throw(RuntimeError("boom")))

    res = tc._list_events({"with_ics": True})
    assert res["result"]["content"] == ["g"] 