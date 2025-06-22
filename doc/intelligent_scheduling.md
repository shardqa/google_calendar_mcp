# Intelligent Scheduling System

## Business Rule

Enable users to request automatic agenda scheduling based on their current tasks
and commitments. The system should analyze existing calendar events and task
lists, then propose optimal time blocks for task completion.

## Core Functionality

### Primary Use Case

User request: "Schedule my tasks for this week based on my current agenda and priorities"

### System Response Process

1. **Read Current State**
   - Fetch all calendar events for specified time period
   - Retrieve all pending tasks from Google Tasks
   - Analyze task priorities, deadlines, and estimated durations

2. **Intelligent Analysis**
   - Identify available time slots in calendar
   - Order tasks by priority algorithm (deadline + importance)
   - Match task duration requirements with available time blocks
   - Consider user preferences (work hours, break intervals)

3. **Schedule Proposal**
   - Generate time block suggestions for each high-priority task
   - Create calendar events for proposed task blocks
   - Provide scheduling rationale and alternatives

## Algorithm Specifications

### Priority Calculation

```python
priority_score = (deadline_urgency * 0.4) + (user_importance * 0.3) + \
                 (estimated_effort * 0.3)
```

### Time Block Matching

- Minimum task block: 30 minutes
- Maximum continuous work block: 2 hours
- Buffer time between tasks: 15 minutes
- Respect existing calendar commitments

## MCP Commands

### `schedule_tasks`

**Input Parameters:**

- `time_period`: "week" | "day" | "month"
- `work_hours_start`: "09:00"
- `work_hours_end`: "18:00"
- `max_task_duration`: 120 (minutes)

**Output:**

- List of proposed calendar events for tasks
- Scheduling summary with rationale
- Alternative time slots for each task

## Implementation Status

### Core Engine (`src/core/scheduling_engine.py`)

✅ **Implemented Features:**

- **Calendar Analysis**: Fetches events for specified time periods (day/week/month)
- **Task Integration**: Retrieves pending tasks from Google Tasks
- **Gap Detection**: Identifies available time slots between existing events
- **Intelligent Filtering**: Excludes slots smaller than 30 minutes
- **Work Hours Respect**: Honors configured start/end work times
- **Duration Matching**: Matches task duration with available slots

✅ **Algorithm Logic:**

```python
def analyze_schedule(time_period, work_hours_start, work_hours_end):
    calendar_events = _get_calendar_events(time_period)
    pending_tasks = _get_pending_tasks()
    available_slots = _find_available_slots(events, work_hours)
    return analysis_result

def propose_schedule(time_period, max_task_duration):
    analysis = analyze_schedule(time_period, work_hours)
    proposed_events = _create_task_events(slots, tasks, max_duration)
    return scheduling_proposal
```

✅ **MCP Integration:**

- Command `schedule_tasks` available via Server-Sent Events
- Full JSON-RPC 2.0 compatibility
- Error handling for service failures
- Real-time streaming for long operations

### Quality Assurance

✅ **100% Test Coverage:**

- **30+ dedicated tests** for scheduling engine
- **Edge case coverage**: Empty calendars, conflicting events, short gaps
- **Error scenarios**: Service failures, malformed data, network issues
- **Branch coverage**: All conditional logic paths tested
- **Integration tests**: End-to-end MCP command flow

## Exemplos Práticos de Uso

### Cenário 1: Desenvolvedor com Múltiplas Tarefas

**Input via MCP:**

```json
{
  "method": "schedule_tasks",
  "params": {
    "time_period": "week",
    "work_hours_start": "09:00",
    "work_hours_end": "18:00",
    "max_task_duration": 180
  }
}
```

**Estado do Calendário:**

- Segunda: Reunião 10:00-11:00, Reunião 15:00-16:00
- Terça: Livre
- Quarta: All-hands 14:00-15:00
- Quinta: 1:1 com manager 11:00-11:30
- Sexta: Sprint review 16:00-17:00

**Tarefas Pendentes no Google Tasks:**

- "Implementar autenticação OAuth" (sem prazo)
- "Code review do PR #123" (vence hoje)
- "Documentar API endpoints" (vence quinta)
- "Configurar CI/CD pipeline" (vence sexta)

**Output Esperado:**

```json
{
  "analysis": {
    "time_period": "week",
    "total_calendar_events": 5,
    "available_time_slots": 12,
    "pending_tasks": 4,
    "work_hours_per_day": 9
  },
  "proposed_schedule": [
    {
      "task": "Code review do PR #123",
      "priority": "HIGH",
      "suggested_slot": {
        "start": "2024-03-25T09:00:00",
        "end": "2024-03-25T10:00:00",
        "duration_minutes": 60
      },
      "rationale": "Tarefa com prazo hoje - prioridade máxima. Slot matinal 
                   para concentração."
    },
    {
      "task": "Documentar API endpoints", 
      "priority": "MEDIUM",
      "suggested_slot": {
        "start": "2024-03-26T09:00:00",
        "end": "2024-03-26T11:30:00", 
        "duration_minutes": 150
      },
      "rationale": "Tarefa complexa em dia livre. Período longo para trabalho ininterrupto."
    },
    {
      "task": "Configurar CI/CD pipeline",
      "priority": "MEDIUM", 
      "suggested_slot": {
        "start": "2024-03-27T09:00:00",
        "end": "2024-03-27T11:00:00",
        "duration_minutes": 120
      },
      "rationale": "Prazo sexta. Slot antes do all-hands para terminar com calma."
    }
  ],
  "alternative_slots": [
    {
      "task": "Implementar autenticação OAuth",
      "alternatives": [
        {
          "start": "2024-03-28T12:00:00",
          "end": "2024-03-28T14:00:00",
          "rationale": "Quinta à tarde, após 1:1 - boa para início de feature"
        },
        {
          "start": "2024-03-29T09:00:00", 
          "end": "2024-03-29T12:00:00",
          "rationale": "Sexta manhã - bloco de 3h para desenvolvimento"
        }
      ]
    }
  ],
  "summary": {
    "scheduled_tasks": 3,
    "remaining_tasks": 1,
    "total_scheduled_time": "5h30m",
    "scheduling_efficiency": "85%"
  }
}
```

### Cenário 2: Gestão de Estudos para Certificação

**Input:**

```json
{
  "method": "schedule_tasks", 
  "params": {
    "time_period": "week",
    "work_hours_start": "19:00",
    "work_hours_end": "22:00", 
    "max_task_duration": 120
  }
}
```

**Calendário (horário de estudos):**

- Segunda: Livre
- Terça: Curso online 20:00-21:00
- Quarta: Livre  
- Quinta: Webinar 19:30-20:30
- Sexta: Livre

**Tarefas de Estudo:**

- "Estudar VPC e Networking" (2h estimadas)
- "Fazer labs de EC2" (1.5h estimadas)
- "Simulado practice test" (2h estimadas)
- "Revisar IAM policies" (1h estimadas)

**Output:**

```json
{
  "analysis": {
    "study_hours_available": 12,
    "tasks_total_time": 6.5,
    "utilization_rate": "54%"
  },
  "proposed_schedule": [
    {
      "task": "Simulado practice test",
      "suggested_slot": {
        "start": "2024-03-25T19:00:00",
        "end": "2024-03-25T21:00:00"
      },
      "rationale": "Simulado completo em dia livre - teste longo sem interrupções"
    },
    {
      "task": "Estudar VPC e Networking",
      "suggested_slot": {
        "start": "2024-03-27T19:00:00", 
        "end": "2024-03-27T21:00:00"
      },
      "rationale": "Tópico complexo em dia livre - 2h para absorver conceitos"
    },
    {
      "task": "Fazer labs de EC2",
      "suggested_slot": {
        "start": "2024-03-28T21:00:00",
        "end": "2024-03-28T22:30:00"  
      },
      "rationale": "Labs práticos após webinar - aproveitar aquecimento mental"
    }
  ]
}
```

### Cenário 3: Coordenação de Equipe Remota

**Input (Manager coordenando 3 equipes):**

```json
{
  "method": "schedule_tasks",
  "params": {
    "time_period": "day",
    "work_hours_start": "08:00", 
    "work_hours_end": "17:00",
    "max_task_duration": 90
  }
}
```

**Calendário do Dia:**

- 09:00-09:30: Standup Team A
- 10:00-10:30: Standup Team B  
- 11:00-11:30: Standup Team C
- 14:00-15:00: Sprint Review
- 16:00-16:30: 1:1 com Product Owner

**Tarefas Gerenciais:**

- "Revisar relatórios das 3 equipes"
- "Preparar apresentação para stakeholders"
- "Feedback individual para 2 desenvolvedores"
- "Planejar arquitetura próxima feature"

**Output:**

```json
{
  "proposed_schedule": [
    {
      "task": "Revisar relatórios das 3 equipes",
      "suggested_slot": {
        "start": "2024-03-25T08:00:00",
        "end": "2024-03-25T08:45:00"
      },
      "rationale": "Início do dia para ter contexto antes dos standups"
    },
    {
      "task": "Feedback individual para 2 desenvolvedores", 
      "suggested_slot": {
        "start": "2024-03-25T12:00:00",
        "end": "2024-03-25T13:00:00"
      },
      "rationale": "Meio-dia - bom para conversas pessoais e feedback"
    },
    {
      "task": "Preparar apresentação para stakeholders",
      "suggested_slot": {
        "start": "2024-03-25T13:00:00", 
        "end": "2024-03-25T14:00:00"
      },
      "rationale": "Antes do sprint review para alinhar informações"
    }
  ],
  "insights": {
    "peak_productivity_hours": "08:00-11:00",
    "meeting_density": "high", 
    "focus_time_available": "3h15m",
    "recommendation": "Consider blocking 1h after lunch for deep work"
  }
}
```

## Integration Points

For implementation details, see [Architecture](architecture.md) and
[Usage](usage.md) documentation.
