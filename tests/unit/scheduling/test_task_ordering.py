import pytest
from datetime import datetime, timedelta

from src.core.task_ordering import order_tasks


def test_order_tasks_by_due_and_importance():
    tasks = [
        {
            'id': '1',
            'title': '[1] Low due sooner',
            'due': '2024-03-22T09:00:00Z'
        },
        {
            'id': '2',
            'title': '[3] High due later',
            'due': '2024-03-23T09:00:00Z'
        },
        {
            'id': '3',
            'title': '[3] High due sooner',
            'due': '2024-03-22T09:00:00Z'
        },
        {
            'id': '4',
            'title': '[2] Medium no due'
        }
    ]

    ordered = order_tasks(tasks)

    assert [t['id'] for t in ordered] == ['3', '1', '2', '4'] 