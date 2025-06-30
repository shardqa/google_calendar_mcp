import json
import sys
import os
from typing import Dict
import importlib

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
        caps = {t["name"]: t["inputSchema"] for t in schema["tools"]}
        response["result"] = {
            "serverInfo": {"name": "google_calendar", "version": "1.0.0"},
            "capabilities": {"tools": caps},
            "protocolVersion": supported_protocol_version,
        }
        print(f"Sent initialize response: {json.dumps(response)}", file=sys.stderr)
    elif method == "tools/call":
        tool_name = params.get("tool") or params.get("name")
        tool_args = params.get("args") or params.get("arguments") or {}
        print(f"DEBUG: Tool call received: {tool_name} with args: {tool_args}", file=sys.stderr)
        response.update(_call_tool(tool_name, tool_args))
    else:
        response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Connection", "close")
    handler.end_headers()
    handler.wfile.write(json.dumps(response).encode())

def _call_tool(tool_name: str, args: Dict) -> Dict:
    svc = auth.get_calendar_service()
    if tool_name == "list_events":
        ics_url = args.get("ics_url")
        if not ics_url and args.get("ics_alias"):
            ics_reg = importlib.import_module("src.core.ics_registry")
            ics_url = ics_reg.get(args["ics_alias"])
        if ics_url:
            mr = args.get("max_results", 10)
            ics_ops = importlib.import_module("src.core.ics_ops")
            content = ics_ops.ICSOperations().list_events(ics_url, mr)
            return {"result": {"content": content}}
        return {"result": {"content": list_events(svc, args.get("max_results", 10), args.get("calendar_id", "primary"))}}
    if tool_name == "list_calendars":
        return {"result": {"content": list_calendars(svc)}}
    if tool_name == "add_event":
        if not all(args.get(k) for k in ("summary", "start_time", "end_time")):
            return {"error": {"code": -32602, "message": "Missing required event parameters"}}
        body = {"summary": args["summary"], "start": {"dateTime": args["start_time"]}, "end": {"dateTime": args["end_time"]}}
        for k in ("location", "description"):
            if args.get(k):
                body[k] = args[k]
        res = add_event(svc, body)
        if res.get("status") != "confirmed":
            txt = f"❌ Erro ao criar evento: {res.get('message', 'Erro desconhecido')}"
            return {"result": {"content": [{"type": "text", "text": txt}]}}
        ev = res["event"]
        txt = f"✅ Evento criado com sucesso!\n🆔 ID: {ev.get('id','N/A')}\n📅 {ev.get('summary','Evento')}\n🕐 {ev.get('start',{}).get('dateTime','')} - {ev.get('end',{}).get('dateTime','')}"
        if ev.get("location"):
            txt += f"\n📍 {ev['location']}"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    if tool_name == "remove_event":
        if not args.get("event_id"):
            return {"error": {"code": -32602, "message": "Missing required event parameter: event_id"}}
        ok = remove_event(svc, args["event_id"])
        txt = "✅ Evento removido" if ok else "❌ Erro ao remover evento"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    if tool_name == "edit_event":
        if not args.get("event_id") or not args.get("updated_details"):
            return {"error": {"code": -32602, "message": "Missing required event parameters: event_id, updated_details"}}
        updated = edit_event(svc, args["event_id"], args["updated_details"])
        if not updated:
            txt = f"❌ Falha ao editar {args['event_id']}"
            return {"result": {"content": [{"type": "text", "text": txt}]}}

        txt = f"✅ Evento editado\n🆔 ID: {updated.get('id','N/A')}"
        if updated.get('location'):
            txt += f"\n📍 {updated['location']}"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    if tool_name == "add_recurring_task":
        if not all(args.get(k) for k in ("summary", "frequency", "count", "start_time", "end_time")):
            return {"error": {"code": -32602, "message": "Missing required recurring task parameters"}}
        return {"result": {"content": add_recurring_event(svc, **args)}}
    return _process_tool(tool_name, args) 