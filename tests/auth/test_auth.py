import pytest
from unittest.mock import Mock, MagicMock, mock_open, patch
import src.auth as auth


def test_load_credentials_success():
    with patch('builtins.open', mock_open(read_data='{"client_id": "abc", "client_secret": "xyz"}')):
        creds = auth.load_credentials('fake_path/credentials.json')
        assert creds['client_id'] == 'abc'
        assert creds['client_secret'] == 'xyz'


def test_get_credentials_new_token():
    mock_creds = MagicMock()
    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = mock_creds

    with patch('os.path.exists', return_value=False), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', return_value=mock_flow), \
         patch('builtins.open', mock_open()), \
         patch('pickle.dump'):
        creds = auth.get_credentials('fake_path/credentials.json')
        assert creds == mock_creds


def test_get_credentials_existing_valid_token():
    mock_creds = MagicMock()
    mock_creds.valid = True

    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds):
        creds = auth.get_credentials('fake_path/credentials.json')
        assert creds == mock_creds


def test_get_calendar_service():
    mock_creds = MagicMock()
    mock_service = MagicMock()

    with patch('src.auth.get_credentials', return_value=mock_creds) as mock_get_creds, \
         patch('src.auth.build', return_value=mock_service) as mock_build:
        service = auth.get_calendar_service()
        mock_get_creds.assert_called_once_with('credentials.json')
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_creds)
        assert service == mock_service 