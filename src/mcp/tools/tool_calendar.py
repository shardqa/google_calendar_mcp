from typing import Dict, Any
from importlib import import_module
from src.core import auth as auth

__all__ = ["handle"]


def _cal_ops():
    return getattr(import_module("src.mcp.mcp_post_other_handler"), "calendar_ops")


def _list_events(args):
    mr = args.get("max_results", 10)
    ics_url = args.get("ics_url")
    if not ics_url and args.get("ics_alias"):
        from src.core.ics_registry import get as _get_ics
        ics_url = _get_ics(args["ics_alias"])
    if ics_url:
        from src.core.ics_ops import ICSOperations
        content = ICSOperations().list_events(ics_url, mr)
    else:
        svc = auth.get_calendar_service()
        cid = args.get("calendar_id", "primary")
        content = _cal_ops().CalendarOperations(svc).list_events(mr, cid)
        if args.get("with_ics"):
            try:
                from src.core.ics_registry import list_all as _ics_list
                from src.core.ics_ops import ICSOperations
                for _url in _ics_list().values():
                    content.extend(ICSOperations().list_events(_url, mr))
            except Exception:
                pass
    return {"result": {"content": content}}


def _list_calendars():
    svc = auth.get_calendar_service()
    return {"result": {"content": _cal_ops().CalendarOperations(svc).list_calendars()}}


def _add_event(args):
    svc = auth.get_calendar_service()
    if not all([args.get("summary"), args.get("start_time"), args.get("end_time")]):
        return {"error": {"code": -32602, "message": "Missing required event parameters"}}
    body = {"summary": args["summary"], "start": {"dateTime": args["start_time"]}, "end": {"dateTime": args["end_time"]}}
    for k in ("location", "description"):
        if args.get(k):
            body[k] = args[k]
    res = _cal_ops().CalendarOperations(svc).add_event(body)
    if res.get("status") != "confirmed":
        msg = res.get("message", "Erro desconhecido")
        return {"result": {"content": [{"type": "text", "text": f"❌ Erro ao criar evento: {msg}"}]}}
    ev = res["event"]
    txt = (f"✅ Evento criado com sucesso!\n🆔 ID: {ev.get('id','N/A')}\n📅 {ev.get('summary','Evento')}\n"
           f"🕐 {ev.get('start',{}).get('dateTime','')} - {ev.get('end',{}).get('dateTime','')}")
    if ev.get("location"):
        txt += f"\n📍 {ev['location']}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def _remove_event(args):
    eid = args.get("event_id")
    if not eid:
        return {"error": {"code": -32602, "message": "Event ID is required"}}
    ok = _cal_ops().CalendarOperations(auth.get_calendar_service()).remove_event(eid)
    txt = f"✅ Evento removido com sucesso!\n🆔 ID: {eid}" if ok else f"❌ Erro ao remover evento {eid}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def _add_recurring(args):
    if not all(args.get(k) for k in ["summary", "frequency", "count", "start_time", "end_time"]):
        return {"error": {"code": -32602, "message": "Missing required recurring task parameters"}}
    ops = _cal_ops().CalendarOperations(auth.get_calendar_service())
    return {"result": ops.add_recurring_event(
        summary=args["summary"],
        frequency=args["frequency"],
        count=args["count"],
        start_time=args["start_time"],
        end_time=args["end_time"],
        location=args.get("location"),
        description=args.get("description"),
    )}


def _edit_event(args):
    eid, details = args.get("event_id"), args.get("updated_details")
    if not eid or not details:
        return {"error": {"code": -32602, "message": "event_id and updated_details are required."}}
    updated = _cal_ops().CalendarOperations(auth.get_calendar_service()).edit_event(eid, details)
    if not updated:
        return {"error": {"code": -32603, "message": f"Failed to edit event {eid}."}}
    txt = f"✅ Evento editado com sucesso!\n🆔 ID: {eid}"
    if updated.get("location"):
        txt += f"\n📍 {updated['location']}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def handle(name: str, args: Dict[str, Any]):
    mp = {
        "list_events": _list_events,
        "list_calendars": lambda a: _list_calendars(),
        "add_event": _add_event,
        "remove_event": _remove_event,
        "add_recurring_task": _add_recurring,
        "edit_event": _edit_event,
    }
    fn = mp.get(name)
    return fn(args) if fn else None 