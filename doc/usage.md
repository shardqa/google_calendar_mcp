# Uso

## Executando a Aplicação

Execute o programa a partir da raiz do projeto:

```bash
python -m src.main
```

Na primeira execução, você será redirecionado para o navegador para autorizar o acesso ao seu Google Calendar.

## Executando o Servidor MCP

### Início Rápido

Para usar com Cursor, execute o servidor MCP:

```bash
# Usando Make (recomendado)
make mcp-start

# Ou usando script direto
src/scripts/run_mcp.sh

# Ou comando manual
python -m src.commands.mcp_cli --port 3001
```

### Gerenciamento do Servidor

```bash
# Iniciar servidor
make mcp-start

# Parar servidor
make mcp-stop

# Reiniciar servidor
make mcp-restart

# Ver ajuda
make help
```

O servidor estará disponível em `http://localhost:3001/sse` para conexões SSE.

### Ferramentas Disponíveis

O servidor MCP oferece 7 ferramentas:

**Google Calendar:**

- `echo` - Teste de conexão
- `list_events` - Listar eventos do calendário
- `add_event` - Adicionar novos eventos
- `remove_event` - Remover eventos existentes

**Google Tasks:**

- `list_tasks` - Listar tarefas pendentes
- `add_task` - Adicionar novas tarefas
- `remove_task` - Remover tarefas existentes

## Comandos CLI Disponíveis

1. **Listar eventos**: Exibe os próximos eventos do calendário.
2. **Adicionar evento**: Solicita título, descrição, data e hora para criar um evento.
3. **Remover evento**: Solicita o ID do evento para removê-lo.

---
Em caso de problemas, consulte [Resolução de Problemas](troubleshooting.md).
Para melhorias planejadas, consulte [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
