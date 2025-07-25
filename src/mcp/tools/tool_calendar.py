from typing import Dict, Any
from importlib import import_module
from src.core import auth as auth
from src.core.calendar import (
    list_events,
    add_event,
    remove_event,
    edit_event,
)

__all__ = ["handle"]


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
        content = list_events(svc, mr, cid)
        if args.get("with_ics"):
            try:
                from src.core.ics_registry import list_all as _ics_list
                from src.core.ics_ops import ICSOperations
                for _url in _ics_list().values():
                    content.extend(ICSOperations().list_events(_url, mr))
            except Exception:
                pass
    return {"result": {"content": content}}


def _add_event(args):
    if not all(args.get(k) for k in ("summary", "start_time", "end_time")):
        return {"error": {"code": -32602, "message": "Missing required event parameters"}}
    ops = auth.get_calendar_service()
    body = {
        "summary": args["summary"],
        "start": {"dateTime": args["start_time"]},
        "end": {"dateTime": args["end_time"]}
    }
    for k in ("location", "description"):
        if args.get(k):
            body[k] = args[k]
    res = add_event(ops, body)
    if res.get("status") != "confirmed":
        txt = f"❌ Erro ao criar evento: {res.get('message', 'Erro desconhecido')}"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    ev = res["event"]
    txt = f"✅ Evento criado com sucesso!\n🆔 ID: {ev.get('id','N/A')}\n📅 {ev.get('summary','Evento')}\n🕐 {ev.get('start',{}).get('dateTime','')} - {ev.get('end',{}).get('dateTime','')}"
    if ev.get("location"):
        txt += f"\n📍 {ev['location']}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def _remove_event(args):
    if not args.get("event_id"):
        return {"error": {"code": -32602, "message": "Missing required parameter: event_id"}}
    svc = auth.get_calendar_service()
    success = remove_event(svc, args["event_id"])
    if success:
        txt = f"✅ Evento removido com sucesso!\n🆔 ID: {args['event_id']}"
    else:
        txt = f"❌ Erro ao remover evento {args['event_id']}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def _add_events(args):
    events = args.get("events", [])
    if not events:
        return {"error": {"code": -32602, "message": "Missing required parameter: events"}}
    
    success_count = 0
    failure_count = 0
    for event_args in events:
        res = _add_event(event_args)
        if "result" in res:
            success_count += 1
        else:
            failure_count += 1
    
    txt = f"{success_count} eventos criados com sucesso, {failure_count} falharam"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def _edit_event(args):
    if not args.get("event_id"):
        return {"error": {"code": -32602, "message": "Missing required parameter: event_id"}}
    if not args.get("updated_details"):
        return {"error": {"code": -32602, "message": "Missing required parameter: updated_details"}}
    svc = auth.get_calendar_service()
    updated = edit_event(svc, args["event_id"], args["updated_details"])
    if not updated:
        txt = f"❌ Falha ao editar evento {args['event_id']}"
        return {"result": {"content": [{"type": "text", "text": txt}]}}
    
    txt = f"✅ Evento editado com sucesso!\n🆔 ID: {updated.get('id','N/A')}"
    if updated.get('location'):
        txt += f"\n📍 {updated['location']}"
    return {"result": {"content": [{"type": "text", "text": txt}]}}


def handle(name: str, args: Dict[str, Any]):
    mp = {
        "list_events": _list_events,
        "add_event": _add_event,
        "add_events": _add_events,
        "remove_event": _remove_event,
        "edit_event": _edit_event,
    }
    fn = mp.get(name)
    return fn(args) if fn else None
