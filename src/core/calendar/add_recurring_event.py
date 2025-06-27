from typing import Dict, Optional
from .utils import ensure_timezone

def add_recurring_event(service, summary: str, frequency: str, count: int, 
                      start_time: str, end_time: str, 
                      location: Optional[str] = None, 
                      description: Optional[str] = None) -> Dict:
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
            'start': {
                'dateTime': ensure_timezone(start_time),
                'timeZone': 'America/Sao_Paulo'
            },
            'end': {
                'dateTime': ensure_timezone(end_time),
                'timeZone': 'America/Sao_Paulo'
            },
            'recurrence': [rrule]
        }
        
        if location:
            event_data['location'] = location
        if description:
            event_data['description'] = description
        
        event = service.events().insert(
            calendarId='primary',
            body=event_data
        ).execute()
        
        return {'status': 'confirmed', 'event': event, **event}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)} 