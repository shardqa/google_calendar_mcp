# Instalação

## Requisitos

- Python 3.8 ou superior
- Conta Google com acesso ao Google Calendar
- Credenciais OAuth2 do Google Cloud Platform

## Configuração Básica

### 1. Clone e Ambiente

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/google_calendar_mcp.git
cd google_calendar_mcp
```

Configure o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate      # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Credenciais Google

Configure as credenciais:

- Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
- Ative a API do Google Calendar.
- Ative a API do Google Tasks.
- Crie credenciais OAuth2 para aplicativo desktop.
- Baixe o arquivo JSON das credenciais como `credentials.json`.
- Coloque-o na raiz do projeto.

### 3. Primeira Execução

Execute a autenticação inicial:

```bash
python -m src.main
```

Na primeira execução, você será redirecionado para o navegador para autorizar o acesso.

## Configuração para Clientes MCP

### Cursor

Para usar com Cursor, inicie o servidor MCP:

```bash
make mcp-start
```

O arquivo `.cursor/mcp.json` será criado automaticamente.

### Google Gemini CLI

Instale o Gemini CLI:

```bash
# Via npm
npm install -g @google-ai/generativelanguage-cli

# Via pipx (recomendado)
pipx install google-generativeai
```

Configure o arquivo `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "google_calendar": {
      "command": "python3",
      "args": ["-m", "src.mcp.mcp_stdio_server"],
      "cwd": "/caminho/absoluto/para/google_calendar_mcp",
      "timeout": 30000,
      "env": {
        "PYTHONPATH": "/caminho/absoluto/para/google_calendar_mcp"
      }
    }
  }
}
```

Configure a chave da API:

```bash
export GEMINI_API_KEY="sua_chave_api_aqui"
```

Teste a configuração:

```bash
gemini mcp list
gemini "Liste meus próximos eventos do calendário"
```

### Claude Desktop

Para configuração com Claude Desktop, edite o arquivo de configuração:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google_calendar": {
      "url": "http://localhost:3001/sse",
      "type": "sse"
    }
  }
}
```

## Configuração Avançada

### Servidor Remoto

Para configuração em servidor remoto com autenticação:

```bash
# Gerar token de autenticação
python scripts/generate_secure_token.py

# Configurar nginx (opcional)
sudo cp config/nginx-mcp-remote-secure.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx-mcp-remote-secure.conf /etc/nginx/sites-enabled/

# Iniciar com autenticação
python -m src.mcp.mcp_server --auth-required --port 3001
```

### Systemd Service

Para execução automática como serviço:

```bash
# Copiar arquivo de serviço
sudo cp config/google-calendar-mcp.service /etc/systemd/system/

# Editar caminhos no arquivo
sudo systemctl edit google-calendar-mcp

# Habilitar e iniciar
sudo systemctl enable google-calendar-mcp
sudo systemctl start google-calendar-mcp
```

## Verificação da Instalação

### Teste Local

```bash
# Testar servidor stdio
python -m src.mcp.mcp_stdio_server

# Testar servidor SSE
make mcp-start
curl http://localhost:3001

# Testar ferramentas
curl -X POST http://localhost:3001/sse \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}'
```

### Teste com Clientes

```bash
# Cursor
# Use @mcp_google_calendar_echo no Cursor

# Gemini CLI
gemini "Echo: teste funcionando"

# Claude Desktop
# Digite: use the echo tool to test "hello world"
```

## Resolução de Problemas

### Problemas Comuns

1. **Módulo não encontrado:**

   ```bash
   export PYTHONPATH=$PWD
   ```

2. **Credenciais inválidas:**

   ```bash
   rm config/token.pickle
   python -m src.main
   ```

3. **Porta em uso:**

   ```bash
   make mcp-stop
   # ou
   lsof -ti:3001 | xargs kill -9
   ```

4. **Gemini CLI não encontra servidor:**
   - Verifique se o caminho em `cwd` é absoluto
   - Confirme que `PYTHONPATH` está definido
   - Teste manualmente: `python -m src.mcp.mcp_stdio_server`

---
Para visão geral, veja [Visão Geral](overview.md).
Para arquitetura, veja [Arquitetura](architecture.md).
Para uso, veja [Uso](usage.md).
Para configuração detalhada, veja [Configuração MCP](mcp_configuration.md).
Para resolução de problemas, veja [Resolução de Problemas](troubleshooting.md).
Para desenvolvimento futuro, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
