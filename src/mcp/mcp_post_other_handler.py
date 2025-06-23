import json
from .mcp_schema import get_mcp_schema
from .. import calendar_ops
from ..core import auth as auth
from ..core import tasks_auth, tasks_ops
from ..core.tasks_calendar_sync import sync_tasks_with_calendar

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
        if tool_name == "echo":
            message = tool_args.get("message", "No message provided")
            print(f"Echoing message via tools/call: {message}")
            response["result"] = {"content": [{"type": "text", "text": f"🔊 Echo: {message}"}]}
        elif tool_name == "list_events":
            service = auth.get_calendar_service()
            max_results = tool_args.get("max_results", 10)
            calendar_id = tool_args.get("calendar_id", "primary")
            response["result"] = {"content": calendar_ops.CalendarOperations(service).list_events(max_results, calendar_id)}
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
                    
                    event_id = event.get('id', 'N/A')
                    event_text = f"✅ Evento criado com sucesso!\n🆔 ID: {event_id}\n📅 {summary}\n🕐 {start_time} - {end_time}"
                    if location:
                        event_text += f"\n📍 {location}"
                    
                    response["result"] = {"content": [{"type": "text", "text": event_text}]}
                else:
                    response["result"] = {"content": [{"type": "text", "text": f"❌ Erro ao criar evento: {result.get('message', 'Erro desconhecido')}"}]}
        elif tool_name == "list_calendars":
            service = auth.get_calendar_service()
            ops = calendar_ops.CalendarOperations(service)
            response["result"] = {"content": ops.list_calendars()}
        elif tool_name == "remove_event":
            service = auth.get_calendar_service()
            event_id = tool_args.get("event_id")
            if not event_id:
                response["error"] = {"code": -32602, "message": "Event ID is required"}
            else:
                ops = calendar_ops.CalendarOperations(service)
                success = ops.remove_event(event_id)
                if success:
                    event_text = f"✅ Evento removido com sucesso!\n🆔 ID: {event_id}"
                    response["result"] = {"content": [{"type": "text", "text": event_text}]}
                else:
                    response["result"] = {"content": [{"type": "text", "text": f"❌ Erro ao remover evento {event_id}"}]}
        elif tool_name == "edit_event":
            service = auth.get_calendar_service()
            event_id = tool_args.get("event_id")
            updated_details = tool_args.get("updated_details")
            if not event_id or not updated_details:
                response["error"] = {"code": -32602, "message": "event_id and updated_details are required."}
            else:
                ops = calendar_ops.CalendarOperations(service)
                updated_event = ops.edit_event(event_id, updated_details)
                if updated_event:
                    # Format response similar to add_event
                    summary = updated_event.get('summary', 'Evento editado')
                    start_time = updated_event.get('start', {}).get('dateTime', 'N/A')
                    end_time = updated_event.get('end', {}).get('dateTime', 'N/A')
                    location = updated_event.get('location', '')
                    
                    event_text = f"✅ Evento editado com sucesso!\n🆔 ID: {event_id}\n📅 {summary}\n🕐 {start_time} - {end_time}"
                    if location:
                        event_text += f"\n📍 {location}"
                    
                    response["result"] = {"content": [{"type": "text", "text": event_text}]}
                else:
                    response["error"] = {"code": -32603, "message": f"Failed to edit event {event_id}."}
        elif tool_name == "list_tasks":
            try:
                service = tasks_auth.get_tasks_service()
                # Keep calendar and tasks in sync
                sync_tasks_with_calendar(auth.get_calendar_service(), service)
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