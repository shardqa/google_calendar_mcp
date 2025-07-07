# Autenticação Bearer Robusta para MCP

## Visão Geral

Esta implementação oferece uma solução de autenticação robusta que funciona perfeitamente com o Cursor IDE, combinando:

- **Bearer tokens seguros** com HMAC-SHA512
- **Rate limiting** inteligente
- **IP whitelisting** opcional
- **Proteção contra ataques** de força bruta
- **HTTPS** sem complexidade de mTLS

## Características de Segurança

### Token Structure
```
Format: mcp2.{base64_encoded_payload}
Payload: {
  "p": {
    "client_id": "cursor-ide",
    "iat": 1704067200,
    "exp": 1704672000,
    "jti": "unique_token_id",
    "nonce": "random_nonce",
    "version": "2.0",
    "client_ip": "192.168.1.100"  // opcional
  },
  "s": "hmac_sha512_signature",
  "alg": "HS512"
}
```

### Proteções Implementadas

1. **Assinatura HMAC-SHA512**: Impede falsificação de tokens
2. **Nonce único**: Previne replay attacks
3. **Expiração configurável**: Tokens com tempo de vida limitado
4. **Rate limiting**: 100 requests/hora por IP
5. **IP binding**: Token pode ser vinculado a IP específico
6. **Proteção força bruta**: Bloqueio após 10 tentativas falhadas

## Setup Rápido

### 1. Configuração Automática

```bash
# Setup completo
./scripts/setup_secure_mcp.sh --server-ip 10.243.215.33 --client-ip 192.168.1.100

# Ou com domínio
./scripts/setup_secure_mcp.sh --domain your-server.com --client-ip 192.168.1.100
```

### 2. Configuração Manual

```bash
# Gerar chave secreta
python3 scripts/generate_secure_token.py --generate-secret --env-file .env.mcp

# Carregar ambiente
source .env.mcp

# Gerar token
python3 scripts/generate_secure_token.py --client-ip 192.168.1.100 --expiry-hours 168
```

## Configuração do Servidor

### Variáveis de Ambiente

```bash
# Obrigatório
export MCP_SECRET_KEY="sua_chave_secreta_aqui"

# Opcional
export MCP_TOKEN_EXPIRY="604800"  # 7 dias em segundos
export MCP_ALLOWED_IPS="192.168.1.0/24,10.0.0.0/8"  # CIDR ou IPs específicos
export MCP_ALLOWED_CLIENTS="cursor-ide,vscode"  # Clientes permitidos
```

### Systemd Service

Criar override para o serviço:

```bash
sudo mkdir -p /etc/systemd/system/google-calendar-mcp.service.d/
sudo tee /etc/systemd/system/google-calendar-mcp.service.d/override.conf << EOF
[Service]
Environment="MCP_SECRET_KEY=your_secret_key_here"
Environment="MCP_TOKEN_EXPIRY=604800"
Environment="MCP_ALLOWED_IPS=192.168.1.0/24"
Environment="MCP_ALLOWED_CLIENTS=cursor-ide"
EOF

sudo systemctl daemon-reload
sudo systemctl restart google-calendar-mcp
```

## Configuração do Nginx

A configuração atualizada inclui:

- **Rate limiting**: Diferentes limites para API e SSE
- **HTTPS obrigatório**: Redirecionamento automático
- **Headers de segurança**: HSTS, CSP, etc.
- **Proxy otimizado**: Keep-alive e timeouts adequados

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=sse:10m rate=5r/s;

# Upstream com keep-alive
upstream mcp_backend {
    server 127.0.0.1:3001;
    keepalive 32;
}
```

## Configuração do Cursor

### mcp.json
```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "https://10.243.215.33/sse",
      "type": "sse",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer mcp2.YOUR_JWT_TOKEN_HERE"
      },
      "description": "Google Calendar Integration (Secure)"
    }
  }
}
```

## Operações de Manutenção

### Rotação de Tokens

```bash
# Gerar novo token
NEW_TOKEN=$(python3 scripts/generate_secure_token.py --client-ip 192.168.1.100 --expiry-hours 168 | grep "Token:" | cut -d' ' -f2)

# Atualizar configuração do Cursor
echo "Novo token: $NEW_TOKEN"

# Opcional: Invalidar tokens antigos (regenerar secret)
python3 scripts/generate_secure_token.py --generate-secret --env-file .env.mcp
```

### Monitoramento

```bash
# Verificar estatísticas de autenticação
curl -H "Authorization: Bearer $TOKEN" https://your-server.com/auth/stats

# Logs do nginx
sudo tail -f /var/log/nginx/mcp_access.log
sudo tail -f /var/log/nginx/mcp_error.log

# Logs do MCP
sudo journalctl -u google-calendar-mcp -f
```

### Troubleshooting

#### Token Inválido
```
HTTP 401: Authentication failed: Invalid signature
```
- Verificar se `MCP_SECRET_KEY` está correto no servidor
- Regenerar token com a chave correta

#### IP Bloqueado
```
HTTP 401: Authentication failed: IP not allowed
```
- Verificar `MCP_ALLOWED_IPS`
- Adicionar IP do cliente à whitelist

#### Rate Limit
```
HTTP 429: Too Many Requests
```
- Aguardar reset do rate limit
- Verificar se há loop de requisições

## Segurança Avançada

### Firewall (UFW)
```bash
# Permitir apenas HTTPS
sudo ufw allow 443/tcp

# Restringir por IP (opcional)
sudo ufw allow from 192.168.1.0/24 to any port 443

# Bloquear acesso direto ao MCP
sudo ufw deny 3001/tcp
```

### Fail2ban
```bash
# /etc/fail2ban/jail.local
[nginx-mcp-auth]
enabled = true
filter = nginx-mcp-auth
action = iptables-allports[name=mcp-auth]
logpath = /var/log/nginx/mcp_error.log
findtime = 600
bantime = 3600
maxretry = 5
```

### Monitoramento com Telegraf
```toml
[[inputs.nginx]]
  urls = ["http://localhost/nginx_status"]
  
[[inputs.logparser]]
  files = ["/var/log/nginx/mcp_access.log"]
  from_beginning = false
  [inputs.logparser.grok]
    patterns = ['%{COMBINED_LOG_FORMAT}']
    measurement = "nginx_access"
```

## Performance

### Métricas Típicas
- **Latência**: < 50ms para operações básicas
- **Throughput**: 1000+ requests/minuto
- **Memória**: ~50MB para middleware
- **CPU**: < 5% em servidor modesto

### Otimizações
- Keep-alive connections no Nginx
- Rate limiting inteligente
- Cache de verificação de tokens
- Cleanup automático de sessions expiradas

## Links Relacionados

- [Plano de Segurança](./security_plan.md)
- [Configuração MCP](./mcp_configuration.md)
- [Troubleshooting](../troubleshooting.md) 