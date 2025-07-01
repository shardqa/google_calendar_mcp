#!/bin/bash

echo "🚀 Configurando serviço MCP no systemd..."

# Parar processo manual se estiver rodando
pkill -f "python.*mcp_server" || true
sleep 2

# Carregar variáveis de ambiente
source ~/.bashrc 2>/dev/null || true
SECRET_KEY=$(grep "export MCP_SECRET_KEY" ~/.bashrc | tail -1 | cut -d"'" -f2)

if [ -z "$SECRET_KEY" ]; then
    echo "❌ MCP_SECRET_KEY não encontrada. Execute primeiro: ./scripts/setup_mcp_auth.sh"
    exit 1
fi

echo "✅ Chave secreta carregada"

# Criar arquivo de serviço systemd
sudo tee /etc/systemd/system/google-calendar-mcp.service > /dev/null << EOF
[Unit]
Description=Google Calendar MCP Server with Authentication
After=network.target
Wants=network.target

[Service]
Type=simple
User=richard
Group=richard
WorkingDirectory=***REMOVED***/git/google_calendar_mcp
Environment=PYTHONPATH=***REMOVED***/git/google_calendar_mcp/src
Environment=MCP_SECRET_KEY=$SECRET_KEY
Environment=MCP_ALLOWED_CLIENTS=cursor-ide,mcp-remote
Environment=MCP_ALLOWED_IPS=127.0.0.1,::1,***REMOVED***
Environment=MCP_TOKEN_EXPIRY=86400
ExecStart=/usr/bin/uvx --from ***REMOVED***/git/google_calendar_mcp google-calendar-mcp
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
KillMode=mixed
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF

echo "📝 Arquivo de serviço criado"

# Recarregar systemd e habilitar serviço
sudo systemctl daemon-reload
sudo systemctl enable google-calendar-mcp.service

echo "🔄 Iniciando serviço..."
sudo systemctl start google-calendar-mcp.service

sleep 3

echo "📊 Status do serviço:"
sudo systemctl status google-calendar-mcp.service --no-pager -l

echo ""
echo "🌐 Testando conectividade:"
if netstat -tuln | grep :3001 > /dev/null; then
    echo "✅ Porta 3001 está ativa"
else
    echo "❌ Porta 3001 não está ativa"
fi

if netstat -tuln | grep :8080 > /dev/null; then
    echo "✅ Porta 8080 (Nginx) está ativa"
else
    echo "❌ Porta 8080 (Nginx) não está ativa"
fi

echo ""
echo "🔧 Para verificar logs:"
echo "sudo journalctl -u google-calendar-mcp.service -f" 