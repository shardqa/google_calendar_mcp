import unittest
from unittest.mock import MagicMock, patch
from src.mcp.mcp_post_other_handler import handle_post_other
import pytest

class TestMcpPostOtherEditEvent(unittest.TestCase):
    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_mcp_call_success(self, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        mock_event_instance = MagicMock()
        mock_service.events().get().execute.return_value = mock_event_instance
        mock_service.events().patch().execute.return_value = {"id": "test_event_id", "summary": "Updated Summary"}

        request = {
            "method": "tools/call",
            "params": {
                "tool": "edit_event",
                "args": {
                    "event_id": "test_event_id",
                    "updated_details": {"summary": "Updated Summary"}
                }
            }
        }
        response = {}
        
        mock_handler = MagicMock()
        handle_post_other(mock_handler, request, response)

        self.assertIn("result", response)
        self.assertEqual(response["result"]["summary"], "Updated Summary")
        mock_event_instance.update.assert_called_once_with({"summary": "Updated Summary"})

    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_mcp_call_missing_params(self, mock_get_service):
        request = {
            "method": "tools/call",
            "params": {
                "tool": "edit_event",
                "args": {"event_id": "test_event_id"}
            }
        }
        response = {}
        
        mock_handler = MagicMock()
        handle_post_other(mock_handler, request, response)

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("updated_details are required", response["error"]["message"])

    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_mcp_call_service_exception(self, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        # Simulate failure during patch execution to trigger error handling
        mock_service.events().get().execute.return_value = MagicMock()
        mock_service.events().patch().execute.side_effect = Exception("Failure")

        request = {
            "method": "tools/call",
            "params": {
                "tool": "edit_event",
                "args": {
                    "event_id": "test_event_id",
                    "updated_details": {"summary": "Updated Summary"}
                }
            }
        }
        response = {}

        mock_handler = MagicMock()
        handle_post_other(mock_handler, request, response)

        self.assertIn("error", response)
        self.assertEqual(response["error"].get("code"), -32603)
        self.assertIn("Failed to edit event", response["error"].get("message", ""))

if __name__ == '__main__':
    unittest.main() 