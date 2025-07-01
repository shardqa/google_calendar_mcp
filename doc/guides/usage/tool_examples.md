# Exemplos de Ferramentas MCP

Esta seção fornece exemplos práticos de como chamar cada ferramenta MCP.

### `list_events`

**Listar os próximos 10 eventos do calendário principal:**

```bash
# Via MCP tool call
mcp_google_calendar_list_events max_results=10
```

### `add_event`

**Criar uma reunião com todos os detalhes:**

```bash
# Via MCP tool call
mcp_google_calendar_add_event \
  summary="Reunião de planejamento da Sprint" \
  start_time="2024-03-25T14:00:00" \
  end_time="2024-03-25T15:30:00" \
  location="Sala de Conferências A" \
  description="Revisar objetivos e definir tarefas."
```

### `add_task`

**Adicionar uma tarefa com título, notas e data de vencimento:**

```bash
# Via MCP tool call
mcp_google_calendar_add_task \
  title="Finalizar relatório mensal" \
  notes="Incluir dados de Q1 e análise de performance." \
  due="2024-03-28T17:00:00"
```

### `schedule_tasks`

**Analisar a agenda da semana e propor horários para tarefas:**

```bash
# Via MCP tool call
mcp_google_calendar_schedule_tasks \
  time_period="week" \
  work_hours_start="09:00" \
  work_hours_end="18:00"
```

### `add_recurring_task`

**Criar um lembrete diário de medicação para 30 dias:**

```bash
# Via MCP tool call
mcp_google_calendar_add_recurring_task \
  summary="Tomar medicação matinal" \
  frequency="daily" \
  count=30 \
  start_time="2024-03-20T08:00:00" \
  end_time="2024-03-20T08:15:00"
```

---
Voltar para o [Guia de Uso](usage_examples.md).
Ver os [Fluxos de Trabalho Típicos](workflows.md). 