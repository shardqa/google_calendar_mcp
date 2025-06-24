from __future__ import annotations
from typing import Dict, Any
from importlib import import_module

parent = import_module('src.mcp.mcp_post_sse_handler')  # late import to access patched vars during tests

_ERR = lambda c, m: {"error": {"code": c, "message": m}}

def handle(name: str, a: Dict[str, Any]):
    try:
        ops_cls = getattr(parent, 'tasks_ops').TasksOperations  # type: ignore[attr-defined]
        svc = getattr(parent, 'tasks_auth').get_tasks_service()  # type: ignore[attr-defined]
        ops = ops_cls(svc)
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

    if name == 'list_tasks':
        return {'result': {'content': ops.list_tasks(a.get('tasklist_id', '@default'))}}

    if name == 'add_task':
        title = a.get('title')
        if not title:
            return _ERR(-32602, 'Task title is required')
        data = {'title': title}
        if a.get('notes'):
            data['notes'] = a['notes']
        if a.get('due'):
            data['due'] = a['due']
        res = ops.add_task(data, a.get('tasklist_id', '@default'))
        if res.get('status') == 'created':
            t = res['task']
            msg = f"✅ Tarefa criada com sucesso!\n🆔 ID: {t.get('id','N/A')}\n✏️ {t.get('title','Tarefa')}" + (f"\n📅 Due: {t['due']}" if t.get('due') else '')
            res['content'] = [{"type": "text", "text": msg}]
        return {'result': res}

    tid = a.get('task_id');status = a.get('status');tl = a.get('tasklist_id', '@default')
    if name in {'update_task_status'} and (not tid or not status):
        return _ERR(-32602, 'Task ID and status are required')
    if not tid:
        return _ERR(-32602, 'Task ID is required')

    if name == 'remove_task':
        return {'result': {'success': ops.remove_task(tid, tl)}}
    if name == 'complete_task':
        return {'result': ops.complete_task(tid, tl)}
    if name == 'update_task_status':
        return {'result': ops.update_task_status(tid, status, tl)}
    return None  # pragma: no cover 