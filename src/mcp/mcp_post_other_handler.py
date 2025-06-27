import json
import sys
import os
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .mcp_schema import get_mcp_schema
from src.core import auth as auth
from src.core import tasks_ops
from src.core import tasks_auth
from src.core.tasks_calendar_sync import sync_tasks_with_calendar
from .other_tool_handlers import process as _process_tool
from src.core.calendar import (
    add_event,
    list_events,
    list_calendars,
    remove_event,
    add_recurring_event,
    edit_event,
)

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
        response_part = _call_tool(tool_name, tool_args)
        response.update(response_part)
    else:
        response["error"] = {"code": -32601, "message": f"Method not found: {method}"}

    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Connection", "close")
    handler.end_headers()
    handler.wfile.write(json.dumps(response).encode())

def _call_tool(tool_name: str, args: Dict) -> Dict:
    service = auth.get_calendar_service()
    if tool_name == 'list_events':
        # Handle ICS URL separately from Google Calendar
        ics_url = args.get("ics_url")
        if not ics_url and args.get("ics_alias"):
            import importlib
            ics_url = importlib.import_module("src.core.ics_registry").get(args["ics_alias"])
        if ics_url:
            import importlib
            max_results = args.get("max_results", 10)
            content = importlib.import_module("src.core.ics_ops").ICSOperations().list_events(ics_url, max_results)
            return {"result": {"content": content}}
        else:
            return {"result": {"content": list_events(service, args.get("max_results", 10), args.get("calendar_id", "primary"))}}
    elif tool_name == 'list_calendars':
        return {"result": {"content": list_calendars(service)}}
    elif tool_name == 'add_event':
        if not all(args.get(k) for k in ("summary", "start_time", "end_time")):
            return {"error": {"code": -32602, "message": "Missing required event parameters"}}
        body = {"summary": args.get("summary"), "start": {"dateTime": args.get("start_time")}, "end": {"dateTime": args.get("end_time")}}
        for k in ("location", "description"):
            if args.get(k):
                body[k] = args[k]
        return {"result": {"content": add_event(service, body)}}
    elif tool_name == 'remove_event':
        if not args.get('event_id'):
            return {"error": {"code": -32602, "message": "Missing required event parameter: event_id"}}
        return {"result": {"content": remove_event(service, args.get('event_id'))}}
    elif tool_name == 'edit_event':
        if not args.get('event_id') or not args.get('updated_details'):
            return {"error": {"code": -32602, "message": "Missing required event parameters: event_id, updated_details"}}
        return {"result": {"content": edit_event(service, args.get('event_id'), args.get('updated_details'))}}
    elif tool_name == 'add_recurring_task': # Note: task in name, but event in reality
        if not all(args.get(k) for k in ("summary", "frequency", "count", "start_time", "end_time")):
            return {"error": {"code": -32602, "message": "Missing required recurring task parameters"}}
        return {"result": {"content": add_recurring_event(service, **args)}}
    else:
        # Fallback to other tool handlers for non-calendar tools
        return _process_tool(tool_name, args) 