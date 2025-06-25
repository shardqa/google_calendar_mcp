import unittest
from unittest.mock import Mock, patch, MagicMock
from src.mcp.mcp_post_sse_handler import handle_post_sse

class TestMcpPostSseTasksBranchCoverage(unittest.TestCase):

    def setUp(self):
        self.handler = Mock()
        self.handler.send_response = Mock()
        self.handler.send_header = Mock()
        self.handler.end_headers = Mock()
        self.handler.wfile = Mock()
        self.handler.wfile.write = Mock()

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_without_notes_and_due(self, mock_get_service, mock_ops_class):
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
                    "title": "Simple Task"
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {"title": "Simple Task"}
        mock_ops.add_task.assert_called_once_with(expected_task_data, "@default")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_with_notes_only(self, mock_get_service, mock_ops_class):
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
                    "title": "Task with Notes",
                    "notes": "Important notes here"
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {
            "title": "Task with Notes",
            "notes": "Important notes here"
        }
        mock_ops.add_task.assert_called_once_with(expected_task_data, "@default")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_with_due_only(self, mock_get_service, mock_ops_class):
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
                    "title": "Task with Due Date",
                    "due": "2024-12-31T23:59:59Z"
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {
            "title": "Task with Due Date",
            "due": "2024-12-31T23:59:59Z"
        }
        mock_ops.add_task.assert_called_once_with(expected_task_data, "@default")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_with_empty_notes_and_due(self, mock_get_service, mock_ops_class):
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
                    "title": "Task with Empty Fields",
                    "notes": "",
                    "due": ""
                }
            }
        }
        response = {}
        
        handle_post_sse(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {"title": "Task with Empty Fields"}
        mock_ops.add_task.assert_called_once_with(expected_task_data, "@default")

    @patch('src.mcp.mcp_post_sse_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_sse_handler.tasks_auth.get_tasks_service')
    def test_add_task_error_status(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.add_task.return_value = {"status": "error", "message": "API failure"}

        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {"title": "Broken Task"}
            }
        }
        response = {}

        handle_post_sse(self.handler, request, response)

        self.assertIn("result", response)
        self.assertEqual(response["result"]["status"], "error")
        mock_ops.add_task.assert_called_once()

if __name__ == '__main__':
    unittest.main() 