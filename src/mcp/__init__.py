import importlib as _il

_TOOL_NAMES = {"tool_calendar", "tool_tasks", "tool_echo", "tool_ics"}


def __getattr__(name):
    if name in _TOOL_NAMES:
        mod = _il.import_module(f"src.mcp.tools.{name}")
        globals()[name] = mod
        return mod
    raise AttributeError(name)
