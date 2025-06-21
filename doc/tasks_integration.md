# Google Tasks Integration

## Overview

Successfully integrated Google Tasks API with the existing Google Calendar MCP system,
following Test-Driven Development (TDD) principles. This integration enables unified
management of both calendar events and tasks through CLI commands and MCP protocols.

## Implementation Summary

### Authentication Module (`src/core/tasks_auth.py`)

- Extended OAuth2 scope to include Google Tasks API access
- Unified credential management for both Calendar and Tasks APIs  
- Reusable authentication patterns from existing calendar module

### Tasks Operations (`src/core/tasks_ops.py`)

- `list_tasks()`: Retrieves and formats tasks from default task list
- `add_task()`: Creates new tasks with title, notes, and due dates
- `remove_task()`: Deletes tasks by ID with error handling
- Consistent response formatting matching calendar operations

### Command Line Interface (`src/commands/tasks_cli.py`)

- `tasks list`: Display all pending tasks in formatted output
- `tasks add <title> [--notes] [--due]`: Create new tasks with metadata
- `tasks remove <task_id>`: Remove tasks by ID
- Argument parsing and user-friendly error messages

## Test Coverage

Comprehensive test suite following TDD methodology:

### Authentication Tests (`tests/tasks/test_tasks_auth.py`)

- Service initialization and credential handling
- OAuth scope validation for Tasks API access
- Mock-based testing for external API dependencies

### Operations Tests (`tests/tasks/test_tasks_ops.py`)  

- Task listing with empty and populated results
- Task creation success and error scenarios
- Task removal with validation and error handling

### CLI Tests (`tests/tasks/test_tasks_cli.py`)

- Command parsing and execution flow
- User interface output formatting
- Integration with operations layer

## MCP Integration

### Google Tasks via MCP Server

O servidor MCP agora oferece integração completa com Google Tasks através de 3 ferramentas:

- **`list_tasks`**: Lista tarefas pendentes do Google Tasks
- **`add_task`**: Adiciona novas tarefas com título, notas e data de vencimento
- **`remove_task`**: Remove tarefas existentes por ID

### Configuração OAuth

Para habilitar Google Tasks no MCP, é necessário:

1. **Atualizar escopos OAuth**: Incluir `https://www.googleapis.com/auth/tasks`
2. **Remover token existente**: `rm config/token.pickle`
3. **Reautorizar aplicação**: Próxima chamada ativará fluxo OAuth
4. **Habilitar Google Tasks API**: Visitar [Google Cloud Console](https://console.developers.google.com/apis/api/tasks.googleapis.com/)

### Uso via Cursor

Após configuração, as ferramentas ficam disponíveis no Cursor:

- `@mcp_google_calendar_list_tasks`
- `@mcp_google_calendar_add_task`
- `@mcp_google_calendar_remove_task`

## Usage Examples

### CLI Usage

```bash
# List all pending tasks
python -m src.commands.tasks_cli list

# Add a new task
python -m src.commands.tasks_cli add "Complete project" --notes "Final review"

# Remove a task
python -m src.commands.tasks_cli remove "task_id_123"
```

## Integration Points

The Tasks system integrates seamlessly with existing architecture patterns and is
ready for future intelligent scheduling features. For more details, see
[Architecture](architecture.md) and [Intelligent Scheduling](intelligent_scheduling.md).
