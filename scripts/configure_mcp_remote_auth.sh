#!/bin/bash

echo "🔧 Configurando mcp-remote com autenticação segura..."

# Parar serviços existentes
echo "🛑 Parando serviços existentes..."
sudo systemctl stop google-calendar-mcp.service 2>/dev/null || true
sudo pkill -f "python.*mcp_server" || true
sudo pkill -f "python.*3001" || true

# Aguardar processos finalizarem
sleep 3

# Copiar nova configuração do Nginx
echo "📝 Atualizando configuração do Nginx..."
sudo cp config/nginx-mcp-remote-secure.conf /etc/nginx/sites-available/mcp-remote
sudo ln -sf /etc/nginx/sites-available/mcp-remote /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração do Nginx
echo "🧪 Testando configuração do Nginx..."
if sudo nginx -t; then
    echo "✅ Configuração do Nginx válida"
    sudo systemctl reload nginx
else
    echo "❌ Erro na configuração do Nginx"
    exit 1
fi

# Configurar autenticação
echo "🔐 Configurando autenticação..."
chmod +x scripts/setup_mcp_auth.sh
./scripts/setup_mcp_auth.sh

# Recarregar variáveis de ambiente
source ~/.bashrc

echo "🚀 Reiniciando servidor MCP com autenticação..."

# Definir variáveis de ambiente para o serviço
sudo tee /etc/systemd/system/google-calendar-mcp.service > /dev/null << EOF
[Unit]
Description=Google Calendar MCP Server
After=network.target

[Service]
Type=simple
User=richard
WorkingDirectory=***REMOVED***/git/google_calendar_mcp
Environment=PYTHONPATH=***REMOVED***/git/google_calendar_mcp/src
Environment=MCP_SECRET_KEY=${MCP_SECRET_KEY}
Environment=MCP_ALLOWED_CLIENTS=cursor-ide,mcp-remote
Environment=MCP_ALLOWED_IPS=127.0.0.1,::1,***REMOVED***
Environment=MCP_TOKEN_EXPIRY=86400
ExecStart=/usr/bin/python3 -m mcp.mcp_server --host 0.0.0.0 --port 3001
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Recarregar e iniciar serviços
sudo systemctl daemon-reload
sudo systemctl enable google-calendar-mcp.service
sudo systemctl start google-calendar-mcp.service

echo "⏳ Aguardando serviço inicializar..."
sleep 5

# Verificar status
echo "📊 Status dos serviços:"
echo "--- MCP Server ---"
sudo systemctl status google-calendar-mcp.service --no-pager -l

echo "--- Nginx ---"
sudo systemctl status nginx --no-pager -l

# Ler token gerado
if [ -f "config/mcp_token.txt" ]; then
    TOKEN=$(cat config/mcp_token.txt)
    echo ""
    echo "🎉 Configuração concluída com sucesso!"
    echo ""
    echo "📋 Configuração para o Cursor:"
    echo '{'
    echo '  "mcpServers": {'
    echo '    "google_calendar_remote": {'
    echo '      "command": "npx",'
    echo '      "args": ["-y", "mcp-remote", "http://***REMOVED***:8080/sse", "--auth-header", "Authorization: Bearer '$TOKEN'"],'
    echo '      "enabled": true'
    echo '    }'
    echo '  }'
    echo '}'
    echo ""
    echo "💾 Token salvo em: config/mcp_token.txt"
    echo "🔑 Token: $TOKEN"
    echo ""
    echo "🧪 Para testar:"
    echo "curl -H 'Authorization: Bearer $TOKEN' http://***REMOVED***:8080/sse"
else
    echo "❌ Erro: Token não foi gerado"
    exit 1
fi 