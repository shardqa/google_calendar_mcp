import unittest
from unittest.mock import MagicMock, patch
import pytest

from src.core.calendar_ops import CalendarOperations

pytestmark = pytest.mark.skip(reason="edit_event WIP")


class TestCalendarOpsEdit(unittest.TestCase):
    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_success(self, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service
        calendar_ops = CalendarOperations(mock_service)

        event_id = "test_event_id"
        updated_details = {
            "summary": "Updated Event Summary",
            "description": "Updated Description",
        }

        mock_event = MagicMock()
        mock_execute = MagicMock()
        mock_service.events().get.return_value = mock_execute
        mock_execute.execute.return_value = mock_event

        calendar_ops.edit_event(event_id, updated_details)

        mock_service.events().get.assert_called_once_with(
            calendarId="primary", eventId=event_id
        )
        
        mock_event.update.assert_called_once_with(updated_details)

        mock_service.events().patch.assert_called_once_with(
            calendarId="primary", eventId=event_id, body=mock_event
        )
        
        self.assertIsNotNone(
            mock_service.events().patch().execute(),
            "The updated event should be returned.",
        )


if __name__ == "__main__":
    unittest.main() 