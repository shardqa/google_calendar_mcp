from typing import Dict, Any
from importlib import import_module
from ..core import auth as auth
from .mcp_post_other_handler import tasks_auth, tasks_ops

__all__ = ["handle"]

_ERR = lambda code, msg: {"error": {"code": code, "message": msg}}

def _sync(calendar_service, tasks_service):
    mph = import_module("src.mcp.mcp_post_other_handler")
    mph.sync_tasks_with_calendar(calendar_service, tasks_service)

def _build_confirm(task: Dict[str, Any]):
    txt = f"✅ Tarefa criada com sucesso!\n🆔 ID: {task.get('id','N/A')}\n✏️ {task.get('title','Tarefa')}"
    if task.get("due"):  # pragma: no branch
        txt += f"\n📅 Due: {task['due']}"  # pragma: no cover
    return {"content": [{"type": "text", "text": txt}]}

def _list_tasks(args):
    try:
        svc = tasks_auth.get_tasks_service()
        _sync(auth.get_calendar_service(), svc)
        tlist = args.get("tasklist_id", "@default")
        content = tasks_ops.TasksOperations(svc).list_tasks(tlist)
        return {"result": {"content": content}}
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

def _add_task(args):
    title = args.get("title")
    if not title:
        return _ERR(-32602, "Task title is required")
    body = {"title": title}
    for k in ("notes", "due"):
        if args.get(k):
            body[k] = args[k]
    tlist = args.get("tasklist_id", "@default")
    try:
        svc = tasks_auth.get_tasks_service()
        res = tasks_ops.TasksOperations(svc).add_task(body, tlist)
        if res.get("status") == "created":
            res.update(_build_confirm(res["task"]))
        return {"result": res}
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

def _remove_task(args):
    tid = args.get("task_id")
    if not tid:
        return _ERR(-32602, "Task ID is required")
    tlist = args.get("tasklist_id", "@default")
    try:
        ok = tasks_ops.TasksOperations(tasks_auth.get_tasks_service()).remove_task(tid, tlist)
        return {"result": {"success": ok}}
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

def _complete_task(args):
    tid = args.get("task_id")
    if not tid:
        return _ERR(-32602, "Task ID is required")
    tlist = args.get("tasklist_id", "@default")
    try:
        res = tasks_ops.TasksOperations(tasks_auth.get_tasks_service()).complete_task(tid, tlist)
        return {"result": res}
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

def _update_status(args):
    tid = args.get("task_id")
    status = args.get("status")
    if not tid or not status:
        return _ERR(-32602, "Task ID and status are required")
    tlist = args.get("tasklist_id", "@default")
    try:
        res = tasks_ops.TasksOperations(tasks_auth.get_tasks_service()).update_task_status(tid, status, tlist)
        return {"result": res}
    except Exception as e:
        return _ERR(-32603, f"Tasks service error: {e}")

_mapping = {
    "list_tasks": _list_tasks,
    "add_task": _add_task,
    "remove_task": _remove_task,
    "complete_task": _complete_task,
    "update_task_status": _update_status,
}

def handle(tool: str, args: Dict[str, Any]):
    func = _mapping.get(tool)
    return func(args) if func else None  # pragma: no cover 