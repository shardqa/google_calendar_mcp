# Ferramentas Disponíveis via MCP

O servidor MCP expõe um conjunto de ferramentas para interagir com o Google Calendar e o Google Tasks de forma programática.

### Calendário

-   **`list_events`**: Lista os próximos eventos do calendário.
    -   Parâmetros: `max_results`, `calendar_id`, `ics_url`, `ics_alias`.
-   **`add_event`**: Cria um novo evento.
    -   Parâmetros: `summary`, `start_time`, `end_time`, `location`, `description`.
-   **`edit_event`**: Modifica um evento existente.
    -   Parâmetros: `event_id`, `summary`, `start_time`, `end_time`, etc.
-   **`remove_event`**: Remove um evento pelo seu ID.
    -   Parâmetros: `event_id`.
-   **`add_recurring_task`**: Cria eventos recorrentes (ex: reuniões semanais).
    -   Parâmetros: `summary`, `frequency`, `count`, `start_time`, `end_time`.
-   **`list_calendars`**: Lista todos os calendários disponíveis na conta.

### Tarefas (Google Tasks)

-   **`list_tasks`**: Lista todas as tarefas pendentes.
-   **`add_task`**: Adiciona uma nova tarefa.
    -   Parâmetros: `title`, `notes`, `due`.
-   **`remove_task`**: Marca uma tarefa como concluída.
    -   Parâmetros: `task_id`.

### Agendamento Inteligente

-   **`schedule_tasks`**: Analisa a agenda em busca de horários livres e sugere encaixes para as tarefas pendentes.
    -   Parâmetros: `time_period`, `work_hours_start`, `work_hours_end`.

### Calendários Externos (ICS)

-   **`register_ics_calendar`**: Associa uma URL de calendário `.ics` a um alias fácil de usar.
    -   Parâmetros: `ics_url`, `alias`.
-   **`list_ics_calendars`**: Lista todos os aliases de calendários ICS registrados.

### Utilitários

-   **`echo`**: Uma ferramenta simples para testes de conectividade. Retorna a mensagem enviada.

---
Voltar para o [Sumário](../../README.md).
Ver [Exemplos de Uso](usage_examples.md). 