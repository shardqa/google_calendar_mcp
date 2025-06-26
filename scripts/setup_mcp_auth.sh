#!/bin/bash

echo "🔐 Configurando autenticação segura para MCP Remote..."

# Gerar chave secreta se não existir
if [ -z "$MCP_SECRET_KEY" ]; then
    SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')
    echo "export MCP_SECRET_KEY='$SECRET_KEY'" >> ~/.bashrc
    export MCP_SECRET_KEY="$SECRET_KEY"
    echo "✅ Chave secreta gerada e salva em ~/.bashrc"
else
    echo "✅ Usando chave secreta existente"
fi

# Configurar variáveis de ambiente para segurança
cat >> ~/.bashrc << 'EOF'
# MCP Security Settings
export MCP_ALLOWED_CLIENTS="cursor-ide,mcp-remote"
export MCP_ALLOWED_IPS="127.0.0.1,::1,***REMOVED***"
export MCP_TOKEN_EXPIRY="86400"
EOF

echo "✅ Configurações de segurança salvas"

# Gerar token de API para mcp-remote
echo "🔑 Gerando token de acesso para mcp-remote..."

python3 << 'EOF'
import sys
import os
sys.path.append('***REMOVED***/git/google_calendar_mcp/src')

from mcp.auth_middleware import RobustAuthMiddleware

auth = RobustAuthMiddleware()
token = auth.generate_secure_token(
    client_id='mcp-remote',
    client_ip='***REMOVED***',
    extra_claims={'purpose': 'remote-access', 'server': 'srv618353'}
)

# Salvar token em arquivo seguro
with open('***REMOVED***/git/google_calendar_mcp/config/mcp_token.txt', 'w') as f:
    f.write(token)

print(f"Token gerado: {token}")
print("Token salvo em: config/mcp_token.txt")
EOF

# Configurar permissões do arquivo de token
chmod 600 config/mcp_token.txt
echo "✅ Permissões do token configuradas (600)"

# Recarregar ambiente
source ~/.bashrc

echo "🎉 Configuração de autenticação concluída!"
echo "📋 Próximos passos:"
echo "   1. Configure o Cursor com o token gerado"
echo "   2. Reinicie o servidor MCP com as novas configurações"
echo "   3. Teste a conexão autenticada" 