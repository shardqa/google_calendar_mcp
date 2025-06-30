from __future__ import annotations
from typing import Any, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import auth as auth

from .tools import tool_echo as _echo
from .tools import tool_calendar as _cal
from .tools import tool_tasks as _tasks
from .tools import tool_ics as _ics

_modules = [_echo, _cal, _tasks, _ics]


def _dispatch(name: str, args: Dict[str, Any]):
    for mod in _modules:
        handler = getattr(mod, "handle", None)
        if handler:  # pragma: no branch
            result = handler(name, args)
            if result is not None:
                return result
    return None  # pragma: no cover


def process(tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
    """Return response dict for a given tool call."""
    # fast-path for simple echo to avoid auth/service imports
    if tool_name == "echo":
        return _echo.handle(tool_name, tool_args)  # type: ignore[arg-type]

    # calendar shortcuts kept here to reuse existing calendar_ops integration
    if tool_name in {"list_events", "add_event", "remove_event", "list_calendars", "edit_event", "add_recurring_task"}:
        return _cal.handle(tool_name, tool_args)  # type: ignore[arg-type]

    dispatched = _dispatch(tool_name, tool_args)
    if dispatched is not None:
        return dispatched

    return {"error": {"code": -32601, "message": f"Tool not found: {tool_name}"}} 