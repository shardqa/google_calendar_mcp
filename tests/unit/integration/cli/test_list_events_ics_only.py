from src.mcp import tool_calendar as tc
import importlib, types


def _setup_fake_ics(monkeypatch, expected_url):
    ics_mod = importlib.import_module("src.core.ics_ops")
    class FakeICS:
        def list_events(self, url, max_results):
            assert url == expected_url
            return ["ics_event"]
    monkeypatch.setattr(ics_mod, "ICSOperations", lambda: FakeICS())


def test_list_events_direct_url(monkeypatch):
    _setup_fake_ics(monkeypatch, "http://example.com/a.ics")
    res = tc._list_events({"ics_url": "http://example.com/a.ics"})
    assert res["result"]["content"] == ["ics_event"]


def test_list_events_alias(monkeypatch):
    registry = importlib.import_module("src.core.ics_registry")
    monkeypatch.setattr(registry, "get", lambda alias: "http://example.com/b.ics")
    _setup_fake_ics(monkeypatch, "http://example.com/b.ics")
    res = tc._list_events({"ics_alias": "work"})
    assert res["result"]["content"] == ["ics_event"] 