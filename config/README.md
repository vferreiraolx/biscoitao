# 📁 Configurações do Projeto

Esta pasta contém todos os arquivos de configuração, templates e constantes do projeto Biscoitão.

## Arquivos de Configuração

### [`constants.gs`](./constants.gs)
Constantes globais do projeto - IDs de recursos, configurações padrão, etc.

### [`templates.gs`](./templates.gs)
Templates para emails, relatórios e outros documentos.

### [`config-example.json`](./config-example.json)
Exemplo de configuração para orientar a configuração inicial.

### [`triggers-setup.gs`](./triggers-setup.gs)
Script para configuração automática de triggers.

## Como Usar

1. **Configuração Inicial**: Copie `config-example.json` e adapte para seu ambiente
2. **Constantes**: Edite `constants.gs` com seus IDs específicos
3. **Templates**: Personalize os templates em `templates.gs`
4. **Triggers**: Execute `triggers-setup.gs` para configurar automações

## Organização

- **Desenvolvimento**: Use configurações de teste
- **Produção**: Use configurações validadas
- **Backup**: Mantenha cópias das configurações importantes

## Segurança

⚠️ **Importante**: Nunca commite IDs reais ou informações sensíveis. Use variáveis de ambiente ou propriedades do script para dados sensíveis.
