# Configuração Avançada

Esta seção cobre cenários de implantação mais complexos, como a execução do servidor MCP em um ambiente remoto ou como um serviço de sistema.

## Servidor Remoto com Autenticação

Para executar o servidor em um ambiente de produção ou acessível pela rede, é crucial habilitar a autenticação para proteger os endpoints.

1.  **Gerar Token de Autenticação**:
    Execute o script para gerar um token seguro. Este token precisará ser fornecido pelos clientes em suas requisições.
    ```bash
    python scripts/security/generate_secure_token.py
    ```

2.  **Iniciar Servidor com Autenticação**:
    Use a flag `--auth-required` para exigir que todas as chamadas para as ferramentas sejam autenticadas.
    ```bash
    python -m src.mcp.mcp_server --auth-required --port 3001
    ```

3.  **Configurar Nginx como Reverse Proxy (Opcional, mas Recomendado)**:
    Usar o Nginx na frente do servidor MCP adiciona uma camada de segurança e robustez (SSL, rate limiting, etc.).
    ```bash
    # Copie a configuração de exemplo
    sudo cp config/nginx-mcp-remote-secure.conf /etc/nginx/sites-available/

    # Ative a configuração
    sudo ln -s /etc/nginx/sites-available/nginx-mcp-remote-secure.conf /etc/nginx/sites-enabled/

    # Teste e reinicie o Nginx
    sudo nginx -t && sudo systemctl restart nginx
    ```

## Execução com Systemd

Para garantir que o servidor MCP seja executado automaticamente na inicialização do sistema e reiniciado em caso de falha, você pode configurá-lo como um serviço `systemd`.

1.  **Copiar Arquivo de Serviço**:
    ```bash
    sudo cp config/google-calendar-mcp.service /etc/systemd/system/
    ```

2.  **Editar e Personalizar o Serviço**:
    É fundamental ajustar os caminhos no arquivo de serviço para corresponder ao seu ambiente.
    ```bash
    sudo systemctl edit google-calendar-mcp --full
    ```
    Modifique as diretivas `WorkingDirectory` e `ExecStart` com os caminhos absolutos corretos.

3.  **Habilitar e Gerenciar o Serviço**:
    ```bash
    # Recarregar o daemon do systemd
    sudo systemctl daemon-reload

    # Habilitar o serviço para iniciar no boot
    sudo systemctl enable google-calendar-mcp

    # Iniciar o serviço imediatamente
    sudo systemctl start google-calendar-mcp

    # Verificar o status do serviço
    sudo systemctl status google-calendar-mcp
    ```

---
Voltar para o guia de [Instalação](installation.md). 