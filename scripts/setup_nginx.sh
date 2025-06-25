#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Configurando Nginx reverse-proxy com HTTPS e mutual TLS..."

if [ "$EUID" -ne 0 ]; then
  echo "❌ Este script precisa ser executado como root (use sudo)"
  exit 1
fi

echo "📦 Instalando Nginx..."
apt update
apt install -y nginx

echo "🔒 Verificando certificados..."
CERT_DIR="***REMOVED***"
if [ ! -f "$CERT_DIR/server-cert.pem" ] || [ ! -f "$CERT_DIR/server-key.pem" ] || [ ! -f "$CERT_DIR/ca-cert.pem" ]; then
    echo "❌ Certificados não encontrados em $CERT_DIR"
    echo "Certifique-se de que os seguintes arquivos existem:"
    echo "  - $CERT_DIR/server-cert.pem"
    echo "  - $CERT_DIR/server-key.pem" 
    echo "  - $CERT_DIR/ca-cert.pem"
    exit 1
fi

echo "🗂️  Fazendo backup da configuração padrão do Nginx..."
cp /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.backup 2>/dev/null || true

echo "📝 Copiando configuração do Nginx..."
cp "$PROJECT_DIR/config/nginx.conf" /etc/nginx/sites-available/mcp-google-calendar

echo "🔗 Criando link simbólico..."
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/mcp-google-calendar /etc/nginx/sites-enabled/

echo "🧪 Testando configuração do Nginx..."
nginx -t

echo "🔄 Recarregando Nginx..."
systemctl restart nginx
systemctl enable nginx

echo "🔥 Configurando firewall..."
ufw allow 443/tcp
ufw allow 80/tcp

echo "📊 Status do Nginx:"
systemctl status nginx --no-pager

echo "🔍 Verificando porta 443..."
netstat -tlnp | grep :443 || echo "Porta 443 não encontrada (pode estar ok se o Nginx acabou de iniciar)"

echo ""
echo "✅ Configuração do Nginx concluída!"
echo ""
echo "📋 Próximos passos:"
echo "  1. O servidor está agora acessível via HTTPS na porta 443"
echo "  2. Mutual TLS está ativado - apenas clientes com certificado válido podem conectar"
echo "  3. HTTP (porta 80) redireciona automaticamente para HTTPS (porta 443)"
echo ""
echo "🧪 Para testar:"
echo "  curl -k --cert client-cert.pem --key client-key.pem https://localhost/"
echo ""
echo "📁 Logs do Nginx:"
echo "  - Access: /var/log/nginx/mcp_access.log"
echo "  - Error: /var/log/nginx/mcp_error.log"
echo ""
echo "🔧 Para gerenciar o Nginx:"
echo "  - Reiniciar: sudo systemctl restart nginx"
echo "  - Status: sudo systemctl status nginx"
echo "  - Logs: sudo journalctl -u nginx -f" 