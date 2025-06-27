from typing import List, Dict, Optional
from datetime import datetime, timezone

def list_events(service, max_results: Optional[int] = None, calendar_id: str = 'primary') -> List[Dict]:
    now = datetime.now(timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    formatted_events = []
    for event in events:
        event_id = event.get('id', 'No ID')
        summary = event.get('summary', 'No Summary')
        start_time = event.get('start', {}).get('dateTime', 'No start time')
        end_time = event.get('end', {}).get('dateTime', 'No end time')
        location = event.get('location', '')
        description = event.get('description', '')
        
        event_text = f"{summary}\n🆔 ID: {event_id}\n📅 Start: {start_time}\n📅 End: {end_time}"
        
        if location:
            event_text += f"\n📍 Location: {location}"
        
        if description:
            event_text += f"\n📝 Description: {description}"
        
        formatted_events.append({"type": "text", "text": event_text})
    return formatted_events 