# Configuração Manual do MCP Remote (Porta 8080)

## Resumo dos Problemas Identificados

Com base nas pesquisas, o Cursor tem os seguintes problemas com MCP servers remotos:

1. **Problemas com HTTPS/certificados**: Cursor não suporta bem self-signed certificates
2. **Limitação de tools**: Cursor só reconhece cerca de 40 tools por vez
3. **Nomes com hífens**: Tools com `-` no nome não são reconhecidos (use `_`)
4. **Primeiro startup falha**: Primeira conexão SSE sempre falha no Windows, funciona no reload

## Solução: Usar mcp-remote

O `mcp-remote` é um adapter que permite usar MCP servers remotos com clientes que só suportam stdio.

## Vantagens desta configuração:

- ✅ **Porta 8080**: Não conflita com outros serviços na porta 80
- ✅ **Sem dependências Google**: Usa suas configurações existentes
- ✅ **Comunicação simples**: Foca apenas na comunicação MCP
- ✅ **HTTP simples**: Sem problemas de certificados

## Comandos para Executar no Servidor

### 1. Execute o script de setup (como root):

```bash
sudo ./scripts/setup_mcp_remote.sh
```

### 2. Verifique se tudo está funcionando:

```bash
./scripts/test_mcp_remote.sh
```

### 3. Se houver problemas, verifique os logs:

```bash
# Logs do MCP Server
sudo journalctl -u google-calendar-mcp -f

# Logs do Nginx
sudo tail -f /var/log/nginx/mcp_remote_error.log

# Status dos serviços
sudo systemctl status google-calendar-mcp
sudo systemctl status nginx
```

### 4. Comandos úteis pentru debug:

```bash
# Reiniciar o MCP Server
sudo systemctl restart google-calendar-mcp

# Reiniciar o Nginx
sudo systemctl restart nginx

# Testar endpoint manualmente
curl -v http://localhost:8080/sse
curl -v http://localhost:3001/sse

# Ver portas abertas
sudo netstat -tuln | grep -E ':(8080|3001)'
```

## Configuração no Cliente (Cursor)

### No seu computador local, edite `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "google_calendar_remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://SEU_IP_DO_SERVIDOR:8080/sse"
      ],
      "enabled": true
    }
  }
}
```

**Substitua `SEU_IP_DO_SERVIDOR`** pelo IP real do seu servidor.

### Exemplo completo para Cursor:

```json
{
  "mcpServers": {
    "google_calendar_remote": {
      "name": "Google Calendar Remote",
      "description": "Google Calendar via mcp-remote",
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://192.168.1.100:8080/sse"
      ],
      "enabled": true,
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

## Troubleshooting

### Se o mcp-remote não funcionar:

1. **Instalar globalmente**:
   ```bash
   npm install -g mcp-remote
   ```

2. **Usar caminho absoluto**:
   ```json
   {
     "command": "/usr/local/bin/node",
     "args": [
       "/usr/local/lib/node_modules/mcp-remote/bin/mcp-remote.js",
       "http://SEU_IP:8080/sse"
     ]
   }
   ```

3. **Debug mode**:
   ```json
   {
     "args": [
       "mcp-remote",
       "http://SEU_IP:8080/sse",
       "--debug"
     ]
   }
   ```

### Se ainda não funcionar, tente HTTP direto:

```json
{
  "mcpServers": {
    "google_calendar_direct": {
      "url": "http://SEU_IP:8080/sse",
      "type": "sse",
      "enabled": true
    }
  }
}
```

## Verificação Final

1. **No servidor**, execute:
   ```bash
   curl http://localhost:8080/sse
   ```

2. **Do seu computador**, execute:
   ```bash
   curl http://SEU_IP_DO_SERVIDOR:8080/sse
   ```

3. **No Cursor**, reinicie e verifique se o MCP server aparece na lista.

## Alternativa: Usar Túnel SSH

Se o acesso direto não funcionar, use um túnel SSH:

```bash
# No seu computador local
ssh -L 8080:localhost:8080 your-username@YOUR_SERVER_IP

# No Cursor, use:
"http://localhost:8080/sse"
```

## Verificar se a porta 8080 está livre

Antes de executar, verifique se a porta 8080 está disponível:

```bash
# Verificar se a porta está em uso
sudo netstat -tuln | grep :8080

# Se estiver ocupada, você pode alterar no arquivo:
# config/nginx-mcp-remote.conf (linha: listen 8080;)
```

## Notas Importantes

- ✅ **Servidor roda na porta 3001**, Nginx proxy na **porta 8080**
- ✅ **Sem configuração Google**: Usa suas configurações existentes
- ✅ **Portas 8080 e 3001**: Devem estar abertas no firewall
- ✅ **mcp-remote**: Funciona como um bridge entre stdio e HTTP+SSE
- ✅ **Underscores**: Sempre use `_` nos nomes dos tools, não hífens (`-`)

## Comandos de Manutenção

```bash
# Ver logs em tempo real
sudo journalctl -u google-calendar-mcp -f

# Restart completo
sudo systemctl restart google-calendar-mcp nginx

# Verificar configuração
sudo nginx -t

# Verificar portas
sudo netstat -tuln | grep -E ':(8080|3001)'

# Limpar logs antigos
sudo journalctl --rotate
sudo journalctl --vacuum-time=1d
```

## Teste Rápido

Para verificar se está funcionando:

```bash
# 1. Testar no servidor
curl -v http://localhost:8080/sse

# 2. Testar do cliente
curl -v http://SEU_IP:8080/sse

# 3. Se ambos funcionarem, configure o Cursor e reinicie
``` 