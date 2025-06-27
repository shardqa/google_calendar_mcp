#!/usr/bin/env python3

import os
import sys
import argparse
import secrets
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp.auth_middleware import RobustAuthMiddleware

def main():
    parser = argparse.ArgumentParser(description='Generate secure MCP Bearer tokens')
    parser.add_argument('--client-id', default='cursor-ide', 
                       help='Client ID for the token (default: cursor-ide)')
    parser.add_argument('--client-ip', 
                       help='Bind token to specific IP address')
    parser.add_argument('--expiry-hours', type=int, default=24,
                       help='Token expiry in hours (default: 24)')
    parser.add_argument('--generate-secret', action='store_true',
                       help='Generate a new secret key')
    parser.add_argument('--env-file', 
                       help='Write environment variables to file')
    
    args = parser.parse_args()
    
    if args.generate_secret:
        secret_key = secrets.token_urlsafe(64)
        print(f"Generated secret key: {secret_key}")
        print(f"Add to environment: export MCP_SECRET_KEY='{secret_key}'")
        
        if args.env_file:
            with open(args.env_file, 'w') as f:
                f.write(f"export MCP_SECRET_KEY='{secret_key}'\n")
                f.write(f"export MCP_TOKEN_EXPIRY='{args.expiry_hours * 3600}'\n")
            print(f"Environment file created: {args.env_file}")
        return
    
    if not os.environ.get('MCP_SECRET_KEY'):
        print("ERROR: MCP_SECRET_KEY not set. Use --generate-secret first.")
        sys.exit(1)
    
    os.environ['MCP_TOKEN_EXPIRY'] = str(args.expiry_hours * 3600)
    
    auth = RobustAuthMiddleware()
    
    extra_claims = {}
    if args.client_ip:
        extra_claims['client_ip'] = args.client_ip
    
    token = auth.generate_secure_token(
        client_id=args.client_id,
        client_ip=args.client_ip,
        extra_claims=extra_claims
    )
    
    print(f"Generated secure token for client '{args.client_id}':")
    print(f"Token: {token}")
    print(f"Expires: {datetime.now() + timedelta(hours=args.expiry_hours)}")
    
    if args.client_ip:
        print(f"Bound to IP: {args.client_ip}")
    
    print("\nCursor MCP configuration:")
    print(f'"Authorization": "Bearer {token}"')
    
    print("\nFull mcp.json example:")
    config = {
        "mcpServers": {
            "google_calendar": {
                "url": "https://your-server.com/sse", 
                "type": "sse",
                "enabled": True,
                "headers": {
                    "Authorization": f"Bearer {token}"
                },
                "description": "Google Calendar Integration (Secure)"
            }
        }
    }
    
    import json
    print(json.dumps(config, indent=2))

if __name__ == '__main__':
    main() 