# 🔧 Resolução de Problemas

Guia completo para identificar e resolver problemas comuns no projeto Biscoitão.

## Problemas Comuns

### 1. Erros de Permissão

#### Sintoma
```
Exception: Request failed for https://sheets.googleapis.com returned code 403
```

#### Causa
- APIs não habilitadas
- Permissões insuficientes
- Conta sem acesso aos recursos

#### Solução
1. Verificar APIs habilitadas no Google Cloud Console
2. Reautorizar o script
3. Verificar permissões da conta

```javascript
// Função para testar permissões
function testarPermissoes() {
  try {
    // Testar Google Sheets
    SpreadsheetApp.getActive();
    console.log('✅ Google Sheets: OK');
    
    // Testar Gmail
    GmailApp.getInboxThreads(0, 1);
    console.log('✅ Gmail: OK');
    
    // Testar Drive
    DriveApp.getRootFolder();
    console.log('✅ Google Drive: OK');
    
  } catch (error) {
    console.error('❌ Erro de permissão:', error.message);
    return false;
  }
  return true;
}
```

### 2. Timeout de Execução

#### Sintoma
```
Exception: Script function exceeded maximum execution time
```

#### Causa
- Processamento muito longo
- Loops infinitos
- Muitas requisições à API

#### Solução
1. **Otimizar código**:
```javascript
// ❌ Ineficiente
function processarDadosIneficiente() {
  const sheet = SpreadsheetApp.getActiveSheet();
  for (let i = 1; i <= 1000; i++) {
    sheet.getRange(i, 1).setValue(`Linha ${i}`); // Muitas chamadas
  }
}

// ✅ Eficiente
function processarDadosEficiente() {
  const dados = [];
  for (let i = 1; i <= 1000; i++) {
    dados.push([`Linha ${i}`]);
  }
  const sheet = SpreadsheetApp.getActiveSheet();
  sheet.getRange(1, 1, dados.length, 1).setValues(dados); // Uma chamada
}
```

2. **Dividir processamento**:
```javascript
function processarEmLotes() {
  const TAMANHO_LOTE = 100;
  const totalItens = obterTotalItens();
  
  for (let inicio = 0; inicio < totalItens; inicio += TAMANHO_LOTE) {
    const fim = Math.min(inicio + TAMANHO_LOTE, totalItens);
    processarLote(inicio, fim);
    
    // Pausa para evitar timeout
    if (fim < totalItens) {
      Utilities.sleep(1000);
    }
  }
}
```

### 3. Erros de Quota/Limite

#### Sintoma
```
Exception: Service invoked too many times in a short time
```

#### Causa
- Muitas requisições em pouco tempo
- Limites da API excedidos

#### Solução
```javascript
function executarComLimitacao(funcao, tentativas = 3) {
  for (let i = 0; i < tentativas; i++) {
    try {
      return funcao();
    } catch (error) {
      if (error.message.includes('too many times')) {
        const tempo = Math.pow(2, i) * 1000; // Backoff exponencial
        console.log(`Aguardando ${tempo}ms antes da tentativa ${i + 1}`);
        Utilities.sleep(tempo);
      } else {
        throw error;
      }
    }
  }
  throw new Error('Número máximo de tentativas excedido');
}
```

### 4. Problemas com Planilhas

#### Planilha não encontrada
```javascript
function verificarPlanilha(id) {
  try {
    const planilha = SpreadsheetApp.openById(id);
    return planilha;
  } catch (error) {
    console.error(`Planilha ${id} não encontrada:`, error.message);
    
    // Tentar encontrar por nome
    const arquivos = DriveApp.getFilesByName('Nome da Planilha');
    if (arquivos.hasNext()) {
      return SpreadsheetApp.open(arquivos.next());
    }
    
    throw new Error('Planilha não encontrada');
  }
}
```

#### Dados corrompidos
```javascript
function validarDados(dados) {
  const erros = [];
  
  dados.forEach((linha, indice) => {
    // Verificar campos obrigatórios
    if (!linha[0] || linha[0].toString().trim() === '') {
      erros.push(`Linha ${indice + 1}: Campo A é obrigatório`);
    }
    
    // Verificar formato de email
    if (linha[1] && !isValidEmail(linha[1])) {
      erros.push(`Linha ${indice + 1}: Email inválido`);
    }
    
    // Verificar formato de data
    if (linha[2] && !isValidDate(linha[2])) {
      erros.push(`Linha ${indice + 1}: Data inválida`);
    }
  });
  
  return erros;
}

function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function isValidDate(data) {
  return data instanceof Date && !isNaN(data);
}
```

### 5. Erros de Email

#### Email não enviado
```javascript
function enviarEmailSeguro(destinatario, assunto, corpo) {
  try {
    // Validar entrada
    if (!destinatario || !isValidEmail(destinatario)) {
      throw new Error('Email de destinatário inválido');
    }
    
    // Verificar limite diário
    const props = PropertiesService.getScriptProperties();
    const hoje = Utilities.formatDate(new Date(), 'GMT-3', 'yyyy-MM-dd');
    const chave = `emails_${hoje}`;
    const emailsEnviados = parseInt(props.getProperty(chave) || '0');
    
    if (emailsEnviados >= 100) {
      throw new Error('Limite diário de emails atingido');
    }
    
    // Enviar email
    GmailApp.sendEmail(destinatario, assunto, corpo);
    
    // Atualizar contador
    props.setProperty(chave, (emailsEnviados + 1).toString());
    
    console.log(`Email enviado para ${destinatario}`);
    return true;
    
  } catch (error) {
    console.error('Erro ao enviar email:', error.message);
    return false;
  }
}
```

## Diagnóstico do Sistema

### Função de Diagnóstico Completo
```javascript
function diagnosticoCompleto() {
  const relatorio = {
    timestamp: new Date(),
    permissoes: {},
    performance: {},
    configuracao: {},
    recursos: {}
  };
  
  // Testar permissões
  try {
    SpreadsheetApp.getActive();
    relatorio.permissoes.sheets = 'OK';
  } catch (e) {
    relatorio.permissoes.sheets = `ERRO: ${e.message}`;
  }
  
  try {
    GmailApp.getInboxThreads(0, 1);
    relatorio.permissoes.gmail = 'OK';
  } catch (e) {
    relatorio.permissoes.gmail = `ERRO: ${e.message}`;
  }
  
  try {
    DriveApp.getRootFolder();
    relatorio.permissoes.drive = 'OK';
  } catch (e) {
    relatorio.permissoes.drive = `ERRO: ${e.message}`;
  }
  
  // Testar performance
  const inicio = new Date();
  Utilities.sleep(100);
  relatorio.performance.tempoResposta = new Date() - inicio;
  
  // Verificar configuração
  const props = PropertiesService.getScriptProperties().getProperties();
  relatorio.configuracao.propriedadesDefinidas = Object.keys(props).length;
  relatorio.configuracao.triggersAtivos = ScriptApp.getProjectTriggers().length;
  
  // Verificar recursos
  try {
    relatorio.recursos.quotaEmails = verificarQuotaEmails();
    relatorio.recursos.espacoDrive = verificarEspacoDrive();
  } catch (e) {
    relatorio.recursos.erro = e.message;
  }
  
  return relatorio;
}

function verificarQuotaEmails() {
  const hoje = Utilities.formatDate(new Date(), 'GMT-3', 'yyyy-MM-dd');
  const props = PropertiesService.getScriptProperties();
  const emailsEnviados = parseInt(props.getProperty(`emails_${hoje}`) || '0');
  return {
    utilizados: emailsEnviados,
    limite: 100,
    percentual: (emailsEnviados / 100) * 100
  };
}

function verificarEspacoDrive() {
  // Verificação básica do Drive (limitada pela API)
  const pasta = DriveApp.getRootFolder();
  const arquivos = pasta.getFiles();
  let contador = 0;
  while (arquivos.hasNext() && contador < 10) {
    arquivos.next();
    contador++;
  }
  return {
    arquivosAcessiveis: contador,
    status: 'Conectado'
  };
}
```

## Logs e Monitoramento

### Sistema de Log Avançado
```javascript
const NIVEL_LOG = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3
};

function log(nivel, mensagem, dados = null) {
  const timestamp = new Date().toISOString();
  const nivelTexto = Object.keys(NIVEL_LOG)[nivel];
  
  const entrada = {
    timestamp,
    nivel: nivelTexto,
    mensagem,
    dados,
    funcao: obterNomeFuncao()
  };
  
  // Log no console
  console.log(`[${timestamp}] ${nivelTexto}: ${mensagem}`, dados || '');
  
  // Salvar em planilha de logs
  salvarLogPlanilha(entrada);
  
  // Enviar alertas críticos
  if (nivel === NIVEL_LOG.ERROR) {
    enviarAlertaCritico(entrada);
  }
}

function obterNomeFuncao() {
  try {
    throw new Error();
  } catch (e) {
    const stack = e.stack.split('\n');
    return stack[3] ? stack[3].trim().split(' ')[1] : 'desconhecida';
  }
}

function salvarLogPlanilha(entrada) {
  try {
    const planilhaId = PropertiesService.getScriptProperties().getProperty('PLANILHA_LOGS');
    if (!planilhaId) return;
    
    const planilha = SpreadsheetApp.openById(planilhaId);
    const aba = planilha.getSheetByName('Logs') || planilha.insertSheet('Logs');
    
    aba.appendRow([
      entrada.timestamp,
      entrada.nivel,
      entrada.funcao,
      entrada.mensagem,
      JSON.stringify(entrada.dados)
    ]);
  } catch (error) {
    console.error('Erro ao salvar log:', error);
  }
}

function enviarAlertaCritico(entrada) {
  const emailAdmin = PropertiesService.getScriptProperties().getProperty('EMAIL_ADMIN');
  if (!emailAdmin) return;
  
  const assunto = `🚨 ALERTA CRÍTICO - Biscoitão`;
  const corpo = `
    <h2>Erro Crítico Detectado</h2>
    <p><strong>Timestamp:</strong> ${entrada.timestamp}</p>
    <p><strong>Função:</strong> ${entrada.funcao}</p>
    <p><strong>Mensagem:</strong> ${entrada.mensagem}</p>
    <p><strong>Dados:</strong> ${JSON.stringify(entrada.dados, null, 2)}</p>
    
    <hr>
    <p>Verifique o sistema o mais rápido possível.</p>
  `;
  
  try {
    GmailApp.sendEmail(emailAdmin, assunto, '', { htmlBody: corpo });
  } catch (error) {
    console.error('Erro ao enviar alerta:', error);
  }
}
```

### Análise de Logs
```javascript
function analisarLogs(dias = 7) {
  const planilhaId = PropertiesService.getScriptProperties().getProperty('PLANILHA_LOGS');
  if (!planilhaId) {
    console.log('Planilha de logs não configurada');
    return;
  }
  
  const planilha = SpreadsheetApp.openById(planilhaId);
  const aba = planilha.getSheetByName('Logs');
  if (!aba) return;
  
  const dados = aba.getDataRange().getValues();
  const agora = new Date();
  const limiteTempo = new Date(agora.getTime() - (dias * 24 * 60 * 60 * 1000));
  
  const analise = {
    total: 0,
    por_nivel: { ERROR: 0, WARN: 0, INFO: 0, DEBUG: 0 },
    erros_frequentes: {},
    periodo: `${dias} dias`
  };
  
  dados.slice(1).forEach(linha => { // Pular cabeçalho
    const [timestamp, nivel, funcao, mensagem] = linha;
    const dataLog = new Date(timestamp);
    
    if (dataLog >= limiteTempo) {
      analise.total++;
      analise.por_nivel[nivel] = (analise.por_nivel[nivel] || 0) + 1;
      
      if (nivel === 'ERROR') {
        analise.erros_frequentes[mensagem] = (analise.erros_frequentes[mensagem] || 0) + 1;
      }
    }
  });
  
  console.log('📊 Análise de Logs:', analise);
  return analise;
}
```

## Recovery e Backup

### Recuperação Automática
```javascript
function tentarRecuperacao() {
  const problemas = [];
  
  // Verificar e recriar triggers se necessário
  if (ScriptApp.getProjectTriggers().length === 0) {
    try {
      configurarTriggers();
      problemas.push('Triggers recriados');
    } catch (e) {
      problemas.push(`Erro ao recriar triggers: ${e.message}`);
    }
  }
  
  // Verificar propriedades essenciais
  const props = PropertiesService.getScriptProperties();
  const propriedadesEssenciais = ['EMAIL_ADMIN', 'SPREADSHEET_PRINCIPAL'];
  
  propriedadesEssenciais.forEach(prop => {
    if (!props.getProperty(prop)) {
      problemas.push(`Propriedade ${prop} não configurada`);
    }
  });
  
  // Tentar restaurar configuração padrão
  if (problemas.length > 0) {
    try {
      restaurarConfiguracaoPadrao();
      problemas.push('Configuração padrão restaurada');
    } catch (e) {
      problemas.push(`Erro na restauração: ${e.message}`);
    }
  }
  
  return problemas;
}

function restaurarConfiguracaoPadrao() {
  const props = PropertiesService.getScriptProperties();
  
  // Configurações padrão mínimas
  const configPadrao = {
    'NIVEL_LOG': 'INFO',
    'MAX_TENTATIVAS': '3',
    'TIMEOUT_MS': '30000'
  };
  
  props.setProperties(configPadrao);
  log(NIVEL_LOG.INFO, 'Configuração padrão restaurada', configPadrao);
}
```

## Checklist de Troubleshooting

### Problemas de Execução
- [ ] Verificar permissões de API
- [ ] Confirmar IDs de recursos (planilhas, pastas)
- [ ] Validar triggers ativos
- [ ] Checar quotas e limites
- [ ] Analisar logs de erro recentes

### Problemas de Performance
- [ ] Revisar tempo de execução das funções
- [ ] Otimizar chamadas à API
- [ ] Implementar cache quando possível
- [ ] Dividir processamento em lotes
- [ ] Verificar uso de memória

### Problemas de Dados
- [ ] Validar formato dos dados de entrada
- [ ] Verificar integridade das planilhas
- [ ] Confirmar backup dos dados importantes
- [ ] Testar recuperação de dados
- [ ] Validar transformações de dados
