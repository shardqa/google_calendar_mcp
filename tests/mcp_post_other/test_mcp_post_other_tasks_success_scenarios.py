import unittest
from unittest.mock import Mock, patch, MagicMock
from src.mcp.mcp_post_other_handler import handle_post_other

class TestMcpPostOtherTasksSuccessScenarios(unittest.TestCase):

    def setUp(self):
        self.handler = Mock()
        self.handler.send_response = Mock()
        self.handler.send_header = Mock()
        self.handler.end_headers = Mock()
        self.handler.wfile = Mock()
        self.handler.wfile.write = Mock()

    @patch('src.mcp.mcp_post_other_handler.sync_tasks_with_calendar')
    @patch('src.mcp.mcp_post_other_handler.auth.get_calendar_service')
    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_list_tasks_success(self, mock_get_service, mock_ops_class, mock_cal_service, mock_sync):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_cal_service.return_value = Mock()
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.list_tasks.return_value = [{"type": "text", "text": "Test task"}]
        
        request = {
            "method": "tools/call",
            "params": {"name": "list_tasks"}
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["content"], [{"type": "text", "text": "Test task"}])
        mock_ops.list_tasks.assert_called_once_with("@default")
        mock_sync.assert_called_once()

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_add_task_basic_success(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.add_task.return_value = {"status": "created", "task": {"id": "123"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "add_task",
                "arguments": {"title": "Test Task"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        mock_ops.add_task.assert_called_once_with({"title": "Test Task"}, "@default")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
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
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        expected_task_data = {
            "title": "Test Task",
            "notes": "Task notes", 
            "due": "2024-12-31T23:59:59Z"
        }
        mock_ops.add_task.assert_called_once_with(expected_task_data, "custom_list")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
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
                "arguments": {"task_id": "task123"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["success"], True)
        mock_ops.remove_task.assert_called_once_with("task123", "@default")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_complete_task_success(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.complete_task.return_value = {"status": "completed", "task": {"id": "task123", "status": "completed"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "complete_task",
                "arguments": {"task_id": "task123"}
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["status"], "completed")
        mock_ops.complete_task.assert_called_once_with("task123", "@default")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_complete_task_with_custom_tasklist(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.complete_task.return_value = {"status": "completed", "task": {"id": "task123"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "complete_task",
                "arguments": {
                    "task_id": "task123",
                    "tasklist_id": "custom_list"
                }
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        mock_ops.complete_task.assert_called_once_with("task123", "custom_list")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_update_task_status_success(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.update_task_status.return_value = {"status": "updated", "task": {"id": "task123", "status": "needsAction"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "update_task_status",
                "arguments": {
                    "task_id": "task123",
                    "status": "needsAction"
                }
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        self.assertEqual(response["result"]["status"], "updated")
        mock_ops.update_task_status.assert_called_once_with("task123", "needsAction", "@default")

    @patch('src.mcp.mcp_post_other_handler.tasks_ops.TasksOperations')
    @patch('src.mcp.mcp_post_other_handler.tasks_auth.get_tasks_service')
    def test_update_task_status_with_custom_tasklist(self, mock_get_service, mock_ops_class):
        mock_service = Mock()
        mock_get_service.return_value = mock_service
        mock_ops = Mock()
        mock_ops_class.return_value = mock_ops
        mock_ops.update_task_status.return_value = {"status": "updated", "task": {"id": "task123"}}
        
        request = {
            "method": "tools/call",
            "params": {
                "name": "update_task_status",
                "arguments": {
                    "task_id": "task123",
                    "status": "completed",
                    "tasklist_id": "custom_list"
                }
            }
        }
        response = {}
        
        handle_post_other(self.handler, request, response)
        
        self.assertIn("result", response)
        mock_ops.update_task_status.assert_called_once_with("task123", "completed", "custom_list")

if __name__ == '__main__':
    unittest.main() 