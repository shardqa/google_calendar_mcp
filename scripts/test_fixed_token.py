#!/usr/bin/env python3

import os
import sys
import requests
import json
from pathlib import Path

def test_fixed_token():
    """Test if the fixed token authentication is working"""
    
    print("🧪 Testando autenticação com token fixo...")
    print("=" * 50)
    
    # Get the fixed token
    fixed_token = os.environ.get('MCP_FIXED_TOKEN')
    if not fixed_token:
        # Try to load from bashrc
        bashrc_path = Path.home() / ".bashrc"
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                for line in f:
                    if 'MCP_FIXED_TOKEN' in line and 'export' in line:
                        fixed_token = line.split("'")[1]
                        break
    
    if not fixed_token:
        print("❌ Token fixo não encontrado!")
        print("Execute: python3 scripts/setup_fixed_token.py")
        return False
    
    print(f"🔑 Token fixo encontrado: {fixed_token[:20]}...")
    
    # Test endpoints
    base_url = "http://127.0.0.1:3001"
    headers = {
        "Authorization": f"Bearer {fixed_token}",
        "Content-Type": "application/json"
    }
    
    tests = [
        {
            "name": "Health Check",
            "method": "GET",
            "url": f"{base_url}/health"
        },
        {
            "name": "MCP Schema",
            "method": "GET", 
            "url": f"{base_url}/schema"
        },
        {
            "name": "Echo Test",
            "method": "POST",
            "url": f"{base_url}/",
            "data": {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "echo",
                    "arguments": {"message": "Hello from fixed token!"}
                },
                "id": 1
            }
        }
    ]
    
    all_passed = True
    
    for test in tests:
        print(f"\n🔍 Testando: {test['name']}")
        
        try:
            if test['method'] == 'GET':
                response = requests.get(test['url'], headers=headers, timeout=10)
            else:
                response = requests.post(test['url'], headers=headers, 
                                       json=test['data'], timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Sucesso (200)")
                if test['name'] == 'Echo Test':
                    result = response.json()
                    if 'result' in result:
                        print(f"   📝 Resposta: {result['result']}")
            elif response.status_code == 401:
                print(f"   ❌ Falha de autenticação (401)")
                print(f"   📝 Erro: {response.text}")
                all_passed = False
            else:
                print(f"   ⚠️  Status inesperado: {response.status_code}")
                print(f"   📝 Resposta: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Conexão recusada - servidor não está rodando")
            all_passed = False
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout - servidor não respondeu")
            all_passed = False
        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Todos os testes passaram!")
        print("✅ Token fixo está funcionando corretamente")
        print("\n💡 Agora você pode usar este token no Cursor:")
        print(f"   Authorization: Bearer {fixed_token}")
        print("\n📁 Configuração do Cursor salva em:")
        print("   config/mcp_cursor_fixed.json")
    else:
        print("❌ Alguns testes falharam")
        print("🔧 Verifique se o servidor MCP está rodando:")
        print("   sudo systemctl status google-calendar-mcp.service")
    
    return all_passed

if __name__ == "__main__":
    # Load environment
    os.system("source ~/.bashrc 2>/dev/null")
    test_fixed_token() 