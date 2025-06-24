from typing import Dict, Any
from importlib import import_module

__all__ = ["handle"]

_ERR = lambda code, msg: {"error": {"code": code, "message": msg}}

def _register(args):
    alias, url = args.get("alias"), args.get("ics_url")
    if not alias or not url:
        return _ERR(-32602, "alias and ics_url are required")
    reg_mod = import_module("src.core.ics_registry")
    reg_mod.register(alias, url)
    txt = f"✅ Calendário ICS registrado com sucesso!\n🔖 Alias: {alias}"
    return {"result": {"registered": True, "content": [{"type": "text", "text": txt}]}}

def _list(_: Dict[str, Any]):
    return {"result": {"calendars": import_module("src.core.ics_registry").list_all()}}

_mapping = {
    "register_ics_calendar": _register,
    "list_ics_calendars": _list,
}

def handle(tool: str, args: Dict[str, Any]):
    func = _mapping.get(tool)
    return func(args) if func else None 