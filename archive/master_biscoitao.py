"""
BISCOITÃO - SISTEMA COMPLETO INTEGRADO
Script master que demonstra toda a capacidade do sistema
"""

import sys
import os
from datetime import datetime

# Importa todos os componentes do sistema
from html_report_generator import ProfessionalHTMLReportGenerator
from visual_assistant import IntelligentReportGenerator
try:
    from nl_query_assistant_v2 import AdvancedQueryBuilder
except ImportError:
    print("⚠️ nl_query_assistant_v2 não encontrado, continuando sem ele...")
    AdvancedQueryBuilder = None

class BiscoitaoMasterSystem:
    """Sistema master que integra todas as funcionalidades do Biscoitão"""
    
    def __init__(self):
        print("🚀 Inicializando Sistema Biscoitão Master...")
        self.html_generator = ProfessionalHTMLReportGenerator()
        self.visual_generator = IntelligentReportGenerator()
        if AdvancedQueryBuilder:
            self.query_builder = AdvancedQueryBuilder()
        else:
            self.query_builder = None
        print("✅ Sistema inicializado com sucesso!")
    
    def process_complete_analysis(self, user_query):
        """Processa análise completa com todos os componentes"""
        
        print(f"\n🎯 ANÁLISE COMPLETA: {user_query}")
        print("=" * 60)
        
        results = {
            'query': user_query,
            'timestamp': datetime.now(),
            'components': {}
        }
        
        # 1. Análise textual (se disponível)
        if self.query_builder:
            print("📝 Executando análise textual avançada...")
            try:
                text_result = self.query_builder.process_instruction(user_query)
                results['components']['text_analysis'] = text_result
                print("✅ Análise textual concluída")
            except Exception as e:
                print(f"⚠️ Análise textual falhou: {e}")
                results['components']['text_analysis'] = None
        else:
            print("⏭️ Análise textual não disponível")
            results['components']['text_analysis'] = None
        
        # 2. Análise visual
        print("📊 Executando análise visual...")
        try:
            visual_result = self.visual_generator.generate_complete_report(user_query)
            results['components']['visual_analysis'] = visual_result
            print("✅ Análise visual concluída")
        except Exception as e:
            print(f"❌ Análise visual falhou: {e}")
            results['components']['visual_analysis'] = None
        
        # 3. Relatório HTML profissional
        print("📄 Gerando relatório HTML profissional...")
        try:
            html_result = self.html_generator.generate_professional_report(user_query)
            results['components']['html_report'] = html_result
            print("✅ Relatório HTML concluído")
        except Exception as e:
            print(f"❌ Relatório HTML falhou: {e}")
            results['components']['html_report'] = None
        
        return results
    
    def generate_summary_report(self, results):
        """Gera relatório resumo da análise completa"""
        
        print(f"\n📋 RELATÓRIO RESUMO")
        print("=" * 40)
        print(f"🕐 Processado em: {results['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"❓ Consulta: {results['query']}")
        print()
        
        # Status dos componentes
        print("🔧 Status dos Componentes:")
        
        for component, result in results['components'].items():
            if component == 'text_analysis':
                icon = "📝"
                name = "Análise Textual"
            elif component == 'visual_analysis':
                icon = "📊"
                name = "Análise Visual"
            elif component == 'html_report':
                icon = "📄"
                name = "Relatório HTML"
            else:
                icon = "🔧"
                name = component
            
            status = "✅ Sucesso" if result else "❌ Falhou"
            print(f"   {icon} {name}: {status}")
        
        print()
        
        # Arquivos gerados
        generated_files = []
        
        if results['components']['visual_analysis']:
            chart_file = results['components']['visual_analysis'].get('chart_file')
            if chart_file:
                generated_files.append(f"📊 Gráfico: {chart_file}")
        
        if results['components']['html_report']:
            html_file = results['components']['html_report'].get('filename')
            if html_file:
                generated_files.append(f"📄 Relatório: {html_file}")
        
        if generated_files:
            print("📁 Arquivos Gerados:")
            for file_info in generated_files:
                print(f"   {file_info}")
        else:
            print("📁 Nenhum arquivo foi gerado")
        
        print()
        
        # Insights consolidados
        all_insights = []
        
        if results['components']['text_analysis']:
            text_insights = results['components']['text_analysis'].get('insights', [])
            all_insights.extend(text_insights)
        
        if results['components']['visual_analysis']:
            visual_insights = results['components']['visual_analysis'].get('insights', [])
            all_insights.extend(visual_insights)
        
        if all_insights:
            print("💡 Insights Consolidados:")
            for insight in all_insights[:5]:  # Top 5 insights
                print(f"   • {insight}")
            if len(all_insights) > 5:
                print(f"   ... e mais {len(all_insights) - 5} insights")
        else:
            print("💡 Nenhum insight específico gerado")
        
        print()
        
        # Recomendações
        print("🎯 Recomendações:")
        if results['components']['html_report']:
            print("   • Abra o relatório HTML para visualização completa")
        if results['components']['visual_analysis']:
            print("   • Analise o gráfico gerado para padrões visuais")
        if not any(results['components'].values()):
            print("   • Refine a consulta para obter melhores resultados")
            print("   • Verifique se há dados disponíveis para o período solicitado")
        
        return results

def show_system_capabilities():
    """Mostra capacidades completas do sistema"""
    
    print("\n🌟 CAPACIDADES DO SISTEMA BISCOITÃO")
    print("=" * 50)
    
    capabilities = [
        {
            "category": "📝 Processamento de Linguagem Natural",
            "features": [
                "Detecção automática de intenção",
                "Mapeamento inteligente de colunas",
                "Extração de filtros temporais",
                "Queries SQL adaptativas com fallbacks"
            ]
        },
        {
            "category": "📊 Visualização Inteligente",
            "features": [
                "Gráficos de linha para evolução temporal",
                "Gráficos de barras para comparações",
                "Paleta viridis profissional",
                "Insights automáticos contextualizados"
            ]
        },
        {
            "category": "📄 Relatórios HTML Profissionais",
            "features": [
                "Design responsivo e elegante",
                "Gráficos embutidos em base64",
                "Abertura automática no navegador",
                "Estatísticas resumidas interativas"
            ]
        },
        {
            "category": "🔧 Integração e Automação",
            "features": [
                "Google Sheets via Apps Script",
                "API Flask para uso programático",
                "Sistema de fallbacks robusto",
                "Tratamento inteligente de erros"
            ]
        }
    ]
    
    for capability in capabilities:
        print(f"\n{capability['category']}")
        print("-" * 40)
        for feature in capability['features']:
            print(f"   ✅ {feature}")
    
    print(f"\n🚀 O Biscoitão é uma solução completa de Business Intelligence conversacional!")

def run_complete_demo():
    """Executa demonstração completa do sistema"""
    
    print("🎨 DEMONSTRAÇÃO COMPLETA DO SISTEMA BISCOITÃO")
    print("=" * 60)
    print("Sistema integrado de análise conversacional com IA")
    print()
    
    # Inicializa sistema
    master_system = BiscoitaoMasterSystem()
    
    # Exemplos de consultas variadas
    demo_queries = [
        "Evolução da média do preço de jan-24 a jan-25",
        "Compare as 5 principais categorias por volume"
    ]
    
    all_results = []
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'🔄' * 3} DEMO {i}/{len(demo_queries)} {'🔄' * 3}")
        
        # Processa análise completa
        results = master_system.process_complete_analysis(query)
        
        # Gera relatório resumo
        summary = master_system.generate_summary_report(results)
        
        all_results.append(summary)
        
        print("-" * 60)
    
    # Relatório final
    print(f"\n🎯 RELATÓRIO FINAL DA DEMONSTRAÇÃO")
    print("=" * 60)
    
    total_queries = len(all_results)
    successful_components = 0
    total_components = 0
    
    for result in all_results:
        for component, status in result['components'].items():
            total_components += 1
            if status:
                successful_components += 1
    
    success_rate = (successful_components / total_components) * 100 if total_components > 0 else 0
    
    print(f"📊 Consultas processadas: {total_queries}")
    print(f"📈 Taxa de sucesso geral: {success_rate:.1f}%")
    print(f"🔧 Componentes ativos: {successful_components}/{total_components}")
    print()
    
    show_system_capabilities()
    
    return all_results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo de uso direto com consulta
        query = " ".join(sys.argv[1:])
        
        print(f"🎯 BISCOITÃO - ANÁLISE DIRETA")
        print("=" * 40)
        
        master_system = BiscoitaoMasterSystem()
        results = master_system.process_complete_analysis(query)
        master_system.generate_summary_report(results)
        
    else:
        # Modo demonstração completa
        run_complete_demo()
        
        print(f"\n🎊 SISTEMA BISCOITÃO PRONTO PARA USO!")
        print("=" * 50)
        print("Para usar diretamente:")
        print("   python master_biscoitao.py 'sua consulta aqui'")
        print()
        print("Componentes disponíveis individualmente:")
        print("   • html_report_generator.py - Relatórios HTML")
        print("   • visual_assistant.py - Análise visual")
        print("   • nl_query_assistant_v2.py - NL-to-SQL avançado")
        print()
        print("🌟 O Biscoitão transforma perguntas em insights visuais profissionais!")
