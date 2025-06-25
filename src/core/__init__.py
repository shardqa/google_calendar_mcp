import sys as _sys
from importlib import import_module as _imp

# task_ordering has no external deps; load first
_order = [
    ("task_ordering", "scheduling.task_ordering"),
    ("time_block_creator", "scheduling.time_block_creator"),
    ("scheduling_engine", "scheduling.scheduling_engine"),
]
for _alias, _path in _order:
    _mod = _imp(f"src.core.{_path}")
    _sys.modules[f"src.core.{_alias}"] = _mod 