#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== MCP Secure Setup ==="
echo

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --server-ip IP    Server IP address"
    echo "  --client-ip IP    Client IP for token binding"
    echo "  --domain DOMAIN   Server domain name"
    echo "  --env-file FILE   Environment file path"
    echo "  --help           Show this help"
    echo
    exit 0
fi

SERVER_IP=""
CLIENT_IP=""
DOMAIN=""
ENV_FILE="$PROJECT_ROOT/.env.mcp"

while [[ $# -gt 0 ]]; do
    case $1 in
        --server-ip)
            SERVER_IP="$2"
            shift 2
            ;;
        --client-ip)
            CLIENT_IP="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --env-file)
            ENV_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "1. Generating secure secret key..."
python3 "$SCRIPT_DIR/generate_secure_token.py" --generate-secret --env-file "$ENV_FILE"

echo
echo "2. Loading environment..."
source "$ENV_FILE"

echo
echo "3. Generating secure token..."
TOKEN_ARGS="--expiry-hours 168"  # 1 week

if [[ -n "$CLIENT_IP" ]]; then
    TOKEN_ARGS="$TOKEN_ARGS --client-ip $CLIENT_IP"
    echo "   - Binding to client IP: $CLIENT_IP"
fi

TOKEN_OUTPUT=$(python3 "$SCRIPT_DIR/generate_secure_token.py" $TOKEN_ARGS)
TOKEN=$(echo "$TOKEN_OUTPUT" | grep "Token:" | cut -d' ' -f2)

echo "   - Generated token: ${TOKEN:0:20}..."

echo
echo "4. Creating MCP configuration..."

if [[ -n "$DOMAIN" ]]; then
    SERVER_URL="https://$DOMAIN/sse"
elif [[ -n "$SERVER_IP" ]]; then
    SERVER_URL="https://$SERVER_IP/sse"
else
    echo "Enter server domain or IP:"
    read -r SERVER_INPUT
    if [[ "$SERVER_INPUT" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        SERVER_URL="https://$SERVER_INPUT/sse"
    else
        SERVER_URL="https://$SERVER_INPUT/sse"
    fi
fi

MCP_CONFIG_FILE="$PROJECT_ROOT/mcp_config.json"

cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "google_calendar": {
      "url": "$SERVER_URL",
      "type": "sse",
      "enabled": true,
      "headers": {
        "Authorization": "Bearer $TOKEN"
      },
      "description": "Google Calendar Integration (Secure Bearer Token)"
    }
  }
}
EOF

echo "   - Created: $MCP_CONFIG_FILE"

echo
echo "5. Creating systemd environment file..."
SYSTEMD_ENV_FILE="/etc/systemd/system/google-calendar-mcp.service.d/override.conf"

if [[ "$EUID" -eq 0 ]]; then
    mkdir -p "$(dirname "$SYSTEMD_ENV_FILE")"
    cat > "$SYSTEMD_ENV_FILE" << EOF
[Service]
Environment="MCP_SECRET_KEY=$MCP_SECRET_KEY"
Environment="MCP_TOKEN_EXPIRY=$MCP_TOKEN_EXPIRY"
Environment="MCP_ALLOWED_IPS=${CLIENT_IP:-}"
Environment="MCP_ALLOWED_CLIENTS=cursor-ide"
EOF
    echo "   - Created: $SYSTEMD_ENV_FILE"
else
    echo "   - Run as root to create systemd override:"
    echo "     sudo mkdir -p $(dirname "$SYSTEMD_ENV_FILE")"
    echo "     sudo tee $SYSTEMD_ENV_FILE << EOF"
    echo "[Service]"
    echo "Environment=\"MCP_SECRET_KEY=$MCP_SECRET_KEY\""
    echo "Environment=\"MCP_TOKEN_EXPIRY=$MCP_TOKEN_EXPIRY\""
    echo "Environment=\"MCP_ALLOWED_IPS=${CLIENT_IP:-}\""
    echo "Environment=\"MCP_ALLOWED_CLIENTS=cursor-ide\""
    echo "EOF"
fi

echo
echo "6. Security recommendations..."
echo "   - Change token every 7 days"
echo "   - Monitor failed authentication attempts"
echo "   - Use IP whitelisting when possible"
echo "   - Enable firewall (UFW/iptables)"
echo "   - Monitor nginx logs regularly"

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Copy $MCP_CONFIG_FILE to your Cursor configuration"
echo "2. Restart MCP server: sudo systemctl restart google-calendar-mcp"
echo "3. Restart nginx: sudo systemctl restart nginx"
echo "4. Test connection: curl -H 'Authorization: Bearer $TOKEN' $SERVER_URL"
echo
echo "Configuration files created:"
echo "- Environment: $ENV_FILE"
echo "- MCP Config: $MCP_CONFIG_FILE"
echo
echo "Token expires in 7 days. Regenerate with:"
echo "python3 $SCRIPT_DIR/generate_secure_token.py $TOKEN_ARGS" 