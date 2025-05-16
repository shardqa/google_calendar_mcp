import json
from .mcp_schema import get_mcp_schema
from . import calendar_ops, auth

def handle_post_sse(handler, request, response):
    method = request.get("method")
    params = request.get("params", {})
    if method == "mcp/cancel" or method == "$/cancelRequest":
        cancel_id = params.get("id") if isinstance(params, dict) else None
        print(f"Received cancellation request/notification with ID: {request.get('id')}, for operation ID: {cancel_id}")
        if method == "mcp/cancel":
            response["result"] = {"cancelled": True}
            print(f"Sending cancellation response: {json.dumps(response)}")
        else:
            handler.send_response(200)
            handler.send_header("Content-Type", "application/json")
            handler.send_header("Access-Control-Allow-Origin", "*")
            handler.send_header("Connection", "close")
            handler.end_headers()
            handler.wfile.write(b"{}")
            return
    elif method == "notifications/cancelled":
        cancel_id = params.get("requestId") if isinstance(params, dict) else None
        print(f"Received cancellation notification for operation ID: {cancel_id}")
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.send_header("Connection", "close")
        handler.end_headers()
        return
    elif method == "$/toolList" or method == "tools/list":
        schema = get_mcp_schema()
        response["result"] = {"tools": schema["tools"]}
        print(f"Sent tools list response: {json.dumps(response)[:100]}...")
    elif method == "initialize":
        schema = get_mcp_schema()
        supported_protocol_version = schema.get("protocol", "2025-03-26")
        capabilities_tools = {tool["name"]: tool["inputSchema"] for tool in schema["tools"]}
        response["result"] = {"serverInfo": {"name": "google_calendar", "version": "1.0.0"}, "capabilities": {"tools": capabilities_tools}, "protocolVersion": supported_protocol_version}
        print(f"Sent initialize response: {json.dumps(response)}")
    elif method == "tools/call":
        tool_name = params.get("tool") or params.get("name")
        tool_args = params.get("args") or params.get("arguments") or {}
        if tool_name == "echo":
            message = tool_args.get("message", "No message provided")
            print(f"Echoing message via tools/call: {message}")
            response["result"] = {"echo": message}
        elif tool_name == "list_events":
            service = auth.get_calendar_service()
            max_results = tool_args.get("max_results", 10)
            response["result"] = calendar_ops.CalendarOperations(service).list_events(max_results)
        elif tool_name == "add_event":
            service = auth.get_calendar_service()
            summary = tool_args.get("summary")
            location = tool_args.get("location")
            description = tool_args.get("description")
            start_time = tool_args.get("start_time")
            end_time = tool_args.get("end_time")
            if not all([summary, start_time, end_time]):
                response["error"] = {"code": -32602, "message": "Missing required event parameters"}
            else:
                ops = calendar_ops.CalendarOperations(service)
                event_data = {"summary": summary, "start": {"dateTime": start_time}, "end": {"dateTime": end_time}}
                if location: event_data["location"] = location
                if description: event_data["description"] = description
                response["result"] = ops.add_event(event_data)
        elif tool_name == "remove_event":
            service = auth.get_calendar_service()
            event_id = tool_args.get("event_id")
            if not event_id:
                response["error"] = {"code": -32602, "message": "Event ID is required"}
            else:
                ops = calendar_ops.CalendarOperations(service)
                response["result"] = {"success": ops.remove_event(event_id)}
        else:
            response["error"] = {"code": -32601, "message": f"Tool not found: {tool_name}"}
    else:
        response["error"] = {"code": -32601, "message": f"Method not found: {method}"}

    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Connection", "close")
    handler.end_headers()
    handler.wfile.write(json.dumps(response).encode()) 