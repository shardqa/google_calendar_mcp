import pytest
import json
from unittest.mock import MagicMock, patch, mock_open
from src.core import tasks_auth


def test_get_tasks_service():
    mock_creds = MagicMock()
    mock_service = MagicMock()

    with patch('src.core.tasks_auth.get_credentials', return_value=mock_creds) as mock_get_creds, \
         patch('src.core.tasks_auth.build', return_value=mock_service) as mock_build:
        service = tasks_auth.get_tasks_service()
        mock_get_creds.assert_called_once_with('config/credentials.json')
        mock_build.assert_called_once_with('tasks', 'v1', credentials=mock_creds)
        assert service == mock_service


def test_load_credentials_success():
    mock_credentials = {'type': 'service_account', 'project_id': 'test'}
    mock_file_content = json.dumps(mock_credentials)
    
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = tasks_auth.load_credentials('test_path.json')
        assert result == mock_credentials


def test_load_credentials_file_error():
    with patch('builtins.open', side_effect=FileNotFoundError('File not found')):
        with pytest.raises(Exception) as exc_info:
            tasks_auth.load_credentials('nonexistent.json')
        assert 'Failed to load credentials' in str(exc_info.value)


def test_get_credentials_existing_valid_token():
    mock_creds = MagicMock()
    mock_creds.valid = True
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds):
        result = tasks_auth.get_credentials('test_path.json')
        assert result == mock_creds


def test_get_credentials_expired_token_refresh():
    mock_creds = MagicMock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = 'refresh_token'
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds), \
         patch('pickle.dump'), \
         patch('google.auth.transport.requests.Request') as mock_request:
        result = tasks_auth.get_credentials('test_path.json')
        mock_creds.refresh.assert_called_once()
        assert result == mock_creds


def test_get_credentials_new_token():
    mock_creds = MagicMock()
    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = mock_creds

    with patch('os.path.exists', return_value=False), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', return_value=mock_flow) as mock_flow_create, \
         patch('builtins.open', mock_open()), \
         patch('pickle.dump'):
        creds = tasks_auth.get_credentials('fake_path/credentials.json')
        mock_flow_create.assert_called_once_with('fake_path/credentials.json', tasks_auth.SCOPES)
        mock_flow.run_local_server.assert_called_once_with(port=0)
        assert creds == mock_creds
        
        
def test_tasks_scopes_include_tasks_api():
    assert 'https://www.googleapis.com/auth/tasks' in tasks_auth.SCOPES
    assert 'https://www.googleapis.com/auth/calendar' in tasks_auth.SCOPES 