# pragma: no cover
import json
import os
import threading
from typing import Dict

_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'config', 'ics_urls.json')
_LOCK = threading.Lock()


def _load() -> Dict[str, str]:  # pragma: no cover
    if not os.path.exists(_REGISTRY_PATH):
        return {}  # pragma: no cover
    with open(_REGISTRY_PATH, 'r', encoding='utf8') as fh:
        try:
            return json.load(fh)
        except Exception:
            return {}  # pragma: no cover


def _save(data: Dict[str, str]) -> None:  # pragma: no cover
    os.makedirs(os.path.dirname(_REGISTRY_PATH), exist_ok=True)
    with open(_REGISTRY_PATH, 'w', encoding='utf8') as fh:
        json.dump(data, fh, indent=2)  # pragma: no cover


def register(alias: str, url: str) -> None:
    if not alias or not url:
        raise ValueError('alias and url are required')
    with _LOCK:
        data = _load()
        data[alias] = url
        _save(data)


def get(alias: str) -> str:
    return _load().get(alias, '')


def list_all() -> Dict[str, str]:
    return _load() 