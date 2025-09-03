/**
 * @OnlyCurrentDoc
 *
 * Biscoitão v2.0 - Sistema Integrado de Análise SIMPLIFICADO
 * Integra API Toqan sem dependência de servidor local
 */

/**
 * Função principal para ser usada na planilha. Ex: =perguntarToqan("evolução do preço de jan-24 a jan-25")
 * 
 * COMPORTAMENTO v2.0 SIMPLIFICADO:
 * - Consulta a API Toqan para obter dados
 * - Retorna resposta melhorada com formatação para Sheets
 * - Gera comando para executar análise local posteriormente
 *
 * @param {string} pergunta A pergunta a ser enviada.
 * @returns {string} Resposta da Toqan + comando para análise local.
 */
function perguntarToqan(pergunta) {
  console.log("🚀 Biscoitão v2.0 - Iniciando análise:", pergunta);
  
  try {
    const apiKey = PropertiesService.getScriptProperties().getProperty('TOQAN_API_KEY');
    if (!apiKey) return '❌ Chave não configurada — rode configurarChaveToqan("SUA_CHAVE") no editor';

    const base = 'https://api.coco.prod.toqan.ai/api';

    console.log("📡 Criando conversação na API Toqan...");

    // 1. Criar a conversa com o payload correto
    const createResp = UrlFetchApp.fetch(base + '/create_conversation', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'x-api-key': apiKey
      },
      payload: JSON.stringify({ user_message: pergunta }),
      muteHttpExceptions: true
    });

    const createCode = createResp.getResponseCode();
    const createBodyText = createResp.getContentText();

    if (createCode !== 200) {
      return `❌ Erro ao criar conversa Toqan (${createCode}): ${createBodyText}`;
    }

    const createBody = JSON.parse(createBodyText);
    const requestId = createBody.request_id;
    const conversationId = createBody.conversation_id;
    if (!requestId || !conversationId) return '❌ IDs não encontrados na resposta da criação de conversa';

    console.log("⏳ Aguardando resposta da Toqan...");

    // 2. Fazer polling em /get_answer usando GET com query parameters
    let toqanAnswer = null;
    for (let i = 0; i < 30; i++) { // Tenta por até 30 segundos
      Utilities.sleep(1000); // Espera 1 segundo entre as tentativas

      // Monta a URL com os parâmetros (padrão HTTP correto para GET)
      const getAnswerUrl = base + '/get_answer?conversation_id=' + 
        encodeURIComponent(conversationId) + '&request_id=' + 
        encodeURIComponent(requestId);

      const ansResp = UrlFetchApp.fetch(getAnswerUrl, {
        method: 'get',
        headers: {
          'x-api-key': apiKey
        },
        muteHttpExceptions: true
      });

      if (ansResp.getResponseCode() !== 200) {
        // Continua tentando se a resposta ainda não estiver pronta (ex: 404), mas falha em outros erros
        if (ansResp.getResponseCode() !== 404) {
          return `❌ Erro ao buscar resposta Toqan (${ansResp.getResponseCode()}): ${ansResp.getContentText()}`;
        }
        continue; // Pula para a próxima iteração
      }

      const ansBody = JSON.parse(ansResp.getContentText());
      const status = ansBody.status;
      const text = ansBody.answer;

      // Se a resposta estiver completa
      if ((status === 'completed' || status === 'finished') && text) {
        toqanAnswer = text;
        break;
      }
      
      // Se ainda estiver processando, continua o loop
      if (status === 'in_progress') {
        continue;
      }
    }

    if (!toqanAnswer) {
      return '❌ Timeout: A resposta da Toqan demorou muito para ser processada.';
    }

    console.log("✅ Resposta da Toqan obtida!");

    // 3. NOVO: Formatação melhorada para Sheets + comando local
    const timestamp = new Date().toLocaleString('pt-BR');
    
    // Escrever resultado na célula abaixo (se possível)
    try {
      const sheet = SpreadsheetApp.getActiveSheet();
      const cell = sheet.getActiveCell();
      
      const resultText = `📊 BISCOITÃO v2.0 - ANÁLISE COMPLETA\n\n` +
        `🔍 Consulta: ${pergunta}\n` +
        `⏰ Processado em: ${timestamp}\n` +
        `🆔 ID Conversação: ${conversationId}\n\n` +
        `📈 RESPOSTA TOQAN:\n${toqanAnswer}\n\n` +
        `🎨 PARA GERAR GRÁFICO E PDF:\n` +
        `Execute no terminal local:\n` +
        `python sheets_integrator.py "${pergunta}"\n\n` +
        `📄 Isso criará automaticamente:\n` +
        `• Gráfico viridis em PNG\n` +
        `• Relatório Markdown profissional\n` +
        `• PDF (se disponível)\n` +
        `• Insights automáticos\n\n` +
        `🔗 Arquivo será salvo como: relatorio_biscoitao_[timestamp]`;
      
      sheet.getRange(cell.getRow() + 1, cell.getColumn()).setValue(resultText);
    } catch (e) {
      // Ignora erros de permissão (quando chamado como função customizada)
    }
    
    // Retorna resposta formatada
    return formatarRespostaSimplificada(pergunta, toqanAnswer, conversationId, timestamp);

  } catch (error) {
    console.error("❌ Erro geral:", error);
    return '❌ ' + (error && error.message ? error.message : String(error));
  }
}

/**
 * Formata resposta simplificada para exibição no Sheets
 */
function formatarRespostaSimplificada(pergunta, toqanAnswer, conversationId, timestamp) {
  let response = `📊 BISCOITÃO v2.0 - ANÁLISE COMPLETA\n\n`;
  response += `🔍 Consulta: ${pergunta}\n`;
  response += `⏰ Processado: ${timestamp}\n`;
  response += `🆔 ID: ${conversationId}\n\n`;
  
  response += `📈 RESPOSTA TOQAN:\n`;
  
  // Limita a resposta da Toqan para não sobrecarregar o Sheets
  const limitedAnswer = toqanAnswer.length > 500 ? 
    toqanAnswer.substring(0, 500) + "..." : toqanAnswer;
  
  response += `${limitedAnswer}\n\n`;
  
  response += `🎨 GERAR GRÁFICO E PDF:\n`;
  response += `Execute: python sheets_integrator.py "${pergunta}"\n\n`;
  
  response += `📄 Arquivos que serão criados:\n`;
  response += `• 📊 Gráfico viridis PNG\n`;
  response += `• 📝 Relatório Markdown\n`;
  response += `• 📄 PDF profissional\n`;
  response += `• 💡 Insights automáticos`;
  
  return response;
}

/**
 * Função para gerar relatório local via comando
 * Execute esta função para gerar automaticamente o comando de terminal
 */
function gerarComandoLocal(pergunta) {
  const comando = `python sheets_integrator.py "${pergunta}"`;
  
  console.log("🎯 COMANDO PARA EXECUTAR NO TERMINAL:");
  console.log(comando);
  
  // Copia para clipboard se possível
  try {
    const sheet = SpreadsheetApp.getActiveSheet();
    const cell = sheet.getActiveCell();
    sheet.getRange(cell.getRow() + 1, cell.getColumn()).setValue(comando);
  } catch (e) {
    console.log("Execute manualmente:", comando);
  }
  
  return comando;
}

/**
 * Salva a chave da API Toqan nas propriedades do script para uso seguro.
 * @param {string} chave A sua chave de API da Toqan.
 */
function configurarChaveToqan(chave) {
  if (!chave || chave === "SUA_CHAVE") return 'Passe a chave como parâmetro: configurarChaveToqan("SUA_CHAVE")';
  PropertiesService.getScriptProperties().setProperty('TOQAN_API_KEY', chave);
  return '✅ Chave da API Toqan salva com sucesso!';
}

/**
 * Função de diagnóstico para testar a conexão com a Toqan.
 * Execute-a diretamente no editor do Apps Script.
 */
function testarToqanEditor() {
  const apiKey = PropertiesService.getScriptProperties().getProperty('TOQAN_API_KEY');
  Logger.log('TOQAN_API_KEY presente: %s', !!apiKey);
  if (!apiKey) {
    Logger.log('❌ Chave TOQAN_API_KEY ausente. Execute configurarChaveToqan("SUA_CHAVE") com sua chave.');
    return;
  }

  const base = 'https://api.coco.prod.toqan.ai/api';
  const testText = 'Confirme sua conexão retornando hello world, vinão';
  
  // Payload correto, conforme documentação e testes
  const payloadObj = {
    user_message: testText
  };

  const opts = {
    method: 'post',
    contentType: 'application/json',
    // Header correto, conforme documentação
    headers: {
      'x-api-key': apiKey
    },
    payload: JSON.stringify(payloadObj),
    muteHttpExceptions: true
  };

  Logger.log('--- INICIANDO TESTE DE CONEXÃO TOQAN ---');
  Logger.log('1. ENVIANDO REQUEST PARA /create_conversation...');
  Logger.log('   URL: %s', base + '/create_conversation');
  Logger.log('   HEADERS: %s', JSON.stringify(opts.headers));
  Logger.log('   PAYLOAD: %s', opts.payload);

  const resp = UrlFetchApp.fetch(base + '/create_conversation', opts);
  
  Logger.log('2. RESPOSTA RECEBIDA:');
  Logger.log('   Status: %s', resp.getResponseCode());
  Logger.log('   Body: %s', resp.getContentText());

  // Se a criação foi bem-sucedida, tenta buscar a resposta
  if (resp.getResponseCode() === 200) {
    const createBody = JSON.parse(resp.getContentText());
    const requestId = createBody.request_id;
    const conversationId = createBody.conversation_id;

    if (requestId && conversationId) {
      Logger.log('✅ Sucesso! Tentando buscar resposta com request_id: %s', requestId);
      Logger.log('3. AGUARDANDO 2 SEGUNDOS...');
      Utilities.sleep(2000); // Dando um tempo para o processamento

      const getAnswerPayload = {
        conversation_id: conversationId,
        request_id: requestId
      };

      Logger.log('4. BUSCANDO RESPOSTA DE /get_answer (via GET com Query Params)...');
      
      // Monta a URL com os parâmetros (igual ao código Don que funciona)
      const getAnswerUrl = base + '/get_answer?conversation_id=' + 
        encodeURIComponent(conversationId) + '&request_id=' + 
        encodeURIComponent(requestId);
      
      Logger.log('   URL: %s', getAnswerUrl);
      
      // Faz polling até obter a resposta final (como na função principal)
      for (let i = 0; i < 30; i++) {
        const ansResp = UrlFetchApp.fetch(getAnswerUrl, {
          method: 'get',
          headers: { 'x-api-key': apiKey },
          muteHttpExceptions: true
        });
        
        Logger.log('5. RESPOSTA DE /get_answer (tentativa %s):', i + 1);
        Logger.log('   Status: %s', ansResp.getResponseCode());
        Logger.log('   Body: %s', ansResp.getContentText());
        
        if (ansResp.getResponseCode() === 200) {
          const ansBody = JSON.parse(ansResp.getContentText());
          const status = ansBody.status;
          const text = ansBody.answer;
          
          // Se a resposta estiver completa, retorna o texto
          if ((status === 'completed' || status === 'finished') && text) {
            Logger.log('🎉 SUCESSO TOTAL! Resposta final recebida: %s', text);
            Logger.log('--- TESTE FINALIZADO COM SUCESSO ---');
            return;
          }
          
          if (status === 'in_progress') {
            Logger.log('   Aguardando... (status: in_progress)');
            Utilities.sleep(1000);
            continue;
          }
        }
        
        // Se chegou aqui e não foi sucesso nem in_progress, algo deu errado
        Logger.log('❌ Erro inesperado ou timeout.');
        break;
      }
      
      Logger.log('--- TESTE FINALIZADO (TIMEOUT OU ERRO) ---');
    } else {
      Logger.log('❌ Erro: conversation_id ou request_id não encontrado no corpo da resposta.');
    }
  } else {
    Logger.log('❌ Teste falhou na criação da conversa.');
  }
}

/**
 * Função auxiliar para teste simplificado
 */
function testarBiscoitao() {
  const resultado = perguntarToqan("Evolução do preço médio de jan-24 a jan-25");
  console.log("Resultado do teste:", resultado);
  return resultado;
}

/**
 * Função para gerar relatório completo via linha de comando
 * Retorna o comando exato para executar no terminal
 */
function obterComandoRelatorio(pergunta) {
  const comando = `python sheets_integrator.py "${pergunta || 'evolução do preço médio de jan-24 a jan-25'}"`;
  
  console.log("🔧 INSTRUÇÕES PARA GERAR RELATÓRIO COMPLETO:");
  console.log("1. Abra o terminal/PowerShell");
  console.log(`2. Navegue até: cd "g:\\Meu Drive\\__AUTOMACOES\\Biscoitão"`);
  console.log(`3. Execute: ${comando}`);
  console.log("4. Arquivos serão gerados automaticamente com timestamp");
  
  return comando;
}
