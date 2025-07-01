# Configuração MCP (Model Context Protocol)

## Visão Geral

Este projeto oferece um servidor MCP completo que expõe tanto funcionalidades
do Google Calendar quanto do Google Tasks para integração com editores como
Cursor e Google Gemini CLI.

## Configuração Inicial

### 1. Habilitação de APIs no Google Cloud

Para funcionar corretamente, você precisa habilitar as seguintes APIs:

- **Google Calendar API**: Geralmente já habilitada
- **Google Tasks API**: [Habilitar aqui](https://console.developers.google.com/apis/api/tasks.googleapis.com/)

### 2. Configuração OAuth

O projeto usa escopos OAuth expandidos para acessar ambas as APIs:

```python
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]
```

#### Reautorização

Se você já tinha o projeto configurado apenas para Calendar, precisa reautorizar:

```bash
# Remover token existente
rm config/token.pickle

# Próxima execução ativará fluxo OAuth
make mcp-start
```

## Configuração por Cliente

### Cursor (Recomendado)

O servidor cria automaticamente o arquivo `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "http://localhost:3001/sse",
      "type": "sse", 
      "enabled": true,
      "description": "Google Calendar Integration"
    }
  }
}
```

### Google Gemini CLI

Para usar com Gemini CLI, configure `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "google_calendar": {
      "command": "python3",
      "args": ["-m", "src.mcp.mcp_stdio_server"],
      "cwd": "/caminho/para/google_calendar_mcp",
      "timeout": 30000,
      "env": {
        "PYTHONPATH": "/caminho/para/google_calendar_mcp"
      }
    }
  }
}
```

**Configuração de Ambiente:**

```bash
# Definir chave da API
export GEMINI_API_KEY="sua_chave_api_aqui"

# Testar configuração
gemini mcp list
```

**Limitações:** Gemini CLI usa stdio/local servers apenas. Para configurações remotas, use proxy ou configuração local.

### Claude Desktop

Para integração com Claude Desktop usando servidor remoto:

```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "http://seu-servidor:3001/sse",
      "type": "sse",
      "headers": {
        "Authorization": "Bearer seu_token_aqui"
      }
    }
  }
}
```

## Uso no Cursor

### Ferramentas Disponíveis

Após configuração, as seguintes ferramentas ficam disponíveis no Cursor:

**Google Calendar:**

- `@mcp_google_calendar_echo`
- `@mcp_google_calendar_list_events`
- `@mcp_google_calendar_add_event`
- `@mcp_google_calendar_remove_event`

**Google Tasks:**

- `@mcp_google_calendar_list_tasks`
- `@mcp_google_calendar_add_task`
- `@mcp_google_calendar_remove_task`

**Agendamento Inteligente:**

- `@mcp_google_calendar_add_recurring_task`
- `@mcp_google_calendar_schedule_tasks`

### Exemplos de Uso

```bash
# Listar próximos eventos
@mcp_google_calendar_list_events max_results=5

# Adicionar evento
@mcp_google_calendar_add_event summary="Reunião importante" \
  start_time="2024-03-25T10:00:00" end_time="2024-03-25T11:00:00"

# Listar tarefas pendentes
@mcp_google_calendar_list_tasks

# Adicionar tarefa
@mcp_google_calendar_add_task title="Revisar código" \
  notes="Verificar implementação MCP"

# Agendamento inteligente de tarefas
@mcp_google_calendar_schedule_tasks time_period="day" \
  work_hours_start="09:00" work_hours_end="18:00" max_task_duration=120

# Adicionar tarefa recorrente
@mcp_google_calendar_add_recurring_task summary="Daily standup" \
  frequency="daily" count=30 start_time="2024-03-25T09:00:00" \
  end_time="2024-03-25T09:30:00"
```

## Modos de Operação

### Servidor Local (Padrão)

Para desenvolvimento e uso pessoal:

```bash
# Iniciar servidor stdio (Gemini CLI)
python -m src.mcp.mcp_stdio_server

# Iniciar servidor SSE (Cursor)
make mcp-start
```

### Servidor Remoto

Para integração em produção com autenticação:

```bash
# Com autenticação Bearer
python -m src.mcp.mcp_server --auth-required

# Configurar nginx para proxy reverso
# Ver: config/nginx-mcp-remote-secure.conf
```

## Gerenciamento do Servidor

### Comandos Make

```bash
# Iniciar servidor
make mcp-start

# Parar servidor  
make mcp-stop

# Reiniciar servidor (útil após mudanças)
make mcp-restart

# Ver todos os comandos
make help
```

### Verificação de Status

```bash
# Verificar se servidor está rodando
curl http://localhost:3001

# Listar ferramentas disponíveis
curl -X POST http://localhost:3001/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}' \
  | jq .
```

## Troubleshooting

### Status Amarelo no Cursor

O status amarelo no Cursor é comum e geralmente não impede o funcionamento. Pode indicar:

- Conexão em estabelecimento
- Handshake inicial em progresso  
- Compatibilidade de protocolo

**Soluções:**

1. Reiniciar o Cursor
2. Aguardar alguns segundos
3. Testar uma ferramenta diretamente

### Ferramentas Não Encontradas

Se o Cursor retorna "Tool not found":

1. **Verificar servidor**: `curl http://localhost:3001`
2. **Reiniciar servidor**: `make mcp-restart`
3. **Limpar cache**: Remover `__pycache__` directories
4. **Verificar logs**: Servidor mostra requisições recebidas

### Problemas com Gemini CLI

Para erros "command not found" ou timeout:

1. **Verificar caminho**: Use caminho absoluto em `cwd`
2. **Verificar PYTHONPATH**: Deve apontar para raiz do projeto
3. **Testar comando**: Execute manualmente `python -m src.mcp.mcp_stdio_server`
4. **Verificar permissões**: Arquivos devem ser executáveis

### Problemas de Autenticação Google

Para erros "insufficient authentication scopes":

1. **Verificar APIs habilitadas** no Google Cloud Console
2. **Reautorizar** removendo `config/token.pickle`
3. **Aguardar propagação** da ativação da API (alguns minutos)

## Arquitetura MCP

### Handlers

O servidor usa múltiplos handlers para diferentes protocolos:

- **`mcp_stdio_server.py`**: Para conexões stdio (Gemini CLI)
- **`mcp_post_sse_handler.py`**: Para conexões SSE (Cursor)
- **`mcp_post_other_handler.py`**: Para requisições HTTP diretas

Todos implementam as mesmas ferramentas para garantir compatibilidade.

### Schema

As ferramentas são definidas em `mcp_schema.py` seguindo o padrão JSON-RPC 2.0.

---
Para troubleshooting detalhado, veja [Resolução de Problemas](troubleshooting.md).
Para informações de desenvolvimento, veja [Práticas de Desenvolvimento](development_best_practices.md).
Voltar para o [Sumário](README.md).
