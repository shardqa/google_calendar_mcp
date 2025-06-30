# Contribuindo

Agradecemos o seu interesse em contribuir com o Google Calendar MCP! Para garantir um processo tranquilo e eficaz para todos, siga estas diretrizes.

## Processo de Desenvolvimento

1.  **Fork e Branch**:
    -   Faça um fork do repositório.
    -   Crie uma branch para a sua feature ou correção:
        `git checkout -b feature/sua-nova-feature`.

2.  **Desenvolvimento Orientado a Testes (TDD)**:
    -   Escreva um teste que falhe antes de implementar a funcionalidade.
    -   Implemente o código necessário para fazer o teste passar.
    -   Refatore o código, garantindo que os testes continuem passando.
    -   Mantenha a cobertura de testes acima de 95%.

3.  **Commit e Push**:
    -   Faça o commit das suas mudanças com uma mensagem clara:
        `git commit -am 'Adiciona nova feature que faz X'`.
    -   Faça o push para a sua branch: `git push origin feature/sua-nova-feature`.

4.  **Pull Request**:
    -   Abra um Pull Request para a branch `main`.
    -   Descreva suas mudanças em detalhes e referencie qualquer issue relevante.

## Padrões de Código

-   Siga as convenções de estilo da PEP 8.
-   Mantenha os arquivos com no máximo 100 linhas.
-   Organize os diretórios com no máximo 10 arquivos.
-   Adicione documentação para novas funcionalidades nos arquivos `doc/guides`.

## Licença

Este projeto está licenciado sob a Licença MIT. Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença.

Para mais detalhes, veja o arquivo `LICENSE` (a ser criado).

---
Voltar para o [Sumário](../../README.md). 