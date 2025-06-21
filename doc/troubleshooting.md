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

1.  **Causa Raiz**: O script sendo executado no subprocesso está travando e não termina. Isso **não** é necessariamente um problema no teste, mas sim um **bug no script sendo testado**.
2.  **Diagnóstico**:
    - Adicione `print` statements no script alvo para rastrear sua execução.
    - Verifique se todos os `try...except` blocos que capturam exceções graves (como `requests.exceptions.ConnectionError` ou `Exception`) terminam com um `return` ou `sys.exit()`. Um `except` que apenas imprime uma mensagem e continua a execução pode fazer com que o script trave, especialmente se ele estiver esperando por uma resposta de rede que nunca virá.
3.  **Solução Definitiva**: A melhor solução é refatorar o teste para não usar `subprocess`, conforme descrito em [Práticas de Desenvolvimento](development_best_practices.md#testando-scripts-executáveis-e-blocos-main).

### Erros de Ambiente Python

Erros como `pytest: error: unrecognized arguments: --cov` ou `error: externally-managed-environment` ao usar `pip` indicam um problema de ambiente.

- **Causa**: O comando (`pytest`, `pip`) está sendo executado a partir do ambiente global do sistema, em vez do ambiente virtual (`.venv`) do projeto.
- **Solução**: Sempre use os executáveis do ambiente virtual especificando o caminho completo.
  - **Exemplo**: `./.venv/bin/python -m pytest --cov=.`
  - **Exemplo**: `./.venv/bin/pip install -r requirements.txt`

Isso garante que as dependências corretas e os plugins instalados no venv (como o `pytest-cov`) sejam utilizados.

---
Para instruções de uso, veja [Uso](usage.md).
Para melhorias planejadas, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
