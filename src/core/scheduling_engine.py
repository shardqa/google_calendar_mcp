from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.core.time_block_creator import calculate_duration, calculate_gaps_between_events


class SchedulingEngine:
    def __init__(self, calendar_service, tasks_service):
        self.calendar_service = calendar_service
        self.tasks_service = tasks_service
    
    def analyze_schedule(self, time_period: str, work_hours_start: str, 
                        work_hours_end: str) -> Dict:
        calendar_events = self._get_calendar_events(time_period)
        pending_tasks = self._get_pending_tasks()
        available_slots = self._find_available_slots(
            calendar_events, work_hours_start, work_hours_end, time_period
        )
        
        return {
            'available_slots': available_slots,
            'tasks_to_schedule': pending_tasks,
            'calendar_events': calendar_events
        }
    
    def propose_schedule(self, time_period: str, work_hours_start: str,
                        work_hours_end: str, max_task_duration: int = 120) -> Dict:
        analysis = self.analyze_schedule(time_period, work_hours_start, work_hours_end)
        proposed_events = self._create_task_events(
            analysis['available_slots'], 
            analysis['tasks_to_schedule'],
            max_task_duration
        )
        
        return {
            'proposed_events': proposed_events,
            'scheduling_summary': {
                'total_tasks': len(analysis['tasks_to_schedule']),
                'scheduled_tasks': len(proposed_events),
                'available_slots': len(analysis['available_slots'])
            }
        }
    
    def _get_calendar_events(self, time_period: str) -> List[Dict]:
        now = datetime.now()
        if time_period == "day":
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=1)).isoformat() + 'Z'
        elif time_period == "week":
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=7)).isoformat() + 'Z'
        else:
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=30)).isoformat() + 'Z'
        
        events_result = self.calendar_service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    
    def _get_pending_tasks(self) -> List[Dict]:
        tasks_result = self.tasks_service.tasks().list(
            tasklist='@default',
            showCompleted=False
        ).execute()
        
        return tasks_result.get('items', [])
    
    def _find_available_slots(self, events: List[Dict], start_hour: str, 
                             end_hour: str, time_period: str) -> List[Dict]:
        if not events:
            start_time = f"2024-03-21T{start_hour}:00Z"
            end_time = f"2024-03-21T{end_hour}:00Z"
            duration = calculate_duration(start_time, end_time)
            
            return [{
                'start_time': start_time,
                'end_time': end_time,
                'duration_minutes': duration
            }]
        
        return calculate_gaps_between_events(events, start_hour, end_hour)
    
    def _create_task_events(self, available_slots: List[Dict], 
                          tasks: List[Dict], max_duration: int) -> List[Dict]:
        from src.core.time_block_creator import create_task_events
        return create_task_events(
            self.calendar_service, available_slots, tasks, max_duration
        )

    # Thin wrappers kept for backward compatibility with existing tests
    def _calculate_gaps_between_events(self, events: List[Dict], start_hour: str, end_hour: str) -> List[Dict]:
        return calculate_gaps_between_events(events, start_hour, end_hour)

    def _calculate_duration(self, start: str, end: str) -> int:
        return calculate_duration(start, end) 