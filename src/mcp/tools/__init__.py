from importlib import import_module as _imp
import sys as _sys

for _name in ("tool_calendar", "tool_tasks", "tool_echo", "tool_ics"):
    _mod = _imp(f"src.mcp.tools.{_name}")
    _sys.modules[f"src.mcp.{_name}"] = _mod
    globals()[_name] = _mod 