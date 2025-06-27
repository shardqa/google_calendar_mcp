#!/bin/bash

echo "🔧 Configurando MCP Google Calendar para Gemini CLI..."

# Criar diretório .gemini se não existir
mkdir -p ~/.gemini

# Instalar dependências Python
echo "📦 Instalando dependências..."
pip install -r requirements_proxy.txt

# Fazer o script executável
chmod +x mcp_proxy.py

# Caminho absoluto do script
SCRIPT_PATH=$(realpath mcp_proxy.py)

# Criar configuração do Gemini CLI
echo "⚙️  Criando configuração settings.json..."

cat > ~/.gemini/settings.json << EOF
{
  "mcpServers": {
    "google_calendar": {
      "command": "python",
      "args": ["$SCRIPT_PATH"],
      "timeout": 30000,
      "env": {
        "PYTHONPATH": "$(pwd)"
      }
    }
  },
  "autoAccept": false,
  "theme": "Default"
}
EOF

echo "✅ Configuração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Reinicie o Gemini CLI"
echo "2. Teste a conexão perguntando sobre eventos do calendário"
echo ""
echo "🔧 Localização da configuração: ~/.gemini/settings.json"
echo "🔧 Script proxy: $SCRIPT_PATH"
echo ""
echo "💡 Para testar manualmente:"
echo "   python $SCRIPT_PATH" 