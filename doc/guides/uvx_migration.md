# Migração para uvx - Google Calendar MCP

## Visão Geral

O Google Calendar MCP foi migrado para usar `uvx` ao invés de execução direta do Python, oferecendo:

- ⚡ **Performance 10-100x superior** ao pip tradicional
- 🔒 **Isolamento completo** de dependências  
- 🧹 **Ambientes efêmeros** sem contaminação global
- 📦 **Gerenciamento automático** de dependências

## Mudanças Implementadas

### 1. Simplificação da Arquitetura

**REMOVIDO** (stdio-only focus):
- ❌ Servidor HTTP/SSE (`mcp_server.py`)
- ❌ CLI complexo (partes não-stdio)
- ❌ Endpoints web diversos

**MANTIDO**:
- ✅ Modo stdio apenas (`mcp_stdio_server.py`)
- ✅ Todas as ferramentas do Google Calendar/Tasks
- ✅ Compatibilidade com Cursor e Gemini CLI

### 2. Configuração uvx

**Antes:**
```json
{
  "command": "python3",
  "args": ["-m", "src.mcp.mcp_stdio_server"],
  "cwd": "/caminho/para/projeto",
  "env": {"PYTHONPATH": "/caminho/para/projeto"}
}
```

**Depois:**
```json
{
  "command": "uvx",
  "args": ["--from", "/caminho/para/projeto", "google-calendar-mcp"]
}
```

### 3. Estrutura do Projeto

Adicionado `pyproject.toml`:
```toml
[project]
name = "google-calendar-mcp"
version = "1.0.0"

[project.scripts]
google-calendar-mcp = "src.mcp.mcp_stdio_server:run_stdio_server"
```

## Como Migrar

### 1. Pré-requisitos

Instalar uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Executar Migração

```bash
python3 scripts/migrate_to_uvx.py
```

O script irá:
- ✅ Fazer backup das configurações existentes
- ✅ Atualizar configs do Cursor (`.cursor/mcp.json`)
- ✅ Atualizar configs do Gemini CLI (`.gemini/settings.json`)
- ✅ Verificar instalação do uv

### 3. Testar Nova Configuração

```bash
# Teste direto
uvx --from /caminho/para/projeto google-calendar-mcp

# Teste via Cursor - reinicie o editor
# Teste via Gemini CLI
gemini mcp list
```

## Configurações por Cliente

### Cursor

Após migração, o arquivo `.cursor/mcp.json` terá:
```json
{
  "mcpServers": {
    "google_calendar_uvx": {
      "command": "uvx",
      "args": ["--from", "/home/user/git/google_calendar_mcp", "google-calendar-mcp"],
      "timeout": 30000
    }
  }
}
```

### Gemini CLI

Após migração, o arquivo `.gemini/settings.json` terá:
```json
{
  "mcpServers": {
    "google_calendar": {
      "command": "uvx",
      "args": ["--from", "/home/user/git/google_calendar_mcp", "google-calendar-mcp"],
      "timeout": 30000
    }
  }
}
```

## Desenvolvimento com uvx

### Executar Testes

```bash
# Com uvx (recomendado)
uvx --from . --with pytest,pytest-cov pytest

# Ou instalando dev dependencies
uv pip install -e ".[dev]"
pytest
```

### Executar Servidor para Debug

```bash
# Direto via uvx
uvx --from . google-calendar-mcp

# Com input de teste
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}' | uvx --from . google-calendar-mcp
```

## Benefícios da Migração

### Performance
- **Resolução de dependências**: 10-100x mais rápida
- **Instalação**: Paralela e otimizada
- **Inicialização**: Ambiente efêmero pronto em segundos

### Isolamento
- **Zero contaminação** do ambiente global
- **Dependências exatas** sempre garantidas
- **Reprodutibilidade** total entre execuções

### Simplicidade  
- **Sem PYTHONPATH** ou configurações complexas
- **Sem ambiente virtual** manual
- **Configuração mínima** necessária

## Troubleshooting

### "uvx: command not found"

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recarregar shell
source ~/.bashrc  # ou ~/.zshrc
```

### "Failed to resolve dependencies"

```bash
# Verificar pyproject.toml
uvx --from . --help

# Testar instalação local
uv pip install -e .
```

### "Timeout connecting to MCP server"

- ✅ Verificar se uvx está funcionando
- ✅ Aumentar timeout na configuração MCP
- ✅ Testar comando uvx manualmente

### Backup de Configurações

Os backups ficam em:
- Cursor: `~/.cursor/mcp.json.backup-uvx`  
- Gemini: `~/.gemini/settings.json.backup-uvx`

Para reverter:
```bash
# Cursor
mv ~/.cursor/mcp.json.backup-uvx ~/.cursor/mcp.json

# Gemini CLI  
mv ~/.gemini/settings.json.backup-uvx ~/.gemini/settings.json
```

## Próximos Passos

Após confirmar que uvx está funcionando:

1. **Remover código HTTP** não utilizado
2. **Simplificar testes** para stdio-only
3. **Limpar configurações python direto**
4. **Atualizar documentação** geral

Ver [TODO.md](../../TODO.md) para tasks pendentes de limpeza. 