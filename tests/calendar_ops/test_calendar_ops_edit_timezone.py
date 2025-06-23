import unittest
from unittest.mock import MagicMock, patch
from src.core.calendar_ops import CalendarOperations


class TestCalendarOpsEditTimezone(unittest.TestCase):
    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_preserves_existing_timezone(self, mock_get_calendar_service):
        mock_service = MagicMock()
        mock_get_calendar_service.return_value = mock_service
        ops = CalendarOperations(mock_service)

        event_id = "tz_existing"
        updated_details = {
            "start": {"dateTime": "2024-03-22T09:00:00", "timeZone": "UTC"},
            "end": {"dateTime": "2024-03-22T10:00:00", "timeZone": "UTC"}
        }

        mock_event = {
            "start": updated_details["start"].copy(),
            "end": updated_details["end"].copy()
        }
        mock_service.events().get.return_value.execute.return_value = mock_event
        mock_service.events().patch.return_value.execute.return_value = {"id": event_id}

        ops.edit_event(event_id, updated_details)

        patched_body = mock_service.events().patch.call_args[1]["body"]
        assert patched_body["start"]["timeZone"] == "UTC"
        assert patched_body["end"]["timeZone"] == "UTC"


if __name__ == "__main__":
    unittest.main() 