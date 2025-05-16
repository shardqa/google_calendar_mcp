import pytest
from unittest.mock import Mock, patch
from src.commands.main import main

@pytest.fixture
def mock_service():
    return Mock()

@pytest.fixture
def mock_calendar_ops():
    with patch('src.main.CalendarOperations') as mock:
        mock.return_value = Mock()
        yield mock

@pytest.fixture
def mock_cli():
    with patch('src.main.CLI') as mock:
        mock.return_value = Mock()
        yield mock

def test_main_initialization(mock_service, mock_calendar_ops, mock_cli):
    # Arrange
    with patch('src.main.get_calendar_service', return_value=mock_service):
        # Act
        result = main()

        # Assert
        mock_calendar_ops.assert_called_once_with(mock_service)
        mock_cli.assert_called_once()
        assert result == 0

def test_main_execution(mock_service, mock_calendar_ops, mock_cli):
    # Arrange
    mock_cli_instance = mock_cli.return_value
    with patch('src.main.get_calendar_service', return_value=mock_service):
        # Act
        result = main()

        # Assert
        mock_cli_instance.run_interactive_loop.assert_called_once()
        assert result == 0

def test_main_error_handling(mock_calendar_ops, mock_cli):
    # Arrange
    with patch('src.main.get_calendar_service', side_effect=Exception("Test error")):
        # Act
        result = main()

        # Assert
        assert result == 1
        mock_calendar_ops.assert_not_called()
        mock_cli.assert_not_called() 