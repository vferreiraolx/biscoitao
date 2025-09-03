"""
Integrador Biscoitão - Google Sheets para PDF
Sistema que processa consultas do Sheets e gera PDFs automaticamente
"""

import sys
import os
import json
from datetime import datetime
from pdf_report_generator import ProfessionalPDFReportGenerator
import requests
import time

class BiscoitaoSheetsIntegrator:
    """Integrador entre Google Sheets e sistema de relatórios PDF"""
    
    def __init__(self):
        self.pdf_generator = ProfessionalPDFReportGenerator()
        self.toqan_api_url = "https://api.toqan.ai"  # URL base da API Toqan
        self.conversation_storage = {}  # Armazena conversações ativas
    
    def process_sheets_query(self, user_query, conversation_id=None):
        """Processa consulta vinda do Google Sheets e gera PDF"""
        
        print(f"📊 BISCOITÃO SHEETS INTEGRATOR")
        print("=" * 50)
        print(f"🔍 Consulta: {user_query}")
        print(f"🆔 Conversation ID: {conversation_id}")
        print()
        
        try:
            # 1. Gera relatório PDF completo
            print("📄 Gerando relatório PDF...")
            result = self.pdf_generator.generate_professional_pdf_report(user_query)
            
            if not result:
                return {
                    'success': False,
                    'error': 'Não foi possível gerar relatório para esta consulta',
                    'timestamp': datetime.now().isoformat()
                }
            
            # 2. Prepara resposta para o Sheets
            response_data = {
                'success': True,
                'query': user_query,
                'timestamp': result['timestamp'],
                'files': {
                    'pdf': result['pdf_file'],
                    'markdown': result['markdown_file'],
                    'chart': result['chart_file']
                },
                'analysis': {
                    'insights': result['analysis_result']['insights'],
                    'summary': result['analysis_result']['response'],
                    'data_points': len(result['analysis_result']['data']),
                    'viz_type': result['analysis_result']['viz_type']
                },
                'download_info': self._generate_download_info(result),
                'conversation_id': conversation_id
            }
            
            # 3. Armazena na conversa (se houver ID)
            if conversation_id:
                self.conversation_storage[conversation_id] = response_data
            
            print("✅ Processamento concluído!")
            return response_data
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'conversation_id': conversation_id
            }
    
    def _generate_download_info(self, result):
        """Gera informações de download para o Sheets"""
        
        download_info = {
            'pdf_path': os.path.abspath(result['pdf_file']) if result['pdf_file'] else None,
            'pdf_size': None,
            'markdown_path': os.path.abspath(result['markdown_file']),
            'chart_path': os.path.abspath(result['chart_file'])
        }
        
        # Calcula tamanho do PDF se existe
        if result['pdf_file'] and os.path.exists(result['pdf_file']):
            download_info['pdf_size'] = os.path.getsize(result['pdf_file'])
        
        return download_info
    
    def create_toqan_conversation(self, user_query):
        """Cria nova conversação na API Toqan (simulação)"""
        
        # Implementação simulada - ajustar conforme API real
        conversation_data = {
            'pergunta': user_query,
            'timestamp': datetime.now().isoformat(),
            'fonte': 'biscoitao_sheets',
            'tipo': 'relatorio_pdf'
        }
        
        # Aqui seria a chamada real para API Toqan
        # response = requests.post(f"{self.toqan_api_url}/conversation", 
        #                         json=conversation_data)
        
        # Por enquanto, retorna ID simulado
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            'conversation_id': conversation_id,
            'status': 'created',
            'data': conversation_data
        }
    
    def get_conversation_response(self, conversation_id):
        """Obtém resposta de uma conversação"""
        
        if conversation_id in self.conversation_storage:
            return self.conversation_storage[conversation_id]
        else:
            return {
                'success': False,
                'error': 'Conversação não encontrada',
                'conversation_id': conversation_id
            }
    
    def format_sheets_response(self, response_data):
        """Formata resposta para exibição no Google Sheets"""
        
        if not response_data['success']:
            return f"❌ Erro: {response_data['error']}"
        
        # Monta resposta formatada para o Sheets
        formatted_response = f"""📊 RELATÓRIO BISCOITÃO GERADO

🔍 Consulta: {response_data['query']}
⏰ Gerado em: {datetime.fromisoformat(response_data['timestamp']).strftime('%d/%m/%Y %H:%M:%S')}

📈 Resultados:
• {response_data['analysis']['data_points']} registros analisados
• Tipo: {response_data['analysis']['viz_type'].replace('_', ' ').title()}

💡 Principais Insights:"""
        
        for insight in response_data['analysis']['insights'][:3]:  # Top 3 insights
            # Remove emojis para melhor exibição no Sheets
            clean_insight = insight[2:].strip() if insight.startswith(('📈', '📉', '📊', '🔝', '🔻', '⚠️', '🥇')) else insight
            formatted_response += f"\n• {clean_insight}"
        
        formatted_response += f"""

📄 Arquivos Gerados:
• PDF: {response_data['files']['pdf'] if response_data['files']['pdf'] else 'Não disponível'}
• Markdown: {response_data['files']['markdown']}
• Gráfico: {response_data['files']['chart']}

💬 Resumo: {response_data['analysis']['summary']}

🔗 ID da Conversação: {response_data['conversation_id']}
"""
        
        return formatted_response

def create_updated_google_apps_script():
    """Cria versão atualizada do Google Apps Script para integração"""
    
    apps_script_code = '''
/**
 * Biscoitão - Função Atualizada para Integração com PDF
 * Versão 2.0 - Integrada com geração de relatórios PDF
 */

function perguntarToqan(pergunta) {
  console.log("🚀 Iniciando pergunta para Biscoitão:", pergunta);
  
  try {
    // 1. Cria nova conversação
    const conversationResponse = criarConversacaoBiscoitao(pergunta);
    
    if (!conversationResponse.success) {
      return `❌ Erro ao criar conversação: ${conversationResponse.error}`;
    }
    
    console.log("✅ Conversação criada:", conversationResponse.conversation_id);
    
    // 2. Processa consulta e gera PDF
    const processResponse = processarConsultaBiscoitao(pergunta, conversationResponse.conversation_id);
    
    if (!processResponse.success) {
      return `❌ Erro no processamento: ${processResponse.error}`;
    }
    
    // 3. Formata resposta para exibição
    const formattedResponse = formatarRespostaBiscoitao(processResponse);
    
    // 4. Abre PDF em nova aba (se disponível)
    if (processResponse.files && processResponse.files.pdf) {
      abrirPDFEmNovaAba(processResponse.files.pdf, processResponse.timestamp);
    }
    
    console.log("🎯 Processamento concluído com sucesso");
    return formattedResponse;
    
  } catch (error) {
    console.error("❌ Erro na função perguntarToqan:", error);
    return `❌ Erro interno: ${error.message}`;
  }
}

function criarConversacaoBiscoitao(pergunta) {
  /**
   * Cria nova conversação no sistema Biscoitão
   */
  
  try {
    // URL do servidor Biscoitão (ajustar conforme necessário)
    const biscoitaoUrl = "http://localhost:5000/api/create-conversation";
    
    const payload = {
      'pergunta': pergunta,
      'fonte': 'google_sheets',
      'timestamp': new Date().toISOString()
    };
    
    const options = {
      'method': 'POST',
      'headers': {
        'Content-Type': 'application/json'
      },
      'payload': JSON.stringify(payload)
    };
    
    // Simulação - em produção fazer chamada real
    // const response = UrlFetchApp.fetch(biscoitaoUrl, options);
    // const data = JSON.parse(response.getContentText());
    
    // Por enquanto, retorna dados simulados
    const conversationId = `conv_${new Date().getTime()}`;
    
    return {
      'success': true,
      'conversation_id': conversationId,
      'status': 'created'
    };
    
  } catch (error) {
    console.error("Erro ao criar conversação:", error);
    return {
      'success': false,
      'error': error.message
    };
  }
}

function processarConsultaBiscoitao(pergunta, conversationId) {
  /**
   * Processa consulta e gera relatório PDF
   */
  
  try {
    // URL do processador Biscoitão
    const processUrl = "http://localhost:5000/api/process-query";
    
    const payload = {
      'query': pergunta,
      'conversation_id': conversationId,
      'output_format': 'pdf',
      'timestamp': new Date().toISOString()
    };
    
    const options = {
      'method': 'POST',
      'headers': {
        'Content-Type': 'application/json'
      },
      'payload': JSON.stringify(payload)
    };
    
    // Chamada real seria:
    // const response = UrlFetchApp.fetch(processUrl, options);
    // const data = JSON.parse(response.getContentText());
    
    // Simulação de resposta
    const timestamp = new Date().getTime();
    
    return {
      'success': true,
      'query': pergunta,
      'timestamp': timestamp,
      'files': {
        'pdf': `relatorio_biscoitao_${timestamp}.pdf`,
        'markdown': `relatorio_biscoitao_${timestamp}.md`,
        'chart': `chart_line_chart_${timestamp}.png`
      },
      'analysis': {
        'insights': [
          '📈 Tendência de crescimento detectada',
          '📊 Análise temporal concluída',
          '🔍 Insights automáticos gerados'
        ],
        'summary': 'Análise completa realizada com sucesso.',
        'data_points': 148,
        'viz_type': 'line_chart'
      },
      'conversation_id': conversationId
    };
    
  } catch (error) {
    console.error("Erro no processamento:", error);
    return {
      'success': false,
      'error': error.message,
      'conversation_id': conversationId
    };
  }
}

function formatarRespostaBiscoitao(responseData) {
  /**
   * Formata resposta para exibição no Google Sheets
   */
  
  if (!responseData.success) {
    return `❌ Erro: ${responseData.error}`;
  }
  
  const timestamp = new Date(responseData.timestamp).toLocaleString('pt-BR');
  
  let formatted = `📊 RELATÓRIO BISCOITÃO GERADO\\n\\n`;
  formatted += `🔍 Consulta: ${responseData.query}\\n`;
  formatted += `⏰ Gerado em: ${timestamp}\\n\\n`;
  
  formatted += `📈 Resultados:\\n`;
  formatted += `• ${responseData.analysis.data_points} registros analisados\\n`;
  formatted += `• Tipo: ${responseData.analysis.viz_type.replace('_', ' ')}\\n\\n`;
  
  formatted += `💡 Principais Insights:\\n`;
  responseData.analysis.insights.slice(0, 3).forEach(insight => {
    const cleanInsight = insight.replace(/[📈📉📊🔝🔻⚠️🥇]/g, '').trim();
    formatted += `• ${cleanInsight}\\n`;
  });
  
  formatted += `\\n📄 Arquivos Gerados:\\n`;
  formatted += `• PDF: ${responseData.files.pdf}\\n`;
  formatted += `• Markdown: ${responseData.files.markdown}\\n`;
  formatted += `• Gráfico: ${responseData.files.chart}\\n\\n`;
  
  formatted += `💬 Resumo: ${responseData.analysis.summary}\\n\\n`;
  formatted += `🔗 ID: ${responseData.conversation_id}`;
  
  return formatted;
}

function abrirPDFEmNovaAba(pdfFile, timestamp) {
  /**
   * Abre PDF em nova aba (implementação dependente do ambiente)
   */
  
  try {
    // Em ambiente real, seria necessário criar URL de download
    // ou integração com Google Drive para abrir o PDF
    
    console.log(`📖 PDF pronto para abertura: ${pdfFile}`);
    console.log(`🕐 Timestamp: ${timestamp}`);
    
    // Implementação futura: upload para Google Drive e abertura
    // const driveFile = DriveApp.createFile(pdfBlob);
    // const fileUrl = driveFile.getUrl();
    // HtmlService.createHtmlOutput(`<script>window.open('${fileUrl}', '_blank');</script>`);
    
  } catch (error) {
    console.error("Erro ao abrir PDF:", error);
  }
}

// Função auxiliar para teste
function testarBiscoitao() {
  const resultado = perguntarToqan("Evolução do preço médio de jan-24 a jan-25");
  console.log("Resultado do teste:", resultado);
  return resultado;
}
'''
    
    return apps_script_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🔧 BISCOITÃO SHEETS INTEGRATOR")
        print("=" * 40)
        print("Uso: python sheets_integrator.py 'sua consulta'")
        print()
        print("Exemplos:")
        print("  python sheets_integrator.py 'Evolução do preço de jan-24 a jan-25'")
        print("  python sheets_integrator.py 'Compare categorias por volume'")
        print()
        print("📄 Para gerar Google Apps Script atualizado:")
        print("  python sheets_integrator.py --generate-script")
        
        if "--generate-script" in sys.argv:
            print("\n📝 Gerando Google Apps Script atualizado...")
            script_code = create_updated_google_apps_script()
            
            with open("biscoitao_sheets_v2.gs", "w", encoding="utf-8") as f:
                f.write(script_code)
            
            print("✅ Arquivo gerado: biscoitao_sheets_v2.gs")
            print("📋 Copie este código para o Google Apps Script")
        
        sys.exit(1)
    
    # Processa consulta diretamente
    query = " ".join(sys.argv[1:])
    
    try:
        integrator = BiscoitaoSheetsIntegrator()
        
        # Simula chamada do Sheets
        conversation = integrator.create_toqan_conversation(query)
        result = integrator.process_sheets_query(query, conversation['conversation_id'])
        
        if result['success']:
            print("\n" + "="*60)
            print("📱 RESPOSTA FORMATADA PARA GOOGLE SHEETS:")
            print("="*60)
            print(integrator.format_sheets_response(result))
            print("="*60)
        else:
            print(f"\n❌ Erro: {result['error']}")
    
    except Exception as e:
        print(f"❌ Erro no integrador: {e}")
        import traceback
        traceback.print_exc()
