import pytest
from unittest.mock import Mock, patch
from src.cli import CLI

@pytest.fixture
def mock_calendar_ops():
    return Mock()

@pytest.fixture
def cli(mock_calendar_ops):
    return CLI(mock_calendar_ops)

def test_display_menu(capsys, cli):
    # Act
    cli.display_menu()
    captured = capsys.readouterr()

    # Assert
    assert "Google Calendar MCP" in captured.out
    assert "1. List Events" in captured.out
    assert "2. Add Event" in captured.out
    assert "3. Remove Event" in captured.out
    assert "4. Exit" in captured.out

@pytest.mark.parametrize("user_input,expected_call", [
    ("1", "list_events"),
    ("4", "exit"),
    ("invalid", None)
])
def test_process_command(cli, mock_calendar_ops, user_input, expected_call):
    # Arrange
    mock_calendar_ops.list_events.return_value = [
        {
            'summary': 'Test Event',
            'start': {'dateTime': '2024-03-20T10:00:00Z'}
        }
    ]

    # Act
    result = cli.process_command(user_input)

    # Assert
    if expected_call == "list_events":
        mock_calendar_ops.list_events.assert_called_once()
        assert result is True
    elif expected_call == "exit":
        assert result is False
    else:
        assert result is True
        mock_calendar_ops.list_events.assert_not_called()

@patch('builtins.input')
def test_process_command_add_event(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.side_effect = [
        "Test Event",
        "2024-03-20 10:00",
        "2024-03-20 11:00"
    ]
    mock_calendar_ops.add_event.return_value = {"status": "confirmed"}

    # Act
    result = cli.process_command("2")

    # Assert
    assert result is True
    mock_calendar_ops.add_event.assert_called_once()
    assert mock_input.call_count == 3

@patch('builtins.input')
def test_process_command_remove_event(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.return_value = "test-event-id"
    mock_calendar_ops.remove_event.return_value = True

    # Act
    result = cli.process_command("3")

    # Assert
    assert result is True
    mock_calendar_ops.remove_event.assert_called_once_with("test-event-id")

@patch('builtins.input')
def test_run_interactive_loop(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.side_effect = ["1", "4"]  # List events then exit
    mock_calendar_ops.list_events.return_value = [
        {
            'summary': 'Test Event',
            'start': {'dateTime': '2024-03-20T10:00:00Z'}
        }
    ]

    # Act
    cli.run_interactive_loop()

    # Assert
    assert mock_input.call_count == 2
    mock_calendar_ops.list_events.assert_called_once()


@patch('builtins.input')
def test_process_command_add_event_invalid_date(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.side_effect = [
        "Test Event",
        "invalid date",
        "2024-03-20 11:00"
    ]

    # Act
    result = cli.process_command("2")

    # Assert
    assert result is True
    mock_calendar_ops.add_event.assert_not_called()


@patch('builtins.input')
def test_process_command_add_event_failed(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.side_effect = [
        "Test Event",
        "2024-03-20 10:00",
        "2024-03-20 11:00"
    ]
    mock_calendar_ops.add_event.return_value = {"status": "error"}

    # Act
    result = cli.process_command("2")

    # Assert
    assert result is True
    mock_calendar_ops.add_event.assert_called_once()


@patch('builtins.input')
def test_process_command_remove_event_failed(mock_input, cli, mock_calendar_ops):
    # Arrange
    mock_input.return_value = "test-event-id"
    mock_calendar_ops.remove_event.return_value = False

    # Act
    result = cli.process_command("3")

    # Assert
    assert result is True
    mock_calendar_ops.remove_event.assert_called_once_with("test-event-id")


def test_process_command_list_events_empty(cli, mock_calendar_ops):
    # Arrange
    mock_calendar_ops.list_events.return_value = []

    # Act
    result = cli.process_command("1")

    # Assert
    assert result is True
    mock_calendar_ops.list_events.assert_called_once() 