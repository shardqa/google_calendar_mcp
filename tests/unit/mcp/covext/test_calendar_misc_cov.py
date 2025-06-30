import sys
from src.core.calendar import add_recurring_event, list_events
from src.mcp.tools import tool_calendar


class Svc:
    class _Events:
        def insert(self, calendarId, body):
            self.body = body
            return self

        def list(self, *a, **k):
            class L:
                def execute(self):
                    return {"items": [{"id": "1", "summary": "M", "start": {"dateTime": "2025-01-01T10:00:00Z"}, "end": {"dateTime": "2025-01-01T11:00:00Z"}, "location": "Loc", "description": "Desc"}]}
            return L()

        def execute(self):
            return {"id": "e", **self.body}

    def events(self):
        return self._Events()


def test_add_recurring_event():
    assert add_recurring_event(Svc(), "X", "daily", 1, "2025-01-01T09:00:00", "2025-01-01T10:00:00")["status"] == "confirmed"
    assert add_recurring_event(Svc(), "X", "yearly", 1, "2025-01-01T09:00:00", "2025-01-01T10:00:00")["status"] == "error"


def test_list_events():
    txt = list_events(Svc(), 1)[0]["text"]
    assert "📍" in txt and "📝" in txt


def test_tool_calendar(monkeypatch):
    from src.core import ics_ops, ics_registry, auth as core_auth

    class Ops:
        def list_events(self, url, max_results):
            return [{"type": "text", "text": url}]

    monkeypatch.setattr(ics_ops, "ICSOperations", Ops)
    monkeypatch.setattr(ics_registry, "get", lambda a: "http://x")
    monkeypatch.setattr(ics_registry, "list_all", lambda: {"a": "http://a", "b": "http://b"})
    monkeypatch.setattr(core_auth, "get_calendar_service", lambda: Svc())
    from src.core.calendar import list_events as _le
    monkeypatch.setattr(sys.modules[_le.__module__], "list_events", lambda *a, **k: [])
    assert tool_calendar.handle("list_events", {"ics_alias": "z"})["result"]["content"][0]["text"] == "http://x"
    assert len(tool_calendar.handle("list_events", {"with_ics": True})["result"]["content"]) >= 2 