import json
import sys
import os
from importlib import import_module

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .mcp_schema import get_mcp_schema
import calendar_ops
import auth
from core import tasks_auth, tasks_ops
from . import sse_tasks as _tasks

_ERR = lambda c, m: {"error": {"code": c, "message": m}}

def _process_tool(name, args):
    if name == "echo":
        return {"result": {"content": [{"type": "text", "text": f"🔊 Echo: {args.get('message', 'No message provided')}"}]}}
    if name == "list_events":
        svc = auth.get_calendar_service()
        mr = args.get("max_results", 10)
        ics = args.get("ics_url") or (args.get("ics_alias") and import_module("core.ics_registry").get(args["ics_alias"]))
        cont = import_module("core.ics_ops").ICSOperations().list_events(ics, mr) if ics else calendar_ops.CalendarOperations(svc).list_events(mr)
        return {"result": {"content": cont}}
    if name == "list_calendars":
        return {"result": {"content": calendar_ops.CalendarOperations(auth.get_calendar_service()).list_calendars()}}
    if name == "add_event":
        if not all(args.get(k) for k in ("summary", "start_time", "end_time")):
            return _ERR(-32602, "Missing required event parameters")
        body = {"summary": args["summary"], "start": {"dateTime": args["start_time"]}, "end": {"dateTime": args["end_time"]}}
        for k in ("location", "description"):
            if args.get(k):
                body[k] = args[k]
        res = calendar_ops.CalendarOperations(auth.get_calendar_service()).add_event(body)
        if res.get("status") != "confirmed":
            return {"result": {"content": [{"type": "text", "text": f"❌ Erro ao criar evento: {res.get('message', 'Erro desconhecido')}"}]}}
        ev = res["event"]
        txt = f"✅ Evento criado com sucesso!\n📅 {ev.get('summary', 'Evento')}\n🕐 {ev.get('start', {}).get('dateTime', 'N/A')} - {ev.get('end', {}).get('dateTime', 'N/A')}"
        if ev.get("location"):
            txt += f"\n📍 {ev['location']}"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    if name == "remove_event":
        eid = args.get("event_id")
        return _ERR(-32602, "Event ID is required") if not eid else {"result": {"success": calendar_ops.CalendarOperations(auth.get_calendar_service()).remove_event(eid)}}
    if name == "add_recurring_task":
        if not all(args.get(k) for k in ("summary", "frequency", "count", "start_time", "end_time")):
            return _ERR(-32602, "Missing required recurring task parameters")
        r = calendar_ops.CalendarOperations(auth.get_calendar_service()).add_recurring_event(
            summary=args["summary"], frequency=args["frequency"], count=args["count"], start_time=args["start_time"], end_time=args["end_time"], location=args.get("location"), description=args.get("description"))
        return {"result": r}
    # tasks block
    if name in {"list_tasks", "add_task", "remove_task", "complete_task", "update_task_status"}:
        try:
            res=_tasks.handle(name, args)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return _ERR(-32603, f"Tasks service error: {e}")  # pragma: no cover
        return res if res is not None else _ERR(-32603, "Unknown tasks outcome")  # pragma: no cover
    if name == "schedule_tasks":
        try:
            from core.scheduling_engine import SchedulingEngine
            if not all(args.get(k) for k in ("time_period", "work_hours_start", "work_hours_end")):
                return _ERR(-32602, "Missing required scheduling parameters")  # pragma: no cover
            eng = SchedulingEngine(auth.get_calendar_service(), tasks_auth.get_tasks_service())
            return {"result": eng.propose_schedule(time_period=args["time_period"], work_hours_start=args["work_hours_start"], work_hours_end=args["work_hours_end"], max_task_duration=args.get("max_task_duration", 120))}
        except Exception as e:
            return _ERR(-32603, f"Scheduling service error: {e}")  # pragma: no cover
    if name == "register_ics_calendar":
        alias, url = args.get("alias"), args.get("ics_url")
        if not alias or not url:
            return _ERR(-32602, "alias and ics_url are required")
        import_module("core.ics_registry").register(alias, url)
        return {"result": {"registered": True, "content": [{"type": "text", "text": f"✅ Calendário ICS registrado com sucesso!\n🔖 Alias: {alias}"}]}}
    if name == "list_ics_calendars":
        return {"result": {"calendars": import_module("core.ics_registry").list_all()}}
    return _ERR(-32601, f"Tool not found: {name}")  # pragma: no cover

def handle_post_sse(handler, request, response):
    m = request.get("method")
    p = request.get("params", {})
    _hdr = lambda: (handler.send_response(200), handler.send_header("Content-Type", "application/json"), handler.send_header("Access-Control-Allow-Origin", "*"), handler.send_header("Connection", "close"), handler.end_headers())
    if m in {"mcp/cancel", "$/cancelRequest"}:
        if m == "mcp/cancel":
            response["result"] = {"cancelled": True}
        _hdr()
        handler.wfile.write(b"{}" if m == "$/cancelRequest" else json.dumps(response).encode())
        return
    if m == "notifications/cancelled":
        _hdr()
        return
    if m in {"$/toolList", "tools/list"}:
        response["result"] = {"tools": get_mcp_schema()["tools"]}
    elif m == "initialize":
        sch = get_mcp_schema()
        response["result"] = {"serverInfo": {"name": "google_calendar", "version": "1.0.0"}, "capabilities": {"tools": {t["name"]: t["inputSchema"] for t in sch["tools"]}}, "protocolVersion": sch.get("protocol", "2025-03-26")}
    elif m == "tools/call":
        name = p.get("tool") or p.get("name")
        args = p.get("args") or p.get("arguments") or {}
        response.update(_process_tool(name, args))
    else:
        response.update(_ERR(-32601, f"Method not found: {m}"))
    _hdr()
    handler.wfile.write(json.dumps(response).encode()) 