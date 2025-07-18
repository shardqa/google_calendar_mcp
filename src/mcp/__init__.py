import importlib as _il

_TOOL_NAMES = {"tool_calendar", "tool_ics"}
_SERVER_NAMES = [
    "mcp_handler",
    "mcp_get_handler",
    "mcp_post_handler",
    "mcp_post_sse_handler",
    "auth_middleware"
]

_HANDLER_NAMES = [
    "mcp_post_other_handler",
    "stdio_handler"
]

_SERVER_CLASS_NAMES = [
    "mcp_server",
    "mcp_stdio_server"
]


def __getattr__(name):
    if name in _TOOL_NAMES:
        mod = _il.import_module(f"src.mcp.tools.{name}")
        globals()[name] = mod
        return mod
    elif name in _SERVER_NAMES:
        mod = _il.import_module(f"src.mcp.{name}")
        globals()[name] = mod
        return mod
    elif name in _HANDLER_NAMES:
        mod = _il.import_module(f"src.mcp.handlers.{name}")
        globals()[name] = mod
        return mod
    elif name in _SERVER_CLASS_NAMES:
        mod = _il.import_module(f"src.mcp.servers.{name}")
        globals()[name] = mod
        return mod
    raise AttributeError(name)
