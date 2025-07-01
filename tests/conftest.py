import pytest
from unittest.mock import Mock, patch
import os
import tempfile

@pytest.fixture
def mock_service():
    service = Mock()
    service.events.return_value = Mock()
    service.calendarList.return_value = Mock()
    return service

@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    """Creates a temporary HOME so tests don't touch real ~/.cursor."""
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path

@pytest.fixture
def mock_credentials(monkeypatch):
    """Mock Google credentials to avoid file dependencies in CI/CD."""
    mock_creds = Mock()
    mock_creds.valid = True
    mock_creds.expired = False
    
    # Mock the auth module functions
    monkeypatch.setattr('src.core.auth.get_credentials', lambda *args, **kwargs: mock_creds)
    monkeypatch.setattr('src.core.auth.get_calendar_service', lambda: Mock())
    
    # Also patch in mcp modules that import auth
    monkeypatch.setattr('src.mcp.mcp_post_other_handler.auth.get_calendar_service', lambda: Mock())
    
    return mock_creds

# @pytest.fixture
# def mock_calendar_ops(mock_google_service):
#     return CalendarOperations(mock_google_service) 