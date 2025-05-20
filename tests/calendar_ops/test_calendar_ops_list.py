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
    assert events[0]['text'] == 'Test Event'
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