from datetime import datetime, timedelta
from typing import List, Dict

from src.core.calendar_ops import CalendarOperations


def _one_hour_after(iso_str: str) -> str:
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return (dt + timedelta(hours=1)).isoformat().replace('+00:00', 'Z')


def _event_exists(calendar_service, title: str) -> bool:
    events = calendar_service.events().list(calendarId='primary', q=title).execute()
    return bool(events.get('items', []))


def sync_tasks_with_calendar(calendar_service, tasks_service):
    """Create calendar events for tasks with due dates that have no matching event."""
    tasks_result = tasks_service.tasks().list(tasklist='@default', showCompleted=False).execute()
    if not isinstance(tasks_result, dict):
        return
    tasks: List[Dict] = tasks_result.get('items', [])

    ops = CalendarOperations(calendar_service)

    for task in tasks:
        due = task.get('due')
        if not due:
            continue
        title = task.get('title', 'Untitled Task')
        if _event_exists(calendar_service, title):
            continue
        event_data = {
            'summary': title,
            'start': {'dateTime': due},
            'end': {'dateTime': _one_hour_after(due)},
            'description': f"Auto-synced for task {task.get('id', '')}"
        }
        try:
            ops.add_event(event_data)
        except Exception:
            # Log or silently ignore; sync should not break
            pass 