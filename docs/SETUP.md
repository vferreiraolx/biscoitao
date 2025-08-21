# 🔧 Configuração Detalhada

Este guia fornece instruções passo a passo para configurar o projeto Biscoitão.

## Pré-requisitos

### Conta Google
- Conta Google ativa
- Acesso ao Google Drive
- Permissões para criar projetos no Apps Script

### Ferramentas Opcionais
- **Google Apps Script CLI (clasp)**: Para desenvolvimento local
- **Git**: Para versionamento
- **Editor de código**: VS Code, Sublime Text, etc.

## Configuração Inicial

### 1. Configuração do Google Apps Script

#### Via Interface Web
1. Acesse [script.google.com](https://script.google.com)
2. Clique em "Novo projeto"
3. Renomeie para "Biscoitão"
4. Copie o conteúdo dos arquivos da pasta `src/`

#### Via CLI (clasp)
```bash
# Instalar clasp globalmente
npm install -g @google/clasp

# Fazer login
clasp login

# Criar projeto
clasp create --title "Biscoitão" --type standalone

# Fazer push do código
clasp push
```

### 2. Configuração de Permissões

#### APIs Necessárias
Habilite as seguintes APIs no [Google Cloud Console](https://console.cloud.google.com):

- [ ] Google Sheets API
- [ ] Google Drive API
- [ ] Gmail API (se aplicável)
- [ ] Google Calendar API (se aplicável)

#### Processo de Habilitação
1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Selecione o projeto do Apps Script
3. Vá para "APIs e Serviços" > "Biblioteca"
4. Procure e habilite cada API necessária

### 3. Configuração de Triggers

#### Triggers Automáticos
```javascript
// Exemplo de configuração de trigger
function configurarTriggers() {
  // Deletar triggers existentes
  ScriptApp.getProjectTriggers().forEach(trigger => {
    ScriptApp.deleteTrigger(trigger);
  });
  
  // Criar novo trigger
  ScriptApp.newTrigger('funcaoPrincipal')
    .timeBased()
    .everyHours(1)
    .create();
}
```

### 4. Variáveis de Ambiente

#### Usando PropertiesService
```javascript
// Configurar propriedades do script
function configurarPropriedades() {
  const props = PropertiesService.getScriptProperties();
  props.setProperties({
    'EMAIL_ADMIN': 'admin@exemplo.com',
    'SPREADSHEET_ID': 'ID_DA_PLANILHA',
    'FOLDER_ID': 'ID_DA_PASTA'
  });
}
```

### 5. Configuração de Desenvolvimento Local

#### Estrutura do clasp
```json
// .clasp.json
{
  "scriptId": "SEU_SCRIPT_ID",
  "rootDir": "./src"
}
```

#### Workflow de Desenvolvimento
```bash
# Baixar código do Apps Script
clasp pull

# Editar localmente
# ... fazer alterações ...

# Enviar para Apps Script
clasp push

# Abrir no navegador
clasp open
```

## Configurações Específicas

### Para Planilhas Google
```javascript
// Configurar acesso à planilha
const SPREADSHEET_ID = 'SEU_ID_AQUI';
const sheet = SpreadsheetApp.openById(SPREADSHEET_ID);
```

### Para Gmail
```javascript
// Configurar filtros de email
const emailConfig = {
  query: 'label:inbox is:unread',
  maxResults: 50
};
```

### Para Google Drive
```javascript
// Configurar pastas
const FOLDER_CONFIG = {
  input: 'ID_PASTA_ENTRADA',
  output: 'ID_PASTA_SAIDA',
  backup: 'ID_PASTA_BACKUP'
};
```

## Validação da Configuração

### Checklist de Verificação
- [ ] Projeto criado no Apps Script
- [ ] Código carregado corretamente
- [ ] APIs habilitadas
- [ ] Permissões concedidas
- [ ] Triggers configurados
- [ ] Propriedades definidas
- [ ] Teste inicial executado com sucesso

### Teste de Configuração
```javascript
function testeConfiguracao() {
  try {
    // Testar acesso às APIs
    console.log('Drive:', DriveApp.getRootFolder().getName());
    console.log('Sheets:', SpreadsheetApp.getActiveSpreadsheet() ? 'OK' : 'Não configurado');
    console.log('Gmail:', GmailApp.getInboxThreads(0, 1).length >= 0 ? 'OK' : 'Erro');
    
    return 'Configuração OK';
  } catch (error) {
    console.error('Erro na configuração:', error);
    return 'Erro: ' + error.message;
  }
}
```

## Próximos Passos

Após concluir a configuração:
1. Execute o teste de configuração
2. Consulte a [documentação da API](./API.md)
3. Revise os [workflows](./WORKFLOWS.md) disponíveis
4. Configure monitoramento e logs conforme necessário
