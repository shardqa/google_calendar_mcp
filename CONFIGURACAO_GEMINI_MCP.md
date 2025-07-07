# Configuração Google Gemini CLI com MCP

## Configuração Funcional

Esta é a configuração testada e funcional para usar o Google Calendar MCP com Gemini CLI.

### 1. Arquivo de Configuração

Editar o arquivo `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "google_calendar": {
      "command": "python3",
      "args": ["-m", "src.mcp.mcp_stdio_server"],
      "cwd": "/home/***REMOVED***/git/google_calendar_mcp",
      "timeout": 30000,
      "env": {
        "PYTHONPATH": "/home/***REMOVED***/git/google_calendar_mcp"
      }
    }
  }
}
```

### 2. Variável de Ambiente

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 3. Teste de Funcionamento

```bash
# Listar servidores MCP
gemini mcp list

# Teste básico
gemini "Use o echo tool para testar: funcionando!"

# Listar eventos do calendário
gemini "Liste meus próximos eventos do calendário"

# Listar tarefas
gemini "Quais tarefas tenho pendentes no Google Tasks?"
```

## Ferramentas Disponíveis

### Google Calendar

- `echo` - Teste de conexão
- `list_events` - Listar eventos
- `list_calendars` - Listar calendários disponíveis
- `add_event` - Adicionar eventos
- `edit_event` - Editar eventos
- `remove_event` - Remover eventos
- `add_recurring_task` - Criar tarefas recorrentes

### Google Tasks

- `list_tasks` - Listar tarefas
- `add_task` - Adicionar tarefas
- `remove_task` - Remover tarefas
- `complete_task` - Marcar como concluída
- `update_task_status` - Atualizar status

### Recursos Avançados

- `schedule_tasks` - Agendamento inteligente
- `register_ics_calendar` - Registrar calendários externos
- `list_ics_calendars` - Listar calendários registrados

## Exemplos de Uso

### Comandos Naturais

```bash
# Eventos
gemini "Adicione uma reunião amanhã às 15h sobre projeto MCP"
gemini "Liste meus próximos 5 eventos"
gemini "Remova o evento 'Reunião de equipe' de amanhã"

# Tarefas
gemini "Adicione uma tarefa para revisar documentação"
gemini "Marque a tarefa 'Finalizar relatório' como concluída"
gemini "Agende minhas tarefas pendentes para esta semana"

# Recorrentes
gemini "Crie um lembrete diário para tomar remédio às 8h por 30 dias"
gemini "Configure uma reunião semanal de standup às segundas 9h"
```

### Comandos Específicos

```bash
# Teste de conectividade
gemini "Use a ferramenta echo com a mensagem: teste funcionando"

# Listar calendários
gemini "Use list_calendars para mostrar meus calendários"

# Agendamento inteligente
gemini "Use schedule_tasks para organizar minhas tarefas hoje das 9h às 17h"
```

## Características Técnicas

### Protocolo

- **Tipo**: stdio (stdin/stdout)
- **Formato**: JSON-RPC 2.0
- **Autenticação**: OAuth2 Google (local)

### Limitações

- Não suporta SSE (Server-Sent Events) remotos
- Requer servidor local funcionando
- Dependente de credenciais Google válidas

### Vantagens

- Integração nativa com Gemini CLI
- Comandos em linguagem natural
- Suporte completo a todas as ferramentas
- Performance otimizada (stdio)

## Resolução de Problemas

### Comando não encontrado

```bash
# Verificar se o caminho está correto
python3 -m src.mcp.mcp_stdio_server

# Verificar PYTHONPATH
echo $PYTHONPATH
```

### Timeout ou falhas

```bash
# Verificar se as dependências estão instaladas
pip install -r requirements.txt

# Verificar autenticação Google
python -m src.main
```

### Gemini CLI não encontra servidor

1. Usar caminho absoluto em `cwd`
2. Definir `PYTHONPATH` corretamente
3. Verificar se `python3` está disponível
4. Testar comando manualmente

## Status de Teste

✅ **Funcionando**: Configuração testada em 2024-12
✅ **Ferramentas**: 15+ ferramentas disponíveis
✅ **Performance**: Resposta < 500ms
✅ **Compatibilidade**: Gemini CLI versão atual

---

Para mais informações, consulte:

- [Configuração MCP](doc/guides/mcp_configuration.md)
- [Instalação](doc/guides/installation.md)
- [Uso](doc/guides/usage.md)
