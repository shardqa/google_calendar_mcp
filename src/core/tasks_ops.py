from typing import List, Dict, Optional

class TasksOperations:
    def __init__(self, service):
        self.service = service

    def list_tasks(self, tasklist_id: str = '@default') -> List[Dict]:
        try:
            tasks_result = self.service.tasks().list(
                tasklist=tasklist_id,
                showCompleted=False
            ).execute()
            
            tasks = tasks_result.get('items', [])
            formatted_tasks = []
            
            for task in tasks:
                title = task.get('title', 'No Title')
                formatted_tasks.append({"type": "text", "text": title})
                
            return formatted_tasks
        except Exception:
            return []

    def add_task(self, task_data: Dict, tasklist_id: str = '@default') -> Dict:
        try:
            task = self.service.tasks().insert(
                tasklist=tasklist_id,
                body=task_data
            ).execute()
            return {'status': 'created', 'task': task}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def remove_task(self, task_id: str, tasklist_id: str = '@default') -> bool:
        try:
            self.service.tasks().delete(
                tasklist=tasklist_id,
                task=task_id
            ).execute()
            return True
        except Exception:
            return False 

    def complete_task(self, task_id: str, tasklist_id: str = '@default') -> Dict:
        try:
            task = self.service.tasks().update(
                tasklist=tasklist_id,
                task=task_id,
                body={'status': 'completed'}
            ).execute()
            return {'status': 'completed', 'task': task}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_task_status(self, task_id: str, status: str, tasklist_id: str = '@default') -> Dict:
        valid_statuses = ['needsAction', 'completed']
        if status not in valid_statuses:
            return {'status': 'error', 'message': f'Invalid status. Must be one of: {valid_statuses}'}
        
        try:
            task = self.service.tasks().update(
                tasklist=tasklist_id,
                task=task_id,
                body={'status': status}
            ).execute()
            return {'status': 'updated', 'task': task}
        except Exception as e:
            return {'status': 'error', 'message': str(e)} 