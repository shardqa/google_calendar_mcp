from datetime import datetime
import re
from typing import List, Dict


ISO_Z_RE = re.compile(r"Z$")
IMPORTANCE_RE = re.compile(r"^\[(\d)\]\s*")


def _parse_due(due: str):
    if not due:
        return None
    return datetime.fromisoformat(ISO_Z_RE.sub("+00:00", due)).replace(tzinfo=None)


def _parse_importance(title: str) -> int:
    match = IMPORTANCE_RE.match(title or "")
    if match:
        return int(match.group(1))
    return 1


def order_tasks(tasks: List[Dict]) -> List[Dict]:
    def key(t):
        due_dt = _parse_due(t.get("due"))
        importance = _parse_importance(t.get("title", ""))
        return (due_dt or datetime.max, -importance)

    return sorted(tasks, key=key) 