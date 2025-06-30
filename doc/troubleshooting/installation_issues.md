# Problemas de Instalação e Ambiente

## Problemas de Setup Inicial

### Módulo Não Encontrado

**Erro**: `ModuleNotFoundError` ao executar o projeto.

**Causa**: O `PYTHONPATH` não está configurado corretamente.

**Solução**:

```bash
export PYTHONPATH=$PWD
```

### Credenciais Inválidas

**Erro**: Falha na autenticação do Google ou erro "invalid credentials".

**Causa**: Credenciais salvas desatualizadas ou corrompidas.

**Solução**:

```bash
rm config/token.pickle
python -m src.main  # Force nova autenticação
```

### Porta em Uso

**Erro**: "Port already in use" ao iniciar o servidor MCP.

**Causa**: Outro processo já está usando a porta 3001.

**Solução**:

```bash
# Pare qualquer instância do servidor
make mcp-stop

# Ou mate o processo manualmente
lsof -ti:3001 | xargs kill -9
```

## Problemas com Google APIs

### API do Google Tasks Não Habilitada

**Erro**: "Google Tasks API has not been used in project [PROJECT_ID]
before or it is disabled"

**Solução**:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto
3. Vá para "APIs & Services" > "Library"
4. Pesquise por "Google Tasks API" e clique em "Enable"
5. Aguarde alguns minutos para a API ser ativada

### Escopo de Autenticação Insuficiente

**Problema**: API habilitada mas operações de tarefas ainda falham.

**Solução**: Certifique-se que os escopos OAuth incluem Tasks:

- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/tasks`

Delete `token.pickle` para forçar nova autenticação com escopos corretos.

## Problemas de Ambiente Python

### Erro "externally-managed-environment"

**Erro**: Erro ao usar `pip` ou `pytest` indicando ambiente externo.

**Causa**: Comando executado no ambiente global em vez do virtual.

**Solução**: Use sempre os executáveis do ambiente virtual:

```bash
./.venv/bin/python -m pytest --cov=.
./.venv/bin/pip install -r requirements.txt
```

---
Voltar para [Resolução de Problemas](../troubleshooting.md).
