# Atividades Completadas ✅

Este arquivo lista apenas os marcos mais recentes. Para o histórico completo, veja [Arquivo de Conquistas](doc/completed/archive_v1.md).

## Recent High Priority Completions ✅

- **Refactor files larger than 100 lines - successfully decomposed 4 major files into smaller, focused modules with logical organization** ✅
  - `src/mcp/auth_middleware.py` (307→98 lines) → extracted `TokenVerifier`, `TokenGenerator`, `RateLimiter` classes into `src/mcp/auth/` 
  - `src/mcp/mcp_stdio_server.py` (240→63 lines) → extracted `StdioRequestHandler` into `src/mcp/stdio_handler.py`
  - `src/core/calendar_ops.py` (186 lines) → decomposed into individual function files in `src/core/calendar/`
  - `src/commands/mcp_cli.py` (120→50 lines) → extracted CLI logic into focused modules
  - Fixed all import cascades and maintained functionality across 279 tests
- **Fix ICS date filtering - eventos do calendário ICS agora respeitam filtro de data (hoje em diante)** ✅
- **Fix failing test suite - todos os testes passando novamente (294 passed, 1 skipped)** ✅
- **Maintain 100% test coverage - cobertura de testes mantida em 100%** ✅
- **Fix test infrastructure - corrigir problemas com cursor.AppImage nos testes de execução** ✅
- **Fix pipeline test failure: mock credentials file access in tasks tests**
- **Remove CLI functionality and focus only on MCP tools to simplify project scope**
- **Implement task completion handling and status updates**
- **Sync tasks with calendar events when due dates are present**
- **Integrate read-only work calendar to display its events in listings**
- **Support viewing events from external ICS calendars**
- **Add SSE support for tasks operations to enable real-time updates**
- **Return user confirmation message when adding tasks**
- **Fix ICS registration to return confirmation response when successfully registering an external calendar**
- **Fix incorrect time display when listing ICS calendar events**
- **Merge ICS calendar events with Google Calendar events in `list_events` output**
- **Fix ICS events listing that previously returned no results** ✅
- **Clean up obsolete mcp-remote scripts and documentation in favor of SSE/token workflow** ✅
- **Test Coverage**: Increased from 83% to 98% by adding comprehensive unit tests for `auth_middleware.py`, `mcp_handler_no_auth.py`, `mcp_cli.py`, and `ics_ops.py`, resolving numerous patching and module import issues along the way.
- **Project Refactoring**: Reorganized the `scripts/` directory into logical sub-folders (`remote_legacy/`, `security/`, `test/`) and split the oversized `doc/guides/operations.md` into smaller, more manageable documents.

---

## Histórico de Desenvolvimento

Este arquivo documenta as funcionalidades e melhorias mais recentes. Para atividades em andamento, consulte [TODO.md](TODO.md).

Links úteis:

- [Architecture](doc/guides/architecture.md)
- [Overview](doc/guides/overview.md)
