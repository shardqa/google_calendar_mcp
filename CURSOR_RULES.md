# Cursor Development Rules

Este documento consolida regras essenciais para desenvolvimento no projeto Google
Calendar MCP.

## Regras Gerais

- **TDD Sempre**: Escreva testes que falhem antes de qualquer implementação.
- **Cobertura Total**: Após qualquer alteração no código, os testes devem
  continuar passando e a cobertura global deve voltar a **100%**.
- **Máximo de dez itens por pasta**: Crie sub-pastas e ajuste imports quando necessário.
- **Arquivos ≤ 100 linhas**: Divida módulos longos e mantenha a legibilidade.
- **Markdown lint**: Ao criar ou editar um arquivo `.md`, execute `markdownlint --fix`.

## Referências

- [Práticas de Desenvolvimento](doc/development_best_practices.md)
- [Arquitetura do Projeto](doc/guides/architecture.md)

- Excluded from auto-refactor/move checks (never move these): .cursor, .github, .venv, .coverage, .coveragerc, .cursorrules, .gitignore, Makefile, README.md, requirements.txt, TODO.md, src/mcp/mcp_schema.py from the root folder.
