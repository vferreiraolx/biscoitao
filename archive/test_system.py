"""
Script de Teste Completo - Sistema Biscoitão v2.0
Testa todos os componentes do sistema integrado
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def test_environment():
    """Testa ambiente Python e dependências"""
    
    print("🔧 TESTE DE AMBIENTE PYTHON")
    print("=" * 40)
    
    # Testa Python
    print(f"🐍 Python: {sys.version}")
    
    # Testa módulos essenciais
    modules_to_test = [
        'matplotlib', 'seaborn', 'pandas', 'numpy', 
        'markdown', 'json', 'subprocess', 'os', 'datetime'
    ]
    
    missing_modules = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}: OK")
        except ImportError:
            print(f"❌ {module}: FALTANDO")
            missing_modules.append(module)
    
    # Testa módulos opcionais (Flask, requests)
    optional_modules = ['flask', 'requests', 'flask_cors']
    
    print("\n📦 Módulos Opcionais (para servidor web):")
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module}: OK")
        except ImportError:
            print(f"⚠️ {module}: Não instalado (instale com: pip install {module})")
    
    if missing_modules:
        print(f"\n❌ Módulos obrigatórios faltando: {', '.join(missing_modules)}")
        return False
    else:
        print("\n✅ Ambiente Python configurado corretamente!")
        return True

def test_file_structure():
    """Testa se todos os arquivos necessários existem"""
    
    print("\n📁 TESTE DE ESTRUTURA DE ARQUIVOS")
    print("=" * 40)
    
    required_files = [
        'visual_assistant.py',
        'pdf_report_generator.py', 
        'sheets_integrator.py',
        'flask_server.py',
        'biscoitao.gs'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file}: {size:,} bytes")
        else:
            print(f"❌ {file}: FALTANDO")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Arquivos faltando: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ Todos os arquivos necessários estão presentes!")
        return True

def test_visual_assistant():
    """Testa o sistema de análise visual"""
    
    print("\n📊 TESTE DO VISUAL ASSISTANT")
    print("=" * 40)
    
    try:
        from visual_assistant import IntelligentReportGenerator
        
        assistant = IntelligentReportGenerator()
        print("✅ Instância criada com sucesso")
        
        # Teste básico dos componentes
        print(f"🔍 Testando componentes internos...")
        
        # Verifica se os atributos existem
        if hasattr(assistant, 'explorer') and hasattr(assistant, 'query_builder'):
            print("✅ Componentes internos carregados")
            return True
        else:
            print("❌ Componentes internos faltando")
            return False
    
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_pdf_generator():
    """Testa o gerador de PDF"""
    
    print("\n📄 TESTE DO GERADOR DE PDF")
    print("=" * 40)
    
    try:
        from pdf_report_generator import ProfessionalPDFReportGenerator
        
        generator = ProfessionalPDFReportGenerator()
        print("✅ Instância criada com sucesso")
        
        # Testa geração de markdown
        test_query = "Relatório de teste"
        print(f"📝 Testando geração de markdown...")
        
        # Simula dados de análise
        test_analysis = {
            'success': True,
            'query': test_query,
            'data': [{'teste': 1}],
            'insights': ['📈 Teste de insight'],
            'response': 'Análise de teste concluída',
            'viz_type': 'line_chart',
            'chart_file': 'test_chart.png'
        }
        
        # Testa o método correto
        markdown_content = generator.generate_markdown_content(
            test_analysis, test_query, "2025-01-01", "test_chart.png"
        )
        
        if markdown_content and len(markdown_content) > 100:
            print("✅ Geração de markdown funcionando")
            print(f"📊 Conteúdo gerado: {len(markdown_content)} caracteres")
            return True
        else:
            print("❌ Erro na geração de markdown")
            return False
    
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_sheets_integrator():
    """Testa o integrador com Google Sheets"""
    
    print("\n📱 TESTE DO INTEGRADOR SHEETS")
    print("=" * 40)
    
    try:
        from sheets_integrator import BiscoitaoSheetsIntegrator
        
        integrator = BiscoitaoSheetsIntegrator()
        print("✅ Instância criada com sucesso")
        
        # Testa criação de conversação
        test_query = "Teste de integração"
        conversation = integrator.create_toqan_conversation(test_query)
        
        if conversation and conversation.get('conversation_id'):
            print("✅ Criação de conversação funcionando")
            print(f"🆔 ID gerado: {conversation['conversation_id']}")
            return True
        else:
            print("❌ Erro na criação de conversação")
            return False
    
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def test_end_to_end():
    """Teste completo end-to-end"""
    
    print("\n🚀 TESTE END-TO-END COMPLETO")
    print("=" * 40)
    
    try:
        # Testa fluxo completo
        test_query = "Análise de teste end-to-end"
        
        print(f"🔍 Consulta: {test_query}")
        print("📊 Executando fluxo completo...")
        
        # Usa o integrador para teste completo
        from sheets_integrator import BiscoitaoSheetsIntegrator
        integrator = BiscoitaoSheetsIntegrator()
        
        # Simula processamento
        conversation = integrator.create_toqan_conversation(test_query)
        
        if conversation['conversation_id']:
            print("✅ Conversação criada")
            
            # Teste de formatação de resposta
            mock_response = {
                'success': True,
                'query': test_query,
                'timestamp': datetime.now().isoformat(),
                'files': {
                    'pdf': 'teste.pdf',
                    'markdown': 'teste.md',
                    'chart': 'teste.png'
                },
                'analysis': {
                    'insights': ['📈 Insight de teste'],
                    'summary': 'Teste concluído',
                    'data_points': 10,
                    'viz_type': 'line_chart'
                },
                'conversation_id': conversation['conversation_id']
            }
            
            formatted = integrator.format_sheets_response(mock_response)
            
            if formatted and len(formatted) > 50:
                print("✅ Formatação para Sheets funcionando")
                print(f"📝 Resposta formatada: {len(formatted)} caracteres")
                return True
            else:
                print("❌ Erro na formatação")
                return False
        else:
            print("❌ Falha na criação de conversação")
            return False
    
    except Exception as e:
        print(f"❌ Erro no teste end-to-end: {e}")
        return False

def generate_test_report():
    """Gera relatório de teste"""
    
    print("\n📋 RELATÓRIO FINAL DE TESTES")
    print("=" * 50)
    
    tests = [
        ("Ambiente Python", test_environment),
        ("Estrutura de Arquivos", test_file_structure),
        ("Visual Assistant", test_visual_assistant),
        ("Gerador de PDF", test_pdf_generator),
        ("Integrador Sheets", test_sheets_integrator),
        ("Teste End-to-End", test_end_to_end)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            if results[test_name]:
                passed += 1
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    print(f"\n🏆 RESULTADO FINAL: {passed}/{total} testes passaram")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 SISTEMA TOTALMENTE FUNCIONAL!")
        print("✅ Pronto para uso no Google Sheets")
        print("\n📱 Próximos passos:")
        print("  1. Instalar Flask e dependências web: pip install flask flask-cors")
        print("  2. Executar servidor: python flask_server.py")
        print("  3. Atualizar Google Apps Script com biscoitao.gs")
        print('  4. Testar no Sheets: =perguntarToqan("sua consulta")')
    else:
        print(f"\n⚠️ SISTEMA PARCIALMENTE FUNCIONAL ({passed}/{total})")
        print("🔧 Corrija os testes que falharam antes de usar")
    
    return passed == total

def show_usage_instructions():
    """Mostra instruções de uso"""
    
    print("\n📚 INSTRUÇÕES DE USO DO SISTEMA")
    print("=" * 50)
    
    instructions = """
🚀 COMO USAR O BISCOITÃO v2.0:

1️⃣ PREPARAÇÃO DO AMBIENTE:
   • Certifique-se de que Python está instalado
   • Instale dependências web: pip install flask flask-cors requests
   • Todos os arquivos Python devem estar no mesmo diretório

2️⃣ INICIANDO O SERVIDOR:
   • Execute: python flask_server.py
   • Servidor rodará em: http://localhost:5000
   • Mantenha o servidor rodando durante o uso

3️⃣ CONFIGURAÇÃO DO GOOGLE SHEETS:
   • Copie o código do arquivo biscoitao.gs atualizado
   • Cole no Google Apps Script do seu projeto
   • Configure a chave da API Toqan: configurarChaveToqan("SUA_CHAVE")

4️⃣ USANDO NO GOOGLE SHEETS:
   • Em qualquer célula digite: =perguntarToqan("sua consulta")
   • Exemplos:
     - =perguntarToqan("evolução do preço de jan-24 a jan-25")
     - =perguntarToqan("compare categorias por volume")
     - =perguntarToqan("top 10 produtos por receita")

5️⃣ RESULTADO:
   • O sistema processará a consulta na API Toqan
   • Gerará análise visual com gráficos viridis
   • Criará relatório PDF profissional
   • Retornará informações sobre os arquivos gerados

📊 TIPOS DE VISUALIZAÇÃO SUPORTADOS:
   • Gráficos de linha (tendências temporais)
   • Gráficos de barras (comparações)
   • Histogramas (distribuições)
   • Scatter plots (correlações)
   • Heatmaps (matrizes de correlação)

🎨 TEMA VIRIDIS:
   • Cores: #440154 (roxo) → #31688e (azul) → #35b779 (verde) → #fde725 (amarelo)
   • Otimizado para acessibilidade e impressão
   • Consistent em todos os gráficos

🔧 SOLUÇÃO DE PROBLEMAS:
   • Se erro de conexão: verifique se o servidor Flask está rodando
   • Se erro de API: verifique a chave Toqan no Google Apps Script
   • Se erro de PDF: verifique se pandoc está instalado (opcional)
   • Logs detalhados aparecem no console do servidor Flask

💡 DICAS AVANÇADAS:
   • Use consultas específicas para melhores resultados
   • O sistema detecta automaticamente o melhor tipo de gráfico
   • PDFs são salvos com timestamp para organização
   • Gráficos são salvos separadamente em PNG de alta qualidade
    """
    
    print(instructions)

if __name__ == "__main__":
    print("🧪 SISTEMA DE TESTES - BISCOITÃO v2.0")
    print("=" * 60)
    print("📊 Testando todos os componentes do sistema integrado")
    print(f"⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Executa todos os testes
    system_ok = generate_test_report()
    
    # Mostra instruções de uso
    show_usage_instructions()
    
    print(f"\n⏰ Testes concluídos em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if system_ok:
        print("🎯 Sistema pronto para uso!")
    else:
        print("⚠️ Sistema precisa de ajustes antes do uso.")
