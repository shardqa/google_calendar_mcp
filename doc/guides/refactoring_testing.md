# Estratégias de Teste Durante a Refatoração

Manter uma suíte de testes robusta e confiável é crucial durante a refatoração para garantir que nenhuma funcionalidade seja quebrada.

## Teste Contínuo

**Princípio**: Execute a suíte de testes completa após cada mudança significativa. Isso fornece feedback imediato e evita o acúmulo de problemas.

```bash
# Após extrair uma função ou módulo
make test

# Se falhar, corrija imediatamente antes de continuar.
```

## Mocking Modularizado

**Problema**: Mover uma função ou classe pode invalidar os `patch` de mock em dezenas de testes, pois os caminhos de importação mudam.

**Solução**: Atualize os alvos dos patches de mock para refletir a nova estrutura de arquivos *junto* com a refatoração do código da aplicação.

```python
# ANTES: Patch na classe monolítica
@patch('src.core.calendar_ops.CalendarOperations')
def test_handler(mock_calendar_ops):
    # ...

# DEPOIS: Patch na função específica e importada
@patch('src.core.calendar.list_events')
def test_handler(mock_list_events):
    # ...
```

## Testes de Regressão e Integração

**Abordagem**: Mantenha um conjunto de testes de integração de alto nível que validam fluxos de trabalho completos do usuário.

-   **Características**:
    -   Não usam mocks extensivos para a lógica de negócio principal.
    -   Verificam a funcionalidade do ponto de vista do usuário final.
    -   Garantem que os "contratos" da API (assinaturas de função, tipos de retorno) não sejam alterados acidentalmente.

**Exemplo**:
```python
def test_calendar_integration_end_to_end():
    """Valida que a refatoração não quebrou o fluxo completo."""
    # 1. Autenticar para obter o 'service'
    service = auth.get_calendar_service()
    
    # 2. Chamar a função refatorada para listar calendários
    calendars = list_calendars(service)
    
    # 3. Adicionar um evento usando a nova função
    event = add_event(service, event_data)
    
    # ... e assim por diante, validando o fluxo completo.
```

---
Voltar para as [Boas Práticas de Refatoração](refactoring_best_practices.md). 