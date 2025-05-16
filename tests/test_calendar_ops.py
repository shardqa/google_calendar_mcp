import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from src.calendar_ops import CalendarOperations

@pytest.fixture
def mock_service():
    service = Mock()
    # Pre-configure events to be called only once per test
    service.events.return_value = Mock()
    return service

@pytest.fixture
def calendar_ops(mock_service):
    return CalendarOperations(mock_service)

def test_list_events_empty(calendar_ops, mock_service):
    # Arrange
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = {}

    # Act
    events = calendar_ops.list_events()

    # Assert
    assert events == []
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once()

def test_list_events_with_results(calendar_ops, mock_service):
    # Arrange
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

    # Act
    events = calendar_ops.list_events(max_results=5)

    # Assert
    assert len(events) == 1
    assert events[0]['summary'] == 'Test Event'
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once()

def test_add_event_success(calendar_ops, mock_service):
    # Arrange
    event_data = {
        'summary': 'Test Event',
        'start': {'dateTime': '2024-03-20T10:00:00Z'},
        'end': {'dateTime': '2024-03-20T11:00:00Z'}
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.return_value = event_data

    # Act
    result = calendar_ops.add_event(event_data)

    # Assert
    assert result['status'] == 'confirmed'
    assert result['event'] == event_data
    mock_service.events.assert_called_once()
    events_mock.insert.assert_called_once()
    events_mock.insert.return_value.execute.assert_called_once()

def test_add_event_failure(calendar_ops, mock_service):
    # Arrange
    event_data = {
        'summary': 'Test Event',
        'start': {'dateTime': 'invalid-date'},
        'end': {'dateTime': 'invalid-date'}
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.side_effect = Exception("Invalid date format")

    # Act
    result = calendar_ops.add_event(event_data)

    # Assert
    assert result['status'] == 'error'
    assert 'message' in result
    mock_service.events.assert_called_once()
    events_mock.insert.assert_called_once()
    events_mock.insert.return_value.execute.assert_called_once()

def test_remove_event_success(calendar_ops, mock_service):
    # Arrange
    event_id = 'test-event-id'
    events_mock = mock_service.events.return_value
    events_mock.delete.return_value.execute.return_value = None

    # Act
    result = calendar_ops.remove_event(event_id)

    # Assert
    assert result is True
    mock_service.events.assert_called_once()
    events_mock.delete.assert_called_once()
    events_mock.delete.return_value.execute.assert_called_once()

def test_remove_event_failure(calendar_ops, mock_service):
    # Arrange
    event_id = 'test-event-id'
    events_mock = mock_service.events.return_value
    events_mock.delete.return_value.execute.side_effect = Exception("Event not found")

    # Act
    result = calendar_ops.remove_event(event_id)

    # Assert
    assert result is False
    mock_service.events.assert_called_once()
    events_mock.delete.assert_called_once()
    events_mock.delete.return_value.execute.assert_called_once() 