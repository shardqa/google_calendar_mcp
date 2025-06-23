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

#### Métricas de Qualidade Atuais

- **230+ testes** executando consistentemente em ~4.0 segundos
- **100% cobertura geral** do projeto (818 statements, 210 branches)
- **100% cobertura de branches** em todos os handlers MCP críticos
- **Zero testes falhando** em produção e CI/CD
- **GitHub Actions**: Pipeline automatizada com deployment contínuo

#### Evolução da Cobertura - Conquista dos 100%

**Marco Histórico:**

- Início: 90% de cobertura com 158 testes
- Progressão: 98% de cobertura com 182 testes  
- **Conquista atual: 100% de cobertura com 230+ testes**

**Marcos Recentes:**

- **Intelligent Scheduling**: Implementação completa com TDD
- **Debugging de branch coverage**: Identificação e correção de bugs lógicos
- **Edge cases abrangentes**: Cobertura de cenários extremos e falhas

**Áreas de Foco para Alcançar 100%:**

- **src/core/calendar_ops.py**: 94% → 100%
  - Cobertura de erro de frequência inválida em `add_recurring_event`
  - Cobertura de tratamento de exceções de serviço
- **src/mcp/mcp_post_sse_handler.py**: 91% → 100%
  - Implementação completa de testes para `add_recurring_task`
  - Cobertura de validação de parâmetros obrigatórios
  - Testes de cenários de sucesso com parâmetros opcionais

**Estratégias Específicas que Funcionaram:**

- **Testes de frequência inválida**: Verificar tratamento de erro para valores não suportados
- **Testes de erro de serviço**: Simular falhas da API Google usando mock exceptions
- **Testes de handlers MCP**: Cobertura completa de cenários com/sem parâmetros opcionais
- **Validação de parâmetros**: Testes específicos para parâmetros obrigatórios ausentes

### Debugging Branch Coverage: Casos Avançados

**Problema Comum: Branch Parts Não Cobertos**

Quando relatórios mostram `97->96` ou similar, indica branches específicos não testados:

```python
# Exemplo problemático original:
event_start = event.get('start', {}).get('dateTime', work_start)  # ❌
if work_start < event_start:  # Sempre False quando dateTime missing
    # Esta branch nunca é executada
```

**Estratégias de Debugging:**

1. **Análise de Lógica**: Questionar se condições são realmente alcançáveis
2. **Testes de Condições Extremas**: Testar valores edge (None, empty, boundary conditions)
3. **Correção de Bugs Lógicos**: Refatorar código para torná-lo testável

```python
# Solução corrigida:
event_start = event.get('start', {}).get('dateTime')  # ✅
if event_start and work_start < event_start:  # Agora testável
    # Branch pode ser coberto com testes apropriados
```

**Lições Aprendidas:**

- **Untestable code pode indicar bugs**: Condições impossíveis revelam problemas de design
- **Fallbacks problemáticos**: Valores padrão que criam condições sempre falsas
- **Preferir correção a pragma**: Corrigir lógica é melhor que ignorar cobertura

## Lidando com Código Intestável: O `pragma: no cover`

A busca por 100% de cobertura de testes é um objetivo nobre, mas nem todo código é prático ou mesmo útil de se testar. Blocos `if __name__ == "__main__"` e saídas de sistema como `sys.exit()` são exemplos clássicos. Tentar cobri-los pode levar a testes complexos e frágeis.

A solução padrão e limpa para esses casos é usar um comentário especial para instruir a ferramenta de cobertura a ignorar essas linhas:

```python
# Exemplo 1: Ignorando um bloco __main__
if __name__ == "__main__":  # pragma: no cover
    main()

# Exemplo 2: Ignorando uma chamada de saída
def main():
    try:
        # ... lógica ...
    except Exception:
        print("Um erro ocorreu.")
        sys.exit(1)  # pragma: no cover
```

Usar `pragma: no cover` mantém o relatório de cobertura limpo e focado no que realmente importa: a lógica de negócios da aplicação, permitindo alcançar um "100% significativo" sem comprometer a qualidade ou a simplicidade dos testes.

## Testando Scripts Executáveis e Blocos `__main__`

Testar o ponto de entrada de scripts executáveis é crucial para garantir a robustez. A abordagem ideal prioriza velocidade e simplicidade.

### Abordagem Recomendada: Refatoração para Testabilidade

1. **Isolar a Lógica**: Mova todo o código do bloco `__main__` para uma função separada, como `main()`. O bloco `__main__` deve apenas chamar essa nova função.

    ```python
    # Em seu_script.py
    def main():
        parser = argparse.ArgumentParser()
        # ... adicionar argumentos ...
        args = parser.parse_args()
        # ... lógica do script ...

    if __name__ == "__main__":
        main()
    ```

2. **Testar a Função `main` Diretamente**: Nos testes, importe e chame a função `main()` diretamente. Use mocks para simular argumentos (`sys.argv`) ou para isolar dependências (chamadas de rede, sistema de arquivos), se necessário.

    ```python
    # Em tests/test_seu_script.py
    from unittest.mock import patch
    from seu_pacote import seu_script

    @patch('seu_pacote.seu_script.funcao_critica')
    def test_main_executa_com_sucesso(mock_funcao_critica):
        """Testa a função main com argumentos simulados."""
        # Simula a linha de comando via sys.argv
        with patch.object(sys, 'argv', ['seu_script.py', 'arg1']):
            seu_script.main()
            # Verifica se a lógica interna foi chamada corretamente
            mock_funcao_critica.assert_called_once_with('arg1')
    ```

3. **Testar o Bloco `__main__` (se necessário)**: Se a cobertura do próprio bloco `if __name__ == "__main__"` for desejada, a abordagem mais limpa é usar o módulo `runpy`. No entanto, como discutido, é muitas vezes mais pragmático simplesmente excluí-lo da cobertura.

### Vantagens da Abordagem Refatorada

- **Velocidade**: Evita a sobrecarga de iniciar um novo processo.
- **Simplicidade**: Evita a complexidade de gerenciar ambientes de subprocesso, `PYTHONPATH` e `coverage`.
- **Depuração**: Erros ocorrem no processo principal do `pytest`, permitindo o uso de depuradores padrão.
- **Robustez**: Menos propenso a falhas intermitentes relacionadas a timeouts ou configuração de ambiente.

## Organização de Código

### Estrutura Modular

- **Máximo 10 itens por pasta**: Criar subpastas quando necessário
- **Máximo 100 linhas por arquivo**: Dividir em módulos menores
- **Separação clara de responsabilidades**: `commands`, `core`, `mcp`, etc.
- **Não misturar código de teste e de aplicação**: Arquivos de teste devem residir na pasta `tests/`, não em `src/`.

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

## Padrões MCP e Formato de Resposta

### Formato Padronizado de Resposta MCP

Todas as ferramentas MCP devem retornar respostas no formato padronizado para garantir compatibilidade com clientes como Cursor IDE:

```python
# ✅ Formato correto - sempre usar
response["result"] = {
    "content": [
        {
            "type": "text", 
            "text": "conteúdo da resposta formatado"
        }
    ]
}

# ❌ Formatos incorretos - evitar
response["result"] = {"echo": message}           # Não padronizado
response["result"] = raw_api_response           # Sem formatação
response["result"] = {"status": "ok"}           # Sem conteúdo visual
```

### Implementação Consistente em Handlers

**Princípio**: Ambos os handlers (`mcp_post_other_handler.py` e `mcp_post_sse_handler.py`) devem implementar exatamente as mesmas ferramentas com o mesmo formato de resposta.

```python
# Exemplo: Ferramenta echo em ambos os handlers
if tool_name == "echo":
    message = tool_args.get("message", "No message provided")
    print(f"Echoing message via tools/call: {message}")
    response["result"] = {"content": [{"type": "text", "text": f"🔊 Echo: {message}"}]}
```

### Tratamento de Erro Padronizado

**Sucessos** devem retornar informações visuais úteis:

```python
# Add Event - Sucesso
if result.get('status') == 'confirmed':
    event = result.get('event', {})
    summary = event.get('summary', 'Evento criado')
    start_time = event.get('start', {}).get('dateTime', 'N/A')
    end_time = event.get('end', {}).get('dateTime', 'N/A')
    location = event.get('location', '')
    
    event_text = f"✅ Evento criado com sucesso!\n📅 {summary}\n🕐 {start_time} - {end_time}"
    if location:
        event_text += f"\n📍 {location}"
    
    response["result"] = {"content": [{"type": "text", "text": event_text}]}
```

**Erros** devem ser informativos:

```python
# Add Event - Erro
else:
    error_msg = result.get('message', 'Erro desconhecido')
    response["result"] = {"content": [{"type": "text", "text": f"❌ Erro ao criar evento: {error_msg}"}]}
```

### Testes de Compatibilidade MCP

Sempre incluir testes que verificam o formato de resposta:

```python
def test_mcp_response_format(monkeypatch):
    # ... setup ...
    mod.handle_post_other(handler, request, response)
    body = parse_response(handler)
    
    # Verificar estrutura padronizada
    assert "result" in body
    assert "content" in body["result"]
    assert isinstance(body["result"]["content"], list)
    assert len(body["result"]["content"]) > 0
    assert "type" in body["result"]["content"][0]
    assert "text" in body["result"]["content"][0]
    assert body["result"]["content"][0]["type"] == "text"
```

### Debugging de Ferramentas MCP

**Diagnóstico de problemas comuns:**

1. **Ferramenta executa mas não retorna**: Verificar formato de resposta
2. **Cliente recebe "no result"**: Comparar com ferramentas funcionais (`list_events`)
3. **Funciona localmente mas não via Cursor**: Verificar logs do servidor e formato de resposta

**Ferramentas de teste:**

```bash
# Teste direto com curl
curl -X POST http://localhost:3001 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"tool": "echo", "args": {"message": "test"}}}'

# Servidor local para desenvolvimento
make mcp-local

# Verificar logs do servidor
# (logs aparecem no terminal onde o servidor está rodando)
```

---
Para visão geral do projeto, veja [Visão Geral](overview.md).
Para arquitetura técnica, veja [Arquitetura](architecture.md).
Voltar para o [Sumário](README.md).
