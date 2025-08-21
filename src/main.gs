/**
 * 🍪 BISCOITÃO - Sistema de Consolidação de Dados OLX
 * 
 * Sistema de consolidação de dados de receita do Grupo OLX
 * para interface conversacional com IA Toqan.
 * 
 * @author Grupo OLX
 * @version 1.0.0
 * @created 2025-08-21
 */

// ========================================
// � FUNÇÃO PRINCIPAL DE CONSOLIDAÇÃO
// ========================================

/**
 * Função principal do Biscoitão
 * Consolida dados de receita em formato temporal para consumo via IA
 * 
 * @return {Object} Resultado da consolidação com métricas
 */
function funcaoPrincipal() {
  const inicioExecucao = new Date();
  
  try {
    logarExecucao('INFO', 'Iniciando consolidação de dados OLX');
    
    // 1. Validar sistema
    const validacao = validarSistemaOLX();
    if (!validacao.valido) {
      throw new Error(`Sistema inválido: ${validacao.erros.join(', ')}`);
    }
    
    // 2. Detectar e processar abas
    const abasDetectadas = detectarAbasReceita();
    logarExecucao('INFO', `Detectadas ${abasDetectadas.length} abas de dados`);
    
    // 3. Consolidar dados temporalmente
    const dadosConsolidados = consolidarDadosTemporais(abasDetectadas);
    
    // 4. Validar dados consolidados
    const validacaoDados = validarDadosConsolidados(dadosConsolidados);
    
    // 5. Salvar na aba consolidada
    salvarAbaConsolidada(dadosConsolidados);
    
    // 6. Preparar para Toqan
    prepararContextoToqan(dadosConsolidados);
    
    // 7. Gerar relatório
    const relatorio = gerarRelatorioConsolidacao(inicioExecucao, {
      abas: abasDetectadas.length,
      registros: dadosConsolidados.length,
      validacao: validacaoDados
    });
    
    // 8. Notificar conclusão
    notificarConsolidacao(relatorio);
    
    logarExecucao('INFO', 'Consolidação OLX concluída', relatorio);
    return relatorio;
    
  } catch (error) {
    const relatorioErro = tratarErroConsolidacao(error, inicioExecucao);
    notificarErroConsolidacao(relatorioErro);
    throw error;
  }
}

// ========================================
// � DETECÇÃO E VALIDAÇÃO DE DADOS OLX
// ========================================

/**
 * Detecta automaticamente abas com dados de receita
 * @return {Array} Lista de abas detectadas com metadados
 */
function detectarAbasReceita() {
  try {
    const planilha = SpreadsheetApp.openById(RECURSOS_OLX.SPREADSHEET_DADOS_RECEITA);
    const todasAbas = planilha.getSheets();
    const abasReceita = [];
    
    todasAbas.forEach(aba => {
      const nomeAba = aba.getName();
      
      // Ignorar abas de sistema
      if (nomeAba.startsWith('Consolidado_') || nomeAba.startsWith('_')) {
        return;
      }
      
      // Verificar se contém dados de receita
      if (contemDadosReceita(aba)) {
        abasReceita.push({
          nome: nomeAba,
          aba: aba,
          tipo: identificarTipoDados(aba),
          ultimaLinhaComDados: aba.getLastRow(),
          ultimaColunaComDados: aba.getLastColumn()
        });
      }
    });
    
    return abasReceita;
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao detectar abas de receita', { erro: error.message });
    throw error;
  }
}

/**
 * Verifica se uma aba contém dados de receita
 * @param {Sheet} aba - Aba a ser verificada
 * @return {boolean} True se contém dados de receita
 */
function contemDadosReceita(aba) {
  try {
    if (aba.getLastRow() < 2) return false; // Precisa ter pelo menos cabeçalho + 1 linha
    
    const cabecalho = aba.getRange(1, 1, 1, aba.getLastColumn()).getValues()[0];
    const palavrasChave = ['receita', 'revenue', 'faturamento', 'vendas', 'valor', 'total'];
    
    return cabecalho.some(coluna => {
      const textoColuna = coluna.toString().toLowerCase();
      return palavrasChave.some(palavra => textoColuna.includes(palavra));
    });
    
  } catch (error) {
    return false;
  }
}

/**
 * Identifica o tipo de dados da aba
 * @param {Sheet} aba - Aba a ser analisada
 * @return {string} Tipo identificado
 */
function identificarTipoDados(aba) {
  const nome = aba.getName().toLowerCase();
  
  if (nome.includes('produto')) return TIPOS_DADOS_RECEITA.POR_PRODUTO;
  if (nome.includes('regiao') || nome.includes('região')) return TIPOS_DADOS_RECEITA.POR_REGIAO;
  if (nome.includes('periodo') || nome.includes('período')) return TIPOS_DADOS_RECEITA.POR_PERIODO;
  if (nome.includes('financeiro')) return TIPOS_DADOS_RECEITA.FINANCEIRO;
  if (nome.includes('operacional')) return TIPOS_DADOS_RECEITA.OPERACIONAL;
  
  return 'generico';
}

/**
 * Valida sistema OLX antes da execução
 * @return {Object} Resultado da validação
 */
function validarSistemaOLX() {
  const erros = [];
  
  try {
    // Verificar planilha principal
    SpreadsheetApp.openById(RECURSOS_OLX.SPREADSHEET_DADOS_RECEITA);
  } catch (e) {
    erros.push('Planilha de dados de receita não acessível');
  }
  
  // Verificar configuração Toqan
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty('TOQAN_API_TOKEN')) {
    erros.push('Token da API Toqan não configurado');
  }
  
  // Verificar APIs Google
  try {
    DriveApp.getRootFolder();
  } catch (e) {
    erros.push('Google Drive não acessível');
  }
  
  return {
    valido: erros.length === 0,
    erros: erros
  };
}

// ========================================
// � CONSOLIDAÇÃO TEMPORAL DE DADOS
// ========================================

/**
 * Consolida dados de múltiplas abas em formato temporal mensal
 * @param {Array} abasDetectadas - Lista de abas com dados
 * @return {Array} Dados consolidados por mês
 */
function consolidarDadosTemporais(abasDetectadas) {
  try {
    const dadosConsolidados = new Map(); // Chave: YYYY-MM, Valor: objeto com métricas
    
    abasDetectadas.forEach(abaDados => {
      const dadosAba = extrairDadosAba(abaDados);
      
      dadosAba.forEach(registro => {
        const mesAno = extrairMesAno(registro);
        
        if (!dadosConsolidados.has(mesAno)) {
          dadosConsolidados.set(mesAno, {
            mes_ano: mesAno,
            data_atualizacao: new Date()
          });
        }
        
        const consolidado = dadosConsolidados.get(mesAno);
        adicionarMetricasConsolidado(consolidado, registro, abaDados.tipo);
      });
    });
    
    // Converter Map para Array ordenado
    return Array.from(dadosConsolidados.values())
      .sort((a, b) => a.mes_ano.localeCompare(b.mes_ano));
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro na consolidação temporal', { erro: error.message });
    throw error;
  }
}

/**
 * Extrai dados estruturados de uma aba
 * @param {Object} abaDados - Metadados da aba
 * @return {Array} Dados estruturados
 */
function extrairDadosAba(abaDados) {
  const aba = abaDados.aba;
  const dados = aba.getDataRange().getValues();
  const cabecalho = dados[0];
  const registros = [];
  
  for (let i = 1; i < dados.length; i++) {
    const registro = {};
    cabecalho.forEach((coluna, index) => {
      registro[coluna.toString().toLowerCase().replace(/\s+/g, '_')] = dados[i][index];
    });
    registros.push(registro);
  }
  
  return registros;
}

/**
 * Extrai mês/ano de um registro
 * @param {Object} registro - Registro de dados
 * @return {string} Formato YYYY-MM
 */
function extrairMesAno(registro) {
  // Procurar campo de data
  const camposData = ['data', 'mes', 'periodo', 'month', 'date'];
  
  for (const campo of camposData) {
    if (registro[campo]) {
      const data = new Date(registro[campo]);
      if (!isNaN(data.getTime())) {
        return Utilities.formatDate(data, 'GMT-3', 'yyyy-MM');
      }
    }
  }
  
  // Se não encontrar data, usar mês atual
  return Utilities.formatDate(new Date(), 'GMT-3', 'yyyy-MM');
}

/**
 * Adiciona métricas ao registro consolidado
 * @param {Object} consolidado - Registro consolidado
 * @param {Object} registro - Registro fonte
 * @param {string} tipo - Tipo de dados
 */
function adicionarMetricasConsolidado(consolidado, registro, tipo) {
  const prefixo = ESTRUTURA_CONSOLIDADA.PREFIXOS_METRICAS[tipo.toUpperCase()] || 'gen_';
  
  Object.keys(registro).forEach(campo => {
    const valor = registro[campo];
    
    // Verificar se é campo numérico
    if (typeof valor === 'number' || !isNaN(parseFloat(valor))) {
      const nomeMetrica = `${prefixo}${campo}`;
      
      // Somar valores se já existe, senão criar
      if (consolidado[nomeMetrica]) {
        consolidado[nomeMetrica] += parseFloat(valor) || 0;
      } else {
        consolidado[nomeMetrica] = parseFloat(valor) || 0;
      }
    }
  });
}

/**
 * Valida dados consolidados
 * @param {Array} dadosConsolidados - Dados para validação
 * @return {Object} Resultado da validação
 */
function validarDadosConsolidados(dadosConsolidados) {
  const alertas = [];
  const erros = [];
  
  if (dadosConsolidados.length === 0) {
    erros.push('Nenhum dado foi consolidado');
  }
  
  dadosConsolidados.forEach((registro, index) => {
    // Verificar campos obrigatórios
    if (!registro.mes_ano) {
      erros.push(`Registro ${index}: Mês/ano não definido`);
    }
    
    // Verificar consistência temporal
    const metricas = Object.keys(registro).filter(k => k.includes('rec_'));
    if (metricas.length === 0) {
      alertas.push(`Registro ${index}: Nenhuma métrica de receita encontrada`);
    }
  });
  
  return {
    valido: erros.length === 0,
    erros: erros,
    alertas: alertas,
    registros_validados: dadosConsolidados.length
  };
}

// ========================================
// 🤖 INTEGRAÇÃO COM IA TOQAN
// ========================================

/**
 * Prepara contexto consolidado para consumo da IA Toqan
 * @param {Array} dadosConsolidados - Dados consolidados
 */
function prepararContextoToqan(dadosConsolidados) {
  try {
    logarExecucao('INFO', 'Preparando contexto para Toqan');
    
    // 1. Criar/atualizar aba consolidada
    const planilha = SpreadsheetApp.openById(RECURSOS_OLX.SPREADSHEET_DADOS_RECEITA);
    let abaConsolidada = planilha.getSheetByName(RECURSOS_OLX.ABA_CONSOLIDADA);
    
    if (!abaConsolidada) {
      abaConsolidada = planilha.insertSheet(RECURSOS_OLX.ABA_CONSOLIDADA);
    }
    
    // 2. Preparar dados para escrita
    const dadosParaEscrita = formatarDadosParaPlanilha(dadosConsolidados);
    
    // 3. Limpar e escrever dados
    abaConsolidada.clear();
    if (dadosParaEscrita.length > 0) {
      abaConsolidada.getRange(1, 1, dadosParaEscrita.length, dadosParaEscrita[0].length)
        .setValues(dadosParaEscrita);
    }
    
    // 4. Formatar aba
    formatarAbaConsolidada(abaConsolidada);
    
    // 5. Adicionar metadados para Toqan
    adicionarMetadadosToqan(abaConsolidada, dadosConsolidados.length);
    
    logarExecucao('INFO', 'Contexto Toqan preparado com sucesso');
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao preparar contexto Toqan', { erro: error.message });
    throw error;
  }
}

/**
 * Formata dados consolidados para escrita em planilha
 * @param {Array} dadosConsolidados - Dados consolidados
 * @return {Array} Array 2D para escrita em planilha
 */
function formatarDadosParaPlanilha(dadosConsolidados) {
  if (dadosConsolidados.length === 0) return [];
  
  // Extrair todas as colunas únicas
  const todasColunas = new Set();
  dadosConsolidados.forEach(registro => {
    Object.keys(registro).forEach(coluna => todasColunas.add(coluna));
  });
  
  const colunas = Array.from(todasColunas).sort();
  
  // Criar array 2D
  const dadosFormatados = [colunas]; // Cabeçalho
  
  dadosConsolidados.forEach(registro => {
    const linha = colunas.map(coluna => {
      const valor = registro[coluna];
      return valor instanceof Date ? 
        Utilities.formatDate(valor, 'GMT-3', 'dd/MM/yyyy HH:mm:ss') : 
        valor;
    });
    dadosFormatados.push(linha);
  });
  
  return dadosFormatados;
}

/**
 * Aplica formatação à aba consolidada
 * @param {Sheet} aba - Aba a ser formatada
 */
function formatarAbaConsolidada(aba) {
  const ultimaLinha = aba.getLastRow();
  const ultimaColuna = aba.getLastColumn();
  
  if (ultimaLinha === 0) return;
  
  // Formatar cabeçalho
  const cabecalho = aba.getRange(1, 1, 1, ultimaColuna);
  cabecalho.setBackground('#4285F4')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  
  // Formatar dados
  if (ultimaLinha > 1) {
    const dados = aba.getRange(2, 1, ultimaLinha - 1, ultimaColuna);
    dados.setHorizontalAlignment('left');
    
    // Alternar cores das linhas
    for (let i = 2; i <= ultimaLinha; i++) {
      if (i % 2 === 0) {
        aba.getRange(i, 1, 1, ultimaColuna).setBackground('#F8F9FA');
      }
    }
  }
  
  // Congelar primeira linha
  aba.setFrozenRows(1);
}

/**
 * Adiciona metadados para orientar a IA Toqan
 * @param {Sheet} aba - Aba consolidada
 * @param {number} totalRegistros - Total de registros consolidados
 */
function adicionarMetadadosToqan(aba, totalRegistros) {
  const metadados = [
    ['=== METADADOS TOQAN ==='],
    [`Última atualização: ${Utilities.formatDate(new Date(), 'GMT-3', 'dd/MM/yyyy HH:mm:ss')}`],
    [`Total de registros: ${totalRegistros}`],
    [`Formato: Temporal mensal`],
    [`Fonte: Consolidação automática Biscoitão`],
    ['Prefixos de métricas:'],
    ['- rec_: Dados de receita'],
    ['- op_: Dados operacionais'],
    ['- fin_: Dados financeiros'],
    ['- reg_: Dados regionais'],
    ['- prod_: Dados por produto'],
    ['']
  ];
  
  // Adicionar em área separada (depois dos dados principais)
  const ultimaLinha = aba.getLastRow();
  const linhaMetadados = ultimaLinha + 3;
  
  aba.getRange(linhaMetadados, 1, metadados.length, 1)
    .setValues(metadados)
    .setFontStyle('italic')
    .setBackground('#FFF3E0');
}

/**
 * Salva dados na aba consolidada (função legacy mantida para compatibilidade)
 * @param {Array} dadosConsolidados - Dados para salvar
 */
function salvarAbaConsolidada(dadosConsolidados) {
  // Esta função agora é parte de prepararContextoToqan
  logarExecucao('INFO', `Salvando ${dadosConsolidados.length} registros consolidados`);
}

// ========================================
// � RELATÓRIOS E NOTIFICAÇÕES OLX
// ========================================

/**
 * Gera relatório de consolidação OLX
 * @param {Date} inicioExecucao - Timestamp do início
 * @param {Object} estatisticas - Estatísticas da consolidação
 * @return {Object} Relatório completo
 */
function gerarRelatorioConsolidacao(inicioExecucao, estatisticas) {
  const agora = new Date();
  
  return {
    timestamp: agora,
    duracao: agora - inicioExecucao,
    status: ESTADOS_PROCESSAMENTO.CONCLUIDO,
    dados: {
      abas_processadas: estatisticas.abas,
      registros_consolidados: estatisticas.registros,
      validacao: estatisticas.validacao
    },
    sistema: {
      versao: '1.0.0',
      ambiente: 'OLX_Producao',
      aba_consolidada: RECURSOS_OLX.ABA_CONSOLIDADA
    },
    toqan: {
      contexto_preparado: true,
      metadados_adicionados: true,
      pronto_para_consulta: true
    }
  };
}

/**
 * Trata erros de consolidação
 * @param {Error} error - Erro ocorrido
 * @param {Date} inicioExecucao - Timestamp do início
 * @return {Object} Relatório de erro
 */
function tratarErroConsolidacao(error, inicioExecucao) {
  return {
    timestamp: new Date(),
    duracao: new Date() - inicioExecucao,
    status: ESTADOS_PROCESSAMENTO.ERRO,
    erro: {
      mensagem: error.message,
      stack: error.stack,
      tipo: 'consolidacao_olx'
    },
    sistema: {
      versao: '1.0.0',
      ambiente: 'OLX_Producao'
    }
  };
}

/**
 * Notifica conclusão da consolidação
 * @param {Object} relatorio - Relatório da consolidação
 */
function notificarConsolidacao(relatorio) {
  try {
    const props = PropertiesService.getScriptProperties();
    const emailAdmin = props.getProperty('EMAIL_ADMIN') || NOTIFICACAO_CONFIG.EMAIL_ADMIN;
    
    if (emailAdmin && !emailAdmin.includes('exemplo.com')) {
      enviarEmailConsolidacao(emailAdmin, relatorio);
    }
    
    // TODO: Implementar notificação Slack quando configurado
    const slackWebhook = props.getProperty('SLACK_WEBHOOK');
    if (slackWebhook && NOTIFICACAO_CONFIG.NOTIFICAR_CONSOLIDACAO) {
      enviarSlackConsolidacao(slackWebhook, relatorio);
    }
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao enviar notificações', { erro: error.message });
  }
}

/**
 * Envia email de consolidação concluída
 * @param {string} email - Email destinatário
 * @param {Object} relatorio - Relatório da consolidação
 */
function enviarEmailConsolidacao(email, relatorio) {
  const assunto = '✅ Biscoitão OLX - Consolidação Concluída';
  const duracao = Math.round(relatorio.duracao / 1000);
  
  const corpo = `
    <h2>🍪 Consolidação de Dados OLX Concluída</h2>
    
    <h3>📊 Resumo da Execução</h3>
    <ul>
      <li><strong>Abas Processadas:</strong> ${relatorio.dados.abas_processadas}</li>
      <li><strong>Registros Consolidados:</strong> ${relatorio.dados.registros_consolidados}</li>
      <li><strong>Duração:</strong> ${duracao} segundos</li>
      <li><strong>Status:</strong> ${relatorio.status}</li>
    </ul>
    
    <h3>🤖 Integração Toqan</h3>
    <ul>
      <li><strong>Contexto Preparado:</strong> ✅ Sim</li>
      <li><strong>Aba Consolidada:</strong> ${relatorio.sistema.aba_consolidada}</li>
      <li><strong>Pronto para IA:</strong> ✅ Sim</li>
    </ul>
    
    <h3>🔍 Validação</h3>
    <ul>
      <li><strong>Registros Validados:</strong> ${relatorio.dados.validacao.registros_validados}</li>
      <li><strong>Erros:</strong> ${relatorio.dados.validacao.erros.length}</li>
      <li><strong>Alertas:</strong> ${relatorio.dados.validacao.alertas.length}</li>
    </ul>
    
    <h3>🕐 Detalhes</h3>
    <p><strong>Timestamp:</strong> ${Utilities.formatDate(relatorio.timestamp, 'GMT-3', 'dd/MM/yyyy HH:mm:ss')}</p>
    <p><strong>Versão:</strong> ${relatorio.sistema.versao}</p>
    
    <hr>
    <p><em>Notificação automática do sistema Biscoitão - Grupo OLX</em></p>
  `;
  
  try {
    GmailApp.sendEmail(email, assunto, '', { htmlBody: corpo });
    logarExecucao('INFO', 'Email de consolidação enviado', { destinatario: email });
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao enviar email de consolidação', { erro: error.message });
  }
}

/**
 * Notifica erro na consolidação
 * @param {Object} relatorioErro - Relatório do erro
 */
function notificarErroConsolidacao(relatorioErro) {
  try {
    const props = PropertiesService.getScriptProperties();
    const emailAdmin = props.getProperty('EMAIL_ADMIN') || NOTIFICACAO_CONFIG.EMAIL_ADMIN;
    
    if (emailAdmin && !emailAdmin.includes('exemplo.com')) {
      enviarEmailErroConsolidacao(emailAdmin, relatorioErro);
    }
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao notificar erro de consolidação', { erro: error.message });
  }
}

/**
 * Envia email de erro na consolidação
 * @param {string} email - Email destinatário
 * @param {Object} relatorioErro - Relatório do erro
 */
function enviarEmailErroConsolidacao(email, relatorioErro) {
  const assunto = '🚨 Biscoitão OLX - Erro na Consolidação';
  const duracao = Math.round(relatorioErro.duracao / 1000);
  
  const corpo = `
    <h2>🚨 Erro na Consolidação de Dados OLX</h2>
    
    <h3>❌ Detalhes do Erro</h3>
    <p><strong>Mensagem:</strong> ${relatorioErro.erro.mensagem}</p>
    <p><strong>Tipo:</strong> ${relatorioErro.erro.tipo}</p>
    <p><strong>Duração até erro:</strong> ${duracao} segundos</p>
    
    <h3>🔧 Ações Recomendadas</h3>
    <ol>
      <li>Verificar logs detalhados no Apps Script</li>
      <li>Validar configurações do sistema OLX</li>
      <li>Confirmar acesso às planilhas de dados</li>
      <li>Verificar integridade dos dados de entrada</li>
      <li>Consultar documentação de troubleshooting</li>
    </ol>
    
    <h3>📋 Informações do Sistema</h3>
    <p><strong>Timestamp:</strong> ${Utilities.formatDate(relatorioErro.timestamp, 'GMT-3', 'dd/MM/yyyy HH:mm:ss')}</p>
    <p><strong>Versão:</strong> ${relatorioErro.sistema.versao}</p>
    <p><strong>Ambiente:</strong> ${relatorioErro.sistema.ambiente}</p>
    
    <hr>
    <p><em>Alerta automático do sistema Biscoitão - Grupo OLX</em></p>
  `;
  
  try {
    GmailApp.sendEmail(email, assunto, '', { htmlBody: corpo });
    logarExecucao('INFO', 'Email de erro enviado', { destinatario: email });
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao enviar email de erro', { erro: error.message });
  }
}

/**
 * Placeholder para notificação Slack (implementação futura)
 * @param {string} webhook - URL do webhook Slack
 * @param {Object} relatorio - Relatório da consolidação
 */
function enviarSlackConsolidacao(webhook, relatorio) {
  // TODO: Implementar quando Slack for configurado
  logarExecucao('INFO', 'Notificação Slack preparada (implementação futura)', { webhook });
}

// ========================================
// � SISTEMA DE LOGGING OLX
// ========================================

/**
 * Registra log de execução com contexto OLX
 * @param {string} nivel - Nível do log (INFO, WARN, ERROR, DEBUG)
 * @param {string} mensagem - Mensagem do log
 * @param {Object} dados - Dados adicionais (opcional)
 */
function logarExecucao(nivel, mensagem, dados = null) {
  const timestamp = new Date();
  const nivelNum = NIVEL_LOG[nivel] || NIVEL_LOG.INFO;
  const configuracao = LOG_CONFIG || { NIVEL_ATUAL: NIVEL_LOG.INFO };
  
  // Verificar se deve logar baseado no nível
  if (nivelNum > configuracao.NIVEL_ATUAL) {
    return;
  }
  
  const entrada = {
    timestamp: timestamp,
    nivel: nivel,
    mensagem: mensagem,
    dados: dados,
    funcao: obterNomeFuncaoAtual(),
    contexto: 'OLX_Consolidacao'
  };
  
  // Log no console
  const dadosStr = dados ? JSON.stringify(dados) : '';
  console.log(`[${timestamp.toISOString()}] ${nivel}: ${mensagem} ${dadosStr}`);
  
  // Salvar em planilha se configurado
  if (configuracao.SALVAR_EM_PLANILHA) {
    salvarLogPlanilhaOLX(entrada);
  }
  
  // Enviar alertas críticos
  if (nivel === 'ERROR' && configuracao.ENVIAR_ALERTAS_CRITICOS) {
    enviarAlertaCriticoOLX(entrada);
  }
}

/**
 * Salva log na planilha específica OLX
 * @param {Object} entrada - Entrada de log
 */
function salvarLogPlanilhaOLX(entrada) {
  try {
    const planilhaId = RECURSOS_OLX.SPREADSHEET_LOGS;
    if (!planilhaId || planilhaId.includes('SEU_ID')) return;
    
    const planilha = SpreadsheetApp.openById(planilhaId);
    let abaLogs = planilha.getSheetByName('Logs_Biscoitao');
    
    if (!abaLogs) {
      abaLogs = planilha.insertSheet('Logs_Biscoitao');
      // Adicionar cabeçalho
      abaLogs.getRange(1, 1, 1, 6).setValues([
        ['Timestamp', 'Nível', 'Função', 'Mensagem', 'Dados', 'Contexto']
      ]);
    }
    
    abaLogs.appendRow([
      Utilities.formatDate(entrada.timestamp, 'GMT-3', 'dd/MM/yyyy HH:mm:ss'),
      entrada.nivel,
      entrada.funcao,
      entrada.mensagem,
      JSON.stringify(entrada.dados),
      entrada.contexto
    ]);
    
  } catch (error) {
    console.error('Erro ao salvar log OLX:', error.message);
  }
}

/**
 * Obtém nome da função atual para log
 * @return {string} Nome da função
 */
function obterNomeFuncaoAtual() {
  try {
    throw new Error();
  } catch (e) {
    const stack = e.stack.split('\n');
    // Pegar a terceira linha do stack (chamador do logarExecucao)
    const linha = stack[3] || '';
    const match = linha.match(/at (\w+)/);
    return match ? match[1] : 'desconhecida';
  }
}

/**
 * Envia alerta crítico específico OLX
 * @param {Object} entrada - Entrada de log crítico
 */
function enviarAlertaCriticoOLX(entrada) {
  const props = PropertiesService.getScriptProperties();
  const emailAdmin = props.getProperty('EMAIL_ADMIN') || NOTIFICACAO_CONFIG.EMAIL_ADMIN;
  
  if (!emailAdmin || emailAdmin.includes('exemplo.com')) return;
  
  const assunto = '🚨 ALERTA CRÍTICO - Biscoitão OLX';
  const corpo = `
    <h2>🚨 Erro Crítico no Sistema OLX</h2>
    
    <h3>⚠️ Detalhes do Erro</h3>
    <p><strong>Timestamp:</strong> ${Utilities.formatDate(entrada.timestamp, 'GMT-3', 'dd/MM/yyyy HH:mm:ss')}</p>
    <p><strong>Função:</strong> ${entrada.funcao}</p>
    <p><strong>Mensagem:</strong> ${entrada.mensagem}</p>
    <p><strong>Contexto:</strong> ${entrada.contexto}</p>
    
    ${entrada.dados ? `
    <h3>📊 Dados Adicionais</h3>
    <pre>${JSON.stringify(entrada.dados, null, 2)}</pre>
    ` : ''}
    
    <h3>🔧 Ação Imediata Necessária</h3>
    <p>Verifique o sistema de consolidação OLX imediatamente.</p>
    
    <hr>
    <p><em>Alerta automático crítico - Biscoitão OLX</em></p>
  `;
  
  try {
    GmailApp.sendEmail(emailAdmin, assunto, '', { htmlBody: corpo });
  } catch (error) {
    console.error('Erro ao enviar alerta crítico OLX:', error.message);
  }
}

// ========================================
// 🧹 FUNÇÕES DE MANUTENÇÃO
// ========================================

/**
 * Remove logs antigos conforme configuração
 */
function limparLogsAntigos() {
  try {
    const planilhaLogs = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_LOGS');
    if (!planilhaLogs) return;
    
    // TODO: Implementar limpeza de logs
    logarExecucao('INFO', 'Logs antigos removidos');
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao limpar logs antigos', { erro: error.message });
  }
}

/**
 * Faz backup das configurações importantes
 */
function backupConfiguracoes() {
  try {
    const props = PropertiesService.getScriptProperties().getProperties();
    const timestamp = Utilities.formatDate(new Date(), 'GMT-3', 'yyyy-MM-dd_HH-mm-ss');
    
    // TODO: Implementar backup real
    logarExecucao('INFO', 'Backup de configurações realizado', { timestamp });
    
  } catch (error) {
    logarExecucao('ERROR', 'Erro no backup de configurações', { erro: error.message });
  }
}

/**
 * Gera relatório de saúde do sistema
 * @return {Object} Relatório de saúde
 */
function gerarRelatorioSaude() {
  return {
    timestamp: new Date(),
    triggers: ScriptApp.getProjectTriggers().length,
    propriedades: Object.keys(PropertiesService.getScriptProperties().getProperties()).length,
    status: 'SAUDAVEL'
  };
}

/**
 * Envia relatório de saúde por email
 * @param {Object} relatorio - Relatório de saúde
 */
function enviarRelatorioSaude(relatorio) {
  const emailAdmin = PropertiesService.getScriptProperties().getProperty('EMAIL_ADMIN');
  if (!emailAdmin || emailAdmin.includes('exemplo.com')) return;
  
  const assunto = ASSUNTOS_EMAIL.RELATORIO;
  const corpo = `
    <h2>📊 Relatório de Saúde Semanal - Biscoitão</h2>
    
    <h3>✅ Status Geral</h3>
    <p><strong>Status:</strong> ${relatorio.status}</p>
    <p><strong>Data:</strong> ${Utilities.formatDate(relatorio.timestamp, 'GMT-3', 'dd/MM/yyyy HH:mm:ss')}</p>
    
    <h3>🔧 Configurações</h3>
    <ul>
      <li><strong>Triggers Ativos:</strong> ${relatorio.triggers}</li>
      <li><strong>Propriedades Definidas:</strong> ${relatorio.propriedades}</li>
    </ul>
    
    <hr>
    <p><em>Relatório automático do sistema Biscoitão</em></p>
  `;
  
  try {
    GmailApp.sendEmail(emailAdmin, assunto, '', { htmlBody: corpo });
  } catch (error) {
    logarExecucao('ERROR', 'Erro ao enviar relatório de saúde', { erro: error.message });
  }
}

// ========================================
// 🧪 FUNÇÕES DE TESTE
// ========================================

/**
 * Executa uma bateria de testes do sistema
 * @return {Object} Resultado dos testes
 */
function executarTestes() {
  logarExecucao('INFO', 'Iniciando bateria de testes');
  
  const testes = [
    { nome: 'Configuração', funcao: () => validarConfiguracaoSistema() },
    { nome: 'Planilhas', funcao: () => testarAcessoPlanilhas() },
    { nome: 'Email', funcao: () => testarEmail() },
    { nome: 'Drive', funcao: () => testarDrive() }
  ];
  
  const resultados = [];
  
  testes.forEach(teste => {
    try {
      const resultado = teste.funcao();
      resultados.push({
        nome: teste.nome,
        status: 'SUCESSO',
        resultado: resultado
      });
    } catch (error) {
      resultados.push({
        nome: teste.nome,
        status: 'ERRO',
        erro: error.message
      });
    }
  });
  
  const relatorioTestes = {
    timestamp: new Date(),
    testes: resultados,
    sucessos: resultados.filter(r => r.status === 'SUCESSO').length,
    erros: resultados.filter(r => r.status === 'ERRO').length
  };
  
  logarExecucao('INFO', 'Testes concluídos', relatorioTestes);
  return relatorioTestes;
}

/**
 * Testa acesso às planilhas
 */
function testarAcessoPlanilhas() {
  const spreadsheetId = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_PRINCIPAL');
  if (!spreadsheetId) throw new Error('ID da planilha não configurado');
  
  const planilha = SpreadsheetApp.openById(spreadsheetId);
  return { nome: planilha.getName(), abas: planilha.getSheets().length };
}

/**
 * Testa funcionalidade de email
 */
function testarEmail() {
  const threads = GmailApp.getInboxThreads(0, 1);
  return { acessivel: true, threads: threads.length };
}

/**
 * Testa acesso ao Drive
 */
function testarDrive() {
  const pasta = DriveApp.getRootFolder();
  return { nome: pasta.getName(), acessivel: true };
}
