import importlib as _il

_TOOL_NAMES = {"tool_calendar", "tool_ics"}
_SERVER_NAMES = [
    "mcp_server",
    "mcp_handler",
    "mcp_get_handler",
    "mcp_post_handler",
    "mcp_post_other_handler",
    "mcp_post_sse_handler",
    "mcp_stdio_server",
    "stdio_handler",
    "auth_middleware"
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
    raise AttributeError(name)
