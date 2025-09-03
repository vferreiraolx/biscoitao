"""
Servidor Flask para Integração Biscoitão - Google Sheets
Recebe consultas do Google Apps Script e gera relatórios PDF
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import traceback

# Importa nossos módulos locais
from pdf_report_generator import ProfessionalPDFReportGenerator
from sheets_integrator import BiscoitaoSheetsIntegrator

app = Flask(__name__)
CORS(app)  # Permite chamadas do Google Apps Script

# Instância global dos processadores
pdf_generator = ProfessionalPDFReportGenerator()
sheets_integrator = BiscoitaoSheetsIntegrator()

@app.route('/api/generate-pdf-report', methods=['POST'])
def generate_pdf_report():
    """Endpoint para gerar relatórios PDF a partir do Google Sheets"""
    
    try:
        # Recebe dados do Google Apps Script
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        query = data.get('query')
        toqan_answer = data.get('toqan_answer', '')
        conversation_id = data.get('conversation_id', f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query não fornecida'
            }), 400
        
        print(f"📊 SERVIDOR BISCOITÃO - Nova consulta recebida")
        print(f"🔍 Query: {query}")
        print(f"🆔 Conversation ID: {conversation_id}")
        print(f"📱 Source: {data.get('source', 'unknown')}")
        
        # Processa consulta com integrador
        result = sheets_integrator.process_sheets_query(query, conversation_id)
        
        if result['success']:
            print(f"✅ Relatório PDF gerado com sucesso!")
            return jsonify(result), 200
        else:
            print(f"❌ Erro na geração: {result['error']}")
            return jsonify(result), 500
    
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se o servidor está funcionando"""
    
    return jsonify({
        'status': 'healthy',
        'service': 'Biscoitão PDF Generator',
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'pdf_generator': 'ready',
            'sheets_integrator': 'ready',
            'visual_assistant': 'ready'
        }
    })

@app.route('/api/test-query', methods=['POST'])
def test_query():
    """Endpoint de teste para validar funcionamento"""
    
    try:
        data = request.get_json() or {}
        test_query = data.get('query', 'Evolução do preço médio de jan-24 a jan-25')
        
        print(f"🧪 TESTE - Processando consulta: {test_query}")
        
        # Usa o integrador para processar
        result = sheets_integrator.process_sheets_query(test_query, 'test_conversation')
        
        return jsonify({
            'test_success': True,
            'query': test_query,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return jsonify({
            'test_success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/list-reports', methods=['GET'])
def list_reports():
    """Lista relatórios gerados recentemente"""
    
    try:
        reports_dir = os.getcwd()  # Diretório atual
        report_files = []
        
        # Busca arquivos PDF e MD gerados
        for file in os.listdir(reports_dir):
            if file.startswith('relatorio_biscoitao_') and (file.endswith('.pdf') or file.endswith('.md')):
                file_path = os.path.join(reports_dir, file)
                file_stats = os.stat(file_path)
                
                report_files.append({
                    'filename': file,
                    'size': file_stats.st_size,
                    'created': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    'type': 'pdf' if file.endswith('.pdf') else 'markdown'
                })
        
        # Ordena por data de criação (mais recente primeiro)
        report_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports_count': len(report_files),
            'reports': report_files[:10],  # Últimos 10 relatórios
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def home():
    """Página inicial do servidor"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Biscoitão PDF Generator - Servidor</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { 
                color: #fff; 
                text-align: center;
                margin-bottom: 30px;
            }
            .endpoint { 
                background: rgba(255,255,255,0.2); 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px;
                border-left: 4px solid #35b779;
            }
            .status { 
                background: rgba(46, 204, 113, 0.2); 
                padding: 10px; 
                border-radius: 5px;
                text-align: center;
                margin: 20px 0;
            }
            code { 
                background: rgba(0,0,0,0.3); 
                padding: 2px 6px; 
                border-radius: 3px; 
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Biscoitão PDF Generator v2.0</h1>
            
            <div class="status">
                ✅ Servidor funcionando corretamente
            </div>
            
            <h2>🔧 Endpoints Disponíveis:</h2>
            
            <div class="endpoint">
                <strong>POST /api/generate-pdf-report</strong><br>
                Gera relatório PDF a partir de consulta do Google Sheets<br>
                <code>{"query": "sua consulta", "conversation_id": "opcional"}</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/health</strong><br>
                Verifica status do servidor e componentes
            </div>
            
            <div class="endpoint">
                <strong>POST /api/test-query</strong><br>
                Testa funcionamento com consulta exemplo<br>
                <code>{"query": "sua consulta de teste"}</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/list-reports</strong><br>
                Lista relatórios PDF e Markdown gerados recentemente
            </div>
            
            <h2>🔗 Integração Google Sheets:</h2>
            <p>Para usar no Google Sheets, certifique-se de que:</p>
            <ul>
                <li>Este servidor está rodando em <code>http://localhost:5000</code></li>
                <li>O Google Apps Script foi atualizado com o código v2.0</li>
                <li>A função <code>=perguntarToqan("sua consulta")</code> está configurada</li>
            </ul>
            
            <h2>📊 Tecnologias:</h2>
            <p>Flask + PyHive + Matplotlib + Seaborn + Pandas + Markdown + PDF</p>
            
            <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
                <small>Gerado em: """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</small>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

if __name__ == '__main__':
    print("🚀 INICIANDO SERVIDOR BISCOITÃO PDF GENERATOR")
    print("=" * 50)
    print("📊 Sistema: Biscoitão PDF Generator v2.0")
    print("🌐 URL: http://localhost:5000")
    print("🔧 Modo: Desenvolvimento")
    print("📱 Integração: Google Sheets + API Toqan")
    print("📄 Output: Relatórios PDF com gráficos viridis")
    print("=" * 50)
    print()
    print("✅ Componentes carregados:")
    print("  • PDF Generator: ProfessionalPDFReportGenerator")
    print("  • Sheets Integrator: BiscoitaoSheetsIntegrator") 
    print("  • Visual Assistant: Sistema de análise visual")
    print("  • Flask Server: Endpoints REST configurados")
    print()
    print("🔗 Endpoints disponíveis:")
    print("  • GET  /              - Página inicial")
    print("  • GET  /api/health    - Status do servidor")
    print("  • POST /api/generate-pdf-report - Gera PDF")
    print("  • POST /api/test-query - Teste do sistema")
    print("  • GET  /api/list-reports - Lista relatórios")
    print()
    print("📱 Para testar do Google Sheets:")
    print('  =perguntarToqan("evolução do preço de jan-24 a jan-25")')
    print()
    
    # Inicia servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
