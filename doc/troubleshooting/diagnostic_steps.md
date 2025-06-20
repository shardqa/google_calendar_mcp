# Passos de Diagnóstico

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

## Documentação Relacionada

- [Índice de Resolução de Problemas](../TROUBLESHOOTING.md)
- [Problemas Iniciais](initial_problems.md)
- [Correções Aplicadas](applied_corrections.md)
- [Visão Geral](../../overview.md)
- [Arquitetura](../../architecture.md)
