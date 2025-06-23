from datetime import datetime, timedelta
from typing import List, Dict

from src.core.task_ordering import order_tasks, _parse_importance


def _add_minutes_to_time(time_str: str, minutes: int) -> str:
    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    return (dt + timedelta(minutes=minutes)).isoformat().replace('+00:00', 'Z')


def create_task_events(calendar_service, available_slots: List[Dict], tasks: List[Dict], max_duration: int) -> List[Dict]:
    proposed_events: List[Dict] = []
    ordered_tasks = order_tasks(tasks)

    for slot, task in zip(available_slots, ordered_tasks):
        task_duration = min(60, max_duration)
        if slot['duration_minutes'] < task_duration:
            continue

        event_payload = {
            'summary': f"Work on: {task.get('title', 'Untitled Task')}",
            'start': {'dateTime': slot['start_time']},
            'end': {'dateTime': _add_minutes_to_time(slot['start_time'], task_duration)},
            'description': f"Scheduled task: {task.get('title', '')}"
        }

        proposed_events.append(event_payload)

        # Auto-create calendar event for high-priority tasks
        if _parse_importance(task.get('title', '')) == 3:
            try:
                calendar_service.events().insert(
                    calendarId='primary',
                    body=event_payload
                ).execute()
            except Exception:
                # Falha não é crítica para a geração de proposta
                pass

    return proposed_events


def calculate_duration(start: str, end: str) -> int:
    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
    return int((end_dt - start_dt).total_seconds() / 60)


def calculate_gaps_between_events(events: List[Dict], start_hour: str, end_hour: str) -> List[Dict]:
    slots: List[Dict] = []
    for i, event in enumerate(events):
        if i == 0:
            work_start = f"2024-03-21T{start_hour}:00Z"
            event_start = event.get('start', {}).get('dateTime')
            if event_start and work_start < event_start:
                duration = calculate_duration(work_start, event_start)
                if duration >= 30:
                    slots.append({
                        'start_time': work_start,
                        'end_time': event_start,
                        'duration_minutes': duration
                    })

    return slots 