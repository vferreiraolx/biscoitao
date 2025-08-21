/**
 * 🔧 Constantes de Configuração do Biscoitão
 * 
 * Sistema de consolidação de dados de receita do Grupo OLX
 * para interface conversacional com IA Toqan.
 */

// ========================================
// � CONFIGURAÇÕES DE DADOS OLX
// ========================================

/**
 * IDs dos recursos Google Sheets
 */
const RECURSOS_OLX = {
  // Planilha principal com abas de dados
  SPREADSHEET_DADOS_RECEITA: 'SEU_ID_PLANILHA_DADOS_AQUI',
  
  // Aba consolidada (será criada automaticamente)
  ABA_CONSOLIDADA: 'Consolidado_Temporal',
  
  // Planilhas de apoio
  SPREADSHEET_LOGS: 'SEU_ID_PLANILHA_LOGS_AQUI',
  SPREADSHEET_CONFIG: 'SEU_ID_PLANILHA_CONFIG_AQUI',
  
  // Pastas para arquivos de contexto
  PASTA_CONTEXTO_IA: 'SEU_ID_PASTA_CONTEXTO_AQUI',
  PASTA_BACKUP: 'SEU_ID_PASTA_BACKUP_AQUI'
};

/**
 * Configurações da LLM Toqan
 */
const TOQAN_CONFIG = {
  API_TOKEN: 'SEU_TOKEN_TOQAN_AQUI',
  ENDPOINT_BASE: 'https://api.toqan.com/v1/',
  MODELO: 'toqan-revenue-assistant',
  MAX_CONTEXTO_TOKENS: 32000
};

/**
 * Estrutura da aba consolidada
 */
const ESTRUTURA_CONSOLIDADA = {
  COLUNAS_FIXAS: ['Mes_Ano', 'Data_Atualizacao'],
  PREFIXOS_METRICAS: {
    RECEITA: 'rec_',
    OPERACIONAL: 'op_',
    FINANCEIRO: 'fin_',
    REGIONAL: 'reg_',
    PRODUTO: 'prod_'
  }
};

/**
 * Configurações de Processamento de Dados
 */
const PROCESSAMENTO_CONFIG = {
  FREQUENCIA_ATUALIZACAO: 'DIARIA',
  HORARIO_EXECUCAO: 8, // 8h da manhã
  FORMATO_TEMPORAL: 'MENSAL',
  AUTO_DETECTAR_ABAS: true,
  VALIDACAO_AUTONOMA: true
};

/**
 * Configurações de Integração APIs
 */
const APIS_EXTERNAS = {
  CRM: {
    ATIVO: false,
    ENDPOINT: '',
    AUTH_TYPE: 'bearer'
  },
  ERP: {
    ATIVO: false,
    ENDPOINT: '',
    AUTH_TYPE: 'oauth2'
  },
  SISTEMAS_INFO: {
    ATIVO: false,
    ENDPOINTS: []
  }
};

/**
 * Configurações de Notificação
 */
const NOTIFICACAO_CONFIG = {
  SLACK_WEBHOOK: 'SEU_WEBHOOK_SLACK_AQUI',
  EMAIL_ADMIN: 'admin@grupoolx.com',
  NOTIFICAR_CONSOLIDACAO: true,
  NOTIFICAR_ERROS: true,
  NOTIFICAR_VALIDACAO: false
};

/**
 * Configurações de Execução
 */
const EXECUCAO_CONFIG = {
  MAX_TENTATIVAS: 3,
  TIMEOUT_MS: 30000,
  INTERVALO_RETRY_MS: 5000,
  TAMANHO_LOTE_PROCESSAMENTO: 100
};

// ========================================
// 📊 CONFIGURAÇÕES DE LOG
// ========================================

/**
 * Níveis de Log
 */
const NIVEL_LOG = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3
};

/**
 * Configurações de Logging
 */
const LOG_CONFIG = {
  NIVEL_ATUAL: NIVEL_LOG.INFO,
  MANTER_DIAS: 30,
  MAX_ENTRADAS_MEMORIA: 1000,
  SALVAR_EM_PLANILHA: true,
  ENVIAR_ALERTAS_CRITICOS: true
};

// ========================================
// 🤖 ESTADOS DO SISTEMA OLX
// ========================================

/**
 * Estados de processamento de dados
 */
const ESTADOS_PROCESSAMENTO = {
  AGUARDANDO: 'AGUARDANDO',
  CONSOLIDANDO: 'CONSOLIDANDO',
  VALIDANDO: 'VALIDANDO',
  CONCLUIDO: 'CONCLUIDO',
  ERRO: 'ERRO',
  INCONSISTENCIA: 'INCONSISTENCIA'
};

/**
 * Status de validação de dados
 */
const STATUS_VALIDACAO = {
  PENDENTE: 'PENDENTE',
  APROVADO: 'APROVADO',
  REJEITADO: 'REJEITADO',
  REQUER_ATENCAO: 'REQUER_ATENCAO'
};

/**
 * Tipos de dados de receita
 */
const TIPOS_DADOS_RECEITA = {
  POR_PRODUTO: 'produto',
  POR_REGIAO: 'regiao',
  POR_PERIODO: 'periodo',
  POR_CANAL: 'canal',
  POR_SEGMENTO: 'segmento',
  FINANCEIRO: 'financeiro',
  OPERACIONAL: 'operacional'
};

// ========================================
// 📋 CONFIGURAÇÕES DE DADOS
// ========================================

/**
 * Formato de colunas para planilhas
 */
const COLUNAS = {
  DADOS_PRINCIPAIS: {
    ID: 0,
    NOME: 1,
    EMAIL: 2,
    DATA_CRIACAO: 3,
    STATUS: 4,
    OBSERVACOES: 5
  },
  
  LOGS: {
    TIMESTAMP: 0,
    NIVEL: 1,
    FUNCAO: 2,
    MENSAGEM: 3,
    DADOS_EXTRA: 4
  }
};

/**
 * Ranges padrão das planilhas
 */
const RANGES = {
  DADOS_COMPLETOS: 'A:Z',
  CABECALHO: 'A1:Z1',
  PRIMEIRA_LINHA_DADOS: 'A2:Z2',
  COLUNA_STATUS: 'E:E'
};

// ========================================
// 🔧 CONFIGURAÇÕES TÉCNICAS
// ========================================

/**
 * Limites da API do Google Apps Script
 */
const LIMITES_API = {
  EMAILS_POR_DIA: 100,
  TEMPO_EXECUCAO_MAX_MS: 360000, // 6 minutos
  REQUISICOES_POR_SEGUNDO: 100,
  TAMANHO_MAX_ARQUIVO_MB: 50
};

/**
 * Configurações de Cache
 */
const CACHE_CONFIG = {
  TEMPO_EXPIRACAO_SEGUNDOS: 3600, // 1 hora
  PREFIXO_CHAVE: 'biscoitao_',
  USAR_CACHE: true
};

/**
 * Configurações de Backup
 */
const BACKUP_CONFIG = {
  FREQUENCIA_HORAS: 24,
  MANTER_BACKUPS_DIAS: 7,
  FORMATO_NOME: 'backup-YYYY-MM-DD-HH-mm',
  INCLUIR_CONFIGURACOES: true,
  INCLUIR_LOGS: false
};

// ========================================
// 🎨 CONFIGURAÇÕES DE FORMATAÇÃO
// ========================================

/**
 * Formatos de data
 */
const FORMATO_DATA = {
  PADRAO: 'dd/MM/yyyy',
  COM_HORA: 'dd/MM/yyyy HH:mm:ss',
  ISO: 'yyyy-MM-dd',
  ARQUIVO: 'yyyy-MM-dd_HH-mm-ss'
};

/**
 * Cores para status (formato hexadecimal)
 */
const CORES_STATUS = {
  SUCESSO: '#4CAF50',
  ERRO: '#F44336',
  AGUARDANDO: '#FF9800',
  PROCESSANDO: '#2196F3',
  CANCELADO: '#9E9E9E'
};

// ========================================
// 📧 TEMPLATES DE MENSAGEM
// ========================================

/**
 * Assuntos padrão para emails
 */
const ASSUNTOS_EMAIL = {
  SUCESSO: '✅ Biscoitão - Processamento Concluído',
  ERRO: '❌ Biscoitão - Erro no Processamento',
  ALERTA: '⚠️ Biscoitão - Alerta do Sistema',
  RELATORIO: '📊 Biscoitão - Relatório Diário'
};

// ========================================
// 🔒 VALIDAÇÕES
// ========================================

/**
 * Expressões regulares para validação
 */
const REGEX_VALIDACAO = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  TELEFONE: /^\(\d{2}\)\s\d{4,5}-\d{4}$/,
  CEP: /^\d{5}-?\d{3}$/,
  CPF: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/
};

/**
 * Mensagens de validação
 */
const MENSAGENS_VALIDACAO = {
  EMAIL_INVALIDO: 'Formato de email inválido',
  CAMPO_OBRIGATORIO: 'Este campo é obrigatório',
  VALOR_MUITO_LONGO: 'Valor excede o limite de caracteres',
  FORMATO_INVALIDO: 'Formato inválido para este campo'
};

// ========================================
// 🔄 CONFIGURAÇÕES DE RETRY
// ========================================

/**
 * Configurações para tentativas de retry
 */
const RETRY_CONFIG = {
  MAX_TENTATIVAS: 3,
  INTERVALO_BASE_MS: 1000,
  MULTIPLICADOR_BACKOFF: 2,
  JITTER_MAX_MS: 500
};

// ========================================
// 🎯 FUNÇÕES UTILITÁRIAS
// ========================================

/**
 * Obtém uma configuração por chave
 * @param {string} categoria - Categoria da configuração
 * @param {string} chave - Chave específica
 * @return {*} Valor da configuração
 */
function obterConfig(categoria, chave) {
  const configs = {
    'RECURSOS': RECURSOS,
    'EMAIL': EMAIL_CONFIG,
    'EXECUCAO': EXECUCAO_CONFIG,
    'LOG': LOG_CONFIG,
    'CACHE': CACHE_CONFIG
  };
  
  return configs[categoria] ? configs[categoria][chave] : null;
}

/**
 * Valida se todas as configurações obrigatórias estão definidas
 * @return {Object} Resultado da validação
 */
function validarConfiguracoes() {
  const obrigatorias = [
    'RECURSOS.SPREADSHEET_PRINCIPAL',
    'EMAIL_CONFIG.ADMIN'
  ];
  
  const faltando = [];
  
  obrigatorias.forEach(config => {
    const [categoria, chave] = config.split('.');
    if (!obterConfig(categoria, chave) || obterConfig(categoria, chave).includes('SEU_ID')) {
      faltando.push(config);
    }
  });
  
  return {
    valido: faltando.length === 0,
    faltando: faltando
  };
}
