# Documentação do Google Calendar MCP

## Índice Geral

### Documentação Essencial

- [**Visão Geral**](guides/overview.md) - Introdução e funcionalidades principais
- [**Instalação**](guides/installation.md) - Guia de configuração inicial (inclui Gemini CLI)
- [**Uso**](guides/usage.md) - Como usar as funcionalidades com diferentes clientes

### Configuração e Setup

- [**Arquitetura**](guides/architecture.md) - Estrutura do sistema
- [**Configuração MCP**](guides/mcp_configuration.md) - Setup para Cursor, Gemini CLI e Claude Desktop
- [**Operações e Deployment**](guides/operations.md) - Procedimentos operacionais e CI/CD

### Desenvolvimento

- [**Melhores Práticas**](guides/development_best_practices.md) - Metodologias e padrões
- [**Desenvolvimento Futuro**](future.md) - Roadmap e melhorias planejadas
- [**Atualizações Recentes**](recent_updates.md) - Últimas melhorias e mudanças

### Funcionalidades Específicas

- [**Integração Tasks**](guides/tasks_integration.md) - Google Tasks
- [**Agendamento Inteligente**](guides/intelligent_scheduling.md) - Recursos avançados

### Suporte e Resolução de Problemas

- [**Troubleshooting**](troubleshooting.md) - Resolução de problemas
- [**TROUBLESHOOTING**](TROUBLESHOOTING.md) - Guia detalhado de diagnóstico
- [**Documentos Relacionados**](related_docs.md) - Links e referências

### Histórico de Problemas

- [**Troubleshooting/**](troubleshooting/) - Pasta com correções aplicadas
  - [Problemas Iniciais](troubleshooting/initial_problems.md)
  - [Passos Diagnósticos](troubleshooting/diagnostic_steps.md)
  - [Testes Realizados](troubleshooting/tests_performed.md)
  - [Correções Aplicadas](troubleshooting/applied_corrections.md)
  - [Próximos Passos](troubleshooting/next_steps.md)

## Clientes Suportados

### Atualmente Suportados

- ✅ **Cursor** - Via SSE (Server-Sent Events)
- ✅ **Google Gemini CLI** - Via stdio/stdin-stdout
- ✅ **Claude Desktop** - Via SSE (Server-Sent Events)
- ✅ **HTTP Direto** - Para integrações customizadas

### Configuração Rápida

```bash
# Para Cursor
make mcp-start

# Para Gemini CLI
export GEMINI_API_KEY="sua_chave"
python -m src.mcp.mcp_stdio_server

# Para Claude Desktop
# Editar arquivo de configuração conforme documentação
```

---
Voltar para o [README principal](../README.md)
