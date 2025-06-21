# Configuração de Servidor MCP Remoto

Este documento descreve como configurar o Google Calendar MCP para acesso remoto.

## Problema Identificado

O servidor MCP está rodando via systemd, mas não está acessível externamente porque:

1. **Binding**: O servidor está fazendo bind apenas em `localhost` (127.0.0.1)
2. **Firewall**: A porta 3001 pode estar bloqueada no firewall
3. **Configuração**: Precisa permitir acesso externo

## Solução

### 1. Atualizar o Service do Systemd

Edite o arquivo `/etc/systemd/system/google-calendar-mcp.service`:

```bash
sudo nano /etc/systemd/system/google-calendar-mcp.service
```

Altere a linha `ExecStart` para:

```ini
[Unit]
Description=Google Calendar MCP Server
After=network.target

[Service]
User=richard
WorkingDirectory=***REMOVED***/git/google_calendar_mcp
ExecStart=***REMOVED***/git/google_calendar_mcp/.venv/bin/python \
          -m src.commands.mcp_cli --port 3001 --host 0.0.0.0
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Mudança**: Adicionar `--host 0.0.0.0` para aceitar conexões de qualquer IP.

### 2. Recarregar e Reiniciar o Service

```bash
sudo systemctl daemon-reload
sudo systemctl restart google-calendar-mcp
sudo systemctl status google-calendar-mcp
```

### 3. Configurar Firewall (se necessário)

```bash
# Verificar se a porta está bloqueada
sudo ufw status

# Abrir a porta 3001 se necessário
sudo ufw allow 3001/tcp

# Ou usando iptables
sudo iptables -A INPUT -p tcp --dport 3001 -j ACCEPT
```

### 4. Testar Conectividade

```bash
# Do cliente, testar se a porta está aberta
telnet ***REMOVED*** 3001

# Testar o endpoint MCP
curl -X POST http://***REMOVED***:3001/sse \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## Configuração do Cliente (Cursor)

### Arquivo `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "http://***REMOVED***:3001/sse",
      "type": "sse",
      "enabled": true,
      "description": "Google Calendar Integration"
    }
  }
}
```

### Verificação

1. **Restart do Cursor**: Reinicie o Cursor após alterar o mcp.json
2. **Logs**: Verifique os logs do Cursor para mensagens de erro
3. **Network**: Verifique se não há proxy/VPN interferindo

## Troubleshooting

### Servidor não acessível externamente

```bash
# Verificar se está fazendo bind em 0.0.0.0
sudo netstat -tlnp | grep 3001

# Deve mostrar algo como:
# tcp   0   0 0.0.0.0:3001   0.0.0.0:*   LISTEN   1627478/python
```

### Firewall bloqueando

```bash
# Verificar regras do firewall
sudo ufw status numbered
sudo iptables -L -n

# Verificar logs de conexão
sudo tail -f /var/log/ufw.log
```

### Logs do servidor

```bash
# Verificar logs do serviço
sudo journalctl -u google-calendar-mcp -f

# Verificar status detalhado
sudo systemctl status google-calendar-mcp -l
```

## Segurança

### Considerações importantes

1. **HTTPS**: Para produção, considere usar HTTPS/TLS
2. **Autenticação**: Implementar autenticação adequada
3. **Firewall**: Restringir acesso apenas a IPs confiáveis
4. **Monitoring**: Configurar monitoramento e alertas

### Exemplo de configuração segura

```bash
# Permitir apenas de IP específico
sudo ufw allow from 192.168.1.0/24 to any port 3001

# Ou usando iptables
sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 3001 -j ACCEPT
```

## Links Relacionados

- [Arquitetura](./architecture.md)
- [Configuração MCP](./mcp_configuration.md)
- [Troubleshooting](./troubleshooting.md)
