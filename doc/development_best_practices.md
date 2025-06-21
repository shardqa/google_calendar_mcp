# Práticas de Desenvolvimento

Este documento captura as metodologias e padrões de qualidade estabelecidos
durante o desenvolvimento do Google Calendar MCP.

## Metodologia Test-Driven Development (TDD)

### Ciclo Red-Green-Refactor

1. **Red**: Escrever um teste que falha
   - Definir o comportamento esperado antes da implementação
   - Garantir que o teste está realmente testando a funcionalidade
   - Verificar que o teste falha pela razão correta

2. **Green**: Implementar código mínimo para passar o teste
   - Focar apenas em fazer o teste passar
   - Evitar over-engineering na primeira implementação
   - Manter simplicidade e clareza

3. **Refactor**: Melhorar o código mantendo os testes verdes
   - Eliminar duplicação
   - Melhorar legibilidade e estrutura
   - Verificar que todos os testes continuam passando

### Benefícios Observados

- **Confiança**: 98% de cobertura com 200+ testes
- **Design**: API mais limpa e testável
- **Documentação viva**: Testes como especificação executável
- **Refatoração segura**: Mudanças com confiança

## Estratégias de Teste

### Isolamento de Dependências

```python
# Exemplo: Mock de APIs externas
@patch('googleapiclient.discovery.build')
def test_list_events_success(mock_build):
    mock_service = Mock()
    mock_build.return_value = mock_service
    # Configurar comportamento esperado
    mock_service.events().list().execute.return_value = expected_response
```

### Testes de Scripts e Utilitários

#### Abordagem para Scripts de Teste

- **Testes unitários isolados**: Testar lógica específica sem chamar
  funções com `pytest.fail()`
- **Simulação de cenários**: Usar mocks para simular condições de erro
- **Decomposição de lógica**: Quebrar lógica complexa em funções testáveis

```python
# Exemplo: Teste de lógica de processamento SSE
def test_line_processing_logic(self):
    test_line = "event: mcp/hello"
    assert test_line.startswith("event:")
    event_name = test_line[6:].strip()
    assert event_name == "mcp/hello"
```

#### Cobertura de Cenários de Erro

- **Timeouts de rede**: Simular requests.exceptions.Timeout
- **Erros HTTP**: Status codes 500, 404, etc.
- **Erros de decodificação**: UnicodeDecodeError, dados binários inválidos
- **Formatos desconhecidos**: Dados que não seguem protocolos esperados
- **Exceções genéricas**: Tratamento de casos inesperados

#### Mocking Estratégico

```python
# Exemplo: Mock completo de dependências externas
@patch('module.socket.socket')
@patch('module.CalendarMCPServer')
@patch('module.requests.Session')
def test_network_operations(self, mock_session, mock_server, mock_socket):
    # Configurar mocks para simular cenários específicos
    mock_socket.return_value.__enter__.return_value.getsockname.return_value = (
        'localhost', 12345)
    mock_server.return_value = MagicMock()
    mock_session.return_value.get.return_value.status_code = 200
```

### Testes de Integração

- **Subprocess**: Teste de scripts executáveis
- **Exec contexts**: Validação de blocos `if __name__ == "__main__"`
- **End-to-end**: Fluxos completos de usuário
- **Ambiente controlado**: Uso de mocks para evitar dependências externas

### Cobertura Estratégica

#### Prioridades de Teste

1. **Código crítico**: Auth, operações principais (98%+ coverage)
2. **Scripts utilitários**: Cenários de conectividade e inicialização
   (94-96% coverage)
3. **Edge cases**: Tratamento de erros e exceções
4. **Cenários reais**: Casos de uso do usuário final

#### Métricas de Qualidade

- **200+ testes** executando consistentemente
- **98% cobertura geral** do projeto
- **Zero testes falhando** em produção
- **Tempo de execução** otimizado (~4 segundos para suite completa)

#### Abordagem para Código Difícil de Testar

- **Blocos `__main__`**: Simulação de argumentos e fluxos
- **I/O externo**: Mocking de sockets, HTTP requests
- **Timing dependencies**: Mock de `time.time()`, `time.sleep()`
- **Sistema de arquivos**: Uso de temporary files ou mocks

## Organização de Código

### Estrutura Modular

- **Máximo 10 itens por pasta**: Criar subpastas quando necessário
- **Máximo 100 linhas por arquivo**: Dividir em módulos menores
- **Separação clara de responsabilidades**: Commands, Core, MCP

### Convenções de Nomenclatura

- **Módulos**: snake_case descritivo
- **Classes**: PascalCase com sufixo do tipo (Handler, Manager, etc.)
- **Funções**: snake_case com verbos claros
- **Constantes**: UPPER_SNAKE_CASE

### Importações

- **Organização**: stdlib, third-party, local
- **Imports relativos**: Para módulos do mesmo pacote
- **Imports explícitos**: Evitar `import *`

## Tratamento de Erros

### Hierarquia de Exceções

```python
# Exemplo: Exceções específicas do domínio
class CalendarError(Exception):
    """Base exception for calendar operations"""
    
class AuthenticationError(CalendarError):
    """Authentication related errors"""
    
class EventNotFoundError(CalendarError):
    """Event not found errors"""
```

### Padrões de Recuperação

- **Retry logic**: Para falhas temporárias de rede
- **Graceful degradation**: Funcionalidade parcial quando possível
- **User feedback**: Mensagens claras e acionáveis

### Estratégias de Debug

#### Scripts de Diagnóstico

- **Conectividade**: Verificação de portas e serviços
- **Autenticação**: Validação de credenciais e tokens
- **SSE Streams**: Teste de comunicação em tempo real
- **Inicialização**: Verificação de setup e dependências

#### Logging e Monitoramento

- **Mensagens informativas**: Status de operações importantes
- **Códigos de erro específicos**: Para facilitar troubleshooting
- **Timeouts configuráveis**: Adaptação a diferentes ambientes

## Documentação

### Código Autodocumentado

- **Nomes descritivos**: Código que explica sua intenção
- **Estrutura clara**: Organização lógica facilita entendimento
- **Evitar comentários**: Preferir código explícito (conforme regras do projeto)

### Documentação Externa

- **README**: Visão geral e início rápido
- **Architecture**: Estrutura e componentes
- **Usage**: Exemplos práticos de uso
- **Troubleshooting**: Problemas comuns e soluções

### Manutenção de Docs

- **Markdownlint**: Consistência e qualidade
- **Links internos**: Navegação entre documentos
- **Atualização contínua**: Documentação sempre sincronizada

## Performance e Qualidade

### Otimizações

- **Threading**: Servidor HTTP multi-thread
- **Lazy loading**: Carregar recursos quando necessário
- **Caching**: Tokens e credenciais persistidas

### Monitoramento

- **Coverage reports**: Acompanhar evolução da cobertura
- **Test metrics**: Tempo de execução e paralelização
- **Code quality**: Linting e análise estática

### Evolução de Qualidade

#### Marcos Alcançados

- **Fase 1**: Funcionalidade básica com 96% coverage
- **Fase 2**: Integração Google Tasks com testes robustos
- **Fase 3**: Scripts utilitários com 94-98% coverage
- **Atual**: 200 testes, 98% coverage, zero falhas

#### Lições Aprendidas

- **Testes isolados** são mais robustos que testes que dependem de `pytest.fail()`
- **Mocking estratégico** permite testar cenários complexos sem dependências externas
- **Decomposição de lógica** facilita tanto desenvolvimento quanto teste
- **Cobertura alta** não deve comprometer a qualidade ou legibilidade dos testes

---
Para visão geral do projeto, veja [Visão Geral](overview.md).
Para arquitetura técnica, veja [Arquitetura](architecture.md).
Voltar para o [Sumário](README.md).
