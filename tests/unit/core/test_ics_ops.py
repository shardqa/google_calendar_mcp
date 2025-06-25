from src.core.ics_ops import ICSOperations
import textwrap

SAMPLE_ICS = textwrap.dedent("""
BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:Team Meeting
DTSTART:20250624T100000Z
DTEND:20250624T110000Z
LOCATION:Conference Room
DESCRIPTION:Weekly sync
END:VEVENT
BEGIN:VEVENT
SUMMARY:Lunch Break
DTSTART:20250624T120000Z
DTEND:20250624T123000Z
END:VEVENT
END:VCALENDAR
""")

def test_list_events_parses_events(monkeypatch):
    def fake_download(self, url):
        return SAMPLE_ICS

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics")
    assert len(events) == 2
    first = events[0]['text']
    assert 'Team Meeting' in first
    assert 'Conference Room' in first
    second = events[1]['text']
    assert 'Lunch Break' in second 

def test_max_results_and_branch_paths(monkeypatch):
    sample = SAMPLE_ICS + "\nNONCOLONLINE\n"  # line without colon to hit branch
    def fake_download(self, url):
        return sample
    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics", max_results=1)
    assert len(events) == 1 

def test_empty_event_branch(monkeypatch):
    sample = "BEGIN:VCALENDAR\nBEGIN:VEVENT\nEND:VEVENT\nEND:VCALENDAR"
    def fake_download(self, url):
        return sample
    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/empty.ics")
    # No events because the VEVENT had no data
    assert events == [] 

def test_timezone_param_parsing(monkeypatch):
    sample = """\nBEGIN:VCALENDAR\nBEGIN:VEVENT\nSUMMARY:Breakfast Meeting\nDTSTART;TZID=America/New_York:20250624T080000\nDTEND;TZID=America/New_York:20250624T090000\nEND:VEVENT\nEND:VCALENDAR\n"""

    def fake_download(self, url):
        return sample

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/tz.ics")
    assert len(events) == 1
    text = events[0]["text"]
    assert "No start time" not in text
    assert "2025-06-24T08:00:00" in text 