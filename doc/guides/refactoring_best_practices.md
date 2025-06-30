# Boas Práticas de Refatoração

Este documento captura as lições aprendidas e as melhores práticas para a refatoração de código no projeto.

## Princípios Fundamentais

-   **Regra das 100 Linhas**: Manter arquivos concisos para maximizar legibilidade, testabilidade e manutenibilidade.
-   **Organização de Diretórios**: Manter no máximo 10 itens por diretório para promover uma estrutura lógica.

## Estratégias de Refatoração

-   **Decomposição Funcional**: Quebrar classes e arquivos grandes em funções ou módulos menores e especializados.
    -   *Ex: `CalendarOperations` (186 linhas) -> 7 módulos de função única.*
-   **Extração de Handlers**: Mover a lógica de tratamento de protocolo (HTTP, STDIO) para classes `Handler` dedicadas.
-   **Reorganização de Diretórios**: Agrupar arquivos em subdiretórios temáticos quando um diretório cresce demais.
    -   *Ex: `scripts/` -> `security/`, `test/`, `remote_legacy/`.*

## Gestão de Efeitos Colaterais

-   **"Import Cascades"**: Para evitar quebras massivas de `import`, use `__init__.py` como uma fachada de API para manter a compatibilidade durante a transição e atualize os imports de forma incremental.
-   **Validação Contínua**: A chave para gerenciar efeitos colaterais é o feedback rápido. Para isso, consulte o guia **[Estratégias de Teste Durante a Refatoração](refactoring_testing.md)**.

## Documentação e Ferramentas

-   **Documentação**: Ao refatorar, atualize todos os documentos relevantes (`README.md`, `architecture.md`, etc.) para refletir a nova estrutura.
-   **Ferramentas Úteis**:
    ```bash
    # Encontrar arquivos grandes
    find src -name "*.py" -exec awk 'END{if(NR>100) print FILENAME ": " NR}' {} \;

    # Mapear dependências de um módulo
    grep -r "from src.antigo.modulo import" .
    ```

## Métricas de Sucesso

-   **Redução de Linhas**: O número de linhas por arquivo deve diminuir.
-   **Complexidade Cognitiva**: A facilidade de entender um único arquivo deve aumentar.
-   **Manutenção da Cobertura**: A cobertura de testes deve ser mantida ou melhorada.

---
Para mais detalhes sobre a arquitetura, veja [Arquitetura](architecture.md).
Para histórico completo das mudanças, veja [COMPLETED.md](../../COMPLETED.md). 