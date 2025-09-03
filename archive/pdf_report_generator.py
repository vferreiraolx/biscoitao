"""
Gerador de Relatórios PDF via Markdown - Biscoitão
Sistema para converter análises em PDF profissionais via Markdown
"""

import sys
import os
import webbrowser
import subprocess
from datetime import datetime
from visual_assistant import IntelligentReportGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO
import warnings
import tempfile

warnings.filterwarnings("ignore")

class ProfessionalPDFReportGenerator:
    """Gerador de relatórios PDF profissionais via Markdown"""
    
    def __init__(self):
        self.visual_generator = IntelligentReportGenerator()
        # Configuração da paleta viridis profissional
        plt.style.use('default')
        self.setup_viridis_theme()
    
    def setup_viridis_theme(self):
        """Configura tema viridis profissional"""
        # Paleta viridis customizada
        viridis_colors = ['#440154', '#31688e', '#35b779', '#fde725']
        sns.set_palette(viridis_colors)
        
        # Configurações matplotlib para gráficos profissionais
        plt.rcParams.update({
            'figure.figsize': (12, 7),
            'figure.dpi': 100,
            'savefig.dpi': 300,
            'font.size': 11,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'axes.grid': True,
            'grid.alpha': 0.3,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.spines.left': True,
            'axes.spines.bottom': True,
            'axes.linewidth': 0.8,
            'grid.linewidth': 0.5
        })
    
    def create_chart_file(self, data, viz_type, instruction, timestamp):
        """Cria arquivo de gráfico para embedding no Markdown"""
        
        # Figura com fundo transparente
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
        
        if viz_type == 'line_chart':
            self._create_professional_line_chart(ax, data, instruction)
        elif viz_type == 'bar_chart':
            self._create_professional_bar_chart(ax, data, instruction)
        else:
            self._create_professional_line_chart(ax, data, instruction)
        
        # Salva arquivo PNG
        chart_filename = f"chart_{viz_type}_{timestamp}.png"
        plt.savefig(chart_filename, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', dpi=300)
        plt.close(fig)
        
        return chart_filename
    
    def _create_professional_line_chart(self, ax, data, instruction):
        """Cria gráfico de linha profissional com tema viridis"""
        
        if 'year' in data.columns and 'month' in data.columns:
            data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))
            x_data = data['date']
            x_label = 'Período'
        else:
            x_data = range(len(data))
            x_label = 'Sequência'
        
        value_cols = [col for col in data.columns if 'avg_' in col or 'value' in col]
        y_col = value_cols[0] if value_cols else data.columns[1]
        
        # Linha principal com cor viridis
        ax.plot(x_data, data[y_col], color='#35b779', linewidth=3, 
               marker='o', markersize=6, markerfacecolor='#440154', 
               markeredgecolor='white', markeredgewidth=1.5)
        
        # Área sob a curva com transparência
        ax.fill_between(x_data, data[y_col], alpha=0.1, color='#35b779')
        
        # Linha de tendência se há múltiplos pontos
        if len(data) > 2:
            import numpy as np
            z = np.polyfit(range(len(data)), data[y_col], 1)
            p = np.poly1d(z)
            ax.plot(x_data, p(range(len(data))), '--', 
                   color='#fde725', linewidth=2, alpha=0.8, label='Tendência')
            ax.legend(frameon=False)
        
        ax.set_xlabel(x_label, fontweight='medium')
        ax.set_ylabel(self._get_metric_label(y_col), fontweight='medium')
        ax.set_title(self._generate_professional_title(instruction), 
                    fontweight='bold', pad=20)
        
        # Formatação dos eixos
        if 'date' in locals():
            ax.tick_params(axis='x', rotation=45)
        
        # Grid sutil
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
    
    def _create_professional_bar_chart(self, ax, data, instruction):
        """Cria gráfico de barras profissional com tema viridis"""
        
        cat_col = data.columns[0]
        value_cols = [col for col in data.columns if 'avg_' in col or 'value' in col or 'count' in col]
        value_col = value_cols[0] if value_cols else data.columns[1]
        
        # Limita para melhor visualização
        if len(data) > 12:
            data = data.head(12)
        
        # Gradiente viridis para as barras
        colors = plt.cm.viridis(range(len(data)))
        
        bars = ax.bar(range(len(data)), data[value_col], 
                     color=colors, alpha=0.8, width=0.7)
        
        # Valores nas barras com formatação elegante
        for i, (bar, value) in enumerate(zip(bars, data[value_col])):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + max(data[value_col])*0.01,
                   f'{value:,.0f}' if value > 1000 else f'{value:.1f}',
                   ha='center', va='bottom', fontweight='medium', fontsize=10)
        
        ax.set_title(self._generate_professional_title(instruction), 
                    fontweight='bold', pad=20)
        ax.set_xlabel(cat_col.replace('_', ' ').title(), fontweight='medium')
        ax.set_ylabel(self._get_metric_label(value_col), fontweight='medium')
        
        # Labels do eixo X com rotação inteligente
        labels = [str(cat)[:20] + '...' if len(str(cat)) > 20 else str(cat) 
                 for cat in data[cat_col]]
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        
        # Grid apenas no eixo Y
        ax.grid(True, alpha=0.3, axis='y', linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
    
    def _generate_professional_title(self, instruction):
        """Gera título profissional para o gráfico"""
        if 'evolução' in instruction.lower() or 'tendência' in instruction.lower():
            return 'Análise de Evolução Temporal'
        elif 'compar' in instruction.lower():
            return 'Análise Comparativa'
        elif 'distribuição' in instruction.lower():
            return 'Análise de Distribuição'
        else:
            return 'Análise de Dados'
    
    def _get_metric_label(self, column_name):
        """Retorna label formatado para a métrica"""
        if 'price' in column_name.lower():
            return 'Valor Médio (R$)'
        elif 'count' in column_name.lower():
            return 'Quantidade'
        elif 'avg_' in column_name:
            return 'Média'
        else:
            return column_name.replace('_', ' ').title()
    
    def generate_markdown_content(self, result, instruction, timestamp, chart_filename):
        """Gera conteúdo Markdown profissional"""
        
        markdown_content = f"""# Relatório de Análise - Biscoitão

**Sistema de Business Intelligence Conversacional**

---

## 📋 Informações do Relatório

- **Data de Geração:** {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}
- **Consulta Analisada:** "{instruction}"
- **Timestamp:** {timestamp}
- **Tipo de Visualização:** {result['viz_type'].replace('_', ' ').title()}

---

## 📊 Visualização dos Dados

![Gráfico de Análise]({chart_filename})

---

## 📈 Estatísticas Resumidas

"""
        
        # Adiciona estatísticas baseadas no tipo de dados
        if result['viz_type'] == 'line_chart' and 'avg_value' in result['data'].columns:
            values = result['data']['avg_value'].dropna()
            if len(values) > 0:
                markdown_content += f"""
| Métrica | Valor |
|---------|-------|
| **Períodos Analisados** | {len(values)} |
| **Valor Médio** | R$ {values.mean():.2f} |
| **Valor Máximo** | R$ {values.max():.2f} |
| **Valor Mínimo** | R$ {values.min():.2f} |
| **Variação Total** | {((values.iloc[-1] - values.iloc[0]) / values.iloc[0] * 100):.1f}% |

"""
        
        elif result['viz_type'] == 'bar_chart':
            value_cols = [col for col in result['data'].columns if 'avg_' in col or 'count' in col or 'value' in col]
            if value_cols:
                values = result['data'][value_cols[0]].dropna()
                markdown_content += f"""
| Métrica | Valor |
|---------|-------|
| **Categorias** | {len(result['data'])} |
| **Total Geral** | {values.sum():,.0f} |
| **Média por Categoria** | {values.mean():.1f} |
| **Maior Valor** | {values.max():,.0f} |

"""
        
        # Insights Automáticos
        if result['insights']:
            markdown_content += """## 🔍 Insights Automáticos

"""
            for insight in result['insights']:
                # Remove emojis dos insights para melhor formatação PDF
                clean_insight = insight[2:].strip() if insight.startswith(('📈', '📉', '📊', '🔝', '🔻', '⚠️', '🥇')) else insight
                markdown_content += f"- {clean_insight}\n"
        
        markdown_content += "\n---\n\n"
        
        # Dados Detalhados (amostra)
        markdown_content += """## 📋 Dados Detalhados

"""
        
        # Limita a 15 linhas para o PDF
        display_data = result['data'].head(15)
        
        if not display_data.empty:
            # Cabeçalho da tabela
            headers = [col.replace('_', ' ').title() for col in display_data.columns]
            markdown_content += "| " + " | ".join(headers) + " |\n"
            markdown_content += "| " + " | ".join(['---'] * len(headers)) + " |\n"
            
            # Dados da tabela
            for _, row in display_data.iterrows():
                formatted_row = []
                for col in display_data.columns:
                    value = row[col]
                    if pd.isna(value):
                        formatted_value = '-'
                    elif isinstance(value, float):
                        formatted_value = f'{value:,.2f}' if value > 1 else f'{value:.3f}'
                    else:
                        formatted_value = str(value)
                    formatted_row.append(formatted_value)
                markdown_content += "| " + " | ".join(formatted_row) + " |\n"
            
            if len(result['data']) > 15:
                markdown_content += f"\n*Mostrando 15 de {len(result['data'])} registros totais.*\n"
        
        markdown_content += "\n---\n\n"
        
        # Resumo Executivo
        markdown_content += f"""## 💼 Resumo Executivo

{result['response']}

---

## 🔧 Informações Técnicas

- **Query SQL Executada:** 
```sql
{result['query']}
```

- **Sistema:** Biscoitão v2.0
- **Engine:** Trino/Hive
- **Visualização:** Matplotlib + Seaborn (Paleta Viridis)

---

*Relatório gerado automaticamente pelo Sistema Biscoitão*  
*© 2025 - Análise Conversacional com IA*
"""
        
        return markdown_content
    
    def convert_markdown_to_pdf(self, markdown_file, pdf_file):
        """Converte Markdown para PDF usando pandoc"""
        
        try:
            # Verifica se pandoc está instalado
            subprocess.run(['pandoc', '--version'], 
                         capture_output=True, check=True)
            
            # Converte MD para PDF com configurações profissionais
            cmd = [
                'pandoc',
                markdown_file,
                '-o', pdf_file,
                '--pdf-engine=wkhtmltopdf',
                '--margin-top=20mm',
                '--margin-bottom=20mm',
                '--margin-left=20mm',
                '--margin-right=20mm',
                '--enable-local-file-access'
            ]
            
            subprocess.run(cmd, check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro na conversão com pandoc: {e}")
            return False
        except FileNotFoundError:
            print("⚠️ Pandoc não encontrado. Tentando conversão alternativa...")
            return self._convert_with_alternative_method(markdown_file, pdf_file)
    
    def _convert_with_alternative_method(self, markdown_file, pdf_file):
        """Método alternativo de conversão usando markdown2 + weasyprint"""
        
        try:
            import markdown2
            from weasyprint import HTML
            
            # Lê o markdown
            with open(markdown_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Converte para HTML
            html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
            
            # Adiciona CSS básico
            styled_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 2cm; line-height: 1.6; }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
                    h2 {{ color: #34495e; margin-top: 2em; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    img {{ max-width: 100%; height: auto; }}
                    code {{ background-color: #f4f4f4; padding: 2px 4px; }}
                    pre {{ background-color: #f4f4f4; padding: 1em; overflow-x: auto; }}
                </style>
            </head>
            <body>
            {html_content}
            </body>
            </html>
            """
            
            # Converte HTML para PDF
            HTML(string=styled_html).write_pdf(pdf_file)
            return True
            
        except ImportError:
            print("❌ Bibliotecas de conversão não encontradas.")
            print("   Instale: pip install markdown2 weasyprint")
            return False
        except Exception as e:
            print(f"❌ Erro na conversão alternativa: {e}")
            return False
    
    def generate_professional_pdf_report(self, instruction, table_name="dw.monetization_total"):
        """Gera relatório PDF profissional completo"""
        
        print(f"📄 Gerando relatório PDF via Markdown para: {instruction}")
        print("=" * 60)
        
        # Gera análise visual
        result = self.visual_generator.generate_complete_report(instruction, table_name)
        
        if not result:
            print("❌ Não foi possível gerar análise para o relatório PDF.")
            return None
        
        print("✅ Análise concluída, gerando Markdown...")
        
        # Timestamp para arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Cria gráfico como arquivo
        chart_filename = self.create_chart_file(
            result['data'], 
            result['viz_type'], 
            instruction,
            timestamp
        )
        
        # Gera conteúdo Markdown
        markdown_content = self.generate_markdown_content(
            result, instruction, timestamp, chart_filename
        )
        
        # Salva arquivo Markdown
        markdown_filename = f"relatorio_biscoitao_{timestamp}.md"
        with open(markdown_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📝 Arquivo Markdown gerado: {markdown_filename}")
        
        # Converte para PDF
        pdf_filename = f"relatorio_biscoitao_{timestamp}.pdf"
        print(f"📄 Convertendo para PDF: {pdf_filename}")
        
        pdf_success = self.convert_markdown_to_pdf(markdown_filename, pdf_filename)
        
        if pdf_success:
            print(f"✅ Relatório PDF gerado: {pdf_filename}")
            
            # Abre PDF automaticamente
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_filename)
                else:  # Linux/Mac
                    subprocess.run(['xdg-open', pdf_filename])
                print("📖 PDF aberto automaticamente!")
            except Exception as e:
                print(f"⚠️ Não foi possível abrir automaticamente: {e}")
                print(f"📁 Abra manualmente: {os.path.abspath(pdf_filename)}")
        else:
            print("⚠️ Falha na conversão para PDF. Markdown disponível.")
            pdf_filename = None
        
        return {
            'markdown_file': markdown_filename,
            'pdf_file': pdf_filename,
            'chart_file': chart_filename,
            'analysis_result': result,
            'timestamp': timestamp
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pdf_report_generator.py 'sua pergunta para análise'")
        print("Exemplos:")
        print("  'Evolução da média do preço de jan-24 a jan-25'")
        print("  'Compare as categorias por faturamento'")
        print("  'Tendência de crescimento nos últimos meses'")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    
    try:
        report_generator = ProfessionalPDFReportGenerator()
        result = report_generator.generate_professional_pdf_report(instruction)
        
        if result:
            print("\n🎯 Relatório PDF profissional gerado com sucesso!")
            print(f"📝 Markdown: {result['markdown_file']}")
            if result['pdf_file']:
                print(f"📄 PDF: {result['pdf_file']}")
            print(f"📊 Gráfico: {result['chart_file']}")
        else:
            print("\n❌ Não foi possível gerar o relatório PDF.")
    
    except Exception as e:
        print(f"❌ Erro na geração do relatório: {e}")
        import traceback
        traceback.print_exc()
