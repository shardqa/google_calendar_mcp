from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.request import urlopen

class ICSOperations:
    def __init__(self, fetch_timeout: int = 10):
        self.fetch_timeout = fetch_timeout

    def _download_ics(self, ics_url: str) -> str:  # pragma: no cover
        with urlopen(ics_url, timeout=self.fetch_timeout) as resp:
            return resp.read().decode()

    def list_events(self, ics_url: str, max_results: Optional[int] = None) -> List[Dict]:
        ics_text = self._download_ics(ics_url)
        events: List[Dict] = []
        current: Dict[str, str] = {}
        now = datetime.now(timezone.utc)
        
        for line in ics_text.splitlines():
            line = line.rstrip()
            if line == 'BEGIN:VEVENT':
                current = {}
            elif line == 'END:VEVENT':
                if current and self._is_future_event(current, now):
                    events.append(self._format_event(current))
            else:
                if ':' not in line:
                    continue
                key, val = line.split(':', 1)
                key = key.split(';', 1)[0]  # Ignore any parameters like TZID=...
                current[key] = val
        
        events.sort(key=lambda e: self._extract_start_datetime(e))
        if max_results is not None:
            events = events[:max_results]
        return events

    def _is_future_event(self, event_data: Dict[str, str], now: datetime) -> bool:
        """Check if event starts today or in the future."""
        start_str = event_data.get('DTSTART', '')
        if not start_str:
            return True  # Include events without start time
        
        try:
            # Parse datetime from ICS format
            if 'T' in start_str and len(start_str) >= 15:
                event_start = datetime.strptime(start_str[:15], '%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc)
                # Compare only dates - include events from today onwards
                today = now.date()
                event_date = event_start.date()
                return event_date >= today
        except Exception:
            pass
        return True  # Include events we can't parse

    def _extract_start_datetime(self, formatted_event: Dict) -> datetime:
        """Extract start datetime from formatted event for sorting."""
        try:
            text = formatted_event.get('text', '')
            for line in text.split('\n'):
                if line.startswith('📅 Start: '):
                    date_str = line.replace('📅 Start: ', '')
                    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            pass
        return datetime.min.replace(tzinfo=timezone.utc)

    def _format_event(self, raw: Dict[str, str]) -> Dict:
        summary = raw.get('SUMMARY', 'No Summary')
        start = raw.get('DTSTART', 'No start time')
        end = raw.get('DTEND', 'No end time')
        location = raw.get('LOCATION', '')
        description = raw.get('DESCRIPTION', '')

        # Convert date if in basic format (YYYYMMDDT...) to ISO-like display
        def _normalize(dt: str):  # pragma: no cover
            if 'T' in dt and len(dt) >= 15:
                try:
                    return datetime.strptime(dt[:15], '%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc).isoformat()
                except Exception:
                    return dt
            return dt

        start_norm = _normalize(start)
        end_norm = _normalize(end)

        text = f"{summary}\n📅 Start: {start_norm}\n📅 End: {end_norm}"
        if location:
            text += f"\n📍 Location: {location}"
        if description:
            text += f"\n📝 Description: {description}"
        return {"type": "text", "text": text} 