# TODO - Atividades Ativas

## Próxima Fase: Intelligent Scheduling

- [x] Design intelligent scheduling algorithm that reads current
  calendar/tasks and suggests time blocks
- [ ] Update project documentation and README with new usage examples
- [x] Run markdownlint --fix on all markdown documents

## Development Tasks

### High Priority

- [ ] **Adicionar opção para editar eventos do calendário**: Implementar
  funcionalidade para editar eventos existentes via MCP
- [ ] **Testar e ajustar adicionar eventos**: Investigar e corrigir problema
  onde add_event está sendo chamado mas não está criando eventos no calendário
- [x] Build MCP command `schedule_tasks` that analyzes current calendar
  and tasks to propose time blocks

### Medium Priority

- [ ] Implement priority-based task ordering algorithm considering
  deadlines and importance
- [ ] Add automatic time block creation for high-priority tasks in
  available calendar slots
- [ ] Sync tasks with calendar events when due dates are present
- [ ] Implement task completion handling and status updates
- [ ] Add SSE support for tasks operations to enable real-time updates

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
- **MCP components**: 98-99% (handlers, server, schemas)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 100% 🏆 (230 tests passing)

### Test Quality Standards

- **230+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~3.6s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/architecture.md)
and [Overview](doc/overview.md) documents.
