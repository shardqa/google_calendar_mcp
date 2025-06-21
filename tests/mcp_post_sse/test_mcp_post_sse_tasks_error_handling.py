import unittest
from unittest.mock import Mock, patch, MagicMock
from src.mcp.mcp_post_sse_handler import handle_post_sse

class TestMcpPostSseTasksErrorHandling(unittest.TestCase):

    def setUp(self):
        self.handler = Mock()
        self.handler.send_response = Mock()
        self.handler.send_header = Mock()
        self.handler.end_headers = Mock()
        self.handler.wfile = Mock()
        self.handler.wfile.write = Mock()

    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_list_tasks_service_error(self, mock_get_service):
        mock_get_service.side_effect = Exception("Service unavailable")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "list_tasks",
                "arguments": {}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Tasks service error", response["error"]["message"])

    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_service_error(self, mock_get_service):
        mock_get_service.side_effect = Exception("API quota exceeded")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {"title": "Test Task"}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Tasks service error", response["error"]["message"])

    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_missing_title(self, mock_get_service):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertEqual(response["error"]["message"], "Task title is required")

    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_remove_task_service_error(self, mock_get_service):
        mock_get_service.side_effect = Exception("Authentication failed")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "remove_task",
                "arguments": {"task_id": "test_id"}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Tasks service error", response["error"]["message"])

    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_remove_task_missing_id(self, mock_get_service):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "remove_task",
                "arguments": {}
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertEqual(response["error"]["message"], "Task ID is required")

if __name__ == '__main__':
    unittest.main() 