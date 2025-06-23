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

- **274 testes** passando sem falhas (crescimento de 235 → 274)
- **100% cobertura** em todos os módulos (1054 statements, 298 branches)
- **Metodologia TDD** rigorosamente aplicada: red-green-refactor
- **Casos edge** cobertos: URLs inválidas, parsing ICS, erro de parâmetros

### Estratégias Avançadas de Teste

- Mocking estratégico para dependências externas (requests, Google APIs)
- Testes de threading para registry thread-safe
- Cobertura de branches condicionais complexas sem pragmas desnecessários
- Performance otimizada: suite completa em ~3.1s

## Regras de Qualidade Consolidadas

- **100% cobertura obrigatória** antes de qualquer commit
- **TDD enforcement**: sempre teste → implementação → refactor
- **Limite de 10 itens** por diretório com sub-pastas quando excedido
- **Máximo 100 linhas** por arquivo com refactoring automático
- **Zero comments policy** para código auto-explicativo

---

Manter este arquivo atualizado com apenas mudanças significativas concluídas.
