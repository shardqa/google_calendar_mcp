# 🛠️ Ferramentas Disponíveis

## 📋 Funcionalidades do Google Calendar MCP

Seu servidor Google Calendar MCP oferece estas funcionalidades através de 
autenticação OAuth:

### 📅 **Gerenciamento de Eventos**
- **Listar eventos** (`mcp_google_calendar_list_events`)
- **Adicionar eventos** (`mcp_google_calendar_add_event`)
- **Editar eventos** (`mcp_google_calendar_edit_event`)
- **Remover eventos** (`mcp_google_calendar_remove_event`)

### 📋 **Gerenciamento de Calendários**
- **Listar calendários** (`mcp_google_calendar_list_calendars`)
- **Calendários externos** (ICS)

### ✅ **Gerenciamento de Tarefas**
- **Listar tarefas** (`mcp_google_calendar_list_tasks`)
- **Adicionar tarefas** (`add_task`)
- **Editar tarefas** (`edit_task`)
- **Remover tarefas** (`remove_task`)

### 🔄 **Funcionalidades Avançadas**
- **Agendamento inteligente** (`mcp_google_calendar_schedule_tasks`)
- **Echo para testes** (`mcp_google_calendar_echo`)

## 🎯 Como Usar

### Autenticação:
O servidor usa OAuth do Google para autenticação. Após a configuração inicial, 
um arquivo `token.pickle` é criado para sessões futuras.

### Exemplos de Comandos:
```bash
# Listar eventos
mcp_google_calendar_list_events

# Adicionar evento
mcp_google_calendar_add_event --summary "Reunião" --start_time "2024-01-15T10:00:00"

# Gerenciar tarefas
mcp_google_calendar_list_tasks

# Agendamento inteligente
mcp_google_calendar_schedule_tasks
```

### Integração com Clientes MCP:
- **Claude Desktop**: Via SSE direto
- **Cursor**: Via stdio
- **Outros clientes MCP**: Compatível com stdio e SSE
