import pytest
from unittest.mock import Mock
from src.core.calendar_ops import CalendarOperations

@pytest.fixture

def mock_service():
    return Mock()

@pytest.fixture
def calendar_ops(mock_service):
    return CalendarOperations(mock_service)


def test_list_calendars_empty(calendar_ops, mock_service):
    cal_mock = mock_service.calendarList.return_value
    cal_mock.list.return_value.execute.return_value = {}
    result = calendar_ops.list_calendars()
    assert result == []
    mock_service.calendarList.assert_called_once()
    cal_mock.list.assert_called_once()
    cal_mock.list.return_value.execute.assert_called_once()


def test_list_calendars_with_items(calendar_ops, mock_service):
    sample = {
        'items': [
            {'id': 'primary', 'summary': 'Minha Agenda'},
            {'id': 'work', 'summary': 'Work Calendar'}
        ]
    }
    cal_mock = mock_service.calendarList.return_value
    cal_mock.list.return_value.execute.return_value = sample
    result = calendar_ops.list_calendars()
    assert len(result) == 2
    assert result[0]['type'] == 'text'
    assert 'Minha Agenda' in result[0]['text']
    assert 'primary' in result[0]['text']
    assert 'Work Calendar' in result[1]['text']
    assert 'work' in result[1]['text'] 