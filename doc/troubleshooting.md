# Resolução de Problemas

## Erros Comuns

- **Falha na autenticação**: Verifique se o arquivo `credentials.json` está correto e na raiz do projeto.
- **Erros de API**: Confirme se a API do Google Calendar está ativada no Console Google Cloud.
- **Token inválido**: Exclua o arquivo `token.pickle` para forçar uma nova autenticação.

## Google Tasks API

### API não habilitada

**Problema**: Erro "Google Tasks API has not been used in project [PROJECT_ID] before or it is disabled"

**Solução**:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto
3. Vá para "APIs & Services" > "Library"
4. Pesquise por "Google Tasks API" e clique em "Enable"
5. Aguarde alguns minutos para a API ser ativada
6. Teste novamente com `tasks list` ou `tasks add`

### Escopo de autenticação insuficiente

**Problema**: Mesmo com a API habilitada, operações de tarefas falham

**Solução**: Certifique-se que os escopos OAuth incluem Tasks:

- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/tasks`

Delete `token.pickle` para forçar nova autenticação com escopos corretos.

## Problemas de CI/CD

### GitHub Actions - Caminhos Python Hardcoded

**Problema**: Testes falhando no GitHub Actions com `FileNotFoundError` para caminhos como `/home/runner/work/.../.../.venv/bin/python`

**Causa**: Testes usando caminhos hardcoded em vez do executável Python atual

**Solução**: Substituir referências diretas ao path do venv por `sys.executable`:

```python
# Antes (problemático)
python_executable = os.path.join(os.getcwd(), '.venv', 'bin', 'python')

# Depois (correto)
python_executable = sys.executable
```

### Subprocess Tests em CI

**Problema**: Testes com subprocess falhando em ambientes CI/CD

**Solução**: Simplificar testes para usar simulação direta em vez de subprocess:

```python
# Abordagem robusta para teste de __main__
@patch('sys.argv', ['script_name'])
@patch('builtins.exec')
def test_main_execution(mock_exec):
    with open(script_path, 'r') as f:
        script_content = f.read()
    exec(script_content)
```

## Problemas na Execução de Testes

### Diagnóstico de Testes Lentos

Quando a suíte de testes (`pytest`) está demorando muito para rodar, o primeiro passo é identificar os gargalos.

- **Comando**: `pytest --durations=10`
- **Análise**: Este comando lista os 10 testes mais lentos. Geralmente, a lentidão está associada a testes que dependem de I/O (rede, disco) ou que usam `subprocess` de forma ineficiente.

### Testes com `subprocess` Falhando com `TimeoutExpired`

Um sintoma comum de problemas em testes de integração é a falha com `subprocess.TimeoutExpired`.

1. **Causa Raiz**: O script sendo executado no subprocesso está travando e não termina. Isso **não** é necessariamente um problema no teste, mas sim um **bug no script sendo testado**.
2. **Diagnóstico**:
    - Adicione `print` statements no script alvo para rastrear sua execução.
    - Verifique se todos os `try...except` blocos que capturam exceções graves (como `requests.exceptions.ConnectionError` ou `Exception`) terminam com um `return` ou `sys.exit()`. Um `except` que apenas imprime uma mensagem e continua a execução pode fazer com que o script trave, especialmente se ele estiver esperando por uma resposta de rede que nunca virá.
3. **Solução Definitiva**: A melhor solução é refatorar o teste para não usar `subprocess`, conforme descrito em [Práticas de Desenvolvimento](development_best_practices.md#testando-scripts-executáveis-e-blocos-main).

### Erros de Ambiente Python

Erros como `pytest: error: unrecognized arguments: --cov` ou `error: externally-managed-environment` ao usar `pip` indicam um problema de ambiente.

- **Causa**: O comando (`pytest`, `pip`) está sendo executado a partir do ambiente global do sistema, em vez do ambiente virtual (`.venv`) do projeto.
- **Solução**: Sempre use os executáveis do ambiente virtual especificando o caminho completo.
  - **Exemplo**: `./.venv/bin/python -m pytest --cov=.`
  - **Exemplo**: `./.venv/bin/pip install -r requirements.txt`

Isso garante que as dependências corretas e os plugins instalados no venv (como o `pytest-cov`) sejam utilizados.

### Servidor MCP não Carrega Código Atualizado

- **Problema**: Alterações no código não são refletidas no servidor MCP em execução
- **Causas**: Cache Python, processo não reiniciado, porta ocupada
- **Soluções**:
  - Limpeza de cache: `find . -name "*.pyc" -delete && find . -type d -name "__pycache__" -exec rm -rf {} +`
  - Reiniciar servidor: `pkill -f "mcp_cli" && make mcp-start`
  - Liberar porta: `sudo fuser -k 3001/tcp`

### Servidor MCP Não Responde ou "Não Traz Tasks"

- **Problema**: Servidor MCP parece estar rodando mas não responde adequadamente ou ferramentas como `list_tasks` não funcionam
- **Sintomas**:
  - Erro "no result from tool"
  - Timeout nas chamadas MCP
  - Ferramentas funcionam localmente mas não via MCP
- **Diagnóstico**:
  - Verificar se servidor está realmente ativo: `ps aux | grep mcp_cli`
  - Testar conectividade: `curl http://localhost:3001/sse`
  - Comparar com CLI local: `python -m src.commands.tasks_cli list`
- **Soluções**:
  - Reiniciar completamente: `make mcp-restart`
  - Verificar logs do servidor por mensagens de erro
  - Confirmar que não há conflitos de versão de código (fazer commit/push se necessário)
  - Testar autenticação independentemente via CLI

### Ferramentas MCP "Tool not found"

- **Problema**: Servidor retorna erro "Tool not found" para ferramentas válidas
- **Causa**: Handlers SSE e Other precisam implementar as mesmas ferramentas
- **Solução**: Verificar se ambos `mcp_post_sse_handler.py` e `mcp_post_other_handler.py` têm as ferramentas implementadas

### Sincronização de Código MCP

- **Problema**: MCP funciona localmente mas não em ambiente remoto/Cursor
- **Causa**: Código local não sincronizado com repositório remoto
- **Solução**:
  - Fazer commit e push das alterações
  - Aguardar deploy automático se houver pipeline CI/CD
  - Verificar se o ambiente remoto está usando a versão correta do código

## Problemas de Resposta MCP

### Ferramentas MCP Não Retornam Resultados

**Problema**: Ferramentas MCP (como `echo` e `add_event`) executam no servidor mas não retornam resultados para o cliente Cursor/MCP.

**Sintomas**:
- `list_events` funciona normalmente
- `echo` e `add_event` executam (visível nos logs do servidor) mas não retornam resposta
- Cliente recebe "no result from tool"

**Causa Raiz**: Inconsistência no formato de resposta entre diferentes ferramentas MCP. O cliente espera sempre o formato padronizado:

```json
{
  "result": {
    "content": [
      {
        "type": "text", 
        "text": "conteúdo da resposta"
      }
    ]
  }
}
```

**Ferramentas afetadas**:
- `echo`: Retornava `{"echo": "message"}` em vez do formato padrão
- `add_event`: Retornava objeto direto em vez do formato padrão
- Outras ferramentas que não seguem o padrão de `content` array

**Solução**:

1. **Padronizar formato de resposta** em `mcp_post_other_handler.py` e `mcp_post_sse_handler.py`:

```python
# Echo - Antes (problemático)
response["result"] = {"echo": message}

# Echo - Depois (correto)
response["result"] = {"content": [{"type": "text", "text": f"🔊 Echo: {message}"}]}

# Add Event - Antes (problemático) 
response["result"] = ops.add_event(event_data)

# Add Event - Depois (correto)
if result.get('status') == 'confirmed':
    event_text = f"✅ Evento criado com sucesso!\n📅 {summary}\n🕐 {start_time} - {end_time}"
    response["result"] = {"content": [{"type": "text", "text": event_text}]}
```

2. **Atualizar testes** para verificar o novo formato:

```python
# Teste antigo
assert body.get("result") == {"echo": "hello"}

# Teste novo
assert body.get("result") == {"content": [{"type": "text", "text": "🔊 Echo: hello"}]}
```

3. **Verificar outras ferramentas** para garantir consistência de formato

**Prevenção**: Sempre usar o formato `{"content": [{"type": "text", "text": "..."}]}` para todas as respostas MCP.

### Ferramenta MCP Funciona Localmente Mas Não Via Cursor

**Problema**: Ferramenta funciona quando testada diretamente (curl, CLI) mas não responde via Cursor

**Diagnóstico**:
- Testar com curl: `curl -X POST http://localhost:3001 -H "Content-Type: application/json" -d '{"method": "tools/call", "params": {"tool": "echo", "args": {"message": "test"}}}'`
- Verificar logs do servidor para ver se requisições estão chegando
- Confirmar se formato de resposta está correto

**Solução**: Geralmente relacionado ao formato de resposta (ver seção anterior) ou configuração de CORS/headers.

## Diagnosticando Problemas de Cobertura de Testes

Alcançar 100% de cobertura é importante, mas às vezes o relatório não reflete a execução real dos testes.

### Cobertura de Subprocessos Não Aparece no Relatório

- **Problema**: Você tem um teste que executa um script via `subprocess`, mas a cobertura desse script permanece em 0% ou não aumenta como esperado. Isso ocorre porque o `coverage` não rastreia subprocessos por padrão.
- **Solução Incorreta**: Tentar invocar o script do subprocesso com `coverage run --append` ou `--parallel-mode` diretamente. Isso geralmente entra em conflito com a execução principal do `pytest-cov`, causando erros como `Can't append to data files in parallel mode`.
- **Solução Correta**: A abordagem mais limpa e robusta é **evitar testar com subprocessos** sempre que possível. Refatore o script para que sua lógica principal esteja em uma função que possa ser importada e testada diretamente. Veja a seção [Testando Scripts Executáveis](development_best_practices.md#testando-scripts-executáveis-e-blocos-main) para o padrão recomendado.

### Cobertura de Código de Teste

- **Problema**: O relatório de cobertura inclui arquivos da pasta `tests/` ou scripts de teste que estão dentro da pasta `src/`.
- **Diagnóstico**: Isso indica um problema na estrutura do projeto ou na configuração do `coverage`. Código de teste não deve ser medido como parte da cobertura da aplicação.
- **Solução**:
  1. **Estrutura de Pastas**: Garanta que todo o código da aplicação esteja em `src/` e todo o código de teste esteja em `tests/`. Scripts que são usados para testar ou interagir com a aplicação, mas não são parte do produto final, não devem estar em `src/`.
  2. **Configuração do `coverage`**: Verifique o arquivo `pytest.ini` ou `.coveragerc` para garantir que o `source` está configurado para o diretório `src`, focando a análise apenas no código da aplicação.

---
Para instruções de uso, veja [Uso](guides/usage.md).
Para melhorias planejadas, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
