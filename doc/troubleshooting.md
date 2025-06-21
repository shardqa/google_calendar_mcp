# Resolução de Problemas

## Erros Comuns

- **Falha na autenticação**: Verifique se o arquivo `credentials.json` está correto e na raiz do projeto.
- **Erros de API**: Confirme se a API do Google Calendar está ativada no Console Google Cloud.
- **Token inválido**: Exclua o arquivo `token.pickle` para forçar uma nova autenticação.

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

### Ferramentas MCP "Tool not found"

- **Problema**: Servidor retorna erro "Tool not found" para ferramentas válidas
- **Causa**: Handlers SSE e Other precisam implementar as mesmas ferramentas
- **Solução**: Verificar se ambos `mcp_post_sse_handler.py` e `mcp_post_other_handler.py` têm as ferramentas implementadas

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
Para instruções de uso, veja [Uso](usage.md).
Para melhorias planejadas, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
