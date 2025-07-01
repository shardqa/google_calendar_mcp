# OpenCode.md

## Build/Test Commands
- **Full test suite with coverage**: `make test` or `uvx --with pytest --with coverage --with-editable . coverage run --parallel-mode --source=src -m pytest`
- **Fast tests without coverage**: `make test-fast` or `uvx --with pytest --with-editable . pytest`
- **Single test file**: `uvx --with pytest --with-editable . pytest tests/path/to/test_file.py`
- **Single test function**: `uvx --with pytest --with-editable . pytest tests/path/to/test_file.py::test_function_name`
- **Clean temp files**: `make clean`
- **Start MCP server**: `make mcp-start` or `src/scripts/run_mcp.sh`

## Code Style Guidelines
- **TDD Required**: Write failing test first, implement, then refactor while keeping tests green
- **File size limit**: Maximum 100 lines per file - split into smaller files if exceeded
- **Folder limit**: Maximum 10 items per folder - create subfolders when exceeded
- **Imports**: Use relative imports within modules (e.g., `from .utils import func`), absolute for cross-module
- **Types**: Use type hints for function parameters and return values (`from typing import Dict, Any`)
- **Error handling**: Return dict with `{'status': 'error', 'message': str(e)}` pattern for errors
- **Naming**: Snake_case for functions/variables, PascalCase for classes
- **Coverage**: Maintain 100% test coverage - run `make test` after any code changes
- **Protected files**: Never move/modify: `.cursor/`, `.github/`, `.venv/`, `Makefile`, `README.md`, `requirements.txt`, `TODO.md`, `src/mcp/mcp_schema.py`
- **Task completion**: Move completed tasks from `TODO.md` to `COMPLETED.md`