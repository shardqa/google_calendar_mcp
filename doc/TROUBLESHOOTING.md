# Troubleshooting Google Calendar MCP

Este documento registra os passos de diagnóstico e correções aplicadas no servidor MCP do Google Calendar.

## 1. Problema inicial
- Chamadas de ferramentas (`list_events`, etc.) retornavam erro de ferramenta não encontrada ou dados inválidos.
- O cliente MCP não registrava as ferramentas porque o `mcp/hello` enviava `"capabilities.tools": {}` vazio.

## 2. Passos de diagnóstico

1. Teste de conexão SSE:
   ```bash
   curl http://localhost:3001/sse -N
   ```
   - Verificou-se que o evento `mcp/hello` vinha com `tools: {}` vazio.

2. Inspeção do código em `src/mcp_server.py`:
   - Handler `do_GET` enviava hello sem preencher `capabilities.tools`.
   - Handler `do_POST` para `initialize` também retornava `"tools": {}` vazio.

3. Teste de chamada JSON-RPC direta:
   ```bash
   curl -X POST http://localhost:3001/sse \
     -H 'Content-Type: application/json' \
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/call",
       "params": {"tool": "list_events", "args": {"max_results": 2}},
       "id": 1
     }'
   ```
   - Retornou corretamente os próximos 2 eventos.

## 3. Correções aplicadas

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

## 4. Testes realizados

- Reiniciar servidor:
  ```bash
  ./run_mcp.sh
  ```
- Verificar SSE handshake:
  ```bash
  curl http://localhost:3001/sse -N
  ```
  - Confirmar hello preenchido e tools/list.

- Teste JSON-RPC direto:
  ```bash
  curl -X POST http://localhost:3001/sse \
    -H 'Content-Type: application/json' \
    -d '{ ... }'
  ```
  - Deve retornar JSON com `result` contendo array de eventos.

## 5. Próximos passos

- Verificar integração com o cliente MCP (Cursor/VSCode).
- Ajustar formatação de retorno no handler, se necessário.
- Documentar qualquer novo erro de deserialização ou schema.
- Implementar testes automatizados em `tests/` para o `mcp_server`.

## Documentação Relacionada

### Documentação Interna

- [Visão Geral](overview.md)
- [Instalação](installation.md)
- [Arquitetura](architecture.md)
- [Uso](usage.md)
- [Desenvolvimento Futuro](future.md)
- [Sumário da Documentação](README.md)
- [Resolução de Problemas](troubleshooting.md) 