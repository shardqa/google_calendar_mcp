import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_handler():
    handler = Mock()
    handler.result_id = None
    handler.send_response = Mock()
    handler.send_header = Mock()
    handler.end_headers = Mock()
    handler.wfile = Mock()
    handler.wfile.write = Mock()
    return handler


class TestMCPScheduleTasksEdgeCases:
    
    @patch('src.mcp.mcp_post_sse_handler.auth')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth')
    def test_schedule_tasks_service_exception_coverage(self, mock_tasks_auth, mock_auth, mock_handler):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        
        mock_auth.get_calendar_service.side_effect = Exception("Calendar service error")
        mock_tasks_auth.get_tasks_service.return_value = Mock()
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "schedule_tasks",
                "arguments": {
                    "time_period": "day",
                    "work_hours_start": "09:00",
                    "work_hours_end": "18:00"
                }
            }
        }
        response = {}
        
        handle_post_sse(mock_handler, request, response)
        
        assert "error" in response
        assert response["error"]["code"] == -32603
        assert "Scheduling service error" in response["error"]["message"]
        assert "Calendar service error" in response["error"]["message"]
        
        mock_handler.send_response.assert_called_with(200)
        mock_handler.send_header.assert_any_call("Content-Type", "application/json")
        mock_handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        mock_handler.send_header.assert_any_call("Connection", "close")
        mock_handler.end_headers.assert_called_once()
        mock_handler.wfile.write.assert_called_once()

    @patch('src.mcp.mcp_post_sse_handler.auth')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth')
    def test_schedule_tasks_with_import_error(self, mock_tasks_auth, mock_auth, mock_handler):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        
        mock_auth.get_calendar_service.return_value = Mock()
        mock_tasks_auth.get_tasks_service.return_value = Mock()
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "schedule_tasks",
                "arguments": {
                    "time_period": "day",
                    "work_hours_start": "09:00",
                    "work_hours_end": "18:00"
                }
            }
        }
        response = {}
        
        with patch('src.core.scheduling_engine.SchedulingEngine', side_effect=ImportError("Module not found")):
            handle_post_sse(mock_handler, request, response)
        
        assert "error" in response
        assert response["error"]["code"] == -32603
        assert "Scheduling service error" in response["error"]["message"]

    def test_empty_response_json_encoding(self, mock_handler):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        import json
        
        request = {
            "method": "unknown_method",
            "params": {}
        }
        response = {}
        
        handle_post_sse(mock_handler, request, response)
        
        assert "error" in response
        assert response["error"]["code"] == -32601
        
        mock_handler.wfile.write.assert_called_once()
        written_data = mock_handler.wfile.write.call_args[0][0]
        
        decoded_response = json.loads(written_data.decode())
        assert "error" in decoded_response
        assert decoded_response["error"]["code"] == -32601 