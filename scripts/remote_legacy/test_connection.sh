#!/bin/bash

echo "🧪 Testando conectividade do MCP Server..."

# Verificar se o token existe
if [ ! -f "config/mcp_token.txt" ]; then
    echo "❌ Token não encontrado. Execute: ./scripts/setup_mcp_auth.sh"
    exit 1
fi

TOKEN=$(cat config/mcp_token.txt)
echo "🔑 Token carregado"

echo ""
echo "📊 Status das portas:"

# Verificar porta 3001
if netstat -tuln 2>/dev/null | grep :3001 > /dev/null; then
    echo "✅ Porta 3001 (MCP Server) - ATIVA"
    PORT_3001_OK=true
else
    echo "❌ Porta 3001 (MCP Server) - INATIVA"
    PORT_3001_OK=false
fi

# Verificar porta 8080
if netstat -tuln 2>/dev/null | grep :8080 > /dev/null; then
    echo "✅ Porta 8080 (Nginx Proxy) - ATIVA" 
    PORT_8080_OK=true
else
    echo "❌ Porta 8080 (Nginx Proxy) - INATIVA"
    PORT_8080_OK=false
fi

echo ""
echo "🌐 Testando conectividade HTTP:"

# Teste sem autenticação (deve retornar 401)
echo "1. Sem autenticação (deve retornar 401):"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3001/sse -m 3 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "401" ]; then
    echo "   ✅ 401 Unauthorized - Autenticação funcionando"
else
    echo "   ⚠️  Código $HTTP_CODE - Esperado: 401"
fi

# Teste com autenticação
echo "2. Com autenticação (deve retornar 200):"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" http://127.0.0.1:3001/sse -m 3 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ 200 OK - Autenticação aceita"
    AUTH_OK=true
else
    echo "   ❌ Código $HTTP_CODE - Esperado: 200"
    AUTH_OK=false
fi

# Teste via Nginx
if [ "$PORT_8080_OK" = true ]; then
    echo "3. Via Nginx Proxy (deve retornar 200):"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" http://***REMOVED***:8080/sse -m 3 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "   ✅ 200 OK - Proxy funcionando"
        PROXY_OK=true
    else
        echo "   ❌ Código $HTTP_CODE - Esperado: 200"
        PROXY_OK=false
    fi
fi

echo ""
echo "📋 RESUMO:"
if [ "$PORT_3001_OK" = true ] && [ "$AUTH_OK" = true ]; then
    echo "✅ Servidor MCP funcionando com autenticação"
    echo "✅ Configuração do Cursor está correta"
    echo ""
    echo "🔄 Se ainda não funciona no Cursor, tente:"
    echo "   1. Reiniciar o Cursor completamente"
    echo "   2. Aguardar alguns segundos para conectar"
    echo "   3. Verificar se não há firewall bloqueando"
else
    echo "❌ Problemas detectados:"
    [ "$PORT_3001_OK" = false ] && echo "   - Servidor MCP não está rodando"
    [ "$AUTH_OK" = false ] && echo "   - Autenticação com problemas"
    echo ""
    echo "🔧 Para corrigir, execute:"
    echo "   sudo systemctl restart google-calendar-mcp.service"
    echo "   sudo journalctl -u google-calendar-mcp.service -f"
fi

echo ""
echo "📝 Configuração atual do Cursor:"
echo '{'
echo '  "mcpServers": {'
echo '    "google_calendar_remote": {'
echo '      "command": "npx",'
echo '      "args": ["-y", "mcp-remote", "http://***REMOVED***:8080/sse", "--auth-header", "Authorization: Bearer '$TOKEN'"],'
echo '      "enabled": true'
echo '    }'
echo '  }'
echo '}' 