# Configuração de Clientes MCP

Para utilizar as ferramentas deste projeto com assistentes de IA, é necessário configurar o cliente para se comunicar com o servidor MCP.

## Cursor

Para usar com o Cursor, basta iniciar o servidor MCP. A configuração é automática.

```bash
make mcp-start
```

Este comando irá iniciar o servidor na porta 3001 e criar o arquivo de configuração `.cursor/mcp.json` na raiz do projeto, que o Cursor detecta automaticamente.

## Google Gemini CLI

A integração com o Gemini CLI requer a configuração manual do arquivo `settings.json`.

1.  **Instale o CLI**:
    ```bash
    # Via npm
    npm install -g @google-ai/generativelanguage-cli

    # Ou via pipx (recomendado)
    pipx install google-generativeai
    ```

2.  **Configure o Servidor**:
    Edite o arquivo `~/.gemini/settings.json` e adicione a seguinte configuração, **substituindo `/caminho/absoluto/para/google_calendar_mcp`** pelo caminho real do projeto:

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

3.  **Teste a Configuração**:
    ```bash
    # Exporte sua chave de API
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

    # Verifique se o servidor é listado
    gemini mcp list

    # Tente usar uma ferramenta
    gemini "Liste meus próximos eventos do calendário"
    ```

## Claude Desktop

Para configurar com o cliente de desktop do Claude, edite o arquivo de configuração correspondente ao seu sistema operacional:

-   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
-   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
-   **Linux**: `~/.config/claude/claude_desktop_config.json`

Adicione a seguinte entrada:

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

---
Voltar para o guia de [Instalação](installation.md). 