"""
Biscoitão Report Generator - Script Principal
Sistema consolidado para gerar relatórios HTML profissionais com análise de dados OLX
"""

import sys
import os
from datetime import datetime

# Adiciona src ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_path)

def main():
    """Função principal do gerador de relatórios"""
    print("🤖 BISCOITÃO REPORT GENERATOR v2.0")
    print("=" * 50)
    print("Sistema Inteligente de Análise de Dados OLX")
    print("=" * 50)
    
    try:
        # Import dos módulos reorganizados
        from generators.html_generator import HTMLReportGenerator
        
        # Inicializa gerador
        generator = HTMLReportGenerator()
        
        # Instruções de exemplo para teste
        sample_instructions = [
            "Mostra a receita total por mês em 2024",
            "Análise de faturamento mensal",
            "Evolução da receita de janeiro a dezembro",
            "Receita total de 2024"
        ]
        
        print("📋 Instruções de exemplo disponíveis:")
        for i, instruction in enumerate(sample_instructions, 1):
            print(f"  {i}. {instruction}")
        
        print("\n" + "=" * 50)
        
        # Solicita instrução do usuário
        print("💡 Digite sua instrução para análise:")
        print("   (ou 'sair' para encerrar)")
        
        while True:
            user_input = input("\n🔍 Instrução: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit', '']:
                print("👋 Encerrando Biscoitão...")
                break
            
            # Se for número, usa instrução de exemplo
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(sample_instructions):
                    user_input = sample_instructions[index]
                    print(f"📝 Usando instrução: {user_input}")
                else:
                    print("❌ Número inválido. Tente novamente.")
                    continue
            
            # Gera relatório
            print(f"\n🚀 Processando: {user_input}")
            print("-" * 40)
            
            try:
                result = generator.generate_html_report(user_input, auto_open=True)
                
                if result:
                    print("\n✅ RELATÓRIO GERADO COM SUCESSO!")
                    print(f"📄 Arquivo HTML: {os.path.basename(result['html_file'])}")
                    if result.get('chart_file'):
                        print(f"📊 Gráfico: {os.path.basename(result['chart_file'])}")
                    print(f"🕐 Timestamp: {result['timestamp']}")
                    print("🌐 Relatório aberto automaticamente no navegador!")
                else:
                    print("❌ Falha na geração do relatório")
                
            except Exception as e:
                print(f"❌ Erro durante geração: {str(e)}")
                print("💡 Verifique se as dependências estão instaladas")
            
            print("\n" + "=" * 50)
    
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 Possíveis soluções:")
        print("1. Verifique se os módulos estão na estrutura correta")
        print("2. Instale as dependências: pip install pandas matplotlib seaborn")
        print("3. Configure as variáveis de ambiente no arquivo .env")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()

def test_imports():
    """Testa se todos os imports estão funcionando"""
    print("🔧 Testando imports do sistema...")
    
    try:
        print("  ✓ Importando core.query...")
        from core.query import execute_query
        
        print("  ✓ Importando generators.visual_assistant...")
        from generators.visual_assistant import IntelligentReportGenerator
        
        print("  ✓ Importando generators.html_generator...")
        from generators.html_generator import HTMLReportGenerator
        
        print("✅ Todos os imports funcionando!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro nos imports: {e}")
        return False

def show_project_structure():
    """Mostra a estrutura do projeto reorganizado"""
    print("📁 ESTRUTURA DO PROJETO BISCOITÃO v2.0")
    print("=" * 40)
    
    structure = """
    Biscoitão/
    ├── src/
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── query.py           # Conexão database
    │   │   ├── data_processor.py  # Processamento dados
    │   │   └── schema_utils.py    # Utilitários schema
    │   ├── generators/
    │   │   ├── __init__.py
    │   │   ├── html_generator.py      # Geração HTML
    │   │   └── visual_assistant.py    # Gráficos e insights
    │   ├── integrations/
    │   │   ├── __init__.py
    │   │   └── apps_script.py     # Integração Google
    │   └── api/
    │       ├── __init__.py
    │       └── cloud_api.py       # API para cloud
    ├── scripts/
    │   └── html_report_generator.py   # Script principal
    ├── output/
    │   ├── reports/               # Relatórios HTML
    │   └── charts/                # Gráficos PNG
    ├── docs/
    │   └── arquitetura.md
    ├── tests/
    └── requirements.txt
    """
    
    print(structure)

if __name__ == "__main__":
    print("🎯 ESCOLHA UMA OPÇÃO:")
    print("1. 🚀 Executar Gerador de Relatórios")
    print("2. 🔧 Testar Imports")
    print("3. 📁 Mostrar Estrutura do Projeto")
    print("4. ❌ Sair")
    
    choice = input("\n👉 Opção: ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        test_imports()
    elif choice == "3":
        show_project_structure()
    elif choice == "4":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida. Executando gerador...")
        main()
