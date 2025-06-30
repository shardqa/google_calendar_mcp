import os.path
import json
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

def _find_project_root():
    """
    Find the project root directory by looking for marker files.
    
    Returns:
        str: Absolute path to the project root directory
    """
    current_dir = Path(__file__).parent
    
    # Look for project markers (pyproject.toml, README.md with specific content, etc.)
    while current_dir != current_dir.parent:
        # Check for project-specific markers
        pyproject_file = current_dir / 'pyproject.toml'
        readme_file = current_dir / 'README.md'
        config_dir = current_dir / 'config'
        
        if (pyproject_file.exists() and 
            readme_file.exists() and 
            config_dir.exists() and config_dir.is_dir()):
            # Additional check: verify this is our project
            try:
                with open(pyproject_file, 'r') as f:
                    content = f.read()
                    if 'google-calendar-mcp' in content:
                        return str(current_dir.absolute())
            except:
                pass
        
        current_dir = current_dir.parent
    
    # Fallback: assume the project is 2 levels up from this file
    fallback_root = Path(__file__).parent.parent.parent
    return str(fallback_root.absolute())

def _get_config_path(filename):
    """
    Get absolute path for a config file.
    
    Args:
        filename: Name of the config file
        
    Returns:
        str: Absolute path to the config file
    """
    project_root = _find_project_root()
    return os.path.join(project_root, 'config', filename)

def load_credentials(credentials_path: str) -> dict:
    try:
        with open(credentials_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Failed to load credentials: {str(e)}")

def get_credentials(credentials_path: str = None) -> object:
    if credentials_path is None:
        credentials_path = _get_config_path('credentials.json')
        
    creds = None
    token_path = _get_config_path('token.pickle')
    
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
    creds = get_credentials()
    service = build('tasks', 'v1', credentials=creds)
    return service 