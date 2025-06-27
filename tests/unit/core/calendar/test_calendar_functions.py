import pytest
from unittest.mock import MagicMock, patch
from src.core.calendar import (
    add_event,
    list_events,
    remove_event,
    edit_event,
    list_calendars,
    add_recurring_event,
    ensure_timezone,
)

@pytest.fixture
def mock_service():
    return MagicMock()

def test_list_events(mock_service):
    mock_service.events().list().execute.return_value = {'items': [{'summary': 'Test Event'}]}
    events = list_events(mock_service)
    assert len(events) == 1
    assert "Test Event" in events[0]['text']

def test_add_event(mock_service):
    mock_service.events().insert().execute.return_value = {'summary': 'New Event'}
    event_data = {'summary': 'New Event', 'start': {'dateTime': '2025-01-01T10:00:00'}, 'end': {'dateTime': '2025-01-01T11:00:00'}}
    result = add_event(mock_service, event_data)
    assert result['status'] == 'confirmed'
    mock_service.events().insert.assert_called()

def test_remove_event(mock_service):
    result = remove_event(mock_service, "event_id")
    assert result is True
    mock_service.events().delete.assert_called_with(calendarId='primary', eventId='event_id')

def test_remove_event_exception(mock_service):
    mock_service.events().delete.side_effect = Exception("API Error")
    result = remove_event(mock_service, "event_id")
    assert result is False

def test_edit_event(mock_service):
    mock_service.events().get().execute.return_value = {'summary': 'Old Event'}
    mock_service.events().patch().execute.return_value = {'summary': 'Updated Event'}
    result = edit_event(mock_service, "event_id", {'summary': 'Updated Event'})
    assert result['summary'] == 'Updated Event'
    mock_service.events().patch.assert_called()

def test_edit_event_with_start_time(mock_service):
    mock_service.events().get().execute.return_value = {
        'summary': 'Old Event',
        'start': {'dateTime': '2025-01-01T10:00:00'}
    }
    mock_service.events().patch().execute.return_value = {'summary': 'Updated Event'}
    
    updated_details = {
        'summary': 'Updated Event',
        'start': {'dateTime': '2025-01-01T11:00:00'}
    }
    result = edit_event(mock_service, "event_id", updated_details)
    assert result['summary'] == 'Updated Event'

def test_edit_event_with_end_time(mock_service):
    mock_service.events().get().execute.return_value = {
        'summary': 'Old Event',
        'end': {'dateTime': '2025-01-01T12:00:00'}
    }
    mock_service.events().patch().execute.return_value = {'summary': 'Updated Event'}
    
    updated_details = {
        'summary': 'Updated Event',
        'end': {'dateTime': '2025-01-01T13:00:00'}
    }
    result = edit_event(mock_service, "event_id", updated_details)
    assert result['summary'] == 'Updated Event'

def test_edit_event_with_timezone_missing(mock_service):
    mock_service.events().get().execute.return_value = {
        'summary': 'Old Event',
        'start': {'dateTime': '2025-01-01T10:00:00'},
        'end': {'dateTime': '2025-01-01T12:00:00'}
    }
    mock_service.events().patch().execute.return_value = {'summary': 'Updated Event'}
    
    updated_details = {
        'start': {'dateTime': '2025-01-01T11:00:00'},
        'end': {'dateTime': '2025-01-01T13:00:00'}
    }
    result = edit_event(mock_service, "event_id", updated_details)
    assert result['summary'] == 'Updated Event'

def test_edit_event_exception(mock_service):
    mock_service.events().get.side_effect = Exception("API Error")
    result = edit_event(mock_service, "event_id", {'summary': 'Updated Event'})
    assert result is None

def test_list_calendars(mock_service):
    mock_service.calendarList().list().execute.return_value = {'items': [{'summary': 'Test Calendar'}]}
    calendars = list_calendars(mock_service)
    assert len(calendars) == 1
    assert 'Test Calendar' in calendars[0]['text']

def test_add_recurring_event(mock_service):
    mock_service.events().insert().execute.return_value = {'summary': 'Recurring Event'}
    result = add_recurring_event(
        mock_service, 'Recurring Event', 'daily', 5, '2025-01-01T10:00:00', '2025-01-01T11:00:00'
    )
    assert result['status'] == 'confirmed'
    mock_service.events().insert.assert_called()

def test_ensure_timezone():
    assert ensure_timezone("2025-01-01T10:00:00Z") == "2025-01-01T10:00:00Z"
    assert ensure_timezone("2025-01-01T10:00:00+01:00") == "2025-01-01T10:00:00+01:00"
    assert ensure_timezone("2025-01-01T10:00:00") == "2025-01-01T10:00:00-03:00" 