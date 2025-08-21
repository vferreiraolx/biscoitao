# 📚 Documentação da API

Documentação completa das funções e métodos disponíveis no projeto Biscoitão.

## Funções Principais

### `funcaoPrincipal()`
Função principal que orquestra o fluxo de automação.

```javascript
/**
 * Função principal do sistema
 * @return {Object} Resultado da execução
 */
function funcaoPrincipal() {
  // Implementação
}
```

**Parâmetros**: Nenhum  
**Retorno**: `Object` - Status da execução  
**Exemplo de uso**:
```javascript
const resultado = funcaoPrincipal();
console.log(resultado);
```

---

## Funções Utilitárias

### `configurarSistema()`
Configura as propriedades iniciais do sistema.

```javascript
/**
 * Configura propriedades e dependências do sistema
 * @param {Object} config - Objeto de configuração
 * @param {string} config.ambiente - Ambiente de execução (dev/prod)
 * @return {boolean} True se configurado com sucesso
 */
function configurarSistema(config = {}) {
  // Implementação
}
```

### `logarExecucao()`
Registra logs de execução para monitoramento.

```javascript
/**
 * Registra log de execução
 * @param {string} nivel - Nível do log (INFO, WARN, ERROR)
 * @param {string} mensagem - Mensagem do log
 * @param {Object} dados - Dados adicionais (opcional)
 */
function logarExecucao(nivel, mensagem, dados = null) {
  // Implementação
}
```

---

## Funções de Integração

### Google Sheets

#### `lerPlanilha()`
```javascript
/**
 * Lê dados de uma planilha específica
 * @param {string} spreadsheetId - ID da planilha
 * @param {string} range - Range de células (ex: 'A1:Z100')
 * @return {Array<Array>} Dados da planilha
 */
function lerPlanilha(spreadsheetId, range) {
  // Implementação
}
```

#### `escreverPlanilha()`
```javascript
/**
 * Escreve dados em uma planilha
 * @param {string} spreadsheetId - ID da planilha
 * @param {string} range - Range de células
 * @param {Array<Array>} dados - Dados para escrever
 * @return {boolean} True se sucesso
 */
function escreverPlanilha(spreadsheetId, range, dados) {
  // Implementação
}
```

### Gmail

#### `enviarEmail()`
```javascript
/**
 * Envia email com template personalizado
 * @param {Object} emailConfig - Configuração do email
 * @param {string} emailConfig.destinatario - Email do destinatário
 * @param {string} emailConfig.assunto - Assunto do email
 * @param {string} emailConfig.corpo - Corpo do email (HTML)
 * @param {Array} emailConfig.anexos - Lista de anexos (opcional)
 * @return {boolean} True se enviado com sucesso
 */
function enviarEmail(emailConfig) {
  // Implementação
}
```

### Google Drive

#### `organizarArquivos()`
```javascript
/**
 * Organiza arquivos em pastas específicas
 * @param {string} pastaOrigemId - ID da pasta de origem
 * @param {Object} regrasOrganizacao - Regras de organização
 * @return {Object} Relatório da organização
 */
function organizarArquivos(pastaOrigemId, regrasOrganizacao) {
  // Implementação
}
```

---

## Constantes e Configurações

### Configurações Globais
```javascript
// Configurações do sistema
const CONFIG = {
  // IDs de recursos
  SPREADSHEET_PRINCIPAL: 'ID_PLANILHA_PRINCIPAL',
  PASTA_ENTRADA: 'ID_PASTA_ENTRADA',
  PASTA_SAIDA: 'ID_PASTA_SAIDA',
  
  // Configurações de email
  EMAIL_ADMIN: 'admin@exemplo.com',
  TEMPLATE_EMAIL: 'template_padrao',
  
  // Configurações de execução
  MAX_TENTATIVAS: 3,
  TIMEOUT_MS: 30000,
  
  // Configurações de log
  NIVEL_LOG: 'INFO',
  MANTER_LOGS_DIAS: 30
};
```

### Estados do Sistema
```javascript
const ESTADOS = {
  SUCESSO: 'SUCESSO',
  ERRO: 'ERRO',
  PROCESSANDO: 'PROCESSANDO',
  AGUARDANDO: 'AGUARDANDO'
};
```

---

## Tratamento de Erros

### Padrão de Error Handling
```javascript
function exemploComTratamentoErro() {
  try {
    // Lógica principal
    const resultado = operacaoRiscosa();
    logarExecucao('INFO', 'Operação concluída', resultado);
    return resultado;
  } catch (error) {
    logarExecucao('ERROR', 'Erro na operação', {
      erro: error.message,
      stack: error.stack
    });
    throw new Error(`Falha na operação: ${error.message}`);
  }
}
```

### Códigos de Erro Comuns
| Código | Descrição | Ação Recomendada |
|--------|-----------|------------------|
| `001` | Planilha não encontrada | Verificar ID da planilha |
| `002` | Permissão negada | Verificar permissões do usuário |
| `003` | Limite de API excedido | Aguardar reset do limite |
| `004` | Timeout de execução | Otimizar código ou dividir processamento |

---

## Exemplos de Uso

### Exemplo Completo
```javascript
function exemploUsoCompleto() {
  // 1. Configurar sistema
  const config = {
    ambiente: 'prod',
    notificarAdmin: true
  };
  
  if (!configurarSistema(config)) {
    throw new Error('Falha na configuração');
  }
  
  // 2. Executar função principal
  try {
    const resultado = funcaoPrincipal();
    
    // 3. Processar resultado
    if (resultado.status === ESTADOS.SUCESSO) {
      logarExecucao('INFO', 'Execução bem-sucedida', resultado);
      
      // 4. Enviar notificação
      enviarEmail({
        destinatario: CONFIG.EMAIL_ADMIN,
        assunto: 'Biscoitão - Execução Concluída',
        corpo: `<h2>Sucesso!</h2><p>Dados processados: ${resultado.totalProcessados}</p>`
      });
    }
  } catch (error) {
    logarExecucao('ERROR', 'Falha na execução', error);
    throw error;
  }
}
```

## Performance e Limites

### Otimizações Recomendadas
- Use `Utilities.sleep()` para evitar rate limits
- Processe dados em lotes para grandes volumes
- Cache resultados quando possível
- Use triggers para execuções longas

### Limites do Google Apps Script
- **Tempo de execução**: 6 minutos por execução
- **Triggers**: 20 triggers por script
- **Email**: 100 emails/dia (conta gratuita)
- **Requisições**: 20.000/dia por usuário
