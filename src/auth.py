from src.core.auth import load_credentials, get_credentials
from googleapiclient.discovery import build

def get_calendar_service():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    return service 