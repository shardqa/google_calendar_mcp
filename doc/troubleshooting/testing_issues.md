# Problemas de Testes

## Execução de Testes

### Testes Lentos

**Problema**: A suíte de testes (`pytest`) demora muito para rodar.

**Diagnóstico**:

```bash
pytest --durations=10
```

Este comando lista os 10 testes mais lentos. Geralmente, a lentidão está
associada a testes que dependem de I/O (rede, disco) ou que usam
`subprocess` de forma ineficiente.

### Testes com `subprocess` Falhando

**Problema**: Falha com `subprocess.TimeoutExpired`.

**Causa Raiz**: O script sendo executado no subprocesso está travando e
não termina.

**Diagnóstico**:

- Adicione `print` statements no script alvo para rastrear execução
- Verifique se todos os `try...except` blocos terminam com `return` ou
  `sys.exit()`

**Solução**: Refatorar o teste para não usar `subprocess`, conforme
descrito em [Práticas de
Desenvolvimento](../guides/development_best_practices.md#testando-scripts-executáveis-e-blocos-main).

### Erro "unrecognized arguments: --cov"

**Problema**: `pytest: error: unrecognized arguments: --cov`

**Causa**: O comando `pytest` está sendo executado do ambiente global em
vez do virtual.

**Solução**: Use o executável do ambiente virtual:

```bash
./.venv/bin/python -m pytest --cov=.
```

## Problemas de Cobertura

### Cobertura de Subprocessos Não Aparece

**Problema**: Testes que executam scripts via `subprocess` mostram 0% de
cobertura.

**Causa**: O `coverage` não rastreia subprocessos por padrão.

**Solução Incorreta**: Tentar usar `coverage run --append` ou
`--parallel-mode` diretamente.

**Solução Correta**: Evitar testar com subprocessos. Refatore o script
para que sua lógica principal esteja em uma função importável.

### Cobertura Inclui Arquivos de Teste

**Problema**: O relatório de cobertura inclui arquivos da pasta `tests/`.

**Causa**: Problema na estrutura do projeto ou configuração do `coverage`.

**Solução**:

1. Garanta que todo código da aplicação esteja em `src/` e teste em
   `tests/`
2. Verifique `pytest.ini` ou `.coveragerc` para garantir que `source`
   está configurado para `src`

## CI/CD Issues

### Testes Falhando no GitHub Actions

**Problema**: Testes passam localmente mas falham no CI com
`FileNotFoundError` para caminhos como `/home/runner/work/...`

**Causa**: Testes usando caminhos hardcoded em vez do executável Python
atual.

**Solução**: Substituir referências diretas ao path do venv por
`sys.executable`:

```python
# Antes (problemático)
python_executable = os.path.join(os.getcwd(), '.venv', 'bin', 'python')

# Depois (correto)
python_executable = sys.executable
```

### Subprocess Tests em CI

**Problema**: Testes com subprocess falhando em ambientes CI/CD.

**Solução**: Simplificar testes para usar simulação direta:

```python
# Abordagem robusta para teste de __main__
@patch('sys.argv', ['script_name'])
@patch('builtins.exec')
def test_main_execution(mock_exec):
    with open(script_path, 'r') as f:
        script_content = f.read()
    exec(script_content)
```

---
Voltar para [Resolução de Problemas](../troubleshooting.md).
