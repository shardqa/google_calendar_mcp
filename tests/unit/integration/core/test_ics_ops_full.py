import textwrap
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo
from unittest.mock import MagicMock

from src.core.ics_ops import ICSOperations


def test_ics_ops_parsing_and_normalize(monkeypatch):
    ics_text = textwrap.dedent("""
    BEGIN:VCALENDAR
    BEGIN:VEVENT
    DTSTART:20200101T120000Z
    DTEND:20200101T130000Z
    SUMMARY:Past Event
    LOCATION:Nowhere
    DESCRIPTION:Desc
    END:VEVENT
    BEGIN:VEVENT
    DTSTART:99999999
    DTEND:99999999
    SUMMARY:Bad Date Event
    END:VEVENT
    BEGIN:VEVENT
    SUMMARY:Undated Event
    END:VEVENT
    END:VCALENDAR
    """)

    # Monkeypatch download to supply inline text
    ops = ICSOperations()
    monkeypatch.setattr(ops, "_download_ics", lambda url: ics_text)

    events = ops.list_events("dummy", max_results=None)
    # Second event should still be included due to parsing fallback
    assert any("Bad Date Event" in e["text"] for e in events)

    # Exercise _extract_start_datetime on malformed text
    for ev in events:
        ops._extract_start_datetime(ev)

    # Directly test _format_event on custom data to hit normalization branches
    ev = ops._format_event({
        'SUMMARY': 'Sample',
        'DTSTART': '20250101T100000Z',
        'DTEND': '20250101T110000Z',
        'LOCATION': 'X',
        'DESCRIPTION': 'Y'
    })
    assert '📅 Start' in ev['text']


def test_normalize_date_failure(monkeypatch):
    ops = ICSOperations()
    # Test _format_event with a value that throws an exception
    # This covers the try/except block
    result = ops._format_event({'DTSTART': 'bad-date-format'})
    assert result['text'].startswith('No Summary')


def test_format_event_with_tz_aware_datetime(monkeypatch):
    """
    Test _format_event when DTSTART is already a timezone-aware datetime.
    This covers the branch where tzinfo is not None.
    """
    ops = ICSOperations()
    tz = ZoneInfo("America/New_York")
    dt_with_tz = datetime.now(tz)
    
    # Simulate the vDDDTypes object that has a .dt attribute
    # and a __str__ method that formats the date.
    mock_dt_start = MagicMock()
    mock_dt_start.dt = dt_with_tz
    mock_dt_start.__str__.return_value = dt_with_tz.strftime("%Y-%m-%d %H:%M:%S")

    # Pass a VEvent-like dictionary with the mocked datetime object
    event_data = {'DTSTART': mock_dt_start, 'SUMMARY': 'Test Event'}
    formatted_event = ops._format_event(event_data)
    
    # Check that the date in the text was correctly formatted
    assert dt_with_tz.strftime('%Y-%m-%d %H:%M') in formatted_event['text'] 