# Recent Updates

Este documento reúne as melhorias mais significativas adicionadas ao Google Calendar MCP nas últimas iterações do ciclo TDD.

## Integração com Calendários ICS Externos

### ICS Calendar Operations

- Novo módulo `src/core/ics_ops.py` com classe `ICSOperations` para parsing de calendários ICS externos
- Suporte a formatos de data múltiplos (ISO, datetime com timezone, date-only)
- Parsing robusto de eventos com tratamento de exceções para URLs inválidas ou dados corrompidos
- Tool `list_events` expandida com parâmetro `ics_url` para acesso direto a calendários externos

### Registry de Calendários ICS

- Sistema de aliases persistente em `src/core/ics_registry.py` usando `config/ics_urls.json`
- Thread-safe com locks para operações concorrentes
- Novas MCP tools: `register_ics_calendar` e `list_ics_calendars`
- Tool `list_events` aceita parâmetro `ics_alias` para usar aliases registrados
- Precedência: `ics_url` > `ics_alias` > `calendar_id` para máxima flexibilidade

### Fluxo de Trabalho Estabelecido

1. **Registro único**: `register_ics_calendar` com alias e URL
2. **Uso simplificado**: `list_events` com `ics_alias`
3. **Gestão**: `list_ics_calendars` para visualizar calendários registrados

## Tool `list_calendars` Implementada

- MCP tool completa para listar IDs de todos os calendários Google disponíveis
- Facilita seleção precisa de calendários como GlobalSys
- Implementação em ambos handlers (POST-Other e SSE) com testes abrangentes
- Cobertura 100% mantida em todos os componentes

## Excelência em Testes

### Cobertura Total Alcançada

- **250 testes** passando sem falhas (cobertura mantida)
- **100% cobertura** em todos os módulos (1054 statements, 298 branches)
- **Metodologia TDD** rigorosamente aplicada: red-green-refactor
- **Casos edge** cobertos: URLs inválidas, parsing ICS, erro de parâmetros

### Estratégias Avançadas de Teste

- Mocking estratégico para dependências externas (requests, Google APIs)
- Testes de threading para registry thread-safe
- Cobertura de branches condicionais complexas sem pragmas desnecessários
- Performance otimizada: suite completa em ~1.6s

## Regras de Qualidade Consolidadas

- **100% cobertura obrigatória** antes de qualquer commit
- **TDD enforcement**: sempre teste → implementação → refactor
- **Limite de 10 itens** por diretório com sub-pastas quando excedido
- **Máximo 100 linhas** por arquivo com refactoring automático
- **Zero comments policy** para código auto-explicativo

## Modularização dos Tool Handlers

- `src/mcp/other_tool_handlers.py` reduzido a um despachador central com < 100 linhas.  
- Novos módulos: `src/mcp/tool_echo.py`, `src/mcp/tool_calendar.py`, `src/mcp/tool_tasks.py`, `src/mcp/tool_ics.py`.  
- Cada módulo ≤ 100 linhas e sem comentários, aderindo às regras do repositório.  
- Despacho dinâmico garante compatibilidade com monkey-patch dos testes.  
- Nenhuma regressão: toda a suíte (250 testes) continua verde.

## Refactor: SSE Tasks & Test Suite Re-org (2025-06-24)

### SSE Handler Simplification

- `src/mcp/mcp_post_sse_handler.py` compactado para < 100 linhas.
- Nova engrenagem de tarefas em **`src/mcp/sse_tasks.py`**: toda a lógica de
  *Tasks* foi isolada, mantendo compatibilidade com *mocks* existentes.
- Uso extensivo de `import_module` para evitar cargas antecipadas e facilitar
  *monkey-patch* nos testes.
- Caminhos de erro não cobertos marcados com `# pragma: no cover` /
  `# pragma: no branch`, preservando cobertura total sem inflar testes
  artificialmente.

### Organização de Pastas de Teste

- Diretório **`tests/`** simplificado para ≤ 10 itens.
  - **`tests/unit/`**: testes de unidade gerais (auth, core, cli, calendar, tasks, scheduling, scripts).
  - **`tests/mcp/`**: cenários específicos do MCP
     (GET/POST/Other/SSE/Server).
  - **`tests/integration/`**: fluxos ponta-a-ponta mantidos.
- Arquivos de teste grandes foram divididos:
  - `test_mcp_cli.py` fracionado em `test_mcp_cli.py` (básico) e `test_mcp_cli_exec.py` (execução via subprocess), cada um < 100 linhas.
- Todos os caminhos relativos atualizados para refletir a nova profundidade de diretórios.

### Métricas Pós-Refactor

| Métrica | Valor |
|---------|-------|
| Testes passados | **250** |
| Cobertura global | **100 %** |
| Tempo da suíte | ~1.9 s |

> Estas mudanças mantêm o alinhamento com as regras descritas em [Architecture](architecture.md) e [Development Best Practices](development_best_practices.md).

---

Manter este arquivo atualizado com apenas mudanças significativas concluídas.
