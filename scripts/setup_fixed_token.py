#!/usr/bin/env python3

import os
import sys
import secrets
import argparse
from pathlib import Path

def generate_fixed_token(length: int = 64) -> str:
    """Generate a secure fixed token"""
    return secrets.token_urlsafe(length)

def setup_fixed_token(token: str = None, save_to_env: bool = True) -> str:
    """Setup a fixed token for permanent MCP access"""
    
    if not token:
        print("🔐 Gerando token fixo seguro...")
        token = generate_fixed_token()
        print(f"✅ Token gerado: {token}")
    else:
        print(f"✅ Usando token fornecido: {token}")
    
    if save_to_env:
        # Add to ~/.bashrc
        bashrc_path = Path.home() / ".bashrc"
        
        # Check if already exists
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                content = f.read()
            
            if 'MCP_FIXED_TOKEN' in content:
                print("⚠️  MCP_FIXED_TOKEN já existe no ~/.bashrc")
                response = input("Deseja substituir? (s/n): ").lower().strip()
                if response == 's':
                    # Remove old entry
                    lines = content.split('\n')
                    lines = [line for line in lines if not line.startswith('export MCP_FIXED_TOKEN')]
                    content = '\n'.join(lines)
                else:
                    print("❌ Cancelado pelo usuário")
                    return token
        
        # Add new token
        with open(bashrc_path, 'a') as f:
            f.write(f'\n# MCP Fixed Token - Token Fixo Permanente\n')
            f.write(f"export MCP_FIXED_TOKEN='{token}'\n")
        
        print(f"✅ Token salvo em {bashrc_path}")
        
        # Also save to local env file
        env_file = Path(__file__).parent.parent / "config" / "fixed_token.env"
        env_file.parent.mkdir(exist_ok=True)
        
        with open(env_file, 'w') as f:
            f.write(f"export MCP_FIXED_TOKEN='{token}'\n")
        
        print(f"✅ Token também salvo em {env_file}")
    
    return token

def create_cursor_config(token: str, server_url: str) -> dict:
    """Create Cursor configuration with fixed token"""
    config = {
        "mcpServers": {
            "google_calendar": {
                "url": server_url,
                "type": "sse",
                "enabled": True,
                "headers": {
                    "Authorization": f"Bearer {token}"
                },
                "description": "Google Calendar Integration (Token Fixo Permanente)"
            }
        }
    }
    return config

def main():
    parser = argparse.ArgumentParser(description='Configurar token fixo para MCP')
    parser.add_argument('--token', help='Usar token específico (opcional)')
    parser.add_argument('--server-url', default='https://***REMOVED***:8443/sse', 
                       help='URL do servidor MCP')
    parser.add_argument('--no-save', action='store_true', 
                       help='Não salvar no ambiente')
    parser.add_argument('--show-config', action='store_true',
                       help='Mostrar configuração do Cursor')
    
    args = parser.parse_args()
    
    print("🚀 Configuração de Token Fixo MCP")
    print("=" * 40)
    
    # Setup fixed token
    token = setup_fixed_token(
        token=args.token,
        save_to_env=not args.no_save
    )
    
    if args.show_config:
        import json
        print("\n📝 Configuração para o Cursor (mcp.json):")
        print("-" * 40)
        config = create_cursor_config(token, args.server_url)
        print(json.dumps(config, indent=2, ensure_ascii=False))
        
        # Save config to file
        config_file = Path(__file__).parent.parent / "config" / "mcp_cursor_fixed.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Configuração salva em: {config_file}")
    
    print("\n🎉 Token fixo configurado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Recarregue o ambiente: source ~/.bashrc")
    print("2. Reinicie o servidor MCP para carregar o token fixo")
    print("3. Use este token no Cursor - ele nunca expira!")
    print(f"\n🔑 Seu token fixo: {token}")
    print("\n💡 Vantagens do token fixo:")
    print("   - Nunca expira")
    print("   - Não precisa copiar/colar toda hora")
    print("   - Funciona de qualquer IP")
    print("   - Configuração única no Cursor")

if __name__ == "__main__":
    main() 