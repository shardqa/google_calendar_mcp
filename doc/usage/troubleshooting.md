# 🔧 Solução de Problemas

## 🚨 Problemas Comuns

### **Problema**: Erro de autenticação OAuth

**Sintoma**: Erro relacionado ao token.pickle ou autenticação Google

**Solução**:

```bash
# Verificar se o token existe
ls -la token.pickle

# Se não existir, recriar autenticação
python -m src.auth
```

### **Problema**: Servidor MCP não inicia

**Sintoma**: Erro ao executar o servidor stdio

**Solução**:

```bash
# Verificar dependências
pip install -r requirements.txt

# Testar servidor
python -m src.mcp.mcp_stdio_server
```

### **Problema**: Ferramentas não respondem

**Sintoma**: Comandos retornam erro ou não funcionam

**Solução**:

```bash
# Verificar configuração MCP
cat ~/.config/mcp/servers/google-calendar.json

# Testar ferramenta específica
mcp_google_calendar_echo "teste"
```

## 🔍 Comandos de Debug

```bash
# Verificar status do servidor
ps aux | grep mcp

# Verificar logs
tail -f /var/log/mcp/google-calendar.log

# Testar conectividade
curl -X POST http://localhost:3001/health
```

## 📞 Suporte

Se os problemas persistirem, verifique:

- Configuração OAuth do Google
- Permissões do token.pickle
- Logs do servidor MCP
