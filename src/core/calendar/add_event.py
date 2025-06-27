from typing import Dict
from .utils import ensure_timezone

def add_event(service, event_data: Dict) -> Dict:
    try:
        processed_event_data = event_data.copy()
        
        if 'start' in processed_event_data and 'dateTime' in processed_event_data['start']:
            processed_event_data['start']['dateTime'] = ensure_timezone(
                processed_event_data['start']['dateTime']
            )
            if 'timeZone' not in processed_event_data['start']:
                processed_event_data['start']['timeZone'] = 'America/Sao_Paulo'
        
        if 'end' in processed_event_data and 'dateTime' in processed_event_data['end']:
            processed_event_data['end']['dateTime'] = ensure_timezone(
                processed_event_data['end']['dateTime']
            )
            if 'timeZone' not in processed_event_data['end']:
                processed_event_data['end']['timeZone'] = 'America/Sao_Paulo'
        
        event = service.events().insert(
            calendarId='primary',
            body=processed_event_data
        ).execute()
        return {'status': 'confirmed', 'event': event}
    except Exception as e:
        return {'status': 'error', 'message': str(e)} 