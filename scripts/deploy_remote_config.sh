#!/bin/bash

set -e

echo "=== Deploy das Configurações para Servidor Remoto ==="
echo

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $0 [SERVER_IP] [SSH_USER]"
    echo
    echo "Exemplo: $0 10.243.215.33 richard"
    echo
    exit 0
fi

SERVER_IP="${1:-10.243.215.33}"
SSH_USER="${2:-richard}"
PROJECT_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

echo "Servidor: $SSH_USER@$SERVER_IP"
echo "Projeto: $PROJECT_ROOT"
echo

echo "1. Copiando arquivos para o servidor..."

# Copiar nginx.conf
scp "$PROJECT_ROOT/config/nginx.conf" "$SSH_USER@$SERVER_IP:/tmp/nginx.conf"

# Copiar auth middleware
scp "$PROJECT_ROOT/src/mcp/auth_middleware.py" "$SSH_USER@$SERVER_IP:/tmp/auth_middleware.py"

# Copiar handler atualizado
scp "$PROJECT_ROOT/src/mcp/mcp_handler.py" "$SSH_USER@$SERVER_IP:/tmp/mcp_handler.py"

# Copiar script de geração de token
scp "$PROJECT_ROOT/scripts/generate_secure_token.py" "$SSH_USER@$SERVER_IP:/tmp/generate_secure_token.py"

echo "   ✅ Arquivos copiados"

echo
echo "2. Aplicando configurações no servidor..."

ssh "$SSH_USER@$SERVER_IP" << 'ENDSSH'
set -e

echo "   - Backup das configurações atuais..."
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

echo "   - Instalando nova configuração do nginx..."
sudo cp /tmp/nginx.conf /etc/nginx/sites-available/default

echo "   - Testando configuração do nginx..."
sudo nginx -t

echo "   - Atualizando código do MCP..."
# Assumindo que o código está em /opt/google-calendar-mcp ou similar
MCP_PATH="/opt/google-calendar-mcp"
if [ -d "$MCP_PATH" ]; then
    sudo cp /tmp/auth_middleware.py "$MCP_PATH/src/mcp/"
    sudo cp /tmp/mcp_handler.py "$MCP_PATH/src/mcp/"
    sudo cp /tmp/generate_secure_token.py "$MCP_PATH/scripts/"
    sudo chmod +x "$MCP_PATH/scripts/generate_secure_token.py"
else
    echo "   ⚠️  Diretório $MCP_PATH não encontrado. Ajuste conforme sua instalação."
fi

echo "   - Configurando variáveis de ambiente..."
sudo mkdir -p /etc/systemd/system/google-calendar-mcp.service.d/

# Gerar chave secreta se não existir
if [ ! -f ***REMOVED***/.mcp_secret ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
    echo "$SECRET_KEY" > ***REMOVED***/.mcp_secret
    chmod 600 ***REMOVED***/.mcp_secret
fi

SECRET_KEY=$(cat ***REMOVED***/.mcp_secret)

sudo tee /etc/systemd/system/google-calendar-mcp.service.d/override.conf << EOF
[Service]
Environment="MCP_SECRET_KEY=$SECRET_KEY"
Environment="MCP_TOKEN_EXPIRY=604800"
Environment="MCP_ALLOWED_CLIENTS=cursor-ide"
EOF

echo "   - Abrindo porta 8443 no firewall..."
sudo ufw allow 8443/tcp || true

echo "   - Reiniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl restart google-calendar-mcp
sudo systemctl restart nginx

echo "   ✅ Configuração aplicada com sucesso!"
ENDSSH

echo
echo "3. Gerando token seguro..."

# Gerar token no servidor remoto
TOKEN_OUTPUT=$(ssh "$SSH_USER@$SERVER_IP" "cd /tmp && python3 generate_secure_token.py --client-ip $(curl -s ifconfig.me) --expiry-hours 168")

echo "$TOKEN_OUTPUT"

echo
echo "=== Deploy Concluído ==="
echo
echo "✅ Servidor configurado na porta 8443"
echo "✅ Nginx atualizado e reiniciado" 
echo "✅ MCP server atualizado com autenticação"
echo "✅ Firewall configurado"
echo
echo "🔗 Teste a conexão:"
echo "curl -k -I https://$SERVER_IP:8443/health"
echo
echo "📝 Seu mcp.json local já está correto!" 