from datetime import datetime, timezone
from typing import List, Dict, Optional

class CalendarOperations:
    def __init__(self, service):
        self.service = service
        self._events = None

    def list_events(self, max_results: Optional[int] = None) -> List[Dict]:
        events_result = self.service.events().list(
            calendarId='primary',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])

    def add_event(self, event_data: Dict) -> Dict:
        try:
            event = self.service.events().insert(
                calendarId='primary',
                body=event_data
            ).execute()
            return {'status': 'confirmed', 'event': event}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def remove_event(self, event_id: str) -> bool:
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True
        except Exception:
            return False 