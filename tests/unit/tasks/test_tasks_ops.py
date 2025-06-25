import pytest
from unittest.mock import MagicMock, patch, Mock
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


def test_complete_task_success(tasks_ops, mock_service):
    task_id = 'task_to_complete'
    mock_updated_task = {
        'id': task_id,
        'title': 'Completed task',
        'status': 'completed',
        'completed': '2024-03-25T12:00:00.000Z'
    }
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.update.return_value.execute.return_value = mock_updated_task
    
    result = tasks_ops.complete_task(task_id)
    
    assert result['status'] == 'completed'
    assert result['task']['status'] == 'completed'
    tasks_mock.update.assert_called_once()
    
    call_args = tasks_mock.update.call_args
    assert call_args[1]['tasklist'] == '@default'
    assert call_args[1]['task'] == task_id
    assert call_args[1]['body']['status'] == 'completed'


def test_complete_task_with_custom_tasklist(tasks_ops, mock_service):
    task_id = 'task_to_complete'
    tasklist_id = 'custom_list'
    mock_updated_task = {
        'id': task_id,
        'status': 'completed'
    }
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.update.return_value.execute.return_value = mock_updated_task
    
    result = tasks_ops.complete_task(task_id, tasklist_id)
    
    assert result['status'] == 'completed'
    tasks_mock.update.assert_called_once_with(
        tasklist=tasklist_id,
        task=task_id,
        body={'status': 'completed'}
    )


def test_complete_task_error(tasks_ops, mock_service):
    task_id = 'nonexistent_task'
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.update.return_value.execute.side_effect = Exception('Task not found')
    
    result = tasks_ops.complete_task(task_id)
    
    assert result['status'] == 'error'
    assert 'Task not found' in result['message']


def test_update_task_status_success(tasks_ops, mock_service):
    task_id = 'task_to_update'
    new_status = 'needsAction'
    mock_updated_task = {
        'id': task_id,
        'status': new_status
    }
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.update.return_value.execute.return_value = mock_updated_task
    
    result = tasks_ops.update_task_status(task_id, new_status)
    
    assert result['status'] == 'updated'
    assert result['task']['status'] == new_status
    tasks_mock.update.assert_called_once_with(
        tasklist='@default',
        task=task_id,
        body={'status': new_status}
    )


def test_update_task_status_invalid_status(tasks_ops, mock_service):
    task_id = 'task_to_update'
    invalid_status = 'invalid_status'
    
    result = tasks_ops.update_task_status(task_id, invalid_status)
    
    assert result['status'] == 'error'
    assert 'Invalid status' in result['message']


def test_update_task_status_error(tasks_ops, mock_service):
    task_id = 'nonexistent_task'
    
    tasks_mock = mock_service.tasks.return_value
    tasks_mock.update.return_value.execute.side_effect = Exception('API Error')
    
    result = tasks_ops.update_task_status(task_id, 'completed')
    
    assert result['status'] == 'error'
    assert 'API Error' in result['message'] 