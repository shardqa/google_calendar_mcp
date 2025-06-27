def remove_event(service, event_id: str) -> bool:
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()
        return True
    except Exception:
        return False 