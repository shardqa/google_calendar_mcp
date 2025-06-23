# Recent Updates

Este documento reúne as melhorias mais significativas adicionadas ao Google Calendar MCP nas últimas iterações do ciclo TDD.

## Algoritmo de Prioridades

- Novo módulo `src/core/task_ordering.py` ordena tarefas por data de vencimento e importância (1–3).
- O `SchedulingEngine` delega a esse módulo antes de alocar blocos de tempo.

## Blocos Automáticos para Tarefas de Alta Prioridade

- Implementado em `src/core/time_block_creator.py`.
- Tarefas com importância 3 geram eventos no Google Calendar automaticamente.

## Sincronização Tarefas ↔ Calendário

- Módulo `src/core/tasks_calendar_sync.py` cria eventos para tarefas com `due` que ainda não constam no calendário.
- Invocado no handler `list_tasks` para manter dados consistentes.

## Integração com Calendários Adicionais (Read-Only)

- `CalendarOperations.list_events` agora aceita `calendar_id`.  
  Ex.: `list_events(max_results=5, calendar_id="globalsys")`.
- Handler `list_events` expõe o parâmetro via `tools/call`.

## Nova MCP Tool: `list_calendars`

Em planejamento (ver TODO). Objetivo: retornar todos os IDs de calendários disponíveis para facilitar seleção de agendas como **GlobalSys**.

## Cobertura de Testes

- Todos os módulos alcançam 100 % de cobertura após cada alteração, conforme `.cursorrules`.
- Suite atual: 255 testes em ~7 s.

## Regras Atualizadas (`.cursorrules`)

- Cobertura global obrigatória de 100 % após cada commit.  
- Máximo de 10 itens por pasta e arquivos ≤ 100 linhas.

---

Manter este arquivo curto e útil: adicione apenas mudanças significativas e removidas do TODO. 