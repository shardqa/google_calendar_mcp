from typing import List, Dict

def list_calendars(service) -> List[Dict]:
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    formatted_calendars = []
    for cal in calendars:
        cal_id = cal.get('id', 'No ID')
        summary = cal.get('summary', 'No Summary')
        formatted_calendars.append({"type": "text", "text": f"{summary}\n🆔 ID: {cal_id}"})
    return formatted_calendars 