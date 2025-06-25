# Regras do Projeto Google Calendar MCP

## Metodologia de Desenvolvimento

### Test-Driven Development (TDD)
- **Seguir sempre o ciclo TDD**: escrever teste que falha → implementar funcionalidade → refatorar mantendo testes verdes
- Após qualquer mudança no código, executar toda a suíte de testes
- **Manter cobertura global de 100%** antes de fazer commits

## Organização de Arquivos e Diretórios

### Limite de Linhas por Arquivo
- **Todos os arquivos do projeto devem ter no máximo 100 linhas**
- Esta regra se aplica a todos os tipos de arquivo: código fonte, documentação, configuração, etc.
- Para arquivos de código, sempre executar testes após refatoração para garantir que a funcionalidade permanece intacta

### Limite de Itens por Pasta
- **Máximo de 10 itens por pasta** (arquivos + subdiretórios)
- Quando exceder, criar sub-pastas e ajustar imports adequadamente
- Manter estrutura lógica e organizada

### Processo de Refatoração
Quando um arquivo exceder 100 linhas, deve-se seguir este processo:

1. **Identificar pontos de divisão lógicos**
   - Separar por funcionalidades relacionadas
   - Manter coesão dentro de cada novo arquivo
   - Considerar dependências entre módulos

2. **Criar novos arquivos**
   - Nomear arquivos de forma clara e descritiva
   - Manter estrutura de diretórios organizada
   - Seguir convenções de nomenclatura do projeto

3. **Ajustar imports e referências**
   - Atualizar todos os imports nos arquivos afetados
   - Verificar e corrigir links de documentação
   - Testar se todas as dependências ainda funcionam

4. **Validar a refatoração**
   - Executar testes para garantir que nada quebrou
   - Verificar se a funcionalidade permanece intacta
   - Revisar se a organização ficou mais clara

### Arquivos Protegidos
**Nunca mover ou refatorar automaticamente estes arquivos:**
- `.cursor`, `.github`, `.venv`, `.coverage`, `.coveragerc`
- `.cursorrules`, `.gitignore`, `Makefile`
- `README.md`, `requirements.txt`, `TODO.md` (da pasta root)

## Documentação

### Arquivos Markdown
- **Após criar qualquer arquivo markdown**: executar `markdownlint --fix`
- **Incluir pelo menos 2 links** para documentos markdown relevantes em cada arquivo
- Manter documentação atualizada e interligada

### Gerenciamento de Tarefas
- **TODO.md**: manter apenas tarefas ativas que requerem ação
- **COMPLETED.md**: ao completar 100% uma tarefa, movê-la de TODO.md para COMPLETED.md
- Manter organização clara do progresso do projeto

## Qualidade e Testes

### Cobertura de Testes
- Manter **cobertura global de 100%** sempre
- Restaurar cobertura completa antes de qualquer commit
- Executar suíte completa de testes após mudanças

### Benefícios desta Organização
- Código mais legível e manutenível
- Facilita revisões de código
- Reduz complexidade de cada arquivo
- Melhora a organização do projeto
- Garante qualidade através de testes
