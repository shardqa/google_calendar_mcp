import pytest
import json
from unittest.mock import Mock, MagicMock, mock_open, patch
from pathlib import Path
import src.auth as auth
import src.core.auth as core_auth


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
        mock_get_creds.assert_called_once_with()
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_creds)
        assert service == mock_service


def test_load_credentials_success():
    mock_credentials = {'type': 'service_account', 'project_id': 'test'}
    mock_file_content = json.dumps(mock_credentials)
    
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = core_auth.load_credentials('test_path.json')
        assert result == mock_credentials


def test_load_credentials_error():
    with patch('builtins.open', side_effect=FileNotFoundError('File not found')):
        with pytest.raises(Exception) as exc_info:
            core_auth.load_credentials('nonexistent.json')
        assert 'Failed to load credentials' in str(exc_info.value)


def test_find_project_root_with_markers():
    """Test project root detection with valid markers"""
    mock_path = MagicMock()
    mock_path.parent = Path('/home')
    mock_path.absolute.return_value = Path('/home/user/project')
    
    with patch('pathlib.Path') as mock_path_class:
        mock_path_class.return_value.parent = mock_path
        
        # Mock the directory structure
        mock_pyproject = MagicMock()
        mock_pyproject.exists.return_value = True
        mock_readme = MagicMock()
        mock_readme.exists.return_value = True
        mock_config = MagicMock()
        mock_config.exists.return_value = True
        mock_config.is_dir.return_value = True
        
        mock_path.__truediv__ = MagicMock()
        mock_path.__truediv__.side_effect = lambda x: {
            'pyproject.toml': mock_pyproject,
            'README.md': mock_readme,
            'config': mock_config
        }[x]
        
        # Mock file reading
        with patch('builtins.open', mock_open(read_data='google-calendar-mcp')):
            result = core_auth._find_project_root()
            assert isinstance(result, str)


def test_find_project_root_fallback():
    """Test project root detection fallback"""
    with patch('pathlib.Path') as mock_path_class:
        # Mock Path(__file__).parent to return a specific structure
        mock_file_path = MagicMock()
        mock_file_path.parent.parent.parent.absolute.return_value = Path('/fallback/path')
        mock_path_class.return_value = mock_file_path
        
        # Make the while loop exit quickly by making parent == parent
        mock_current = MagicMock()
        mock_current.parent = mock_current  # This will break the while loop
        mock_file_path.parent = mock_current
        
        result = core_auth._find_project_root()
        assert isinstance(result, str)


def test_get_config_path():
    """Test config path generation"""
    with patch('src.core.auth._find_project_root', return_value='/test/project'):
        result = core_auth._get_config_path('credentials.json')
        assert result.endswith('config/credentials.json')
        assert '/test/project' in result


def test_get_calendar_service_core():
    mock_creds = MagicMock()
    mock_service = MagicMock()

    with patch('src.core.auth.get_credentials', return_value=mock_creds) as mock_get_creds, \
         patch('src.core.auth.build', return_value=mock_service) as mock_build:
        service = core_auth.get_calendar_service()
        mock_get_creds.assert_called_once_with()
        mock_build.assert_called_once_with('calendar', 'v3', credentials=mock_creds)
        assert service == mock_service


def test_get_credentials_expired_without_refresh_token():
    mock_creds = MagicMock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = None
    mock_flow = MagicMock()
    mock_flow.run_local_server.return_value = mock_creds

    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds), \
         patch('pickle.dump'), \
         patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file', return_value=mock_flow):
        result = core_auth.get_credentials('test_path.json')
        mock_flow.run_local_server.assert_called_once_with(port=0)
        assert result == mock_creds


def test_get_credentials_refresh_scenario():
    """Test the credentials refresh path (line 45)"""
    mock_creds = MagicMock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = 'valid_refresh_token'
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open()), \
         patch('pickle.load', return_value=mock_creds), \
         patch('pickle.dump'):
        
        result = core_auth.get_credentials('test_path.json')
        
        # This should trigger the refresh path (line 45)
        mock_creds.refresh.assert_called_once()
        assert result == mock_creds 