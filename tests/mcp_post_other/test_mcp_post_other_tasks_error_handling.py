import unittest
from unittest.mock import Mock, patch
from src.mcp.mcp_post_other_handler import handle_post_other

class TestMcpPostOtherTasksErrorHandling(unittest.TestCase):

    def setUp(self):
        self.handler = Mock()

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_list_tasks_service_error(self, mock_get_service, mock_ops_class):
        mock_get_service.side_effect = Exception("Service unavailable")
        
        request = {
            "method": "tools/call",
            "params": {"name": "list_tasks"}
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Service unavailable", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_add_task_missing_title(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {"notes": "Task without title"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Task title is required", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_add_task_service_error(self, mock_get_service, mock_ops_class):
        mock_get_service.side_effect = Exception("Tasks API error")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {"title": "Test Task"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Tasks API error", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_remove_task_missing_task_id(self, mock_get_service, mock_ops_class):
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
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Task ID is required", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_remove_task_service_error(self, mock_get_service, mock_ops_class):
        mock_get_service.side_effect = Exception("Task not found")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "remove_task",
                "arguments": {"task_id": "task123"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Task not found", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_complete_task_missing_task_id(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "complete_task",
                "arguments": {}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Task ID is required", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_complete_task_service_error(self, mock_get_service, mock_ops_class):
        mock_get_service.side_effect = Exception("Task completion failed")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "complete_task",
                "arguments": {"task_id": "task123"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Task completion failed", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_update_task_status_missing_task_id(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "update_task_status",
                "arguments": {"status": "completed"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Task ID and status are required", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_update_task_status_missing_status(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "update_task_status",
                "arguments": {"task_id": "task123"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("Task ID and status are required", response["error"]["message"])

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_update_task_status_service_error(self, mock_get_service, mock_ops_class):
        mock_get_service.side_effect = Exception("Status update failed")
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "update_task_status",
                "arguments": {
                    "task_id": "task123",
                    "status": "completed"
                }
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32603)
        self.assertIn("Status update failed", response["error"]["message"])

if __name__ == '__main__':
    unittest.main() 