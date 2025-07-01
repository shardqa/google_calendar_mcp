# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
- **Full test suite with coverage**: `make test` or `uvx --with pytest --with coverage --with-editable . coverage run --parallel-mode --source=src -m pytest`
- **Fast tests without coverage**: `make test-fast` or `uvx --with pytest --with-editable . pytest`
- **Clean temporary files**: `make clean`

### MCP Server Management
- **Start MCP server**: `make mcp-start` or `src/scripts/run_mcp.sh`
- **Start locally on port 3001**: `make mcp-local`
- **Stop MCP server**: `make mcp-stop`
- **Restart MCP server**: `make mcp-restart`

### CLI Usage
- **Setup MCP configuration**: `python -m src.commands.mcp_cli`
- **Start stdio server**: `python -m src.mcp.mcp_stdio_server`
- **Start with custom port**: `python -m src.commands.mcp_cli --port 3000`

## Architecture Overview

This is a Google Calendar MCP (Model Context Protocol) server that provides AI assistants with calendar and task management capabilities.

### Core Structure
- **`src/core/`**: Business logic layer with modular functions for calendar operations
  - `calendar/`: Google Calendar operations (list, add, edit, remove events)
  - `ics_ops.py`: External calendar (ICS) operations
  - `auth.py`: Google API authentication
- **`src/mcp/`**: MCP protocol implementation
  - `tools/`: MCP tool definitions (tool_calendar.py, tool_ics.py)
  - `mcp_stdio_server.py`: STDIO mode server
  - `auth/`: Authentication middleware and token management
- **`src/commands/`**: CLI interface (`mcp_cli.py`)

### Key Design Principles
- **Modular Functions**: Each calendar operation is a pure, testable function
- **Protocol Separation**: Business logic is independent of MCP protocol
- **Comprehensive Testing**: 90% test coverage with 279+ automated tests
- **uvx Integration**: Uses uvx for dependency management and execution

## Available MCP Tools

### Calendar Operations
- `list_events`: List upcoming calendar events
- `add_event`: Create new calendar events  
- `edit_event`: Modify existing events
- `remove_event`: Delete events by ID

### ICS Calendar Support
- `register_ics_calendar`: Register external ICS calendar URLs with aliases
- `list_ics_calendars`: List registered ICS calendar aliases

## Development Rules

### Code Quality Standards
- **TDD Required**: Write failing tests before implementation
- **100% Test Coverage**: All code changes must maintain full coverage
- **File Size Limit**: Maximum 100 lines per file
- **Folder Organization**: Maximum 10 items per folder (create subfolders when exceeded)

### Testing Requirements
- Run `make test` after any code changes to verify coverage
- All tests must pass before commits
- Use uvx for dependency isolation

### File Structure Constraints
- Never move/modify these files: `.cursor/`, `.github/`, `.venv/`, Makefile, README.md, requirements.txt, TODO.md, `src/mcp/mcp_schema.py`
- Keep markdown files linted with `markdownlint --fix`

## Project Configuration

- **Python Version**: >= 3.8
- **Package Manager**: uvx (preferred) or pip with virtual environments
- **Test Framework**: pytest with coverage reporting
- **Entry Point**: `google-calendar-mcp` command (via pyproject.toml)