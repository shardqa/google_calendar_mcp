# Correções Aplicadas

1. **Preencher `capabilities.tools` no evento `mcp/hello`** (`do_GET` em `src/mcp_server.py`):

   ```diff
   - "capabilities": {"tools": {}},
   + capabilities_tools = {tool.name: tool.inputSchema for tool in schema.tools}
   + "capabilities": {"tools": capabilities_tools},
   ```

2. **Atualizar resposta de `initialize`** (`do_POST` em `src/mcp_server.py`):

   ```diff
   - "capabilities": {"tools": {}},
   + capabilities_tools = {tool.name: tool.inputSchema for tool in schema.tools}
   + "capabilities": {"tools": capabilities_tools},
   ```

3. **Aceitar chaves `name`/`arguments` além de `tool`/`args`** nas chamadas `tools/call`:

   ```diff
   - tool_name = params.get("tool")
   - tool_args = params.get("args", {})
   + tool_name = params.get("tool") or params.get("name")
   + tool_args = params.get("args") or params.get("arguments") or {}
   ```

   - Aplicado nos dois blocos de `tools/call` (rota SSE e rota padrão).

4. **Ajustar formato de resposta para `list_events`**
   - No `src/mcp/mcp_post_other_handler.py` e `src/mcp/mcp_post_sse_handler.py`, ajustar a resposta para incluir a chave `"content"` envolvendo o resultado da chamada `calendar_ops.CalendarOperations(service).list_events(max_results)`.

     ```python
     response["result"] = {"content": calendar_ops.CalendarOperations(service).list_events(max_results)}
     ```

5. **Formatar itens do array de eventos**
   - No `src/core/calendar_ops.py`, modificar a função `list_events` para mapear cada evento retornado pela API do Google Calendar para um dicionário com as chaves `"type": "text"` e `"text"` contendo o resumo do evento.

     ```python
     events = events_result.get('items', [])
     formatted_events = []
     for event in events:
         summary = event.get('summary', 'No Summary')
         formatted_events.append({"type": "text", "text": summary})
     return formatted_events
     ```

6. **Adicionar `timeMin` na chamada da API `list_events`**
   - No `src/core/calendar_ops.py`, adicionar o parâmetro `timeMin` com a data/hora atual na chamada da API `service.events().list` para garantir que apenas eventos futuros sejam retornados.

     ```python
     now = datetime.now(timezone.utc).isoformat()
     events_result = self.service.events().list(
         calendarId='primary',
         timeMin=now,
         maxResults=max_results,
         singleEvents=True,
         orderBy='startTime'
     ).execute()
     ```

7. **Corrigir asserções nos testes de exceção (`test_sse_stream_read.py`)**
   - Atualizar os testes `test_get_url_error`, `test_status_not_200` e `test_open_exception` para capturar a exceção específica `_pytest.outcomes.Failed` em vez de `Exception` genérica.
   - Mudar as asserções para verificar o atributo `.msg` da exceção capturada (`excinfo.value.msg`) em vez da representação em string completa (`str(excinfo.value)`), que inclui o prefixo "Failed:".

8. **Ajustar asserção no teste `test_list_events_with_results`**
   - Modificar o teste em `tests/calendar_ops/test_calendar_ops_list.py` para esperar o formato correto retornado pela função `CalendarOperations.list_events`, que é uma lista de dicionários com as chaves `"type": "text"` e `"text": "..."`, em vez de tentar acessar diretamente a chave `"summary"` do evento original da API.

9. **Atualizar asserções nos testes `test_list_events` dos handlers**
   - Corrigir os testes `test_list_events` em `tests/mcp_post_other/test_mcp_post_other_list_events_ops.py` e `test_tools_call_list_events` em `tests/mcp_post_sse/test_mcp_post_sse_tools_call_list_and_add_event.py`.
   - Ajustar as asserções para esperar que o resultado da chamada `list_events` seja envolvido em um dicionário com a chave `"content"`, refletindo a forma como os handlers empacotam a resposta antes de enviá-la.

## Documentação Relacionada

- [Índice de Resolução de Problemas](../TROUBLESHOOTING.md)
- [Problemas Iniciais](initial_problems.md)
- [Passos de Diagnóstico](diagnostic_steps.md)
- [Testes Realizados](tests_performed.md)
- [Visão Geral](../../overview.md)
- [Arquitetura](../../architecture.md)
