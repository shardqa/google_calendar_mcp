# Princípios Arquiteturais

A arquitetura do projeto é guiada por um conjunto de princípios fundamentais para garantir a qualidade, manutenibilidade e escalabilidade do código.

## Regra dos 100 Linhas

**Motivação**: Facilitar manutenção, compreensão e testabilidade.

**Implementação**:
-   Todos os arquivos de código são limitados a um máximo de 100 linhas.
-   Arquivos de dados, como schemas ou configurações, são exceções explícitas.
-   A regra é reforçada por scripts de validação e revisões de código.
-   Quando um arquivo excede o limite, ele é imediatamente refatorado.

**Benefícios Comprovados**:
-   **Redução da Complexidade Cognitiva**: Desenvolvedores conseguem manter o contexto de um arquivo inteiro na mente.
-   **Isolamento de Responsabilidades**: Cada módulo tem um propósito claro e único.
-   **Testabilidade Aprimorada**: Testes unitários se tornam mais fáceis de escrever e mais focados.
-   **Facilidade de Revisão**: Pull requests são menores e mais rápidos de revisar.

## Modularização por Função

**Abordagem**: Substituir classes monolíticas por funções especializadas e independentes, agrupadas em módulos por funcionalidade.

**Antes**:
Uma única classe `CalendarOperations` com mais de 8 métodos, lidando com listagem, criação, edição e remoção de eventos.

**Depois**:
Módulos separados para cada operação, como `list_events.py`, `add_event.py`, etc., contendo funções puras e bem definidas.

**Exemplo Prático**:
```python
# Em src/core/calendar/list_events.py
def list_events(service, max_results=10, calendar_id="primary"):
    # ... lógica específica para listar eventos ...
```

**Benefícios**:
-   **Importações Granulares**: Consumidores podem importar apenas a função de que precisam.
-   **Reutilização de Código**: Funções podem ser facilmente reutilizadas em diferentes partes do sistema.
-   **Baixo Acoplamento**: Módulos não dependem uns dos outros, apenas de suas entradas.
-   **Testes Independentes**: Cada função pode ser testada de forma isolada, simplificando mocks.

## Padrões de Design Aplicados

-   **Separação de Responsabilidades (SoC)**: Camadas de negócio, dados e apresentação são claramente distintas.
-   **Inversão de Dependência (DI)**: Dependências são injetadas (ex: `service`), não criadas internamente.
-   **Single Responsibility Principle (SRP)**: Cada módulo ou função tem uma única razão para mudar.
-   **Don't Repeat Yourself (DRY)**: Lógica compartilhada é abstraída em funções utilitárias.
-   **Composição sobre Herança**: A arquitetura favorece a composição de funções e pequenos componentes em vez de hierarquias de classes complexas.

---
Voltar para a [Arquitetura Principal](architecture.md). 