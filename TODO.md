# TODO - Atividades Ativas

## Development Tasks

### High Priority

- [ ] Fix ICS registration to return confirmation response when successfully
  registering an external calendar
- [ ]  Colocar retorno de mensagem ao adicionar tarefa. Tá funcionando, mas não tem retorno
- [ ] Fix time display issue when listing ICS calendar events (events show
  but times are incorrect) - ensure fix doesn't break existing calendar
  listing functionality

### Medium Priority

- [ ] Refactor any directory exceeding ten items into logical sub-folders
  and adjust imports
- [ ] Maintain comprehensive test coverage during refactors

## Future Enhancements

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: 100% (auth, calendar_ops, tasks_ops)
- **CLI handlers**: 100% (main, mcp_cli, tasks_cli)
- **MCP components**: 100% (handlers, server, schemas)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 100% 🏆 (246 tests passing) ✅

### Test Quality Standards

- **246+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~2.8s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/architecture.md)
and [Overview](doc/overview.md) documents.

- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL
