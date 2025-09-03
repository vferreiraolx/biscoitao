"""
API Flask para Visual Assistant - Biscoitão
Endpoint web para análise conversacional com geração de gráficos
"""

from flask import Flask, request, jsonify, send_file
from visual_assistant import IntelligentReportGenerator
import os
import json
from datetime import datetime
import traceback

app = Flask(__name__)

# Inicializa o gerador de relatórios
report_generator = IntelligentReportGenerator()

@app.route('/', methods=['GET'])
def home():
    """Endpoint principal com documentação"""
    return jsonify({
        'service': 'Biscoitão Visual Assistant API',
        'version': '1.0',
        'description': 'API para análise conversacional com geração automática de gráficos',
        'endpoints': {
            '/analyze': 'POST - Analisa pergunta e gera relatório visual',
            '/charts': 'GET - Lista gráficos gerados',
            '/chart/<filename>': 'GET - Download de gráfico específico'
        },
        'example_queries': [
            "Mostre a evolução da média do preço de jan-24 a jan-25",
            "Compare as categorias por faturamento",
            "Qual a tendência dos últimos 6 meses?",
            "Gráfico da distribuição por plataforma"
        ]
    })

@app.route('/analyze', methods=['POST'])
def analyze_query():
    """Endpoint principal para análise conversacional"""
    
    try:
        # Obtém dados da requisição
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Campo "query" é obrigatório',
                'example': {'query': 'Mostre a evolução do preço médio'}
            }), 400
        
        user_query = data['query']
        table_name = data.get('table', 'dw.monetization_total')
        
        print(f"📝 Processando: {user_query}")
        
        # Gera relatório completo
        result = report_generator.generate_complete_report(user_query, table_name)
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Não foi possível gerar análise para esta consulta',
                'query': user_query,
                'suggestions': [
                    'Tente ser mais específico sobre as datas (ex: jan-24, dez-23)',
                    'Mencione métricas específicas (preço, quantidade, faturamento)',
                    'Use palavras como "evolução", "comparar", "distribuição"'
                ]
            }), 400
        
        # Prepara resposta
        response = {
            'success': True,
            'query': user_query,
            'analysis': {
                'query_sql': result['query'],
                'visualization_type': result['viz_type'],
                'data_points': len(result['data']),
                'insights': result['insights'],
                'conversational_response': result['response']
            },
            'chart': {
                'filename': result['chart_file'],
                'download_url': f"/chart/{result['chart_file']}"
            },
            'data_sample': result['data'].head(10).to_dict('records') if len(result['data']) > 10 else result['data'].to_dict('records'),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': str(e),
            'query': data.get('query', 'N/A') if 'data' in locals() else 'N/A',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/charts', methods=['GET'])
def list_charts():
    """Lista todos os gráficos gerados"""
    
    try:
        chart_files = []
        
        # Lista arquivos PNG no diretório atual
        for filename in os.listdir('.'):
            if filename.startswith('grafico_') and filename.endswith('.png'):
                file_info = os.stat(filename)
                chart_files.append({
                    'filename': filename,
                    'size_bytes': file_info.st_size,
                    'created': datetime.fromtimestamp(file_info.st_ctime).isoformat(),
                    'download_url': f'/chart/{filename}'
                })
        
        # Ordena por data de criação (mais recente primeiro)
        chart_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'charts': chart_files,
            'total': len(chart_files),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/chart/<filename>', methods=['GET'])
def download_chart(filename):
    """Download de gráfico específico"""
    
    try:
        # Verifica se o arquivo existe e é seguro
        if not filename.startswith('grafico_') or not filename.endswith('.png'):
            return jsonify({'error': 'Nome de arquivo inválido'}), 400
        
        if not os.path.exists(filename):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quick-analyze', methods=['GET'])
def quick_analyze():
    """Endpoint rápido para análise via GET (para testes)"""
    
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'error': 'Parâmetro "q" com a pergunta é obrigatório',
            'example': '/quick-analyze?q=Mostre a evolução do preço médio'
        }), 400
    
    # Redireciona para análise completa
    return analyze_query()

@app.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde do serviço"""
    
    try:
        # Testa conexão com banco
        from query import execute_query
        test_result = execute_query("SELECT 1 as test")
        
        database_ok = len(test_result) > 0
        
        return jsonify({
            'status': 'healthy',
            'database_connection': 'ok' if database_ok else 'error',
            'timestamp': datetime.now().isoformat(),
            'service': 'Biscoitão Visual Assistant API'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Biscoitão Visual Assistant API")
    print("=" * 50)
    print("📊 Endpoints disponíveis:")
    print("   • POST /analyze - Análise conversacional completa")
    print("   • GET /charts - Lista gráficos gerados")
    print("   • GET /chart/<filename> - Download de gráfico")
    print("   • GET /quick-analyze?q=<pergunta> - Análise rápida")
    print("   • GET /health - Status do serviço")
    print()
    print("💡 Exemplo de uso:")
    print("   curl -X POST http://localhost:5000/analyze \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"query\": \"Mostre a evolução do preço médio\"}'")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
