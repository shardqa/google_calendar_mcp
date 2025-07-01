import pytest
from unittest.mock import Mock

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

# @pytest.fixture
# def mock_calendar_ops(mock_google_service):
#     return CalendarOperations(mock_google_service) 