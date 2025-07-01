# Plano de Segurança - Google Calendar MCP

## Visão Geral

Este documento descreve a implementação de segurança para o servidor Google Calendar MCP, incluindo:

- Nginx reverse-proxy com HTTPS
- Mutual TLS (mTLS) enforcement
- Configuração de firewall
- Rate limiting e proteção contra ataques
- Monitoramento e logging

## Arquitetura de Segurança

```
Cliente (Cursor)     Nginx Reverse Proxy     MCP Server
    |                        |                    |
    |-- HTTPS + mTLS -------->|                    |
    |                        |-- HTTP ---------> |
    |                        |   (localhost)      |
    |                        |                    |
  (443)                    (443)              (3001)
```

## Certificados e PKI

### Certificados Utilizados

**No VPS (Servidor):**
- `ca-cert.pem` - Certificado da Autoridade Certificadora (CA)
- `server-cert.pem` - Certificado do servidor
- `server-key.pem` - Chave privada do servidor

**Local (Cliente):**
- `ca-cert.pem` - Certificado da CA (para validar servidor)
- `client-cert.pem` - Certificado do cliente
- `client-key.pem` - Chave privada do cliente

### Localização dos Certificados

```bash
# VPS
***REMOVED***/ca-cert.pem
***REMOVED***/server-cert.pem
***REMOVED***/server-key.pem

# Cliente Local
~/mcp_certs/client_certs/ca-cert.pem
~/mcp_certs/client_certs/client-cert.pem
~/mcp_certs/client_certs/client-key.pem
```

## Configuração do Nginx

### Características Principais

1. **HTTPS Obrigatório**: Redirecionamento automático de HTTP para HTTPS
2. **Mutual TLS**: Verificação de certificado cliente obrigatória
3. **Headers de Segurança**: HSTS, X-Frame-Options, etc.
4. **Proxy Reverso**: Encaminha requisições para o servidor MCP interno

### Configuração SSL/TLS

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers on;
ssl_verify_client on;
```

### Headers de Segurança

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```

## Configuração de Firewall

### UFW (Uncomplicated Firewall)

```bash
# Permitir apenas HTTPS e SSH
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 80/tcp    # HTTP (redirect)

# Bloquear acesso direto ao MCP server
sudo ufw deny 3001/tcp

# Restringir a interface ZeroTier (opcional)
sudo ufw allow in on zt+ to any port 443
```

### Iptables (alternativa)

```bash
# Limpar regras existentes
sudo iptables -F

# Permitir loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Permitir conexões estabelecidas
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permitir SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Permitir HTTPS
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Permitir HTTP (redirect)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Bloquear MCP direto
sudo iptables -A INPUT -p tcp --dport 3001 -j DROP

# Política padrão: DROP
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
```

## Rate Limiting e Proteção

### Nginx Rate Limiting

Adicionar ao `nginx.conf`:

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=sse:10m rate=5r/s;
    
    server {
        location / {
            limit_req zone=api burst=20 nodelay;
        }
        
        location /sse {
            limit_req zone=sse burst=10 nodelay;
        }
    }
}
```

### Fail2ban

Configuração para proteger contra ataques de força bruta:

```ini
# /etc/fail2ban/jail.local
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/mcp_error.log
findtime = 600
bantime = 7200
maxretry = 10
```

## Monitoramento e Logging

### Logs do Nginx

```bash
# Logs de acesso
tail -f /var/log/nginx/mcp_access.log

# Logs de erro
tail -f /var/log/nginx/mcp_error.log

# Análise de logs com fail2ban
sudo fail2ban-client status nginx-limit-req
```

### Logs do Sistema

```bash
# Status do Nginx
sudo systemctl status nginx

# Logs do sistema
sudo journalctl -u nginx -f

# Verificar certificados SSL
openssl s_client -connect localhost:443 -cert client-cert.pem -key client-key.pem
```

### Logrotate

Configuração para rotação de logs:

```bash
# /etc/logrotate.d/nginx-mcp
/var/log/nginx/mcp_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 640 nginx adm
    sharedscripts
    prerotate
        if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
            run-parts /etc/logrotate.d/httpd-prerotate; \
        fi
    endscript
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1
    endscript
}
```

## Configuração do Cliente

### Cursor MCP Configuration

Atualizar `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "https://localhost:443/sse",
      "type": "sse",
      "enabled": true,
      "description": "Google Calendar Integration (HTTPS + mTLS)",
      "sslOptions": {
        "cert": "~/mcp_certs/client_certs/client-cert.pem",
        "key": "~/mcp_certs/client_certs/client-key.pem",
        "ca": "~/mcp_certs/client_certs/ca-cert.pem"
      }
    }
  }
}
```

### Teste de Conectividade

```bash
# Teste básico com curl
curl -k --cert ~/mcp_certs/client_certs/client-cert.pem \
       --key ~/mcp_certs/client_certs/client-key.pem \
       --cacert ~/mcp_certs/client_certs/ca-cert.pem \
       https://localhost:443/

# Teste do endpoint SSE
curl -k --cert ~/mcp_certs/client_certs/client-cert.pem \
       --key ~/mcp_certs/client_certs/client-key.pem \
       --cacert ~/mcp_certs/client_certs/ca-cert.pem \
       -X POST https://localhost:443/sse \
       -H "Content-Type: application/json" \
       -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

## Instalação e Configuração

### 1. Execução do Script de Setup

```bash
# Dar permissão de execução
chmod +x scripts/setup_nginx.sh

# Executar como root
sudo ./scripts/setup_nginx.sh
```

### 2. Verificação da Instalação

```bash
# Verificar status do Nginx
sudo systemctl status nginx

# Verificar configuração
sudo nginx -t

# Verificar portas abertas
sudo netstat -tlnp | grep nginx
```

### 3. Configuração do Firewall

```bash
# Verificar status do UFW
sudo ufw status

# Aplicar regras se necessário
sudo ufw enable
```

## Troubleshooting

### Problemas Comuns

1. **Certificado inválido**
   ```bash
   # Verificar certificado
   openssl x509 -in server-cert.pem -text -noout
   ```

2. **Nginx não inicia**
   ```bash
   # Verificar logs
   sudo journalctl -u nginx -n 50
   
   # Testar configuração
   sudo nginx -t
   ```

3. **Cliente não consegue conectar**
   ```bash
   # Verificar se o certificado cliente é válido
   openssl verify -CAfile ca-cert.pem client-cert.pem
   ```

4. **Rate limiting ativo**
   ```bash
   # Verificar logs de rate limiting
   grep "limiting requests" /var/log/nginx/mcp_error.log
   ```

### Comandos Úteis

```bash
# Recarregar configuração do Nginx
sudo nginx -s reload

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar processos Nginx
ps aux | grep nginx

# Verificar conexões ativas
sudo netstat -anp | grep :443

# Verificar certificados SSL
openssl s_client -connect localhost:443 -showcerts
```

## Atualizações de Segurança

### Dependency Scanning

```bash
# Scan de vulnerabilidades Python
pip-audit --requirement requirements.txt

# Atualização de pacotes do sistema
sudo apt update && sudo apt upgrade

# Atualização do Nginx
sudo apt update nginx
```

### Renovação de Certificados

```bash
# Verificar validade dos certificados
openssl x509 -in server-cert.pem -noout -dates

# Procedimento de renovação (manual)
# 1. Gerar novos certificados
# 2. Substituir arquivos antigos
# 3. Recarregar Nginx
sudo nginx -s reload
```

## Backup e Disaster Recovery

### Backup dos Certificados

```bash
# Criar backup dos certificados
tar -czf nginx-certs-backup-$(date +%Y%m%d).tar.gz \
    ***REMOVED***/*.pem

# Backup da configuração do Nginx
cp -r /etc/nginx /etc/nginx-backup-$(date +%Y%m%d)
```

### Restauração

```bash
# Restaurar certificados
tar -xzf nginx-certs-backup-YYYYMMDD.tar.gz -C /

# Restaurar configuração
cp -r /etc/nginx-backup-YYYYMMDD/* /etc/nginx/

# Recarregar Nginx
sudo systemctl restart nginx
```

## Referências

- [Nginx SSL/TLS Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP TLS Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [Let's Encrypt Best Practices](https://letsencrypt.org/docs/) 