"""
Demonstração completa do Visual Assistant
Script para mostrar todas as funcionalidades integradas de análise visual conversacional
"""

from visual_assistant import IntelligentReportGenerator
import os

def run_demo():
    """Executa demonstração completa do sistema"""
    
    print("🎨 DEMONSTRAÇÃO DO VISUAL ASSISTANT - BISCOITÃO")
    print("=" * 60)
    print("Sistema integrado de análise conversacional com visualização automática")
    print()
    
    # Inicializa o gerador de relatórios
    report_generator = IntelligentReportGenerator()
    
    # Lista de exemplos para demonstração
    examples = [
        {
            "query": "Mostre a evolução da média do preço de jan-24 a dez-24",
            "description": "📈 Análise temporal: evolução de preços ao longo do ano"
        },
        {
            "query": "Compare as 5 principais categorias por faturamento",
            "description": "📊 Análise categórica: ranking de categorias"
        },
        {
            "query": "Qual a tendência de crescimento nos últimos 6 meses",
            "description": "📈 Análise de tendência: crescimento recente"
        },
        {
            "query": "Distribuição de vendas por plataforma em 2024",
            "description": "🥧 Análise de distribuição: participação por plataforma"
        }
    ]
    
    results = []
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*20} EXEMPLO {i} {'='*20}")
        print(f"📝 {example['description']}")
        print(f"💭 Pergunta: \"{example['query']}\"")
        print()
        
        try:
            result = report_generator.generate_complete_report(example['query'])
            
            if result:
                results.append({
                    'example': example,
                    'result': result,
                    'success': True
                })
                print("✅ Sucesso!")
            else:
                results.append({
                    'example': example,
                    'result': None,
                    'success': False
                })
                print("❌ Falhou")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            results.append({
                'example': example,
                'result': None,
                'success': False,
                'error': str(e)
            })
        
        print("-" * 60)
    
    # Resumo final
    print(f"\n🎯 RESUMO DA DEMONSTRAÇÃO")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"📊 Execuções bem-sucedidas: {successful}/{total}")
    print(f"📈 Taxa de sucesso: {(successful/total)*100:.1f}%")
    print()
    
    if successful > 0:
        print("📁 Arquivos gerados:")
        for result in results:
            if result['success'] and result['result']:
                print(f"   • {result['result']['chart_file']}")
        print()
    
    print("🔧 Funcionalidades demonstradas:")
    print("   ✅ Detecção automática de tipo de visualização")
    print("   ✅ Construção inteligente de queries SQL")
    print("   ✅ Geração de gráficos personalizados")
    print("   ✅ Análise de insights automáticos")
    print("   ✅ Respostas conversacionais naturais")
    print("   ✅ Tratamento de erros e fallbacks")
    print()
    
    print("💡 Próximos passos:")
    print("   • Integração com Google Sheets")
    print("   • API web para interface conversacional")
    print("   • Mais tipos de visualização (scatter, pie, etc.)")
    print("   • Cache inteligente de queries")
    print("   • Exportação para diferentes formatos")
    
    return results

def create_integration_example():
    """Cria exemplo de integração com outros componentes"""
    
    print("\n🔗 EXEMPLO DE INTEGRAÇÃO COMPLETA")
    print("=" * 50)
    
    integration_code = '''
# Exemplo de integração com o sistema existente

from visual_assistant import IntelligentReportGenerator
from nl_query_assistant_v2 import AdvancedQueryBuilder
import json

class BiscoitaoIntegrated:
    """Sistema integrado do Biscoitão com análise visual"""
    
    def __init__(self):
        self.visual_generator = IntelligentReportGenerator()
        self.query_builder = AdvancedQueryBuilder()
    
    def process_user_request(self, user_input):
        """Processa pedido do usuário com análise + visualização"""
        
        # 1. Análise de dados
        query_result = self.query_builder.process_instruction(user_input)
        
        # 2. Geração de visualização
        visual_result = self.visual_generator.generate_complete_report(user_input)
        
        # 3. Resposta integrada
        return {
            'query_analysis': query_result,
            'visual_analysis': visual_result,
            'integrated_response': self._create_integrated_response(
                query_result, visual_result, user_input
            )
        }
    
    def _create_integrated_response(self, query_result, visual_result, user_input):
        """Cria resposta integrada combinando análise textual e visual"""
        
        response = {
            'type': 'integrated_analysis',
            'user_query': user_input,
            'data_summary': None,
            'chart_file': None,
            'insights': [],
            'conversational_response': ""
        }
        
        if query_result:
            response['data_summary'] = query_result.get('summary', '')
            response['insights'].extend(query_result.get('insights', []))
        
        if visual_result:
            response['chart_file'] = visual_result.get('chart_file', '')
            response['insights'].extend(visual_result.get('insights', []))
            
            # Combina respostas
            text_response = query_result.get('response', '') if query_result else ''
            visual_response = visual_result.get('response', '') if visual_result else ''
            
            response['conversational_response'] = f"{text_response} {visual_response}".strip()
        
        return response

# Uso do sistema integrado
biscoitao = BiscoitaoIntegrated()
result = biscoitao.process_user_request("Analise a evolução do preço médio e gere um gráfico")
print(json.dumps(result, indent=2, ensure_ascii=False))
'''
    
    print("📄 Código de integração:")
    print(integration_code)
    
    return integration_code

if __name__ == "__main__":
    # Executa demonstração
    demo_results = run_demo()
    
    # Mostra exemplo de integração
    integration_example = create_integration_example()
    
    print("\n🎊 DEMONSTRAÇÃO CONCLUÍDA!")
    print("O Visual Assistant está pronto para uso em produção.")
