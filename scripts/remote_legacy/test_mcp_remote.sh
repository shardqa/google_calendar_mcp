#!/bin/bash

set -e

echo "=== Testando Google Calendar MCP Server para mcp-remote ==="
echo ""

# Verificar se os serviços estão rodando
echo "1. Verificando serviços..."
echo ""

if systemctl is-active --quiet google-calendar-mcp; then
    echo "✓ Serviço google-calendar-mcp está rodando"
else
    echo "✗ Serviço google-calendar-mcp NÃO está rodando"
    echo "Execute: sudo systemctl start google-calendar-mcp"
fi

if systemctl is-active --quiet nginx; then
    echo "✓ Nginx está rodando"
else
    echo "✗ Nginx NÃO está rodando"
    echo "Execute: sudo systemctl start nginx"
fi

echo ""

# Verificar se as portas estão abertas
echo "2. Verificando portas..."
echo ""

if netstat -tuln | grep -q ":3001 "; then
    echo "✓ Porta 3001 está aberta (MCP Server)"
else
    echo "✗ Porta 3001 NÃO está aberta"
fi

if netstat -tuln | grep -q ":8080 "; then
    echo "✓ Porta 8080 está aberta (Nginx)"
else
    echo "✗ Porta 8080 NÃO está aberta"
fi

echo ""

# Testar endpoint local
echo "3. Testando endpoint local..."
echo ""

if curl -s -f http://localhost:8080/sse >/dev/null 2>&1; then
    echo "✓ Endpoint local http://localhost:8080/sse responde"
else
    echo "✗ Endpoint local http://localhost:8080/sse NÃO responde"
fi

# Testar endpoint direto do MCP
if curl -s -f http://localhost:3001/sse >/dev/null 2>&1; then
    echo "✓ Endpoint direto http://localhost:3001/sse responde"
else
    echo "✗ Endpoint direto http://localhost:3001/sse NÃO responde"
fi

echo ""

# Obter IP externo e testar
echo "4. Testando endpoint externo..."
echo ""

EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || echo "N/A")
if [ "$EXTERNAL_IP" != "N/A" ]; then
    echo "IP externo: $EXTERNAL_IP"
    
    if curl -s -f --connect-timeout 10 http://$EXTERNAL_IP:8080/sse >/dev/null 2>&1; then
        echo "✓ Endpoint externo http://$EXTERNAL_IP:8080/sse responde"
    else
        echo "✗ Endpoint externo http://$EXTERNAL_IP:8080/sse NÃO responde"
        echo "  (pode ser bloqueado pelo firewall ou provedor)"
    fi
else
    echo "Não foi possível obter IP externo"
fi

echo ""

# Verificar logs
echo "5. Últimas linhas dos logs:"
echo ""

echo "--- Logs do MCP Server ---"
sudo journalctl -u google-calendar-mcp --no-pager -n 5 2>/dev/null || echo "Nenhum log encontrado"

echo ""
echo "--- Logs do Nginx ---"
sudo tail -n 5 /var/log/nginx/mcp_remote_error.log 2>/dev/null || echo "Nenhum log de erro do Nginx"

echo ""

# Mostrar configuração para o Cursor
echo "6. Configuração para o Cursor:"
echo ""
echo "Adicione em ~/.cursor/mcp.json:"
echo "{"
echo "  \"mcpServers\": {"
echo "    \"google_calendar_remote\": {"
echo "      \"command\": \"npx\","
echo "      \"args\": ["
echo "        \"-y\","
echo "        \"mcp-remote\","
if [ "$EXTERNAL_IP" != "N/A" ]; then
    echo "        \"http://$EXTERNAL_IP:8080/sse\""
else
    echo "        \"http://YOUR_SERVER_IP:8080/sse\""
fi
echo "      ],"
echo "      \"enabled\": true"
echo "    }"
echo "  }"
echo "}"

echo ""
echo "=== Teste concluído ===" 