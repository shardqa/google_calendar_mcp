import os.path
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

def load_credentials(credentials_path: str) -> dict:
    try:
        with open(credentials_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Failed to load credentials: {str(e)}")

def get_credentials(credentials_path: str) -> object:
    creds = None
    token_path = 'config/token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_tasks_service():
    creds = get_credentials('config/credentials.json')
    service = build('tasks', 'v1', credentials=creds)
    return service 