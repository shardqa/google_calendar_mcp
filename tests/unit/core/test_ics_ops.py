from src.core.ics_ops import ICSOperations
import textwrap
from datetime import datetime, timezone, timedelta

# Use current and future dates for testing
today = datetime.now(timezone.utc)
tomorrow = today + timedelta(days=1)
today_str = today.strftime('%Y%m%dT%H%M%S')
tomorrow_str = tomorrow.strftime('%Y%m%dT%H%M%S')

SAMPLE_ICS = textwrap.dedent(f"""
BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:Team Meeting
DTSTART:{today_str}Z
DTEND:{today_str}Z
LOCATION:Conference Room
DESCRIPTION:Weekly sync
END:VEVENT
BEGIN:VEVENT
SUMMARY:Lunch Break
DTSTART:{tomorrow_str}Z
DTEND:{tomorrow_str}Z
END:VEVENT
END:VCALENDAR
""")

# Sample with past dates for filtering test
SAMPLE_ICS_WITH_PAST = textwrap.dedent(f"""
BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:Past Meeting
DTSTART:{(today - timedelta(days=3)).strftime('%Y%m%dT%H%M%S')}Z
DTEND:{(today - timedelta(days=3)).strftime('%Y%m%dT%H%M%S')}Z
END:VEVENT
BEGIN:VEVENT
SUMMARY:Future Meeting
DTSTART:{(today + timedelta(days=3)).strftime('%Y%m%dT%H%M%S')}Z
DTEND:{(today + timedelta(days=3)).strftime('%Y%m%dT%H%M%S')}Z
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
    # Use today's date for timezone test
    today_tz = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    sample = f"""\nBEGIN:VCALENDAR\nBEGIN:VEVENT\nSUMMARY:Breakfast Meeting\nDTSTART;TZID=America/New_York:{today_tz}\nDTEND;TZID=America/New_York:{today_tz}\nEND:VEVENT\nEND:VCALENDAR\n"""

    def fake_download(self, url):
        return sample

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/tz.ics")
    assert len(events) == 1
    text = events[0]["text"]
    assert "No start time" not in text

def test_date_filtering_excludes_past_events(monkeypatch):
    """Test that past events are filtered out while future events are included."""
    def fake_download(self, url):
        return SAMPLE_ICS_WITH_PAST

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics")
    
    # Should only include the future event (June 27), not the past one (June 24)
    assert len(events) == 1
    assert "Future Meeting" in events[0]['text']
    assert "Past Meeting" not in str(events) 