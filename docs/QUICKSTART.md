# 🚀 Guia de Início Rápido - Biscoitão OLX

Guia para colocar o sistema em funcionamento rapidamente.

## ⚡ Setup Rápido (15 minutos)

### 1. **Configurar Google Apps Script** (5 min)

```bash
# 1. Acesse script.google.com
# 2. Novo Projeto → Renomeie para "Biscoitão OLX"
# 3. Cole o código de src/main.gs
# 4. Cole o código de config/constants.gs
# 5. Substitua appsscript.json pelo nosso
```

### 2. **Configurar IDs dos Recursos** (3 min)

Edite `config/constants.gs`:

```javascript
const RECURSOS_OLX = {
  // Substitua pelos IDs reais
  SPREADSHEET_DADOS_RECEITA: 'COLE_ID_DA_PLANILHA_PRINCIPAL_AQUI',
  SPREADSHEET_LOGS: 'COLE_ID_DA_PLANILHA_LOGS_AQUI',
  // ... outros IDs
};
```

### 3. **Configurar Propriedades do Script** (2 min)

No Apps Script, vá em **Projeto → Propriedades do Script** e adicione:

```
EMAIL_ADMIN = seu.email@grupoolx.com
TOQAN_API_TOKEN = seu_token_toqan_aqui
AMBIENTE = producao
```

### 4. **Teste Inicial** (3 min)

Execute no Apps Script:

```javascript
// 1. Teste de validação
function testeRapido() {
  const validacao = validarSistemaOLX();
  console.log('Validação:', validacao);
  
  // 2. Teste de detecção
  const abas = detectarAbasReceita();
  console.log('Abas detectadas:', abas.length);
}
```

### 5. **Primeira Consolidação** (2 min)

```javascript
// Execute a função principal
funcaoPrincipal();
```

---

## 📋 Checklist de Configuração

### Antes de Começar
- [ ] Planilha principal com dados de receita criada
- [ ] Planilha de logs criada (opcional, mas recomendado)
- [ ] Token da API Toqan obtido
- [ ] Permissões Google adequadas

### Configuração Básica
- [ ] Código copiado para Apps Script
- [ ] IDs das planilhas configurados
- [ ] Email do administrador definido
- [ ] Token Toqan configurado
- [ ] Teste de validação executado

### Configuração Avançada
- [ ] Triggers automáticos configurados
- [ ] Notificações por email testadas
- [ ] Sistema de logs validado
- [ ] Backup configurado

---

## 🔧 Configuração por Cenário

### **Cenário 1: Ambiente de Teste**

```javascript
// Configurações mínimas para teste
const config = {
  EMAIL_ADMIN: 'seu.email@grupoolx.com',
  SPREADSHEET_DADOS_RECEITA: 'id_planilha_teste',
  AMBIENTE: 'teste'
};
```

### **Cenário 2: Produção Simples**

```javascript
// Configuração para produção básica
const config = {
  EMAIL_ADMIN: 'admin@grupoolx.com',
  SPREADSHEET_DADOS_RECEITA: 'id_planilha_producao',
  SPREADSHEET_LOGS: 'id_planilha_logs',
  TOQAN_API_TOKEN: 'token_real',
  AMBIENTE: 'producao'
};
```

### **Cenário 3: Produção Completa**

```javascript
// Configuração completa com todas as funcionalidades
const config = {
  // Recursos principais
  SPREADSHEET_DADOS_RECEITA: 'id_planilha_producao',
  SPREADSHEET_LOGS: 'id_planilha_logs',
  PASTA_CONTEXTO_IA: 'id_pasta_contexto',
  PASTA_BACKUP: 'id_pasta_backup',
  
  // Notificações
  EMAIL_ADMIN: 'admin@grupoolx.com',
  SLACK_WEBHOOK: 'url_webhook_slack',
  
  // APIs
  TOQAN_API_TOKEN: 'token_real',
  
  // Sistema
  AMBIENTE: 'producao',
  NIVEL_LOG: 'INFO'
};
```

---

## 🚨 Troubleshooting Rápido

### Erro: "Planilha não encontrada"
```javascript
// Verifique o ID da planilha
function verificarPlanilha() {
  try {
    const planilha = SpreadsheetApp.openById('SEU_ID_AQUI');
    console.log('✅ Planilha encontrada:', planilha.getName());
  } catch (e) {
    console.log('❌ Erro:', e.message);
  }
}
```

### Erro: "Permissão negada"
```javascript
// Verifique permissões
function verificarPermissoes() {
  try {
    DriveApp.getRootFolder();
    console.log('✅ Google Drive: OK');
    
    GmailApp.getInboxThreads(0, 1);
    console.log('✅ Gmail: OK');
    
  } catch (e) {
    console.log('❌ Erro de permissão:', e.message);
  }
}
```

### Erro: "Token Toqan inválido"
```javascript
// Verifique configuração Toqan
function verificarToqan() {
  const token = PropertiesService.getScriptProperties().getProperty('TOQAN_API_TOKEN');
  
  if (!token) {
    console.log('❌ Token Toqan não configurado');
  } else {
    console.log('✅ Token configurado (primeiros 10 chars):', token.substring(0, 10) + '...');
  }
}
```

---

## 📊 Primeiros Dados

### Estrutura Esperada das Abas

Suas abas de dados devem ter:

```
| Data       | Produto    | Receita | Região    |
|------------|------------|---------|-----------|
| 2024-01-01 | Imóveis    | 100000  | São Paulo |
| 2024-01-01 | Autos      | 80000   | Rio       |
```

### Resultado da Consolidação

O sistema criará uma aba `Consolidado_Temporal`:

```
| mes_ano | data_atualizacao | rec_receita | rec_produto_imoveis | reg_sao_paulo |
|---------|------------------|-------------|---------------------|---------------|
| 2024-01 | 21/08/2025 10:30 | 180000      | 100000              | 100000        |
```

---

## 📞 Suporte

### Em caso de problemas:

1. **Verificar logs**: Execute `analisarLogs()` no Apps Script
2. **Validar sistema**: Execute `validarSistemaOLX()`
3. **Testar funções**: Use as funções de teste individuais
4. **Documentação**: Consulte [`docs/TROUBLESHOOTING.md`](./docs/TROUBLESHOOTING.md)

### Contatos de suporte:
- **Email**: admin@grupoolx.com
- **Documentação completa**: [`README.md`](../README.md)
- **API Reference**: [`docs/API-OLX.md`](./docs/API-OLX.md)
