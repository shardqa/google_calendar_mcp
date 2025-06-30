from types import SimpleNamespace
from unittest.mock import patch
from src.mcp.tools import tool_calendar as tc


def _dummy_svc():
    return SimpleNamespace(name="svc")


def test_list_events_merge_with_ics(monkeypatch):
    # Google events returns list ['g1']
    monkeypatch.setattr(tc, "list_events", lambda svc, mr, cid: ["g1"])
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: _dummy_svc())

    # ICS list returns two URLs
    monkeypatch.setattr(
        "src.core.ics_registry.list_all",
        lambda: {"a": "u1", "b": "u2"},
    )

    class FakeOps:
        def list_events(self, url, mr):
            return [url[-1]]  # return last char so '1' or '2'

    with patch("src.core.ics_ops.ICSOperations", return_value=FakeOps()):
        res = tc.handle("list_events", {"with_ics": True})

    content = res["result"]["content"]
    # Expect google + two ics events
    assert sorted(content) == ["1", "2", "g1"]


def test_add_recurring_task(monkeypatch):
    def fake_add_recurring_event(**kwargs):
        return {"ok": True}

    monkeypatch.setattr(tc, "add_recurring_event", fake_add_recurring_event)
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: _dummy_svc())

    args = {
        "summary": "s",
        "frequency": "daily",
        "count": 3,
        "start_time": "s",
        "end_time": "e",
    }
    res = tc.handle("add_recurring_task", args)
    assert res["result"]["ok"] is True 