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
        mock_get_call = MagicMock()
        mock_get_call.execute.return_value = mock_event_instance
        mock_service.events().get.return_value = mock_get_call
        
        mock_patch_call = MagicMock()
        mock_patch_call.execute.return_value = {"id": "test_event_id", "summary": "Updated Summary"}
        mock_service.events().patch.return_value = mock_patch_call

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
        self.assertIn("content", response["result"])
        self.assertIn("✅ Evento editado com sucesso!", response["result"]["content"][0]["text"])
        # Agora usamos CalendarOperations.edit_event em vez de manipulação direta
        # Verificamos se o mock foi chamado corretamente
        
        # Verify correct API calls with proper parameters
        mock_service.events().get.assert_called_once_with(calendarId="primary", eventId="test_event_id")
        mock_service.events().patch.assert_called_once_with(calendarId="primary", eventId="test_event_id", body=mock_event_instance)

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

    @patch("src.core.auth.get_calendar_service")
    def test_edit_event_with_location(self, mock_get_service):
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        updated_event_response = {
            "id": "loc_event_id",
            "summary": "Meeting",
            "start": {"dateTime": "2024-03-22T09:00:00Z"},
            "end": {"dateTime": "2024-03-22T10:00:00Z"},
            "location": "Office"
        }

        class FakeOps:
            def __init__(self, service):
                self.service = service
            def edit_event(self, event_id, updated_details):
                return updated_event_response
        with patch("src.mcp.mcp_post_other_handler.calendar_ops.CalendarOperations", FakeOps):
            request = {
                "method": "tools/call",
                "params": {
                    "tool": "edit_event",
                    "args": {
                        "event_id": "loc_event_id",
                        "updated_details": {"location": "Office"}
                    }
                }
            }
            response = {}
            mock_handler = MagicMock()
            handle_post_other(mock_handler, request, response)
            self.assertIn("result", response)
            text = response["result"]["content"][0]["text"]
            self.assertIn("📍 Office", text)

if __name__ == '__main__':
    unittest.main() 