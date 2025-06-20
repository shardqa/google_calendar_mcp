# Testes Realizados

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

## Documentação Relacionada

- [Índice de Resolução de Problemas](../TROUBLESHOOTING.md)
- [Problemas Iniciais](initial_problems.md)
- [Passos de Diagnóstico](diagnostic_steps.md)
- [Correções Aplicadas](applied_corrections.md)
- [Próximos Passos](next_steps.md)
- [Visão Geral](../../overview.md)
- [Arquitetura](../../architecture.md)
