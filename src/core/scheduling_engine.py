from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re


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
            duration = self._calculate_duration(start_time, end_time)
            
            return [{
                'start_time': start_time,
                'end_time': end_time,
                'duration_minutes': duration
            }]
        
        return self._calculate_gaps_between_events(events, start_hour, end_hour)
    
    def _calculate_duration(self, start: str, end: str) -> int:
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
        return int((end_dt - start_dt).total_seconds() / 60)
    
    def _calculate_gaps_between_events(self, events: List[Dict], 
                                     start_hour: str, end_hour: str) -> List[Dict]:
        slots = []
        for i, event in enumerate(events):
            if i == 0:
                work_start = f"2024-03-21T{start_hour}:00Z"
                event_start = event.get('start', {}).get('dateTime')
                if event_start and work_start < event_start:
                    duration = self._calculate_duration(work_start, event_start)
                    if duration >= 30:
                        slots.append({
                            'start_time': work_start,
                            'end_time': event_start,
                            'duration_minutes': duration
                        })
        
        return slots
    
    def _create_task_events(self, available_slots: List[Dict], 
                          tasks: List[Dict], max_duration: int) -> List[Dict]:
        proposed_events = []
        
        for task in tasks:
            if available_slots:
                slot = available_slots[0]
                task_duration = min(60, max_duration)
                
                if slot['duration_minutes'] >= task_duration:
                    proposed_events.append({
                        'summary': f"Work on: {task.get('title', 'Untitled Task')}",
                        'start': {'dateTime': slot['start_time']},
                        'end': {'dateTime': self._add_minutes_to_time(slot['start_time'], task_duration)},
                        'description': f"Scheduled task: {task.get('title', '')}"
                    })
        
        return proposed_events
    
    def _add_minutes_to_time(self, time_str: str, minutes: int) -> str:
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        new_dt = dt + timedelta(minutes=minutes)
        return new_dt.isoformat().replace('+00:00', 'Z') 