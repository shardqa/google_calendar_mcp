import pytest
from unittest.mock import MagicMock, patch
from src.core.calendar import (
    add_event,
    list_events,
    remove_event,
    edit_event,
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

def test_list_events_with_location_and_description(mock_service):
    mock_service.events().list().execute.return_value = {
        'items': [{
            'id': 'event123',
            'summary': 'Meeting with Team',
            'start': {'dateTime': '2025-01-01T10:00:00Z'},
            'end': {'dateTime': '2025-01-01T11:00:00Z'},
            'location': 'Conference Room A',
            'description': 'Quarterly planning meeting'
        }]
    }
    events = list_events(mock_service)
    assert len(events) == 1
    event_text = events[0]['text']
    assert "Meeting with Team" in event_text
    assert "📍 Location: Conference Room A" in event_text
    assert "📝 Description: Quarterly planning meeting" in event_text

def test_add_event(mock_service):
    mock_service.events().insert().execute.return_value = {'summary': 'New Event'}
    event_data = {'summary': 'New Event', 'start': {'dateTime': '2025-01-01T10:00:00'}, 'end': {'dateTime': '2025-01-01T11:00:00'}}
    result = add_event(mock_service, event_data)
    assert result['status'] == 'confirmed'
    mock_service.events().insert.assert_called()

def test_add_event_exception(mock_service):
    mock_service.events().insert().execute.side_effect = Exception("API Error")
    event_data = {'summary': 'Failed Event', 'start': {'dateTime': '2025-01-01T10:00:00'}, 'end': {'dateTime': '2025-01-01T11:00:00'}}
    result = add_event(mock_service, event_data)
    assert result['status'] == 'error'
    assert result['message'] == 'API Error'

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

def test_ensure_timezone():
    assert ensure_timezone("2025-01-01T10:00:00Z") == "2025-01-01T10:00:00Z"
    assert ensure_timezone("2025-01-01T10:00:00+01:00") == "2025-01-01T10:00:00+01:00"
    assert ensure_timezone("2025-01-01T10:00:00") == "2025-01-01T10:00:00-03:00" 