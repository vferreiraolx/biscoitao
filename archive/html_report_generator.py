"""
Gerador de Relatórios HTML Profissionais - Biscoitão
Sistema para consolidar análises em relatórios elegantes com abertura automática
"""

import sys
import os
import webbrowser
from datetime import datetime
from visual_assistant import IntelligentReportGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

class ProfessionalHTMLReportGenerator:
    """Gerador de relatórios HTML profissionais e elegantes"""
    
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
    
    def create_chart_base64(self, data, viz_type, instruction):
        """Cria gráfico em base64 para embedding no HTML"""
        
        # Figura com fundo transparente
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
        
        if viz_type == 'line_chart':
            self._create_professional_line_chart(ax, data, instruction)
        elif viz_type == 'bar_chart':
            self._create_professional_bar_chart(ax, data, instruction)
        else:
            self._create_professional_line_chart(ax, data, instruction)
        
        # Salva em base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', 
                   facecolor='white', edgecolor='none', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return image_base64
    
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
    
    def generate_html_template(self):
        """Gera template HTML profissional e elegante"""
        template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise - Biscoitão</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .header .timestamp {{
            font-size: 0.95em;
            opacity: 0.8;
            margin-top: 15px;
        }}
        
        .section {{
            background: white;
            margin-bottom: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        .section-header {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px 30px;
            font-size: 1.3em;
            font-weight: 500;
        }}
        
        .section-content {{
            padding: 30px;
        }}
        
        .query-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            font-style: italic;
            font-size: 1.1em;
            color: #495057;
        }}
        
        .chart-container {{
            text-align: center;
            margin: 30px 0;
        }}
        
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .insights {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        
        .insight-card {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #35b779;
        }}
        
        .insight-card .icon {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .insight-card .text {{
            font-size: 1em;
            line-height: 1.5;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
        }}
        
        .data-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 500;
        }}
        
        .data-table td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .data-table tr:hover {{
            background: #e3f2fd;
        }}
        
        .summary-box {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 10px;
            margin: 25px 0;
            border-left: 4px solid #fde725;
        }}
        
        .summary-box .title {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #d35400;
        }}
        
        .summary-box .content {{
            font-size: 1em;
            line-height: 1.6;
            color: #5d4e75;
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .section-content {{
                padding: 20px;
            }}
            
            .insights {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Relatório de Análise</h1>
            <div class="subtitle">Sistema Biscoitão - Análise Conversacional com Visualização</div>
            <div class="timestamp">Gerado em: {timestamp}</div>
        </div>
        
        <div class="section">
            <div class="section-header">
                📝 Consulta Analisada
            </div>
            <div class="section-content">
                <div class="query-box">
                    "{query}"
                </div>
            </div>
        </div>
        
        {stats_section}
        
        <div class="section">
            <div class="section-header">
                📊 Visualização dos Dados
            </div>
            <div class="section-content">
                <div class="chart-container">
                    <img src="data:image/png;base64,{chart_base64}" alt="Gráfico de Análise">
                </div>
            </div>
        </div>
        
        {insights_section}
        
        <div class="section">
            <div class="section-header">
                📋 Dados Detalhados
            </div>
            <div class="section-content">
                {data_table}
            </div>
        </div>
        
        <div class="section">
            <div class="section-header">
                💬 Resumo Executivo
            </div>
            <div class="section-content">
                <div class="summary-box">
                    <div class="title">Conclusão da Análise</div>
                    <div class="content">{summary}</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Relatório gerado automaticamente pelo Sistema Biscoitão</p>
            <p>© 2025 - Análise Conversacional com IA</p>
        </div>
    </div>
</body>
</html>'''
        return template
    
    def create_data_table_html(self, data):
        """Cria tabela HTML elegante dos dados"""
        if data.empty:
            return "<p>Nenhum dado disponível.</p>"
        
        # Limita a 20 linhas para relatório mais limpo
        display_data = data.head(20)
        
        html = '<table class="data-table">\n<thead>\n<tr>\n'
        
        # Cabeçalhos
        for col in display_data.columns:
            formatted_col = col.replace('_', ' ').title()
            html += f'<th>{formatted_col}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        # Dados
        for _, row in display_data.iterrows():
            html += '<tr>\n'
            for col in display_data.columns:
                value = row[col]
                if pd.isna(value):
                    formatted_value = '-'
                elif isinstance(value, float):
                    formatted_value = f'{value:,.2f}' if value > 1 else f'{value:.3f}'
                else:
                    formatted_value = str(value)
                html += f'<td>{formatted_value}</td>\n'
            html += '</tr>\n'
        
        html += '</tbody>\n</table>\n'
        
        if len(data) > 20:
            html += f'<p style="margin-top: 15px; color: #7f8c8d; font-style: italic;">Mostrando 20 de {len(data)} registros totais.</p>'
        
        return html
    
    def create_insights_html(self, insights):
        """Cria seção de insights em HTML"""
        if not insights:
            return ""
        
        html = '''
        <div class="section">
            <div class="section-header">
                🔍 Insights Automáticos
            </div>
            <div class="section-content">
                <div class="insights">
        '''
        
        for insight in insights:
            # Extrai ícone do insight
            icon = insight[:2] if insight.startswith(('📈', '📉', '📊', '🔝', '🔻', '⚠️', '🥇')) else '💡'
            text = insight[2:].strip() if insight.startswith(('📈', '📉', '📊', '🔝', '🔻', '⚠️', '🥇')) else insight
            
            html += f'''
                    <div class="insight-card">
                        <div class="icon">{icon}</div>
                        <div class="text">{text}</div>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
        </div>
        '''
        
        return html
    
    def create_stats_section(self, data, viz_type):
        """Cria seção de estatísticas resumidas"""
        if data.empty:
            return ""
        
        stats = []
        
        # Estatísticas baseadas no tipo de dados
        if viz_type == 'line_chart' and 'avg_value' in data.columns:
            values = data['avg_value'].dropna()
            if len(values) > 0:
                stats.append(('Períodos', len(values)))
                stats.append(('Valor Médio', f'R$ {values.mean():.2f}'))
                stats.append(('Valor Máximo', f'R$ {values.max():.2f}'))
                stats.append(('Valor Mínimo', f'R$ {values.min():.2f}'))
        
        elif viz_type == 'bar_chart':
            value_cols = [col for col in data.columns if 'avg_' in col or 'count' in col or 'value' in col]
            if value_cols:
                values = data[value_cols[0]].dropna()
                stats.append(('Categorias', len(data)))
                stats.append(('Total Geral', f'{values.sum():,.0f}'))
                stats.append(('Média por Categoria', f'{values.mean():.1f}'))
                stats.append(('Maior Valor', f'{values.max():,.0f}'))
        
        if not stats:
            return ""
        
        html = '''
        <div class="section">
            <div class="section-header">
                📊 Estatísticas Resumidas
            </div>
            <div class="section-content">
                <div class="stats-grid">
        '''
        
        for label, value in stats:
            html += f'''
                    <div class="stat-card">
                        <div class="number">{value}</div>
                        <div class="label">{label}</div>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
        </div>
        '''
        
        return html
    
    def generate_professional_report(self, instruction, table_name="dw.monetization_total"):
        """Gera relatório HTML profissional completo"""
        
        print(f"📄 Gerando relatório HTML profissional para: {instruction}")
        print("=" * 60)
        
        # Gera análise visual
        result = self.visual_generator.generate_complete_report(instruction, table_name)
        
        if not result:
            print("❌ Não foi possível gerar análise para o relatório HTML.")
            return None
        
        print("✅ Análise concluída, gerando HTML...")
        
        # Cria gráfico em base64
        chart_base64 = self.create_chart_base64(
            result['data'], 
            result['viz_type'], 
            instruction
        )
        
        # Monta componentes HTML
        data_table_html = self.create_data_table_html(result['data'])
        insights_html = self.create_insights_html(result['insights'])
        stats_html = self.create_stats_section(result['data'], result['viz_type'])
        
        # Template completo
        html_content = self.generate_html_template().format(
            timestamp=datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
            query=instruction,
            chart_base64=chart_base64,
            data_table=data_table_html,
            insights_section=insights_html,
            stats_section=stats_html,
            summary=result['response']
        )
        
        # Salva arquivo HTML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_biscoitao_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Relatório HTML gerado: {filename}")
        
        # Abre automaticamente no navegador
        try:
            file_path = os.path.abspath(filename)
            webbrowser.open(f'file://{file_path}')
            print("🌐 Relatório aberto no navegador automaticamente!")
        except Exception as e:
            print(f"⚠️ Não foi possível abrir automaticamente: {e}")
            print(f"📁 Abra manualmente: {os.path.abspath(filename)}")
        
        return {
            'filename': filename,
            'full_path': os.path.abspath(filename),
            'analysis_result': result
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python html_report_generator.py 'sua pergunta para análise'")
        print("Exemplos:")
        print("  'Evolução da média do preço de jan-24 a jan-25'")
        print("  'Compare as categorias por faturamento'")
        print("  'Tendência de crescimento nos últimos meses'")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    
    try:
        report_generator = ProfessionalHTMLReportGenerator()
        result = report_generator.generate_professional_report(instruction)
        
        if result:
            print("\n🎯 Relatório HTML profissional gerado com sucesso!")
            print(f"📁 Arquivo: {result['filename']}")
            print(f"🌐 Localização: {result['full_path']}")
        else:
            print("\n❌ Não foi possível gerar o relatório HTML.")
    
    except Exception as e:
        print(f"❌ Erro na geração do relatório: {e}")
        import traceback
        traceback.print_exc()
