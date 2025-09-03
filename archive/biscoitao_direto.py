"""
Sistema Biscoitão - Gerador Direto via Comando
Executa análise completa diretamente via linha de comando
"""

import sys
import os
from datetime import datetime
from sheets_integrator import BiscoitaoSheetsIntegrator

def main():
    print("🚀 BISCOITÃO v2.0 - GERADOR DIRETO")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("📋 Uso: python biscoitao_direto.py 'sua consulta'")
        print()
        print("📊 Exemplos:")
        print("  python biscoitao_direto.py 'evolução do preço de jan-24 a jan-25'")
        print("  python biscoitao_direto.py 'compare categorias por volume'")
        print("  python biscoitao_direto.py 'top 10 produtos por receita'")
        print()
        print("✨ Este comando gera:")
        print("  • 📊 Gráfico viridis em PNG")
        print("  • 📝 Relatório Markdown profissional")
        print("  • 📄 PDF (se disponível)")
        print("  • 💡 Insights automáticos")
        print("  • 📱 Resposta formatada para Sheets")
        print()
        sys.exit(1)
    
    # Obtém consulta dos argumentos
    query = " ".join(sys.argv[1:])
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"🔍 Consulta: {query}")
    print(f"⏰ Timestamp: {timestamp}")
    print()
    
    try:
        # Usa o integrador existente
        integrator = BiscoitaoSheetsIntegrator()
        
        print("📊 Iniciando processamento completo...")
        
        # Cria conversação
        conversation = integrator.create_toqan_conversation(query)
        conversation_id = conversation['conversation_id']
        
        print(f"🆔 Conversação criada: {conversation_id}")
        
        # Processa consulta completa
        result = integrator.process_sheets_query(query, conversation_id)
        
        if result['success']:
            print("\n" + "=" * 60)
            print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print("=" * 60)
            
            print(f"\n📊 ARQUIVOS GERADOS:")
            print(f"  • 📄 PDF: {result['files']['pdf'] if result['files']['pdf'] else 'Não disponível'}")
            print(f"  • 📝 Markdown: {result['files']['markdown']}")
            print(f"  • 📊 Gráfico: {result['files']['chart']}")
            
            print(f"\n📈 ANÁLISE:")
            print(f"  • Registros: {result['analysis']['data_points']}")
            print(f"  • Tipo: {result['analysis']['viz_type'].replace('_', ' ').title()}")
            print(f"  • Insights: {len(result['analysis']['insights'])}")
            
            print(f"\n💡 PRINCIPAIS INSIGHTS:")
            for i, insight in enumerate(result['analysis']['insights'][:3], 1):
                clean_insight = insight.replace('📈', '').replace('📉', '').replace('📊', '').replace('🔝', '').replace('🔻', '').replace('⚠️', '').replace('🥇', '').strip()
                print(f"  {i}. {clean_insight}")
            
            print(f"\n💬 RESUMO:")
            print(f"  {result['analysis']['summary']}")
            
            # Gera resposta formatada para Google Sheets
            sheets_response = integrator.format_sheets_response(result)
            
            print("\n" + "=" * 60)
            print("📱 RESPOSTA FORMATADA PARA GOOGLE SHEETS:")
            print("=" * 60)
            print(sheets_response)
            print("=" * 60)
            
            # Salva resposta em arquivo para cópia fácil
            sheets_file = f"resposta_sheets_{timestamp}.txt"
            with open(sheets_file, 'w', encoding='utf-8') as f:
                f.write(sheets_response)
            
            print(f"\n📋 Resposta salva em: {sheets_file}")
            print("   (Copie este conteúdo para o Google Sheets se necessário)")
            
            # Comando para abrir arquivos
            print(f"\n🔧 COMANDOS PARA ABRIR ARQUIVOS:")
            if result['files']['pdf']:
                print(f"  • PDF: start {result['files']['pdf']}")
            print(f"  • Markdown: notepad {result['files']['markdown']}")
            print(f"  • Gráfico: start {result['files']['chart']}")
            
            return True
            
        else:
            print(f"\n❌ ERRO NO PROCESSAMENTO:")
            print(f"   {result['error']}")
            return False
    
    except Exception as e:
        print(f"\n❌ ERRO GERAL:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    print(f"\n⏰ Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if success:
        print("🎉 Sistema executado com sucesso!")
        print("\n📚 PRÓXIMOS PASSOS:")
        print("  1. Verifique os arquivos gerados")
        print("  2. Copie a resposta formatada para o Google Sheets (se necessário)")
        print("  3. Use os insights gerados em suas análises")
    else:
        print("⚠️ Execução finalizada com erros.")
        print("\n🔧 VERIFIQUE:")
        print("  • Conexão com banco de dados")
        print("  • Sintaxe da consulta")
        print("  • Dependências Python instaladas")
