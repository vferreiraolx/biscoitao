"""
Demonstração Completa do Sistema de Relatórios HTML - Biscoitão
Script para mostrar todos os recursos integrados do sistema
"""

from html_report_generator import ProfessionalHTMLReportGenerator
import os
import time

def run_html_demo():
    """Executa demonstração completa do sistema de relatórios HTML"""
    
    print("🎨 DEMONSTRAÇÃO COMPLETA - SISTEMA DE RELATÓRIOS HTML BISCOITÃO")
    print("=" * 70)
    print("Sistema integrado de análise conversacional com relatórios HTML profissionais")
    print()
    
    # Inicializa o gerador
    report_generator = ProfessionalHTMLReportGenerator()
    
    # Exemplos de consultas variadas
    examples = [
        {
            "query": "Evolução da média do preço de jan-24 a jan-25",
            "description": "📈 Análise Temporal: Comparação entre períodos",
            "type": "temporal"
        },
        {
            "query": "Compare as 10 principais categorias por volume",
            "description": "📊 Análise Categórica: Ranking e comparação",
            "type": "categorical"
        },
        {
            "query": "Tendência de crescimento nos últimos 12 meses",
            "description": "📈 Análise de Tendência: Evolução anual",
            "type": "trend"
        }
    ]
    
    generated_reports = []
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*25} RELATÓRIO {i} {'='*25}")
        print(f"📝 {example['description']}")
        print(f"💭 Consulta: \"{example['query']}\"")
        print(f"🏷️  Tipo: {example['type']}")
        print()
        
        try:
            print("⏳ Gerando relatório HTML...")
            
            result = report_generator.generate_professional_report(example['query'])
            
            if result:
                generated_reports.append({
                    'example': example,
                    'result': result,
                    'success': True
                })
                
                print("✅ Relatório gerado com sucesso!")
                print(f"📄 Arquivo: {result['filename']}")
                print(f"🌐 Aberto automaticamente no navegador")
                
                # Pequena pausa para não sobrecarregar
                time.sleep(2)
                
            else:
                generated_reports.append({
                    'example': example,
                    'result': None,
                    'success': False
                })
                print("❌ Falha na geração do relatório")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            generated_reports.append({
                'example': example,
                'result': None,
                'success': False,
                'error': str(e)
            })
        
        print("-" * 70)
    
    # Resumo final da demonstração
    print(f"\n🎯 RESUMO DA DEMONSTRAÇÃO")
    print("=" * 70)
    
    successful = sum(1 for r in generated_reports if r['success'])
    total = len(generated_reports)
    
    print(f"📊 Relatórios gerados: {successful}/{total}")
    print(f"📈 Taxa de sucesso: {(successful/total)*100:.1f}%")
    print()
    
    if successful > 0:
        print("📁 Arquivos HTML gerados:")
        for report in generated_reports:
            if report['success'] and report['result']:
                filename = report['result']['filename']
                query = report['example']['query'][:50] + "..." if len(report['example']['query']) > 50 else report['example']['query']
                print(f"   • {filename} - \"{query}\"")
        print()
    
    print("🎨 Recursos demonstrados:")
    print("   ✅ Geração automática de HTML profissional")
    print("   ✅ Gráficos com paleta viridis integrada")
    print("   ✅ Design responsivo e elegante")
    print("   ✅ Insights automáticos contextualizados")
    print("   ✅ Abertura automática no navegador")
    print("   ✅ Estatísticas resumidas interativas")
    print("   ✅ Tabelas de dados formatadas")
    print("   ✅ Layout sem excessos, focado em resultados")
    print()
    
    print("💡 Funcionalidades avançadas:")
    print("   • Gráficos em base64 embutidos (sem dependência de arquivos)")
    print("   • CSS com gradientes e animações sutis")
    print("   • Responsividade para dispositivos móveis")
    print("   • Tipografia profissional (Segoe UI)")
    print("   • Paleta de cores harmoniosa e elegante")
    print("   • Cards interativos com hover effects")
    print()
    
    return generated_reports

def show_integration_examples():
    """Mostra exemplos de integração com outros sistemas"""
    
    print("\n🔗 EXEMPLOS DE INTEGRAÇÃO")
    print("=" * 50)
    
    integration_examples = [
        {
            "title": "📧 Integração com Email",
            "code": """
# Envio automático de relatórios por email
from html_report_generator import ProfessionalHTMLReportGenerator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_relatorio_email(destinatario, consulta):
    generator = ProfessionalHTMLReportGenerator()
    result = generator.generate_professional_report(consulta)
    
    if result:
        with open(result['filename'], 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        msg = MIMEMultipart()
        msg['Subject'] = f"Relatório Biscoitão: {consulta}"
        msg.attach(MIMEText(html_content, 'html'))
        
        # Envio por SMTP...
"""
        },
        {
            "title": "📅 Relatórios Agendados",
            "code": """
# Geração automática de relatórios diários/semanais
import schedule
import time

def gerar_relatorio_diario():
    queries = [
        "Vendas de hoje vs ontem",
        "Top 10 produtos do dia",
        "Tendência semanal"
    ]
    
    for query in queries:
        generator.generate_professional_report(query)

schedule.every().day.at("08:00").do(gerar_relatorio_diario)
"""
        },
        {
            "title": "🌐 API REST para Relatórios",
            "code": """
# Endpoint Flask para geração sob demanda
@app.route('/api/relatorio', methods=['POST'])
def gerar_relatorio_api():
    data = request.get_json()
    consulta = data.get('consulta')
    
    generator = ProfessionalHTMLReportGenerator()
    result = generator.generate_professional_report(consulta)
    
    return jsonify({
        'success': bool(result),
        'arquivo': result['filename'] if result else None,
        'url_download': f'/download/{result["filename"]}' if result else None
    })
"""
        }
    ]
    
    for example in integration_examples:
        print(f"\n{example['title']}")
        print("-" * 40)
        print(example['code'])
    
    print("\n💼 Casos de Uso Empresariais:")
    print("   • Relatórios executivos automáticos")
    print("   • Dashboards para stakeholders")
    print("   • Análises ad-hoc para tomada de decisão")
    print("   • Relatórios de performance mensal/trimestral")
    print("   • Alertas automáticos baseados em métricas")

def show_customization_options():
    """Mostra opções de customização do sistema"""
    
    print("\n🎨 OPÇÕES DE CUSTOMIZAÇÃO")
    print("=" * 50)
    
    print("🎯 Temas e Paletas:")
    print("   • Viridis (atual): Científico e profissional")
    print("   • Plasma: Vibrante e energético")
    print("   • Corporate: Azul corporativo tradicional")
    print("   • Minimal: Monocromático minimalista")
    print()
    
    print("📊 Tipos de Gráfico Suportados:")
    print("   ✅ Linha temporal (evolução, tendências)")
    print("   ✅ Barras (comparações, rankings)")
    print("   🔄 Pizza (distribuições) - Em desenvolvimento")
    print("   🔄 Scatter (correlações) - Em desenvolvimento")
    print("   🔄 Heatmap (matrizes) - Em desenvolvimento")
    print()
    
    print("🔧 Configurações Personalizáveis:")
    print("   • Logo da empresa no cabeçalho")
    print("   • Cores corporativas customizadas")
    print("   • Fontes e tipografia")
    print("   • Idioma dos relatórios")
    print("   • Formato de data e números")
    print("   • Seções opcionais (insights, dados, etc.)")

if __name__ == "__main__":
    # Executa demonstração principal
    demo_results = run_html_demo()
    
    # Mostra exemplos de integração
    show_integration_examples()
    
    # Mostra opções de customização
    show_customization_options()
    
    print(f"\n🎊 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("O Sistema de Relatórios HTML do Biscoitão está pronto para uso!")
    print("Relatórios profissionais, elegantes e automatizados com um comando.")
    print()
    print("📚 Para usar:")
    print("   python html_report_generator.py 'sua consulta aqui'")
    print()
    print("🌟 Principais benefícios:")
    print("   • Zero configuração manual")
    print("   • Design profissional automático")
    print("   • Abertura automática no navegador")
    print("   • Gráficos de alta qualidade embutidos")
    print("   • Responsivo para todos os dispositivos")
    print("   • Insights inteligentes inclusos")
