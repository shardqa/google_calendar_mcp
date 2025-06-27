from typing import Dict, Optional
from .utils import ensure_timezone

def edit_event(service, event_id: str, updated_details: Dict) -> Optional[Dict]:
    try:
        event = service.events().get(
            calendarId="primary", 
            eventId=event_id
        ).execute()

        for key, value in updated_details.items():
            event[key] = value

        if 'start' in updated_details and 'dateTime' in updated_details['start']:
            event['start']['dateTime'] = ensure_timezone(
                updated_details['start']['dateTime']
            )
            if 'timeZone' not in event['start']:
                event['start']['timeZone'] = 'America/Sao_Paulo'
        
        if 'end' in updated_details and 'dateTime' in updated_details['end']:
            event['end']['dateTime'] = ensure_timezone(
                updated_details['end']['dateTime']
            )
            if 'timeZone' not in event['end']:
                event['end']['timeZone'] = 'America/Sao_Paulo'

        updated_event = service.events().patch(
            calendarId="primary",
            eventId=event_id,
            body=event
        ).execute()

        return updated_event
    except Exception as e:
        print(f"Error editing event {event_id}: {str(e)}")
        return None 