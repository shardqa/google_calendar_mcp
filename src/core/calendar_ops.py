from datetime import datetime, timezone
from typing import List, Dict, Optional

class CalendarOperations:
    def __init__(self, service):
        self.service = service
        self._events = None

    def list_events(self, max_results: Optional[int] = None) -> List[Dict]:
        now = datetime.now(timezone.utc).isoformat()
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        formatted_events = []
        for event in events:
            summary = event.get('summary', 'No Summary')
            start_time = event.get('start', {}).get('dateTime', 'No start time')
            end_time = event.get('end', {}).get('dateTime', 'No end time')
            location = event.get('location', '')
            description = event.get('description', '')
            
            event_text = f"{summary}\n📅 Start: {start_time}\n📅 End: {end_time}"
            
            if location:
                event_text += f"\n📍 Location: {location}"
            
            if description:
                event_text += f"\n📝 Description: {description}"
            
            formatted_events.append({"type": "text", "text": event_text})
        return formatted_events

    def _ensure_timezone(self, datetime_str: str) -> str:
        """Ensure datetime string has timezone information."""
        if datetime_str.endswith('Z') or '+' in datetime_str[-6:] or '-' in datetime_str[-6:]:
            return datetime_str
        
        if '.' in datetime_str:
            return f"{datetime_str}+00:00"
        else:
            return f"{datetime_str}.000+00:00"

    def add_event(self, event_data: Dict) -> Dict:
        try:
            processed_event_data = event_data.copy()
            
            if 'start' in processed_event_data and 'dateTime' in processed_event_data['start']:
                processed_event_data['start']['dateTime'] = self._ensure_timezone(
                    processed_event_data['start']['dateTime']
                )
            
            if 'end' in processed_event_data and 'dateTime' in processed_event_data['end']:
                processed_event_data['end']['dateTime'] = self._ensure_timezone(
                    processed_event_data['end']['dateTime']
                )
            
            event = self.service.events().insert(
                calendarId='primary',
                body=processed_event_data
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

    def add_recurring_event(self, summary: str, frequency: str, count: int, 
                          start_time: str, end_time: str, 
                          location: Optional[str] = None, 
                          description: Optional[str] = None) -> Dict:
        """Create a recurring event in Google Calendar.
        
        Args:
            summary: Title of the event
            frequency: Recurrence frequency ('daily', 'weekly', 'monthly')
            count: Number of occurrences
            start_time: Start time in ISO format
            end_time: End time in ISO format
            location: Optional location
            description: Optional description
            
        Returns:
            Dict containing the created event data
        """
        try:
            frequency_map = {
                'daily': 'DAILY',
                'weekly': 'WEEKLY', 
                'monthly': 'MONTHLY'
            }
            
            if frequency not in frequency_map:
                raise ValueError(f"Unsupported frequency: {frequency}")
            
            rrule = f"RRULE:FREQ={frequency_map[frequency]};COUNT={count}"
            
            event_data = {
                'summary': summary,
                'start': {'dateTime': self._ensure_timezone(start_time)},
                'end': {'dateTime': self._ensure_timezone(end_time)},
                'recurrence': [rrule]
            }
            
            if location:
                event_data['location'] = location
            if description:
                event_data['description'] = description
            
            event = self.service.events().insert(
                calendarId='primary',
                body=event_data
            ).execute()
            
            return {'status': 'confirmed', 'event': event, **event}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)} 