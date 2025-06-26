#!/bin/bash

set -e

echo "=== Deploy das Configurações para Servidor Remoto ==="
echo

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $0 [SERVER_IP] [SSH_USER] [--skip-nginx]"
    echo
    echo "Exemplo: $0 10.243.215.33 richard --skip-nginx"
    echo
    exit 0
fi

# Detect optional flag --skip-nginx
SKIP_NGINX=0
for arg in "$@"; do
  if [[ "$arg" == "--skip-nginx" ]]; then
    SKIP_NGINX=1
  fi
done

# Remove flags from positional params
POSITIONAL=()
for arg in "$@"; do
  case $arg in
    --skip-nginx)
      ;;
    *)
      POSITIONAL+=("$arg")
      ;;
  esac
done
set -- "${POSITIONAL[@]}"

SERVER_IP="${1:-10.243.215.33}"
SSH_USER="${2:-richard}"
PROJECT_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"

echo "Servidor: $SSH_USER@$SERVER_IP"
echo "Projeto: $PROJECT_ROOT"
echo

echo "1. Copiando arquivos para o servidor..."

if [[ "$SKIP_NGINX" -eq 0 ]]; then
  # Copiar nginx.conf
  scp "$PROJECT_ROOT/config/nginx.conf" "$SSH_USER@$SERVER_IP:/tmp/nginx.conf"
fi

# Copiar auth middleware
scp "$PROJECT_ROOT/src/mcp/auth_middleware.py" "$SSH_USER@$SERVER_IP:/tmp/auth_middleware.py"

# Copiar handler atualizado
scp "$PROJECT_ROOT/src/mcp/mcp_handler.py" "$SSH_USER@$SERVER_IP:/tmp/mcp_handler.py"

# Copiar script de geração de token
scp "$PROJECT_ROOT/scripts/generate_secure_token.py" "$SSH_USER@$SERVER_IP:/tmp/generate_secure_token.py"

echo "   ✅ Arquivos copiados"

echo
echo "2. Aplicando configurações no servidor..."

ssh "$SSH_USER@$SERVER_IP" "SKIP_NGINX=$SKIP_NGINX" << 'ENDSSH'
set -e

if [ "$SKIP_NGINX" -eq 0 ]; then
  echo "   - Backup das configurações atuais..."
  sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

  echo "   - Instalando nova configuração do nginx..."
  SITE_CONF="/etc/nginx/sites-available/mcp-google-calendar"
  sudo cp /tmp/nginx.conf "$SITE_CONF"
  if [ ! -f /etc/nginx/sites-enabled/mcp-google-calendar ]; then
      sudo ln -s "$SITE_CONF" /etc/nginx/sites-enabled/mcp-google-calendar
  fi

  echo "   - Testando configuração do nginx..."
  sudo nginx -t
fi

echo "   - Atualizando código do MCP..."
# Descobre o caminho do projeto (checkout do git) no servidor
# Ex.: /home/<user>/git/google_calendar_mcp
MCP_PATH="$(eval echo ~$USER)/git/google_calendar_mcp"
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
SECRET_FILE="$HOME/.mcp_secret"
if [ ! -f "$SECRET_FILE" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
    echo "$SECRET_KEY" > "$SECRET_FILE"
    chmod 600 "$SECRET_FILE"
fi

SECRET_KEY=$(cat "$SECRET_FILE")

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
if [ "$SKIP_NGINX" -eq 0 ]; then
  sudo systemctl restart nginx
fi

echo "   ✅ Configuração aplicada com sucesso!"
ENDSSH

echo
echo "3. Gerando token seguro..."

# Gerar token no servidor remoto no diretório correto do projeto
TOKEN_OUTPUT=$(ssh "$SSH_USER@$SERVER_IP" "MCP_SECRET_KEY=\$(cat ~/.mcp_secret) python3 ~/git/google_calendar_mcp/scripts/generate_secure_token.py --client-ip $(curl -s ifconfig.me) --expiry-hours 168")

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