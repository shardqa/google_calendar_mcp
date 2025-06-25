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

class TestSchedulingEngineEdgeCases:
    
    def test_should_handle_week_time_period(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="week",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'available_slots' in result
        assert len(result['available_slots']) >= 1

    def test_should_handle_month_time_period(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="month",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'available_slots' in result
        assert len(result['available_slots']) >= 1

    def test_should_calculate_gaps_between_events(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'event1',
                    'summary': 'Meeting',
                    'start': {'dateTime': '2024-03-21T10:00:00Z'},
                    'end': {'dateTime': '2024-03-21T11:00:00Z'}
                }
            ]
        }
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'available_slots' in result
        slots = result['available_slots']
        if slots:
            assert slots[0]['start_time'] == '2024-03-21T09:00:00Z'
            assert slots[0]['end_time'] == '2024-03-21T10:00:00Z'
            assert slots[0]['duration_minutes'] == 60

    def test_should_handle_short_gaps_less_than_30_minutes(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'event1',
                    'summary': 'Meeting',
                    'start': {'dateTime': '2024-03-21T09:15:00Z'},
                    'end': {'dateTime': '2024-03-21T10:00:00Z'}
                }
            ]
        }
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        result = engine.analyze_schedule(
            time_period="day", 
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert 'available_slots' in result
        slots = result['available_slots']
        assert len(slots) == 0

    def test_should_handle_tasks_with_no_available_slots(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [
                {'id': '1', 'title': 'Task 1'},
                {'id': '2', 'title': 'Task 2'}
            ]
        }
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        engine._find_available_slots = Mock(return_value=[])
        
        result = engine.propose_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00"
        )
        
        assert result['proposed_events'] == []
        assert result['scheduling_summary']['scheduled_tasks'] == 0

    def test_should_handle_slot_smaller_than_task_duration(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [{'id': '1', 'title': 'Task 1'}]
        }
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        small_slot = [{
            'start_time': '2024-03-21T09:00:00Z',
            'end_time': '2024-03-21T09:30:00Z',
            'duration_minutes': 30
        }]
        engine._find_available_slots = Mock(return_value=small_slot)
        
        result = engine.propose_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00",
            max_task_duration=120
        )
        
        assert len(result['proposed_events']) == 0

    def test_should_respect_max_task_duration_larger_than_60(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [{'id': '1', 'title': 'Long Task'}]
        }
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        large_slot = [{
            'start_time': '2024-03-21T09:00:00Z',
            'end_time': '2024-03-21T11:00:00Z',
            'duration_minutes': 120
        }]
        engine._find_available_slots = Mock(return_value=large_slot)
        
        result = engine.propose_schedule(
            time_period="day",
            work_hours_start="09:00",
            work_hours_end="18:00",
            max_task_duration=90
        )
        
        assert len(result['proposed_events']) == 1
        proposed = result['proposed_events'][0]
        start_time = proposed['start']['dateTime']
        end_time = proposed['end']['dateTime']
        
        assert start_time == '2024-03-21T09:00:00Z'
        assert end_time == '2024-03-21T10:00:00Z' 