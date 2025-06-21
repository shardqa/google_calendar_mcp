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

O servidor MCP oferece 8 ferramentas:

**Google Calendar:**

- `echo` - Teste de conexão
- `list_events` - Listar eventos do calendário com informações detalhadas (data/hora, localização, descrição)
- `add_event` - Adicionar novos eventos
- `add_recurring_task` - Criar tarefas recorrentes (diário, semanal, mensal) como lembretes de medicação
- `remove_event` - Remover eventos existentes

**Google Tasks:**

- `list_tasks` - Listar tarefas pendentes
- `add_task` - Adicionar novas tarefas
- `remove_task` - Remover tarefas existentes

### Tarefas Recorrentes

O sistema agora suporta criação de tarefas recorrentes através do Google Calendar, ideal para atividades repetitivas como:

- Lembretes de medicação
- Exercícios diários
- Reuniões semanais
- Check-ups mensais

**Exemplo de uso:**

```bash
# Criar lembrete diário para tomar remédio
add_recurring_task:
  summary: "Tomar medicação"
  frequency: "daily"
  count: 30
  start_time: "2024-03-20T08:00:00Z"
  end_time: "2024-03-20T08:30:00Z"
  description: "Lembrete diário - medicação da manhã"
```

**Frequências suportadas:**

- `daily`: Recorrência diária
- `weekly`: Recorrência semanal  
- `monthly`: Recorrência mensal

### Exibição Aprimorada de Eventos

Os eventos do calendário agora exibem informações completas:

- 📅 Data e hora de início/fim
- 📍 Localização (quando disponível)
- 📝 Descrição (quando disponível)
- Formatação visual com emojis para melhor legibilidade

## Comandos CLI Disponíveis

1. **Listar eventos**: Exibe os próximos eventos do calendário.
2. **Adicionar evento**: Solicita título, descrição, data e hora para criar um evento.
3. **Remover evento**: Solicita o ID do evento para removê-lo.

---
Em caso de problemas, consulte [Resolução de Problemas](troubleshooting.md).
Para melhorias planejadas, consulte [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
