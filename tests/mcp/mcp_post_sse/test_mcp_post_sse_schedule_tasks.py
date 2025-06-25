import pytest
from unittest.mock import Mock, patch, MagicMock


@pytest.fixture
def mock_handler():
    handler = Mock()
    handler.result_id = None
    return handler


@pytest.fixture
def mock_calendar_service():
    service = Mock()
    return service


@pytest.fixture 
def mock_tasks_service():
    service = Mock()
    return service


class TestMCPScheduleTasks:
    @patch('src.mcp.mcp_post_sse_handler.auth')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth')
    def test_schedule_tasks_command_should_exist(self, mock_tasks_auth, mock_auth, 
                                               mock_handler, mock_calendar_service, mock_tasks_service):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        
        mock_auth.get_calendar_service.return_value = mock_calendar_service
        mock_tasks_auth.get_tasks_service.return_value = mock_tasks_service
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {'items': []}
        
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
        
        assert "result" in response
        assert "proposed_events" in response["result"]
        assert "scheduling_summary" in response["result"]

    @patch('src.mcp.mcp_post_sse_handler.auth')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth')
    def test_schedule_tasks_missing_required_params(self, mock_tasks_auth, mock_auth, 
                                                  mock_handler, mock_calendar_service, mock_tasks_service):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "schedule_tasks",
                "arguments": {}
            }
        }
        response = {}
        
        handle_post_sse(mock_handler, request, response)
        
        assert "error" in response
        assert response["error"]["code"] == -32602

    @patch('src.mcp.mcp_post_sse_handler.auth')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth')
    def test_schedule_tasks_with_custom_work_hours(self, mock_tasks_auth, mock_auth,
                                                 mock_handler, mock_calendar_service, mock_tasks_service):
        from src.mcp.mcp_post_sse_handler import handle_post_sse
        
        mock_auth.get_calendar_service.return_value = mock_calendar_service
        mock_tasks_auth.get_tasks_service.return_value = mock_tasks_service
        
        mock_calendar_service.events().list().execute.return_value = {'items': []}
        mock_tasks_service.tasks().list().execute.return_value = {
            'items': [{'id': '1', 'title': 'Test Task'}]
        }
        
        request = {
            "method": "tools/call", 
            "params": {
                "name": "schedule_tasks",
                "arguments": {
                    "time_period": "week",
                    "work_hours_start": "08:00",
                    "work_hours_end": "17:00",
                    "max_task_duration": 90
                }
            }
        }
        response = {}
        
        handle_post_sse(mock_handler, request, response)
        
        assert "result" in response
        result = response["result"]
        assert "proposed_events" in result
        assert "scheduling_summary" in result
        assert result["scheduling_summary"]["total_tasks"] >= 0 