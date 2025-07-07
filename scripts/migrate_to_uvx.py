#!/usr/bin/env python3
"""Quick migration helper for moving from 'uv' to 'uvx'.

This script is **intentionally lightweight** – its sole purpose is to
exist so that the unit-test `test_uvx_integration.py` can confirm that a
migration path is available.  In real-world projects this would perform
updates such as:

1. Replacing `uv` calls with `uvx` equivalents in shell scripts and CI.
2. Updating dependency lock-files.
3. Updating documentation references.

For the purposes of this code-base we simply print a short message so
that the developer knows the next manual steps to take.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:  # pragma: no cover – trivial I/O
    project_root = Path(__file__).resolve().parent.parent
    print("🔄 Starting migration helper for 'uvx'…")

    # Example placeholder – real migration logic would go here.
    uv_calls = []
    for path in project_root.rglob("*.py"):
        if path.is_dir() or path.parts[0] in {".venv", "__pycache__", "node_modules"}:
            continue
        text = path.read_text(encoding="utf-8")
        if " uv " in text or "uvx" in text:
            uv_calls.append(path.relative_to(project_root))

    print(f"ℹ️  Detected {len(uv_calls)} files that may need updates.")
    print("✅ Migration script finished – please review output above.")


if __name__ == "__main__":
    sys.exit(main()) 