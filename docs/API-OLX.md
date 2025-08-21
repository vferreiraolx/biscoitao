# 📚 Documentação da API - Biscoitão OLX

Documentação completa das funções do sistema de consolidação de dados de receita do Grupo OLX.

## Funções Principais

### `funcaoPrincipal()`

Função principal que executa a consolidação completa de dados OLX.

```javascript
/**
 * Consolida dados de receita em formato temporal para consumo via IA Toqan
 * @return {Object} Resultado da consolidação com métricas
 */
function funcaoPrincipal() {
  // Implementação
}
```

**Parâmetros**: Nenhum  
**Retorno**: `Object` - Relatório completo da consolidação  
**Frequência**: Diária (configurável)

**Exemplo de retorno**:
```javascript
{
  timestamp: Date,
  duracao: 45000, // milissegundos
  status: "CONCLUIDO",
  dados: {
    abas_processadas: 5,
    registros_consolidados: 24,
    validacao: { valido: true, erros: [], alertas: [] }
  },
  toqan: {
    contexto_preparado: true,
    pronto_para_consulta: true
  }
}
```

---

## Funções de Detecção e Validação

### `detectarAbasReceita()`

Detecta automaticamente abas com dados de receita na planilha principal.

```javascript
/**
 * Detecta automaticamente abas com dados de receita
 * @return {Array} Lista de abas detectadas com metadados
 */
function detectarAbasReceita() {
  // Implementação
}
```

**Critérios de Detecção**:
- Presença de palavras-chave: 'receita', 'revenue', 'faturamento', 'vendas'
- Mínimo 2 linhas (cabeçalho + dados)
- Exclusão de abas de sistema (prefixo `_` ou `Consolidado_`)

### `validarSistemaOLX()`

Valida configurações e acessos necessários para operação.

```javascript
/**
 * Valida sistema OLX antes da execução
 * @return {Object} Resultado da validação
 */
function validarSistemaOLX() {
  // Implementação
}
```

**Verificações**:
- Acesso à planilha de dados de receita
- Token da API Toqan configurado
- Permissões Google Drive
- APIs necessárias habilitadas

---

## Funções de Consolidação

### `consolidarDadosTemporais()`

Consolida dados de múltiplas abas em formato temporal mensal.

```javascript
/**
 * Consolida dados de múltiplas abas em formato temporal mensal
 * @param {Array} abasDetectadas - Lista de abas com dados
 * @return {Array} Dados consolidados por mês
 */
function consolidarDadosTemporais(abasDetectadas) {
  // Implementação
}
```

**Estrutura de Saída**:
- Uma linha por mês (formato YYYY-MM)
- Métricas prefixadas por tipo:
  - `rec_`: Dados de receita
  - `op_`: Dados operacionais  
  - `fin_`: Dados financeiros
  - `reg_`: Dados regionais
  - `prod_`: Dados por produto

### `extrairMesAno()`

Extrai informação temporal de registros para consolidação mensal.

```javascript
/**
 * Extrai mês/ano de um registro
 * @param {Object} registro - Registro de dados
 * @return {string} Formato YYYY-MM
 */
function extrairMesAno(registro) {
  // Implementação
}
```

**Campos Reconhecidos**: `data`, `mes`, `periodo`, `month`, `date`

---

## Funções de Integração Toqan

### `prepararContextoToqan()`

Prepara dados consolidados para consumo pela IA Toqan.

```javascript
/**
 * Prepara contexto consolidado para consumo da IA Toqan
 * @param {Array} dadosConsolidados - Dados consolidados
 */
function prepararContextoToqan(dadosConsolidados) {
  // Implementação
}
```

**Operações**:
- Cria/atualiza aba consolidada
- Aplica formatação padronizada
- Adiciona metadados para orientar a IA
- Prepara contexto para consultas conversacionais

### `formatarAbaConsolidada()`

Aplica formatação visual e funcional à aba consolidada.

```javascript
/**
 * Aplica formatação à aba consolidada
 * @param {Sheet} aba - Aba a ser formatada
 */
function formatarAbaConsolidada(aba) {
  // Implementação
}
```

**Formatações Aplicadas**:
- Cabeçalho em azul com texto branco
- Alternância de cores nas linhas
- Primeira linha congelada
- Alinhamento apropriado por tipo de dado

---

## Sistema de Logs e Monitoramento

### `logarExecucao()`

Sistema de logging integrado com contexto OLX.

```javascript
/**
 * Registra log de execução com contexto OLX
 * @param {string} nivel - Nível do log (INFO, WARN, ERROR, DEBUG)
 * @param {string} mensagem - Mensagem do log
 * @param {Object} dados - Dados adicionais (opcional)
 */
function logarExecucao(nivel, mensagem, dados = null) {
  // Implementação
}
```

**Níveis Suportados**:
- `ERROR`: Erros críticos (geram alertas)
- `WARN`: Avisos importantes
- `INFO`: Informações gerais
- `DEBUG`: Detalhes de depuração

**Saídas**:
- Console do Apps Script
- Planilha de logs (se configurada)
- Alertas por email (erros críticos)

---

## Funções de Notificação

### `notificarConsolidacao()`

Envia notificações sobre conclusão da consolidação.

```javascript
/**
 * Notifica conclusão da consolidação
 * @param {Object} relatorio - Relatório da consolidação
 */
function notificarConsolidacao(relatorio) {
  // Implementação
}
```

**Canais de Notificação**:
- Email para administrador
- Slack (implementação futura)

### `enviarEmailConsolidacao()`

Envia email detalhado sobre a consolidação.

```javascript
/**
 * Envia email de consolidação concluída
 * @param {string} email - Email destinatário
 * @param {Object} relatorio - Relatório da consolidação
 */
function enviarEmailConsolidacao(email, relatorio) {
  // Implementação
}
```

**Conteúdo do Email**:
- Resumo da execução (abas, registros, duração)
- Status da integração Toqan
- Resultados da validação
- Links para recursos relevantes

---

## Constantes e Configurações OLX

### Recursos Principais

```javascript
const RECURSOS_OLX = {
  SPREADSHEET_DADOS_RECEITA: 'ID_da_planilha_principal',
  ABA_CONSOLIDADA: 'Consolidado_Temporal',
  SPREADSHEET_LOGS: 'ID_planilha_logs',
  PASTA_CONTEXTO_IA: 'ID_pasta_contexto'
};
```

### Configuração Toqan

```javascript
const TOQAN_CONFIG = {
  API_TOKEN: 'token_da_api',
  ENDPOINT_BASE: 'https://api.toqan.com/v1/',
  MODELO: 'toqan-revenue-assistant',
  MAX_CONTEXTO_TOKENS: 32000
};
```

### Estados de Processamento

```javascript
const ESTADOS_PROCESSAMENTO = {
  AGUARDANDO: 'AGUARDANDO',
  CONSOLIDANDO: 'CONSOLIDANDO', 
  VALIDANDO: 'VALIDANDO',
  CONCLUIDO: 'CONCLUIDO',
  ERRO: 'ERRO',
  INCONSISTENCIA: 'INCONSISTENCIA'
};
```

---

## Triggers e Automação

### Trigger Principal

```javascript
// Execução diária às 8h
ScriptApp.newTrigger('funcaoPrincipal')
  .timeBased()
  .everyDays(1)
  .atHour(8)
  .create();
```

### Detecção de Mudanças

O sistema detecta automaticamente:
- Novas abas adicionadas
- Modificações em dados existentes
- Estruturas de dados alteradas

---

## Exemplo de Uso Completo

```javascript
// Execução manual completa
function exemploUsoCompleto() {
  try {
    // 1. Validar sistema
    const validacao = validarSistemaOLX();
    if (!validacao.valido) {
      throw new Error('Sistema não validado');
    }
    
    // 2. Executar consolidação
    const resultado = funcaoPrincipal();
    
    // 3. Verificar resultado
    if (resultado.status === 'CONCLUIDO') {
      console.log('✅ Consolidação concluída');
      console.log(`📊 ${resultado.dados.registros_consolidados} registros processados`);
      console.log(`🤖 Toqan: ${resultado.toqan.pronto_para_consulta ? 'Pronto' : 'Pendente'}`);
    }
    
  } catch (error) {
    console.error('❌ Erro:', error.message);
  }
}
```

---

## Performance e Limites

### Otimizações Implementadas

- Processamento em lotes para grandes volumes
- Cache de resultados de validação
- Detecção inteligente de mudanças
- Formatação eficiente de planilhas

### Limites Considerados

- **Planilhas**: Máximo 10 milhões de células por planilha
- **APIs**: Rate limits respeitados com backoff exponencial
- **Memória**: Processamento em chunks para datasets grandes
- **Tempo**: Execução otimizada para < 6 minutos (limite Apps Script)
