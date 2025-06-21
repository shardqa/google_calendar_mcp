# TODO

## Status: Fase 1 Completa + Script Testing Optimization ✅

### Google Tasks Integration (Concluída)

- [x] **API Integration**: Google Tasks API com autenticação OAuth2 completa
- [x] **CLI Commands**: `tasks list`, `tasks add`, `tasks remove` funcionais
- [x] **Unified Auth**: Sistema compartilhado Calendar + Tasks
- [x] **Documentation**: Arquitetura, práticas e troubleshooting atualizados

### Testing Excellence (Concluída)

- [x] **Test Coverage**: 98% geral do projeto com 200+ testes
- [x] **Script Testing**: 94-96% cobertura em scripts utilitários
- [x] **Zero Failures**: Todos os testes passando consistentemente
- [x] **TDD Implementation**: Metodologia red-green-refactor consolidada
- [x] **Edge Case Coverage**: Timeouts, erros HTTP, decodificação,
  formatos desconhecidos
- [x] **Performance**: Suite completa executando em ~4 segundos
- [x] **Isolated Testing**: Testes unitários com mocking estratégico
- [x] **Diagnostic Scripts**: Conectividade, SSE, inicialização,
  cancelamento

## Próxima Fase: Intelligent Scheduling

- [ ] Design intelligent scheduling algorithm that reads current
  calendar/tasks and suggests time blocks
- [ ] Update project documentation and README with new usage examples
- [ ] Run markdownlint --fix on all markdown documents

## Next

- [ ] Build MCP command `schedule_tasks` that analyzes current calendar
  and tasks to propose time blocks
- [ ] Implement priority-based task ordering algorithm considering
  deadlines and importance
- [ ] Add automatic time block creation for high-priority tasks in
  available calendar slots
- [ ] Sync tasks with calendar events when due dates are present
- [ ] Implement task completion handling and status updates
- [ ] Add SSE support for tasks operations to enable real-time updates
- [ ] Refactor any directory exceeding ten items into logical sub-folders
  and adjust imports
- [ ] Maintain comprehensive test coverage during refactors

## Later

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: 100% (auth, calendar_ops, tasks_ops)
- **CLI handlers**: 100% (main, mcp_cli, tasks_cli)
- **MCP components**: 98%+ (handlers, server, schemas)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 98%

### Test Quality Standards

- **200+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/architecture.md)
and [Overview](doc/overview.md) documents.
