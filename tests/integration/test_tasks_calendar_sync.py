from unittest.mock import MagicMock, patch

import pytest

from src.core.tasks_calendar_sync import sync_tasks_with_calendar


@pytest.fixture
def mock_calendar_service():
    return MagicMock()


@pytest.fixture
def mock_tasks_service():
    return MagicMock()


def _make_task(task_id, title, due=None):
    t = {'id': task_id, 'title': title}
    if due:
        t['due'] = due
    return t


def test_creates_event_when_not_exists(mock_calendar_service, mock_tasks_service):
    due = '2024-03-23T10:00:00Z'
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [_make_task('t1', 'Finish report', due)]
    }
    # events().list should return empty to simulate non-existent event
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {
        'items': []
    }
    sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)
    assert mock_calendar_service.events.return_value.insert.called, 'Event not created'


def test_skip_if_event_already_exists(mock_calendar_service, mock_tasks_service):
    due = '2024-03-23T10:00:00Z'
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [_make_task('t2', 'Finish report', due)]
    }
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {
        'items': [{'summary': 'Finish report'}]
    }
    sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)
    assert not mock_calendar_service.events.return_value.insert.called


def test_handles_insert_error_gracefully(mock_calendar_service, mock_tasks_service):
    due = '2024-03-23T10:00:00Z'
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [_make_task('t3', 'Important', due)]
    }
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {
        'items': []
    }
    mock_calendar_service.events.return_value.insert.return_value.execute.side_effect = Exception('API error')
    # Should not raise
    sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)


def test_tasks_result_not_dict(mock_calendar_service, mock_tasks_service):
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = []  # not dict
    sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)
    # Should not attempt to insert events
    assert not mock_calendar_service.events.return_value.insert.called


def test_add_event_exception_handled(mock_calendar_service, mock_tasks_service):
    due = '2024-03-23T10:00:00Z'
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [_make_task('t4', 'Faulty', due)]
    }
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {'items': []}

    class FakeOps:
        def __init__(self, svc):
            pass
        def add_event(self, data):
            raise Exception('fail')
    with patch('src.core.tasks_calendar_sync.CalendarOperations', FakeOps):
        # Should not raise despite exception inside add_event
        sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)


def test_skip_tasks_without_due(mock_calendar_service, mock_tasks_service):
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [_make_task('t5', 'No due')]
    }
    sync_tasks_with_calendar(mock_calendar_service, mock_tasks_service)
    assert not mock_calendar_service.events.return_value.insert.called 