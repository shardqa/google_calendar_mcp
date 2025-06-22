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

class TestSchedulingEngineFinalCoverage:
    
    def test_should_handle_event_starting_before_work_hours(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'early_event',
                    'summary': 'Early Meeting',
                    'start': {'dateTime': '2024-03-21T07:00:00Z'},
                    'end': {'dateTime': '2024-03-21T08:00:00Z'}
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
        
    def test_should_handle_work_start_not_less_than_event_start(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'same_time_event',
                    'summary': 'Same Time Meeting',
                    'start': {'dateTime': '2024-03-21T08:00:00Z'},
                    'end': {'dateTime': '2024-03-21T09:00:00Z'}
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

    def test_should_handle_event_starting_exactly_at_work_hours(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'exact_time_event',
                    'summary': 'Exact Start Meeting',
                    'start': {'dateTime': '2024-03-21T09:00:00Z'},
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

    def test_should_handle_event_with_missing_datetime(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {
            'items': [
                {
                    'id': 'no_datetime_event',
                    'summary': 'Event without datetime',
                    'start': {}
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

    def test_calculate_gaps_direct_false_branch(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        events = [
            {
                'id': 'test_event',
                'summary': 'Test Event',
                'start': {'dateTime': '2024-03-21T08:00:00Z'},
                'end': {'dateTime': '2024-03-21T09:00:00Z'}
            }
        ]
        
        result = engine._calculate_gaps_between_events(events, "09:00", "18:00")
        
        assert result == [] 

    def test_should_handle_different_max_task_duration_values(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [{'id': '1', 'title': 'Task 1'}]
        }
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        available_slot = [{
            'start_time': '2024-03-21T09:00:00Z',
            'end_time': '2024-03-21T11:00:00Z',
            'duration_minutes': 120
        }]
        engine._find_available_slots = Mock(return_value=available_slot)
        
        result_small = engine.propose_schedule("day", "09:00", "18:00", max_task_duration=30)
        assert len(result_small['proposed_events']) == 1
        
        result_large = engine.propose_schedule("day", "09:00", "18:00", max_task_duration=180)
        assert len(result_large['proposed_events']) == 1

    def test_should_handle_events_starting_before_work_hours(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        events_before_work = [
            {'start': {'dateTime': '2024-03-21T08:00:00Z'}}
        ]
        
        result = engine._calculate_gaps_between_events(events_before_work, "09:00", "18:00")
        assert len(result) == 0

    def test_should_handle_events_starting_at_work_hours(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        events_at_work_start = [
            {'start': {'dateTime': '2024-03-21T09:00:00Z'}}
        ]
        
        result = engine._calculate_gaps_between_events(events_at_work_start, "09:00", "18:00")
        assert len(result) == 0

    def test_should_handle_short_gaps_filtering(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        events_with_short_gap = [
            {'start': {'dateTime': '2024-03-21T09:20:00Z'}}
        ]
        
        result = engine._calculate_gaps_between_events(events_with_short_gap, "09:00", "18:00")
        assert len(result) == 0

    def test_should_process_multiple_events_in_loop(self, mock_calendar_service, mock_tasks_service):
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        multiple_events = [
            {'start': {'dateTime': '2024-03-21T10:00:00Z'}},
            {'start': {'dateTime': '2024-03-21T14:00:00Z'}},
            {'start': {'dateTime': '2024-03-21T16:00:00Z'}}
        ]
        
        result = engine._calculate_gaps_between_events(multiple_events, "09:00", "18:00")
        
        assert len(result) == 1
        assert result[0]['start_time'] == '2024-03-21T09:00:00Z'
        assert result[0]['end_time'] == '2024-03-21T10:00:00Z'

    def test_should_handle_events_with_missing_datetime_field(self, mock_calendar_service, mock_tasks_service):
        """Test the case where event.start.dateTime is None or missing"""
        from src.core.scheduling_engine import SchedulingEngine
        
        engine = SchedulingEngine(mock_calendar_service, mock_tasks_service)
        
        # Event with completely missing start.dateTime field
        events_missing_datetime = [
            {'start': {}}  # No dateTime field at all
        ]
        
        result = engine._calculate_gaps_between_events(events_missing_datetime, "09:00", "18:00")
        assert len(result) == 0  # Should return empty since event_start is None
        
        # Event with None dateTime
        events_none_datetime = [
            {'start': {'dateTime': None}}  # Explicit None
        ]
        
        result_none = engine._calculate_gaps_between_events(events_none_datetime, "09:00", "18:00")
        assert len(result_none) == 0  # Should return empty since event_start is None 