import argparse
import sys
import os
from typing import Dict, List, Optional

try:
    from ..core.tasks_auth import get_tasks_service
    from ..core.tasks_ops import TasksOperations
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.core.tasks_auth import get_tasks_service
    from src.core.tasks_ops import TasksOperations


class TasksCLI:
    def __init__(self, tasks_ops: TasksOperations):
        self.tasks_ops = tasks_ops

    def list_tasks(self) -> List[Dict]:
        tasks = self.tasks_ops.list_tasks()
        if not tasks:
            print("No tasks found.")
            return []
        
        print("\nYour Tasks:")
        print("-" * 40)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['text']}")
        print("-" * 40)
        return tasks

    def add_task(self, title: str, notes: Optional[str] = None, due: Optional[str] = None) -> Dict:
        task_data = {'title': title}
        if notes:
            task_data['notes'] = notes
        if due:
            task_data['due'] = due
            
        result = self.tasks_ops.add_task(task_data)
        
        if result['status'] == 'created':
            print(f"✓ Task created: {title}")
        else:
            print(f"✗ Error creating task: {result.get('message', 'Unknown error')}")
            
        return result

    def remove_task(self, task_id: str) -> bool:
        result = self.tasks_ops.remove_task(task_id)
        
        if result:
            print(f"✓ Task removed: {task_id}")
        else:
            print(f"✗ Error removing task: {task_id}")
            
        return result


def main():
    parser = argparse.ArgumentParser(description='Google Tasks CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    list_parser = subparsers.add_parser('list', help='List all tasks')
    
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--notes', help='Task notes/description')
    add_parser.add_argument('--due', help='Due date (ISO format)')
    
    remove_parser = subparsers.add_parser('remove', help='Remove a task')
    remove_parser.add_argument('task_id', help='Task ID to remove')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        service = get_tasks_service()
        tasks_ops = TasksOperations(service)
        cli = TasksCLI(tasks_ops)

        if args.command == 'list':
            cli.list_tasks()
        elif args.command == 'add':
            cli.add_task(args.title, notes=args.notes, due=args.due)
        elif args.command == 'remove':
            cli.remove_task(args.task_id)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main() 