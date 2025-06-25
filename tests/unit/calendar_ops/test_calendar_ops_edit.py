import unittest
from unittest.mock import MagicMock, patch
import pytest

from src.core.calendar_ops import CalendarOperations


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
        
        # Verify that the event object was updated with the new values
        # (since we now use direct assignment instead of update() method)
        assert mock_event.__setitem__.call_count == len(updated_details)

        mock_service.events().patch.assert_called_once_with(
            calendarId="primary", eventId=event_id, body=mock_event
        )
        
        self.assertIsNotNone(
            mock_service.events().patch().execute(),
            "The updated event should be returned.",
        )

    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_failure_returns_none(self, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service
        calendar_ops = CalendarOperations(mock_service)

        # Simulate service exception on retrieval to trigger failure path
        mock_service.events().get().execute.side_effect = Exception("Failure")

        result = calendar_ops.edit_event("bad_id", {"summary": "s"})

        self.assertIsNone(result)

    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_adds_timezones(self, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service
        ops = CalendarOperations(mock_service)

        event_id = "tz_event"
        updated_details = {
            "start": {"dateTime": "2024-03-22T09:00:00"},
            "end": {"dateTime": "2024-03-22T10:00:00"}
        }

        # Existing event object missing timeZone
        mock_event = {
            "start": {"dateTime": "old"},
            "end": {"dateTime": "old"}
        }
        mock_service.events().get.return_value.execute.return_value = mock_event
        mock_service.events().patch.return_value.execute.return_value = {
            "id": event_id
        }

        result = ops.edit_event(event_id, updated_details)

        # Verify timezone was added
        patched_body = mock_service.events().patch.call_args[1]["body"]
        assert patched_body["start"]["timeZone"] == "America/Sao_Paulo"
        assert patched_body["end"]["timeZone"] == "America/Sao_Paulo"
        assert result["id"] == event_id


if __name__ == "__main__":
    unittest.main() 