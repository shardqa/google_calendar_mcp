import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

@pytest.fixture
def mock_calendar_service():
    service = Mock()
    return service

@pytest.fixture
def mock_tasks_service():
    service = Mock()
    return service

class TestSchedulingEngine:
    def test_should_exist_scheduling_engine_class(self):
        from src.core.scheduling_engine import SchedulingEngine
        assert SchedulingEngine is not None

    def test_should_initialize_with_services(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        assert engine.calendar_service == mock_calendar_service
        assert engine.tasks_service == mock_tasks_service

    def test_should_analyze_schedule_for_empty_calendar_and_tasks(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'available_slots' in result
        assert 'tasks_to_schedule' in result
        assert len(result['tasks_to_schedule']) == 0

    def test_should_identify_full_day_slot_when_no_events(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="day",
            work_hours_start="09:00", 
            work_hours_end="18:00"
        )
        
        assert len(result['available_slots']) >= 1
        assert result['available_slots'][0]['duration_minutes'] >= 540

    def test_should_suggest_time_blocks_for_pending_tasks(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [
                {'id': '1', 'title': 'Task 1', 'due': '2024-03-21T18:00:00Z'},
                {'id': '2', 'title': 'Task 2', 'notes': 'Important task'}
            ]
        }
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.propose_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'proposed_events' in result
        assert 'scheduling_summary' in result
        assert len(result['proposed_events']) > 0 