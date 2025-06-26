import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .mcp_schema import get_mcp_schema
import calendar_ops
from src.core import auth as auth
from src.core import tasks_ops
from src.core import tasks_auth
from src.core.tasks_calendar_sync import sync_tasks_with_calendar
from .other_tool_handlers import process as _process_tool

def handle_post_other(handler, request, response):
    method = request.get("method")
    params = request.get("params", {})
    if method == "initialize":
        schema = get_mcp_schema()
        supported_protocol_version = schema.get("protocol", "2025-03-26")
        capabilities_tools = {tool["name"]: tool["inputSchema"] for tool in schema["tools"]}
        response["result"] = {"serverInfo": {"name": "google_calendar", "version": "1.0.0"}, "capabilities": {"tools": capabilities_tools}, "protocolVersion": supported_protocol_version}
        print(f"Sent initialize response: {json.dumps(response)}")
    elif method == "tools/call":
        tool_name = params.get("tool") or params.get("name")
        tool_args = params.get("args") or params.get("arguments") or {}
        print(f"DEBUG: Tool call received: {tool_name} with args: {tool_args}")
        response_part = _process_tool(tool_name, tool_args)
        response.update(response_part)
    else:
        response["error"] = {"code": -32601, "message": f"Method not found: {method}"}

    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Connection", "close")
    handler.end_headers()
    handler.wfile.write(json.dumps(response).encode()) 