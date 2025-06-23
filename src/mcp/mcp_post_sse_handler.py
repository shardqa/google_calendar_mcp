import json
from .mcp_schema import get_mcp_schema
from .. import calendar_ops, auth
from ..core import tasks_auth, tasks_ops

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
            response["result"] = {"content": [{"type": "text", "text": f"🔊 Echo: {message}"}]}
        elif tool_name == "list_events":
            service = auth.get_calendar_service()
            max_results = tool_args.get("max_results", 10)
            response["result"] = {"content": calendar_ops.CalendarOperations(service).list_events(max_results)}
        elif tool_name == "list_calendars":
            service = auth.get_calendar_service()
            ops = calendar_ops.CalendarOperations(service)
            response["result"] = {"content": ops.list_calendars()}
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
                result = ops.add_event(event_data)
                if result.get('status') == 'confirmed':
                    event = result.get('event', {})
                    summary = event.get('summary', 'Evento criado')
                    start_time = event.get('start', {}).get('dateTime', 'N/A')
                    end_time = event.get('end', {}).get('dateTime', 'N/A')
                    location = event.get('location', '')
                    
                    event_text = f"✅ Evento criado com sucesso!\n📅 {summary}\n🕐 {start_time} - {end_time}"
                    if location:
                        event_text += f"\n📍 {location}"
                    
                    response["result"] = {"content": [{"type": "text", "text": event_text}]}
                else:
                    response["result"] = {"content": [{"type": "text", "text": f"❌ Erro ao criar evento: {result.get('message', 'Erro desconhecido')}"}]}
        elif tool_name == "remove_event":
            service = auth.get_calendar_service()
            event_id = tool_args.get("event_id")
            if not event_id:
                response["error"] = {"code": -32602, "message": "Event ID is required"}
            else:
                ops = calendar_ops.CalendarOperations(service)
                response["result"] = {"success": ops.remove_event(event_id)}
        elif tool_name == "list_tasks":
            try:
                service = tasks_auth.get_tasks_service()
                tasklist_id = tool_args.get("tasklist_id", "@default")
                ops = tasks_ops.TasksOperations(service)
                response["result"] = {"content": ops.list_tasks(tasklist_id)}
            except Exception as e:
                response["error"] = {"code": -32603, "message": f"Tasks service error: {str(e)}"}
        elif tool_name == "add_task":
            try:
                service = tasks_auth.get_tasks_service()
                title = tool_args.get("title")
                if not title:
                    response["error"] = {"code": -32602, "message": "Task title is required"}
                else:
                    task_data = {"title": title}
                    if tool_args.get("notes"):
                        task_data["notes"] = tool_args.get("notes")
                    if tool_args.get("due"):
                        task_data["due"] = tool_args.get("due")
                    
                    tasklist_id = tool_args.get("tasklist_id", "@default")
                    ops = tasks_ops.TasksOperations(service)
                    response["result"] = ops.add_task(task_data, tasklist_id)
            except Exception as e:
                response["error"] = {"code": -32603, "message": f"Tasks service error: {str(e)}"}
        elif tool_name == "remove_task":
            try:
                service = tasks_auth.get_tasks_service()
                task_id = tool_args.get("task_id")
                if not task_id:
                    response["error"] = {"code": -32602, "message": "Task ID is required"}
                else:
                    tasklist_id = tool_args.get("tasklist_id", "@default")
                    ops = tasks_ops.TasksOperations(service)
                    response["result"] = {"success": ops.remove_task(task_id, tasklist_id)}
            except Exception as e:
                response["error"] = {"code": -32603, "message": f"Tasks service error: {str(e)}"}
        elif tool_name == "add_recurring_task":
            service = auth.get_calendar_service()
            summary = tool_args.get("summary")
            frequency = tool_args.get("frequency")
            count = tool_args.get("count")
            start_time = tool_args.get("start_time")
            end_time = tool_args.get("end_time")
            location = tool_args.get("location")
            description = tool_args.get("description")
            
            if not all([summary, frequency, count, start_time, end_time]):
                response["error"] = {"code": -32602, "message": "Missing required recurring task parameters"}
            else:
                ops = calendar_ops.CalendarOperations(service)
                response["result"] = ops.add_recurring_event(
                    summary=summary,
                    frequency=frequency,
                    count=count,
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                    description=description
                )
        elif tool_name == "schedule_tasks":
            try:
                from ..core.scheduling_engine import SchedulingEngine
                
                calendar_service = auth.get_calendar_service()
                tasks_service = tasks_auth.get_tasks_service()
                
                time_period = tool_args.get("time_period")
                work_hours_start = tool_args.get("work_hours_start")
                work_hours_end = tool_args.get("work_hours_end")
                max_task_duration = tool_args.get("max_task_duration", 120)
                
                if not all([time_period, work_hours_start, work_hours_end]):
                    response["error"] = {"code": -32602, "message": "Missing required scheduling parameters"}
                else:
                    engine = SchedulingEngine(calendar_service, tasks_service)
                    result = engine.propose_schedule(
                        time_period=time_period,
                        work_hours_start=work_hours_start,
                        work_hours_end=work_hours_end,
                        max_task_duration=max_task_duration
                    )
                    response["result"] = result
            except Exception as e:
                response["error"] = {"code": -32603, "message": f"Scheduling service error: {str(e)}"}
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