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
    # Should now return informative message instead of empty list
    assert len(events) == 1
    assert "No events found" in events[0]['text']

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

def test_current_day_events_are_included(monkeypatch):
    """Test that events happening today should be included even if they started earlier."""
    now = datetime.now(timezone.utc)
    # Event that started 2 hours ago but ends 1 hour from now (still ongoing)
    ongoing_start = (now - timedelta(hours=2)).strftime('%Y%m%dT%H%M%S')
    ongoing_end = (now + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
    
    # Event later today
    later_start = (now + timedelta(hours=3)).strftime('%Y%m%dT%H%M%S')
    later_end = (now + timedelta(hours=4)).strftime('%Y%m%dT%H%M%S')
    
    sample_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    BEGIN:VEVENT
    SUMMARY:Ongoing Meeting
    DTSTART:{ongoing_start}Z
    DTEND:{ongoing_end}Z
    LOCATION:Conference Room
    DESCRIPTION:Important meeting in progress
    END:VEVENT
    BEGIN:VEVENT
    SUMMARY:Later Today Meeting
    DTSTART:{later_start}Z
    DTEND:{later_end}Z
    LOCATION:Office
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return sample_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics")
    
    # Both events should be included - one ongoing, one later today
    assert len(events) >= 1, f"Expected at least 1 event, got {len(events)}. Events: {events}"
    
    # The ongoing meeting should be included because it's still happening today
    event_texts = [event['text'] for event in events]
    assert any("Ongoing Meeting" in text for text in event_texts), f"Ongoing meeting not found in {event_texts}"

def test_all_day_events_are_included(monkeypatch):
    """Test that all-day events (DATE format) are handled correctly."""
    today_date = datetime.now(timezone.utc).strftime('%Y%m%d')
    tomorrow_date = (datetime.now(timezone.utc) + timedelta(days=1)).strftime('%Y%m%d')
    
    sample_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    BEGIN:VEVENT
    SUMMARY:All Day Event Today
    DTSTART;VALUE=DATE:{today_date}
    DTEND;VALUE=DATE:{tomorrow_date}
    DESCRIPTION:Important all-day event
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return sample_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics")
    
    # All-day event should be included
    assert len(events) == 1
    assert "All Day Event Today" in events[0]['text']

def test_network_error_handling(monkeypatch):
    """Test that network errors are handled gracefully."""
    def fake_download_error(self, url):
        raise Exception("Network error")

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download_error)
    ops = ICSOperations()
    
    # Should now handle errors gracefully and return error message
    events = ops.list_events("http://example.com/calendar.ics")
    assert len(events) == 1
    assert "Failed to fetch ICS calendar" in events[0]['text']
    assert "Network error" in events[0]['text']

def test_empty_ics_calendar(monkeypatch):
    """Test behavior with completely empty ICS calendar."""
    def fake_download(self, url):
        return "BEGIN:VCALENDAR\nEND:VCALENDAR"

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/empty.ics")
    
    # Should return informative message instead of empty list
    assert len(events) == 1
    assert "No events found" in events[0]['text']

def test_malformed_ics_calendar(monkeypatch):
    """Test behavior with malformed ICS data."""
    def fake_download(self, url):
        return "INVALID ICS DATA\nNOT A CALENDAR"

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/malformed.ics")
    
    # Should return informative message instead of empty list
    assert len(events) == 1
    assert "No events found" in events[0]['text']

def test_debug_info_when_no_events_returned(monkeypatch):
    """Test that we can debug why no events are returned."""
    now = datetime.now(timezone.utc)
    # Create events that should be visible but might be filtered out
    today_event = (now + timedelta(hours=2)).strftime('%Y%m%dT%H%M%S')
    
    sample_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Test//Test//EN
    BEGIN:VEVENT
    UID:test@example.com
    SUMMARY:Today's Event
    DTSTART:{today_event}Z
    DTEND:{today_event}Z
    DESCRIPTION:This should be visible
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return sample_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/calendar.ics")
    
    # This event should definitely be returned
    assert len(events) == 1, f"Expected 1 event but got {len(events)}. Raw ICS: {sample_ics}"
    assert "Today's Event" in events[0]['text']

def test_real_world_ics_format_variations(monkeypatch):
    """Test various real-world ICS format variations that might cause issues."""
    now = datetime.now(timezone.utc)
    future_time = (now + timedelta(hours=2)).strftime('%Y%m%dT%H%M%S')
    
    # Test with various real-world ICS complications
    complex_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Google Inc//Google Calendar 70.9054//EN
    CALSCALE:GREGORIAN
    METHOD:PUBLISH
    X-WR-CALNAME:Test Calendar
    X-WR-TIMEZONE:America/New_York
    BEGIN:VTIMEZONE
    TZID:America/New_York
    X-LIC-LOCATION:America/New_York
    BEGIN:DAYLIGHT
    TZOFFSETFROM:-0500
    TZOFFSETTO:-0400
    TZNAME:EDT
    DTSTART:20070311T020000
    RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
    END:DAYLIGHT
    BEGIN:STANDARD
    TZOFFSETFROM:-0400
    TZOFFSETTO:-0500
    TZNAME:EST
    DTSTART:20071104T020000
    RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
    END:STANDARD
    END:VTIMEZONE
    BEGIN:VEVENT
    DTSTART;TZID=America/New_York:{future_time}
    DTEND;TZID=America/New_York:{future_time}
    RRULE:FREQ=WEEKLY;BYDAY=MO
    SUMMARY:Weekly Meeting
    DESCRIPTION:Important weekly sync meeting
    LOCATION:Conference Room A
    UID:weekly-meeting@example.com
    CREATED:20240101T120000Z
    LAST-MODIFIED:20240101T120000Z
    SEQUENCE:0
    STATUS:CONFIRMED
    TRANSP:OPAQUE
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return complex_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/complex.ics")
    
    # Should handle timezone and other complex fields
    assert len(events) == 1
    assert "Weekly Meeting" in events[0]['text']

def test_ics_operations_error_handling_and_debug_info(monkeypatch):
    """Test that ICS operations provide useful error information and don't fail silently."""
    
    # Test case 1: Network error should be handled gracefully
    def fake_download_network_error(self, url):
        raise ConnectionError("Failed to connect to ICS server")

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download_network_error)
    ops = ICSOperations()
    
    # Currently this will raise an exception, but it should return informative error
    try:
        events = ops.list_events("http://broken.example.com/calendar.ics")
        # If we get here, the implementation was improved to handle errors
        assert isinstance(events, list)
        # Should include error information for debugging
        if events:
            assert any("error" in str(event).lower() or "failed" in str(event).lower() for event in events)
    except Exception:
        # Current behavior - exception is raised
        # This is the failing test case that we need to fix
        assert False, "ICS operations should handle network errors gracefully and return debug info"

def test_ics_no_events_provides_debug_info(monkeypatch):
    """Test that when no events are returned, we get debug information about why."""
    
    # Calendar with no future events (all events are in the past)
    past_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y%m%dT%H%M%S')
    
    past_events_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Test//Test//EN
    BEGIN:VEVENT
    SUMMARY:Past Event 1
    DTSTART:{past_date}Z
    DTEND:{past_date}Z
    END:VEVENT
    BEGIN:VEVENT
    SUMMARY:Past Event 2
    DTSTART:{past_date}Z
    DTEND:{past_date}Z
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return past_events_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    events = ops.list_events("http://example.com/past-events.ics")
    
    # Currently returns empty list with no debug info
    # Should provide information about why no events were returned
    assert len(events) >= 1, "Should return debug information when no future events are found"
    
    # Should include debug information about filtered events
    if events:
        debug_text = str(events)
        assert any(word in debug_text.lower() for word in ["filtered", "past", "found", "debug", "info"])

def test_improved_list_events_with_debug_and_error_handling(monkeypatch):
    """Test that the improved list_events function provides better debugging and error handling."""
    
    # Test with realistic scenario: calendar with mix of past and future events
    now = datetime.now(timezone.utc)
    past_event = (now - timedelta(hours=3)).strftime('%Y%m%dT%H%M%S')
    future_event = (now + timedelta(hours=3)).strftime('%Y%m%dT%H%M%S')
    
    mixed_ics = textwrap.dedent(f"""
    BEGIN:VCALENDAR
    VERSION:2.0
    BEGIN:VEVENT
    SUMMARY:Already Happened
    DTSTART:{past_event}Z
    DTEND:{past_event}Z
    END:VEVENT
    BEGIN:VEVENT
    SUMMARY:Upcoming Event
    DTSTART:{future_event}Z
    DTEND:{future_event}Z
    END:VEVENT
    END:VCALENDAR
    """)

    def fake_download(self, url):
        return mixed_ics

    monkeypatch.setattr(ICSOperations, "_download_ics", fake_download)
    ops = ICSOperations()
    
    # Request with debug flag (new feature we'll implement)
    events = ops.list_events("http://example.com/mixed.ics", debug=True)
    
    # Should return future events plus debug information
    assert len(events) >= 1, "Should return future events and debug info"
    
    # Should include the future event
    event_texts = [event.get('text', '') for event in events]
    assert any("Upcoming Event" in text for text in event_texts), "Should include future events"
    
    # Debug info should mention filtered past events
    if len(events) > 1:  # If debug info is included
        debug_info = str(events)
        assert any(word in debug_info.lower() for word in ["filtered", "past", "found"])
    
    # Test case fails because current implementation doesn't support debug parameter
    # This is what we need to implement! 