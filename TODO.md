# TODO

## Status: Atividades Ativas

### Servidor MCP - Status ✅

- [x] **Servidor MCP funcionando**: Problema resolvido! Servidor MCP está trazendo as tasks corretamente via MCP tools.

### MCP Agenda Enhancement

- [x] **Melhorar listagem de eventos**: Implementado exibição completa com data/hora, localização, descrição e outras informações relevantes usando TDD. Eventos agora mostram todas as informações contextuais com formatação visual (emojis).

### Recurring Tasks Implementation

- [x] **Implementar tarefas recorrentes (Opção 1 - Híbrida)**: Comando `add_recurring_task` implementado! Adiciona eventos recorrentes no Google Calendar (daily, weekly, monthly) usando TDD. Cobertura 100% alcançada.

### Quality Metrics Achievement  

- [x] **100% Code Coverage**: Alcançado! 725 statements, 178 branches, 193 testes passando. Melhorias nos testes de `calendar_ops.py` e `mcp_post_sse_handler.py`.

### Próxima Fase: Intelligent Scheduling

- [ ] Design intelligent scheduling algorithm that reads current
  calendar/tasks and suggests time blocks
- [ ] Update project documentation and README with new usage examples
- [ ] Run markdownlint --fix on all markdown documents

### Next

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

### Later

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: 100% (auth, calendar_ops, tasks_ops)
- **CLI handlers**: 100% (main, mcp_cli, tasks_cli)
- **MCP components**: 98-99% (handlers, server, schemas)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 100% 🏆

### Test Quality Standards

- **182+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~3.6s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/architecture.md)
and [Overview](doc/overview.md) documents.

## Completed Activities ✅

### Google Tasks Integration (Concluída)

- [x] **API Integration**: Google Tasks API com autenticação OAuth2 completa
- [x] **CLI Commands**: `tasks list`, `tasks add`, `tasks remove` funcionais
- [x] **Unified Auth**: Sistema compartilhado Calendar + Tasks
- [x] **Documentation**: Arquitetura, práticas e troubleshooting atualizados

### Testing Excellence (Concluída) ✅

- [x] **Test Coverage**: 100% geral do projeto com 182+ testes 🏆
- [x] **Coverage Improvement**: Meta ultrapassada! Aumentou de 90% para 100%:
  - `mcp_post_other_handler.py` (64% → 100%): +36% melhoria
  - `mcp_post_sse_handler.py` (72% → 100%): +28% melhoria
- [x] **Branch Coverage**: 100% - todas as branches condicionais testadas
- [x] **Script Testing**: 94-96% cobertura em scripts utilitários
- [x] **Zero Failures**: Todos os testes passando consistentemente
- [x] **TDD Implementation**: Metodologia red-green-refactor consolidada
- [x] **Edge Case Coverage**: Timeouts, erros HTTP, decodificação,
  formatos desconhecidos + cenários de erro Tasks + branches condicionais
- [x] **Performance**: Suite completa executando em ~3.6 segundos
- [x] **Isolated Testing**: Testes unitários com mocking estratégico
- [x] **Diagnostic Scripts**: Conectividade, SSE, inicialização,
  cancelamento
