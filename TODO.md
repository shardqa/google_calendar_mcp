# TODO - Atividades Ativas

## Development Tasks

### High Priority

### Medium Priority

- [ ] Add automatic time block creation for high-priority tasks in
  available calendar slots
- [ ] Sync tasks with calendar events when due dates are present
- [ ] Implement task completion handling and status updates
- [ ] Add SSE support for tasks operations to enable real-time updates
- [ ] Increase CalendarOperations.edit_event timezone branch test coverage to
  100%

### Maintenance

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
- **Overall project**: 100% 🏆 (235 tests passing)

### Test Quality Standards

- **235+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~2.8s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/architecture.md)
and [Overview](doc/overview.md) documents.
