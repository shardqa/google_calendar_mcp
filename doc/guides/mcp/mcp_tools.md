# Ferramentas Disponíveis via MCP

O servidor MCP expõe um conjunto de ferramentas para interagir com o Google Calendar e o Google Tasks de forma programática.

### Calendário

-   **`list_events`**: Lista os próximos eventos do calendário.
    -   Parâmetros: `max_results`, `calendar_id`, `ics_url`, `ics_alias`.
-   **`add_event`**: Cria um novo evento.
    -   Parâmetros: `summary`, `start_time`, `end_time`, `location`, `description`.
-   **`add_events`**: Cria múltiplos eventos em batch.
    -   Parâmetros: `events` (array de objetos com `summary`, `start_time`, `end_time`, `location`, `description`).
-   **`edit_event`**: Modifica um evento existente.
    -   Parâmetros: `event_id`, `summary`, `start_time`, `end_time`, etc.
-   **`remove_event`**: Remove um evento pelo seu ID.
    -   Parâmetros: `event_id`.

### Calendários Externos (ICS)

-   **`register_ics_calendar`**: Associa uma URL de calendário `.ics` a um alias fácil de usar.
    -   Parâmetros: `ics_url`, `alias`.
-   **`list_ics_calendars`**: Lista todos os aliases de calendários ICS registrados.

---
Voltar para o [Sumário](../../README.md).
Ver [Exemplos de Uso](../usage/tool_examples.md).
Ver [Configuração MCP](../mcp/mcp_configuration.md).
