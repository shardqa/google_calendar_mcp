# 🚀 Como Usar o Google Calendar MCP com Autenticação

## ✅ Status Atual
- ✅ Servidor MCP rodando na porta 3001 com autenticação
- ✅ Proxy Nginx na porta 8080
- ✅ Token de autenticação gerado
- ✅ Serviço systemd configurado

## 📋 1. Configuração no Cursor

Cole esta configuração no seu arquivo MCP do Cursor:

```json
{
  "mcpServers": {
    "google_calendar_remote": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://***REMOVED***:8080/sse", "--auth-header", "Authorization: Bearer mcp2.TOKEN"],
      "enabled": true
    }
  }
}
```

## 🔄 2. Passos para Usar

### No Servidor (***REMOVED***):

1. **Verificar se está rodando:**
   ```bash
   ./scripts/test_connection.sh
   ```

2. **Se não estiver funcionando, reiniciar:**
   ```bash
   sudo systemctl restart google-calendar-mcp.service
   sudo systemctl status google-calendar-mcp.service
   ```

3. **Ver logs se houver problemas:**
   ```bash
   sudo journalctl -u google-calendar-mcp.service -f
   ```

### No Cursor (PC Local):

1. **Reiniciar o Cursor completamente**
2. **Aguardar alguns segundos para conectar**
3. **Verificar se aparece "google_calendar_remote" habilitado**
4. **Testar um comando simples como "list my calendar events"**

## 🔧 3. Comandos Disponíveis

Depois que conectar, você pode usar estes comandos no Cursor:

- **Listar eventos:** "Show my calendar events for today"
- **Adicionar evento:** "Add a meeting tomorrow at 2 PM called 'Project Review'"
- **Listar calendários:** "Show all my calendars"
- **Listar tarefas:** "Show my pending tasks"
- **Adicionar tarefa:** "Add a task to call client tomorrow"

## 🔐 4. Segurança

- ✅ **Token JWT** com expiração (24 horas)
- ✅ **Verificação de IP** (só aceita do seu PC)
- ✅ **Rate limiting** (máximo 10 req/s)
- ✅ **Headers de segurança**

## 🚨 5. Troubleshooting

### Se não conectar:

1. **Verificar firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 8080
   sudo ufw allow 3001
   ```

2. **Regenerar token (se expirou):**
   ```bash
   ./scripts/setup_mcp_auth.sh
   ```

3. **Verificar se Nginx está rodando:**
   ```bash
   sudo systemctl status nginx
   ```

4. **No Cursor, verificar:**
   - Se o mcp-remote está instalado: `npx mcp-remote --version`
   - Se não há outras extensões MCP conflitando
   - Se as configurações foram salvas corretamente

### Logs importantes:

- **MCP Server:** `sudo journalctl -u google-calendar-mcp.service -f`
- **Nginx:** `sudo tail -f /var/log/nginx/mcp_error.log`
- **Cursor:** Ver logs no DevTools do Cursor

## 📞 Token de Acesso

O token atual expira em 24 horas. Para gerar um novo:

```bash
cd ***REMOVED***/git/google_calendar_mcp
./scripts/setup_mcp_auth.sh
```

Depois copie o novo token para a configuração do Cursor.

---

**✨ Agora você tem um servidor MCP seguro rodando! Teste no Cursor e veja as ferramentas do Google Calendar aparecendo.** 