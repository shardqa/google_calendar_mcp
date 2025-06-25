#!/bin/bash

set -e

echo "🧪 Testando configuração do Nginx com HTTPS e mutual TLS..."

CERT_DIR="***REMOVED***"
CLIENT_CERT_DIR="$HOME/mcp_certs/client_certs"

echo "🔍 Verificando se o Nginx está rodando..."
if ! systemctl is-active --quiet nginx; then
    echo "❌ Nginx não está rodando"
    echo "Execute: sudo systemctl start nginx"
    exit 1
fi
echo "✅ Nginx está ativo"

echo "🔍 Verificando se a porta 443 está aberta..."
if ! netstat -tlnp | grep -q ":443"; then
    echo "❌ Porta 443 não está aberta"
    exit 1
fi
echo "✅ Porta 443 está aberta"

echo "🔍 Verificando certificados do servidor..."
for cert in "ca-cert.pem" "server-cert.pem" "server-key.pem"; do
    if [ ! -f "$CERT_DIR/$cert" ]; then
        echo "❌ Certificado não encontrado: $CERT_DIR/$cert"
        exit 1
    fi
done
echo "✅ Certificados do servidor encontrados"

echo "🔍 Verificando certificados do cliente..."
if [ -d "$CLIENT_CERT_DIR" ]; then
    for cert in "ca-cert.pem" "client-cert.pem" "client-key.pem"; do
        if [ ! -f "$CLIENT_CERT_DIR/$cert" ]; then
            echo "⚠️  Certificado do cliente não encontrado: $CLIENT_CERT_DIR/$cert"
            echo "   Este é necessário para testar a conectividade do cliente"
        fi
    done
    echo "✅ Certificados do cliente encontrados"
else
    echo "⚠️  Diretório de certificados do cliente não encontrado: $CLIENT_CERT_DIR"
    echo "   Criando estrutura de exemplo..."
    mkdir -p "$CLIENT_CERT_DIR"
    echo "   Copie os certificados do cliente para este diretório"
fi

echo "🔍 Testando configuração do Nginx..."
if ! sudo nginx -t 2>/dev/null; then
    echo "❌ Configuração do Nginx inválida"
    echo "Execute: sudo nginx -t"
    exit 1
fi
echo "✅ Configuração do Nginx válida"

echo "🔍 Testando redirecionamento HTTP -> HTTPS..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -L http://localhost/ 2>/dev/null || echo "000")
if [ "$HTTP_RESPONSE" != "200" ]; then
    echo "⚠️  Redirecionamento HTTP pode não estar funcionando (código: $HTTP_RESPONSE)"
else
    echo "✅ Redirecionamento HTTP funcionando"
fi

echo "🔍 Testando conectividade HTTPS sem certificado cliente..."
HTTPS_NO_CERT=$(curl -k -s -o /dev/null -w "%{http_code}" https://localhost/ 2>/dev/null || echo "000")
if [ "$HTTPS_NO_CERT" = "400" ] || [ "$HTTPS_NO_CERT" = "403" ]; then
    echo "✅ Mutual TLS está funcionando (rejeitou conexão sem certificado cliente)"
else
    echo "⚠️  Mutual TLS pode não estar configurado corretamente (código: $HTTPS_NO_CERT)"
fi

if [ -f "$CLIENT_CERT_DIR/client-cert.pem" ] && [ -f "$CLIENT_CERT_DIR/client-key.pem" ]; then
    echo "🔍 Testando conectividade HTTPS com certificado cliente..."
    HTTPS_WITH_CERT=$(curl -k \
        --cert "$CLIENT_CERT_DIR/client-cert.pem" \
        --key "$CLIENT_CERT_DIR/client-key.pem" \
        --cacert "$CLIENT_CERT_DIR/ca-cert.pem" \
        -s -o /dev/null -w "%{http_code}" \
        https://localhost/ 2>/dev/null || echo "000")
    
    if [ "$HTTPS_WITH_CERT" = "200" ]; then
        echo "✅ Conectividade HTTPS com certificado cliente funcionando"
    else
        echo "❌ Falha na conectividade HTTPS com certificado cliente (código: $HTTPS_WITH_CERT)"
    fi

    echo "🔍 Testando endpoint SSE..."
    SSE_RESPONSE=$(curl -k \
        --cert "$CLIENT_CERT_DIR/client-cert.pem" \
        --key "$CLIENT_CERT_DIR/client-key.pem" \
        --cacert "$CLIENT_CERT_DIR/ca-cert.pem" \
        -s -o /dev/null -w "%{http_code}" \
        -X POST https://localhost/sse \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' \
        2>/dev/null || echo "000")
    
    if [ "$SSE_RESPONSE" = "200" ]; then
        echo "✅ Endpoint SSE funcionando"
    else
        echo "❌ Falha no endpoint SSE (código: $SSE_RESPONSE)"
    fi
else
    echo "⚠️  Certificados do cliente não encontrados - pulando testes de conectividade"
fi

echo "🔍 Verificando logs do Nginx..."
if [ -f "/var/log/nginx/mcp_access.log" ]; then
    echo "✅ Log de acesso encontrado: /var/log/nginx/mcp_access.log"
    echo "   Últimas 5 entradas:"
    tail -n 5 /var/log/nginx/mcp_access.log 2>/dev/null | sed 's/^/   /'
else
    echo "⚠️  Log de acesso não encontrado"
fi

if [ -f "/var/log/nginx/mcp_error.log" ]; then
    echo "✅ Log de erro encontrado: /var/log/nginx/mcp_error.log"
    if [ -s "/var/log/nginx/mcp_error.log" ]; then
        echo "   Últimas 5 entradas de erro:"
        tail -n 5 /var/log/nginx/mcp_error.log 2>/dev/null | sed 's/^/   /'
    else
        echo "   (Nenhum erro registrado)"
    fi
else
    echo "⚠️  Log de erro não encontrado"
fi

echo "🔍 Verificando processo do MCP server..."
if pgrep -f "mcp_cli.*3001" > /dev/null; then
    echo "✅ MCP server está rodando na porta 3001"
else
    echo "❌ MCP server não está rodando na porta 3001"
    echo "Execute: sudo systemctl start google-calendar-mcp"
fi

echo ""
echo "📋 Resumo dos testes:"
echo "  - Nginx ativo: ✅"
echo "  - Porta 443 aberta: ✅"
echo "  - Certificados servidor: ✅"
echo "  - Configuração válida: ✅"
echo "  - Redirecionamento HTTP: $([ "$HTTP_RESPONSE" = "200" ] && echo "✅" || echo "⚠️")"
echo "  - Mutual TLS: $([ "$HTTPS_NO_CERT" = "400" ] || [ "$HTTPS_NO_CERT" = "403" ] && echo "✅" || echo "⚠️")"
if [ -f "$CLIENT_CERT_DIR/client-cert.pem" ]; then
    echo "  - HTTPS c/ certificado: $([ "$HTTPS_WITH_CERT" = "200" ] && echo "✅" || echo "❌")"
    echo "  - Endpoint SSE: $([ "$SSE_RESPONSE" = "200" ] && echo "✅" || echo "❌")"
fi
echo "  - MCP server: $(pgrep -f "mcp_cli.*3001" > /dev/null && echo "✅" || echo "❌")"

echo ""
echo "🔧 Comandos úteis para debugging:"
echo "  - Status Nginx: sudo systemctl status nginx"
echo "  - Logs Nginx: sudo journalctl -u nginx -f"
echo "  - Teste config: sudo nginx -t"
echo "  - Status MCP: sudo systemctl status google-calendar-mcp"
echo "  - Logs MCP: sudo journalctl -u google-calendar-mcp -f" 