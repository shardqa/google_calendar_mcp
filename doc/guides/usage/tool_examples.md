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

## ICS External Calendars

### Basic ICS Listing

```python
# List events from external ICS calendar
events = list_events(ics_url="https://example.com/calendar.ics")
```

### Enhanced Error Handling

```python
# With debug information for troubleshooting
events = list_events(
    ics_url="https://example.com/calendar.ics", 
    debug=True
)

# Example responses:
# Success: Returns formatted events
# Network error: "❌ Failed to fetch ICS calendar: Connection timeout"
# Empty calendar: "📅 No events found in ICS calendar (may be empty or all events filtered)"
# Debug mode: Shows processing details and filtering explanations
```

### Common ICS Issues and Solutions

**Issue**: No events returned despite calendar having events

```python
# Solution: Enable debug mode to see what's happening
events = list_events(ics_url="...", debug=True)
# May show: "Events found but filtered (past dates)" or network issues
```

**Issue**: Network connectivity problems

```python
# Response now includes helpful error message instead of crash:
# "❌ Failed to fetch ICS calendar from https://...:
# Connection timeout"
```

**Issue**: Malformed calendar data

```python
# Response provides useful feedback:
# "⚠️ ICS calendar has parsing issues but found X events"
```

## Advanced Usage

---
Voltar para o [Guia de Uso](usage_examples.md).
Ver os [Fluxos de Trabalho Típicos](workflows.md).
