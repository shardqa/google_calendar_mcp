import os.path
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Escopo necessário para acessar o Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def load_credentials(credentials_path: str) -> dict:
    """
    Load client credentials from a JSON file.
    
    Args:
        credentials_path: Path to the client credentials JSON file
        
    Returns:
        dict: Client credentials
    """
    try:
        with open(credentials_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Failed to load credentials: {str(e)}")

def get_credentials(credentials_path: str) -> object:
    """
    Get valid user credentials from storage.
    
    Args:
        credentials_path: Path to the client credentials file
        
    Returns:
        object: Valid credentials object
    """
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

def get_calendar_service():
    """
    Get an authorized Google Calendar service instance.
    
    Returns:
        object: Authorized Google Calendar service
    """
    creds = get_credentials('config/credentials.json')
    service = build('calendar', 'v3', credentials=creds)
    return service 