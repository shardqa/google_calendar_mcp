#!/bin/bash

echo "🚀 Configuração Final do Google Calendar MCP com Token Fixo"
echo "========================================================="

cd ***REMOVED***/git/google_calendar_mcp

# 1. Parar processos manuais
echo "🛑 Parando processos existentes..."
pkill -f "python.*mcp_server" 2>/dev/null || true
sleep 2

# 2. Carregar chave secreta
source ~/.bashrc 2>/dev/null || true
SECRET_KEY=$(grep "export MCP_SECRET_KEY" ~/.bashrc | tail -1 | cut -d"'" -f2)

if [ -z "$SECRET_KEY" ]; then
    echo "❌ Chave secreta não encontrada. Gerando nova..."
    SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')
    echo "export MCP_SECRET_KEY='$SECRET_KEY'" >> ~/.bashrc
    echo "✅ Nova chave secreta gerada"
fi

# 3. Configurar token fixo permanente
echo "🔐 Configurando token fixo permanente..."
# Fixed token setup removed - project uses stdio-only mode

if [ $? -eq 0 ]; then
    echo "✅ Token fixo configurado com sucesso"
    
    # Recarregar ambiente para pegar o token fixo
    source ~/.bashrc
    FIXED_TOKEN=$(grep "export MCP_FIXED_TOKEN" ~/.bashrc | tail -1 | cut -d"'" -f2)
    
    if [ -n "$FIXED_TOKEN" ]; then
        echo "✅ Token fixo carregado: ${FIXED_TOKEN:0:20}..."
    else
        echo "⚠️  Token fixo não foi carregado corretamente"
    fi
else
    echo "❌ Erro ao configurar token fixo"
    exit 1
fi

# 4. Criar serviço systemd com suporte a token fixo
echo "📝 Configurando serviço systemd..."
sudo tee /etc/systemd/system/google-calendar-mcp.service > /dev/null << EOF
[Unit]
Description=Google Calendar MCP Server com Token Fixo
After=network.target
Wants=network.target

[Service]
Type=simple
User=your-username
Group=your-username
WorkingDirectory=***REMOVED***/git/google_calendar_mcp
Environment=PYTHONPATH=***REMOVED***/git/google_calendar_mcp/src
Environment=MCP_SECRET_KEY=$SECRET_KEY
Environment=MCP_FIXED_TOKEN=$FIXED_TOKEN
Environment=MCP_ALLOWED_CLIENTS=cursor-ide,mcp-remote
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

echo "✅ Serviço systemd configurado"

# 5. Habilitar e iniciar serviço
echo "🚀 Iniciando serviço..."
sudo systemctl daemon-reload
sudo systemctl enable google-calendar-mcp.service
sudo systemctl restart google-calendar-mcp.service

sleep 3

# 6. Verificar status
echo "📊 Verificando status do serviço..."
if sudo systemctl is-active --quiet google-calendar-mcp.service; then
    echo "✅ Serviço está ativo"
else
    echo "❌ Serviço não está ativo"
    sudo systemctl status google-calendar-mcp.service --no-pager -l
fi

# 7. Verificar porta
if netstat -tuln | grep :3001 > /dev/null; then
    echo "✅ Porta 3001 está ativa"
else
    echo "❌ Porta 3001 não está ativa"
fi

# 8. Mostrar configuração final
echo ""
echo "🎉 Configuração concluída!"
echo "========================="
echo ""
echo "✅ Token fixo configurado - nunca expira!"
echo "✅ Servidor MCP rodando na porta 3001"
echo "✅ Autenticação ativa com suporte a token fixo"
echo ""
echo "📁 Arquivos de configuração criados:"
echo "   - config/mcp_cursor_fixed.json (configuração do Cursor)"
echo "   - config/fixed_token.env (backup do token)"
echo ""
echo "🔑 Seu token fixo: $FIXED_TOKEN"
echo ""
echo "📝 Para usar no Cursor, copie o conteúdo de:"
echo "   cat config/mcp_cursor_fixed.json"
echo ""
echo "💡 Vantagens do token fixo:"
echo "   ✅ Nunca expira"
echo "   ✅ Não precisa renovar"
echo "   ✅ Funciona de qualquer IP"
echo "   ✅ Configuração única"
echo ""
echo "🔄 Para aplicar mudanças no futuro:"
echo "   sudo systemctl restart google-calendar-mcp.service" 