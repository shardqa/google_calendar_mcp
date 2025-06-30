# Guia de Instalação

Este guia cobre os passos essenciais para colocar o projeto em funcionamento no seu ambiente local.

## 1. Pré-requisitos

-   **Python 3.8+**: Necessário para executar o projeto.
-   **Projeto no Google Cloud**:
    -   APIs do **Google Calendar** e **Google Tasks** devem estar ativadas.
-   **Credenciais OAuth2**:
    -   Faça o download do arquivo `credentials.json` do seu projeto no Google Cloud.
    -   Coloque este arquivo no diretório `config/` do projeto (`config/credentials.json`).

## 2. Configuração do Ambiente Local

1.  **Clone o Repositório**:
    ```bash
    git clone https://github.com/seu-usuario/google_calendar_mcp.git
    cd google_calendar_mcp
    ```

2.  **Crie o Ambiente Virtual**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    ```

3.  **Instale as Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Autenticação Inicial

Na primeira vez que você executar qualquer funcionalidade que acesse a API do Google, será necessário autorizar o acesso.

```bash
# Exemplo de primeira execução
python -m src.commands.mcp_cli --setup-only
```

Um navegador será aberto para que você possa fazer login na sua conta Google e conceder as permissões necessárias. Um arquivo `token.pickle` será criado para armazenar suas credenciais para execuções futuras.

## 4. Verificação da Instalação

Para garantir que tudo está configurado corretamente, execute a suíte de testes.

```bash
make test
```

## Próximos Passos

-   **Configurar Clientes de IA**: Para usar o projeto com Cursor, Gemini ou outros assistentes, veja o **[Guia de Configuração de Clientes](client_setup.md)**.
-   **Deploy em Produção**: Para cenários de implantação mais robustos, consulte o **[Guia de Configuração Avançada](advanced_setup.md)**.
-   **Solução de Problemas**: Se encontrar algum problema, verifique o **[Guia de Resolução de Problemas](../../troubleshooting.md)**.

---
Voltar para o [Sumário](../../README.md).
