import pytest
from unittest.mock import Mock
from src.calendar_ops import CalendarOperations

@pytest.fixture
def mock_service():
    service = Mock()
    service.events.return_value = Mock()
    return service

@pytest.fixture
def calendar_ops(mock_service):
    return CalendarOperations(mock_service) 