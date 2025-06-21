import unittest
from unittest.mock import Mock, patch, MagicMock
from src.mcp.mcp_post_sse_handler import handle_post_sse

class TestMcpPostSseTasksSuccessScenarios(unittest.TestCase):

    def setUp(self):
        self.handler = Mock()
        self.handler.send_response = Mock()
        self.handler.send_header = Mock()
        self.handler.end_headers = Mock()
        self.handler.wfile = Mock()
        self.handler.wfile.write = Mock()

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_list_tasks_success(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.list_tasks.return_value = [{"title": "Test Task"}]
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "list_tasks",
                "arguments": {"tasklist_id": "custom_list"}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertIn("content", response["result"])
        mock_ops.list_tasks.assert_called_once_with("custom_list")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_with_notes_and_due(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.add_task.return_value = {"status": "created", "task": {"id": "123"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {
                    "title": "Test Task",
                    "notes": "Task notes",
                    "due": "2024-12-31T23:59:59Z",
                    "tasklist_id": "custom_list"
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {
            "title": "Test Task",
            "notes": "Task notes", 
            "due": "2024-12-31T23:59:59Z"
        }
        mock_ops.add_task.assert_called_once_with(expected_task_data, "custom_list")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_remove_task_success(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.remove_task.return_value = True
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "remove_task",
                "arguments": {
                    "task_id": "test_task_123",
                    "tasklist_id": "custom_list"
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertIn("success", response["result"])
        mock_ops.remove_task.assert_called_once_with("test_task_123", "custom_list")

if __name__ == '__main__':
    unittest.main() 