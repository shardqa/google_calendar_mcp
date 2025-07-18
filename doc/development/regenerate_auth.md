# Como Regenerar a Autenticação Google (OAuth2)

Se você encontrar erros como:

```
google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.', ...)
```

ou se precisar reautorizar o acesso do Google Calendar MCP à sua conta Google, siga os passos abaixo para forçar uma nova autenticação:

---

## 1. Remova o token antigo

O token de autenticação é salvo em `config/token.pickle`. Para forçar o fluxo OAuth novamente, apague este arquivo:

```bash
rm config/token.pickle
```

---

## 2. Verifique o arquivo de credenciais

- Certifique-se de que `config/credentials.json` existe e é válido.
- Se precisar gerar um novo:
  1. Acesse o [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
  2. Selecione seu projeto.
  3. Clique em "Criar credenciais" > "ID do cliente OAuth".
  4. Escolha "Aplicativo para computador".
  5. Baixe o JSON e coloque em `config/credentials.json`.

---

## 3. Execute o fluxo de autenticação

Rode o comando:

```bash
make auth
```

- Um navegador será aberto para login e autorização.
- Após o sucesso, um novo `token.pickle` será criado.

---

## 4. Pronto

Sua autenticação foi renovada. Se encontrar erros, consulte a [documentação de troubleshooting](../troubleshooting.md) ou [guia de instalação](../setup/installation.md).

---

**Links úteis:**

- [Google Cloud Console - Credenciais](https://console.cloud.google.com/apis/credentials)
- [Guia de Instalação](../setup/installation.md)
- [Troubleshooting](../troubleshooting.md)
