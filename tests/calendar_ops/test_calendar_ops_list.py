import pytest
from unittest.mock import Mock
from src.core.calendar_ops import CalendarOperations

@pytest.fixture
def mock_service():
    return Mock()

@pytest.fixture
def calendar_ops(mock_service):
    return CalendarOperations(mock_service)

def test_list_events_empty(calendar_ops, mock_service):
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = {}
    events = calendar_ops.list_events()
    assert events == []
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once()

def test_list_events_no_results(calendar_ops, mock_service):
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = {'items': []}
    events = calendar_ops.list_events()
    assert isinstance(events, list)
    assert len(events) == 0

def test_list_events_with_results(calendar_ops, mock_service):
    mock_events = {
        'items': [
            {
                'id': '1',
                'summary': 'Test Event',
                'start': {'dateTime': '2024-03-20T10:00:00Z'},
                'end': {'dateTime': '2024-03-20T11:00:00Z'}
            }
        ]
    }
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = mock_events
    events = calendar_ops.list_events(max_results=5)
    assert len(events) == 1
    assert events[0]['type'] == 'text'
    assert 'Test Event' in events[0]['text']
    assert '2024-03-20T10:00:00Z' in events[0]['text']
    assert '2024-03-20T11:00:00Z' in events[0]['text']
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once()

def test_add_event(calendar_ops, mock_service):
    mock_event_data = {
        'summary': 'New Event',
        'start': {'dateTime': '2024-03-21T10:00:00Z'},
        'end': {'dateTime': '2024-03-21T11:00:00Z'},
    }
    mock_response = {'status': 'confirmed', 'event': mock_event_data}
    insert_mock = mock_service.events.return_value.insert.return_value
    insert_mock.execute.return_value = mock_response
    response = calendar_ops.add_event(mock_event_data)
    assert response == {'status': 'confirmed', 'event': mock_response}
    mock_service.events().insert.assert_called_once_with(
        calendarId='primary',
        body=mock_event_data
    )

def test_add_event_error(calendar_ops, mock_service):
    insert_mock = mock_service.events.return_value.insert.return_value
    insert_mock.execute.side_effect = Exception('Insert failed')
    mock_event_data = {'summary': 'Failing Event'}
    response = calendar_ops.add_event(mock_event_data)
    assert response['status'] == 'error'
    assert 'Insert failed' in response['message']

def test_remove_event_success(calendar_ops, mock_service):
    delete_mock = mock_service.events.return_value.delete.return_value
    delete_mock.execute.return_value = None
    result = calendar_ops.remove_event('event_id_123')
    assert result is True
    mock_service.events().delete.assert_called_once_with(
        calendarId='primary',
        eventId='event_id_123'
    )

def test_remove_event_failure(calendar_ops, mock_service):
    delete_mock = mock_service.events.return_value.delete.return_value
    delete_mock.execute.side_effect = Exception('Delete failed')
    result = calendar_ops.remove_event('event_id_456')
    assert result is False
    mock_service.events().delete.assert_called_once_with(
        calendarId='primary',
        eventId='event_id_456'
    )

def test_list_events_with_detailed_info(calendar_ops, mock_service):
    """Test that list_events returns detailed event information including date/time, location, and description."""
    mock_events = {
        'items': [
            {
                'id': 'event_1',
                'summary': 'Meeting with Team',
                'start': {'dateTime': '2024-03-20T10:00:00Z'},
                'end': {'dateTime': '2024-03-20T11:00:00Z'},
                'location': 'Conference Room A',
                'description': 'Weekly team meeting to discuss project progress'
            },
            {
                'id': 'event_2', 
                'summary': 'Doctor Appointment',
                'start': {'dateTime': '2024-03-20T14:30:00Z'},
                'end': {'dateTime': '2024-03-20T15:00:00Z'},
                'location': 'Medical Center'
            },
            {
                'id': 'event_3',
                'summary': 'Lunch with Client', 
                'start': {'dateTime': '2024-03-21T12:00:00Z'},
                'end': {'dateTime': '2024-03-21T13:30:00Z'}
            }
        ]
    }
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = mock_events
    
    events = calendar_ops.list_events(max_results=10)
    
    assert len(events) == 3
    
    # First event with all details
    first_event = events[0]
    assert first_event['type'] == 'text'
    assert 'Meeting with Team' in first_event['text']
    assert '2024-03-20T10:00:00Z' in first_event['text']
    assert '2024-03-20T11:00:00Z' in first_event['text']
    assert 'Conference Room A' in first_event['text']
    assert 'Weekly team meeting to discuss project progress' in first_event['text']
    
    # Second event with location but no description
    second_event = events[1]
    assert 'Doctor Appointment' in second_event['text']
    assert '2024-03-20T14:30:00Z' in second_event['text']
    assert 'Medical Center' in second_event['text']
    
    # Third event with minimal details
    third_event = events[2]
    assert 'Lunch with Client' in third_event['text']
    assert '2024-03-21T12:00:00Z' in third_event['text']

def test_list_events_other_calendar(calendar_ops, mock_service):
    mock_events = {'items': []}
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = mock_events
    calendar_ops.list_events(calendar_id='globalsys')
    events_mock.list.assert_called_once()
    kwargs = events_mock.list.call_args.kwargs
    assert kwargs['calendarId'] == 'globalsys' 