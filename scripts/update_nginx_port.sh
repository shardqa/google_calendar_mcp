#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Atualizando Nginx para usar porta 8443..."

if [ "$EUID" -ne 0 ]; then
  echo "❌ Este script precisa ser executado como root (use sudo)"
  exit 1
fi

echo "📝 Atualizando configuração do Nginx..."
cp "$PROJECT_DIR/config/nginx.conf" /etc/nginx/sites-available/mcp-google-calendar

echo "🧪 Testando nova configuração..."
nginx -t

echo "🔄 Recarregando Nginx..."
systemctl reload nginx

echo "🔥 Configurando firewall para porta 8443..."
ufw allow 8443/tcp
ufw allow 8080/tcp

echo "🔍 Verificando nova porta..."
netstat -tlnp | grep :8443 || echo "Aguardando Nginx..."

echo ""
echo "✅ Nginx atualizado para porta 8443!"
echo ""
echo "📋 Mudanças aplicadas:"
echo "  - HTTPS MCP: porta 8443"
echo "  - HTTP redirect: porta 8080 -> 8443"
echo "  - Firewall: portas 8443 e 8080 abertas"
echo ""
echo "🧪 Para testar:"
echo "  curl -k --cert client-cert.pem --key client-key.pem https://localhost:8443/"
echo ""
echo "📊 Status:"
systemctl status nginx --no-pager -l 