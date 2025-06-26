#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Iniciando Google Calendar MCP Server para mcp-remote..."

cd "$PROJECT_ROOT"

export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"
export MCP_SERVER_HOST="0.0.0.0"
export MCP_SERVER_PORT="3001"
export MCP_TRANSPORT="sse"

echo "Configurações:"
echo "  Host: $MCP_SERVER_HOST"
echo "  Port: $MCP_SERVER_PORT"
echo "  Transport: $MCP_TRANSPORT"
echo ""

if [ ! -d .venv ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

echo "Ativando ambiente virtual..."
source .venv/bin/activate

echo "Instalando dependências..."
pip install -q -r requirements.txt

echo "Iniciando servidor MCP em modo SSE..."
python3 -m src.mcp.mcp_server --host "$MCP_SERVER_HOST" --port "$MCP_SERVER_PORT" 