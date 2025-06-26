#!/bin/bash

echo "🧪 Testando autenticação do MCP Server..."

# Verificar se o token existe
if [ ! -f "config/mcp_token.txt" ]; then
    echo "❌ Token não encontrado. Execute primeiro: ./scripts/configure_mcp_remote_auth.sh"
    exit 1
fi

TOKEN=$(cat config/mcp_token.txt)
echo "🔑 Usando token: ${TOKEN:0:20}..."

echo ""
echo "🌐 Testando endpoint direto (porta 3001)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" http://127.0.0.1:3001/sse)
echo "Código HTTP: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Acesso direto funcionando"
else
    echo "❌ Acesso direto com problema - Código: $HTTP_CODE"
fi

echo ""
echo "🔄 Testando através do Nginx (porta 8080)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" http://***REMOVED***:8080/sse)
echo "Código HTTP: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Proxy Nginx funcionando"
else
    echo "❌ Proxy Nginx com problema - Código: $HTTP_CODE"
fi

echo ""
echo "🚫 Testando sem autenticação (deve falhar)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://***REMOVED***:8080/sse)
echo "Código HTTP: $HTTP_CODE"

if [ "$HTTP_CODE" = "401" ]; then
    echo "✅ Autenticação obrigatória funcionando corretamente"
else
    echo "⚠️ Inesperado - deveria retornar 401, retornou: $HTTP_CODE"
fi

echo ""
echo "📊 Status dos serviços:"
echo "--- Porta 3001 (MCP Server) ---"
if netstat -tuln | grep :3001 > /dev/null; then
    echo "✅ Porta 3001 ativa"
else
    echo "❌ Porta 3001 não ativa"
fi

echo "--- Porta 8080 (Nginx) ---"
if netstat -tuln | grep :8080 > /dev/null; then
    echo "✅ Porta 8080 ativa"
else
    echo "❌ Porta 8080 não ativa"
fi

echo ""
echo "📝 Para configurar no Cursor, use:"
echo '{'
echo '  "mcpServers": {'
echo '    "google_calendar_remote": {'
echo '      "command": "npx",'
echo '      "args": ["-y", "mcp-remote", "http://***REMOVED***:8080/sse", "--auth-header", "Authorization: Bearer '$TOKEN'"],'
echo '      "enabled": true'
echo '    }'
echo '  }'
echo '}' 