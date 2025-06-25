from unittest.mock import MagicMock

import pytest

from src.core.scheduling_engine import SchedulingEngine


@pytest.fixture
def mock_calendar_service():
    return MagicMock()


@pytest.fixture
def mock_tasks_service():
    return MagicMock()


def test_auto_block_creation_for_high_priority(mock_calendar_service, mock_tasks_service):
    # No existing events so full day slot available
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {
        'items': []
    }
    # One high-priority task ([3])
    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [
            {
                'id': 'hp1',
                'title': '[3] Important feature',
                'due': '2024-03-22T10:00:00Z'
            }
        ]
    }

    engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
    engine.propose_schedule(time_period="day", work_hours_start="08:00", work_hours_end="18:00")

    # Verify that a calendar event insert was triggered
    assert mock_calendar_service.events.return_value.insert.called, "High-priority task did not trigger event creation"


def test_auto_block_creation_handles_insert_error(mock_calendar_service, mock_tasks_service):
    mock_calendar_service.events.return_value.list.return_value.execute.return_value = {'items': []}
    mock_calendar_service.events.return_value.insert.return_value.execute.side_effect = Exception("API Error")

    mock_tasks_service.tasks.return_value.list.return_value.execute.return_value = {
        'items': [{'id': 'hp2', 'title': '[3] Critical', 'due': '2024-03-22T11:00:00Z'}]
    }

    engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
    engine.propose_schedule(time_period="day", work_hours_start="08:00", work_hours_end="18:00")

    # Even with exception, code should continue without raising
    assert mock_calendar_service.events.return_value.insert.called 