import pytest
from unittest.mock import MagicMock, patch
from src.core.tasks_ops import TasksOperations


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def tasks_ops(mock_service):
    return TasksOperations(mock_service)


def test_list_tasks_empty_result(tasks_ops, mock_service):
    mock_service.tasks.return_value.list.return_value.execute.return_value = {'items': []}
    result = tasks_ops.list_tasks()
    assert result == []
    mock_service.tasks.assert_called_once()


def test_list_tasks_with_results(tasks_ops, mock_service):
    mock_tasks = {
        'items': [
            {
                'id': 'task1',
                'title': 'Complete project',
                'status': 'needsAction',
                'due': '2024-03-25T10:00:00.000Z'
            },
            {
                'id': 'task2', 
                'title': 'Review code',
                'status': 'needsAction'
            }
        ]
    }
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.list.return_value.execute.return_value = mock_tasks
    
    result = tasks_ops.list_tasks()
    
    assert len(result) == 2
    assert result[0]['type'] == 'text'
    assert result[0]['text'] == 'Complete project'
    assert result[1]['type'] == 'text'
    assert result[1]['text'] == 'Review code'


def test_add_task_success(tasks_ops, mock_service):
    task_data = {
        'title': 'New task',
        'notes': 'Task description',
        'due': '2024-03-25T10:00:00.000Z'
    }
    mock_response = {'id': 'new_task_id', **task_data}
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.insert.return_value.execute.return_value = mock_response
    
    result = tasks_ops.add_task(task_data)
    
    assert result['status'] == 'created'
    assert result['task']['id'] == 'new_task_id'
    tasks_mock.insert.assert_called_once()


def test_add_task_error(tasks_ops, mock_service):
    task_data = {'title': 'New task'}
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.insert.return_value.execute.side_effect = Exception('API Error')
    
    result = tasks_ops.add_task(task_data)
    
    assert result['status'] == 'error'
    assert 'API Error' in result['message']


def test_remove_task_success(tasks_ops, mock_service):
    task_id = 'task_to_remove'
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.delete.return_value.execute.return_value = None
    
    result = tasks_ops.remove_task(task_id)
    
    assert result is True
    tasks_mock.delete.assert_called_once_with(tasklist='@default', task=task_id)


def test_remove_task_error(tasks_ops, mock_service):
    task_id = 'nonexistent_task'
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.delete.return_value.execute.side_effect = Exception('Not found')
    
    result = tasks_ops.remove_task(task_id)
    
    assert result is False


def test_list_tasks_with_custom_tasklist(tasks_ops, mock_service):
    mock_tasks = {'items': [{'id': 'task1', 'title': 'Custom task'}]}
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.list.return_value.execute.return_value = mock_tasks
    
    result = tasks_ops.list_tasks(tasklist_id='custom_list')
    
    tasks_mock.list.assert_called_once_with(tasklist='custom_list', showCompleted=False)
    assert len(result) == 1


def test_list_tasks_exception_handling(tasks_ops, mock_service):
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.list.return_value.execute.side_effect = Exception('API Error')
    
    result = tasks_ops.list_tasks()
    
    assert result == []


def test_add_task_with_custom_tasklist(tasks_ops, mock_service):
    task_data = {'title': 'Custom task'}
    mock_response = {'id': 'task_id', **task_data}
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.insert.return_value.execute.return_value = mock_response
    
    result = tasks_ops.add_task(task_data, tasklist_id='custom_list')
    
    tasks_mock.insert.assert_called_once_with(tasklist='custom_list', body=task_data)
    assert result['status'] == 'created'


def test_remove_task_with_custom_tasklist(tasks_ops, mock_service):
    task_id = 'task_to_remove'
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.delete.return_value.execute.return_value = None
    
    result = tasks_ops.remove_task(task_id, tasklist_id='custom_list')
    
    tasks_mock.delete.assert_called_once_with(tasklist='custom_list', task=task_id)
    assert result is True 