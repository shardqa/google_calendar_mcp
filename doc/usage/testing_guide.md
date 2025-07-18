# 🧪 Guia de Testes

## ✅ Status da Configuração

- ✅ Servidor MCP Google Calendar rodando
- ✅ Autenticação OAuth configurada
- ✅ Token.pickle válido
- ✅ Ferramentas disponíveis

## 🎯 Testes Disponíveis

### 1. **Teste de Conexão**

```bash
# Teste básico de conectividade
python -m src.mcp.mcp_stdio_server
```

### 2. **Teste das Ferramentas**

```bash
# Listar eventos
mcp_google_calendar_list_events

# Adicionar evento de teste
mcp_google_calendar_add_event --summary "Teste" --start_time "2024-01-15T10:00:00"

# Teste echo
mcp_google_calendar_echo "teste de conexão"
```

### 3. **Teste com Clientes MCP**

- 🟢 **Claude Desktop** (via SSE direto)
- 🟢 **Cursor** (via stdio)
- 🟢 **Outros clientes MCP** (compatível)

## 🚀 Próximos Passos

**Tudo configurado! Você pode começar a usar o Google Calendar MCP!** 🎉
