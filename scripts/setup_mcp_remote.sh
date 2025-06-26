#!/bin/bash

set -e

if [[ $EUID -ne 0 ]]; then
   echo "Este script deve ser executado como root (usar sudo)"
   exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
USER_HOME="***REMOVED***"

echo "=== Configurando Google Calendar MCP Server para mcp-remote ==="
echo ""

echo "1. Atualizando sistema..."
apt update -qq

echo "2. Instalando dependências..."
apt install -y nginx python3 python3-pip python3-venv curl

echo "3. Parando serviços existentes..."
systemctl stop nginx 2>/dev/null || true
systemctl stop google-calendar-mcp 2>/dev/null || true

echo "4. Configurando Nginx..."
cp "$PROJECT_ROOT/config/nginx-mcp-remote.conf" /etc/nginx/sites-available/mcp-remote
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-enabled/mcp-remote
ln -sf /etc/nginx/sites-available/mcp-remote /etc/nginx/sites-enabled/

echo "5. Testando configuração do Nginx..."
nginx -t

echo "6. Configurando permissões do script..."
chmod +x "$PROJECT_ROOT/scripts/start_mcp_remote.sh"
chown richard:richard "$PROJECT_ROOT/scripts/start_mcp_remote.sh"

echo "7. Configurando serviço systemd..."
cp "$PROJECT_ROOT/config/google-calendar-mcp.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable google-calendar-mcp

echo "8. Configurando firewall..."
ufw allow 8080/tcp
ufw allow 3001/tcp

echo "9. Configurando logs..."
mkdir -p /var/log/nginx
touch /var/log/nginx/mcp_remote_access.log
touch /var/log/nginx/mcp_remote_error.log
chown www-data:www-data /var/log/nginx/mcp_remote_*.log

echo "10. Verificando arquivo .env..."
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "AVISO: Arquivo .env não encontrado!"
    echo "Crie o arquivo $PROJECT_ROOT/.env com:"
    echo "GOOGLE_CLIENT_ID=your_client_id"
    echo "GOOGLE_CLIENT_SECRET=your_client_secret"
    echo "GOOGLE_REDIRECT_URI=http://localhost:8080/auth/callback"
    echo ""
fi

echo "11. Iniciando serviços..."
systemctl start google-calendar-mcp
systemctl start nginx

echo ""
echo "=== Configuração concluída! ==="
echo ""
echo "Status dos serviços:"
systemctl status google-calendar-mcp --no-pager -l || true
systemctl status nginx --no-pager -l || true

echo ""
echo "URLs para testar:"
echo "  Local: http://localhost:8080/sse"
echo "  Externo: http://$(curl -s ifconfig.me):8080/sse"
echo ""

echo "Para usar com mcp-remote no Cursor, adicione em ~/.cursor/mcp.json:"
echo "{"
echo "  \"mcpServers\": {"
echo "    \"google_calendar_remote\": {"
echo "      \"command\": \"npx\","
echo "      \"args\": ["
echo "        \"-y\","
echo "        \"mcp-remote\","
echo "        \"http://$(curl -s ifconfig.me):8080/sse\""
echo "      ],"
echo "      \"enabled\": true"
echo "    }"
echo "  }"
echo "}"
echo ""

echo "Comandos úteis:"
echo "  Ver logs: sudo journalctl -u google-calendar-mcp -f"
echo "  Reiniciar: sudo systemctl restart google-calendar-mcp"
echo "  Status: sudo systemctl status google-calendar-mcp" 