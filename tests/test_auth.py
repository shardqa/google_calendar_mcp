import pytest
from unittest.mock import patch, mock_open, MagicMock
from src import auth


def test_load_credentials_success():
    with patch('builtins.open', mock_open(read_data='{"client_id": "abc", "client_secret": "xyz"}')) as mock_file:
        creds = auth.load_credentials('fake_path/credentials.json')
        assert creds['client_id'] == 'abc'
        assert creds['client_secret'] == 'xyz'


def test_get_token_success():
    mock_creds = MagicMock()
    mock_creds.to_json.return_value = '{"token": "fake_token"}'
    
    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = mock_creds
    
    with patch('src.auth.load_credentials', return_value={'client_id': 'abc', 'client_secret': 'xyz'}), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', return_value=mock_flow):
        token = auth.get_token('fake_path/credentials.json')
        assert token == '{"token": "fake_token"}' 