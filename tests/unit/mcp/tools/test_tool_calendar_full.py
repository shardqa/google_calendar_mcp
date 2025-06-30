import pytest
from types import SimpleNamespace
from unittest.mock import patch
from src.mcp.tools import tool_calendar as tc


def make_dummy_service():
    return SimpleNamespace(name="svc")


def test_list_events_google(monkeypatch):
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: make_dummy_service())
    monkeypatch.setattr(tc, "list_events", lambda svc, mr, cid: ["g"])
    res = tc.handle("list_events", {})
    assert res["result"]["content"] == ["g"]


def test_list_events_ics(monkeypatch):
    class FakeOps:
        def list_events(self, url, mr):
            assert url == "http://x.com/ics.ics"
            assert mr == 7
            return ["i"]
    monkeypatch.setattr(tc, "auth", SimpleNamespace(get_calendar_service=lambda: make_dummy_service()))
    with patch("src.core.ics_ops.ICSOperations", return_value=FakeOps()):
        res = tc.handle("list_events", {"ics_url": "http://x.com/ics.ics", "max_results": 7})
    assert res["result"]["content"] == ["i"]


def test_add_event_success(monkeypatch):
    def fake_add(service, body):
        return {"status": "confirmed", "event": {"id": "1", "summary": "t", "start": {"dateTime": "s"}, "end": {"dateTime": "e"}}}
    monkeypatch.setattr(tc, "add_event", fake_add)
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: make_dummy_service())
    res = tc.handle("add_event", {"summary": "t", "start_time": "s", "end_time": "e"})
    txt = res["result"]["content"][0]["text"]
    assert "✅ Evento criado" in txt


def test_add_event_error(monkeypatch):
    def fake_add(service, body):
        return {"status": "error", "message": "fail"}
    monkeypatch.setattr(tc, "add_event", fake_add)
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: make_dummy_service())
    res = tc.handle("add_event", {"summary": "t", "start_time": "s", "end_time": "e"})
    txt = res["result"]["content"][0]["text"]
    assert "❌" in txt


def test_remove_event(monkeypatch):
    monkeypatch.setattr(tc, "remove_event", lambda svc, eid: True)
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: make_dummy_service())
    res = tc.handle("remove_event", {"event_id": "abc"})
    assert "✅" in res["result"]["content"][0]["text"]


def test_edit_event(monkeypatch):
    def fake_edit(svc, eid, det):
        return {"id": eid, "summary": "x"}
    monkeypatch.setattr(tc, "edit_event", fake_edit)
    monkeypatch.setattr(tc.auth, "get_calendar_service", lambda: make_dummy_service())
    res = tc.handle("edit_event", {"event_id": "abc", "updated_details": {"summary": "x"}})
    txt = res["result"]["content"][0]["text"]
    assert "✅" in txt 