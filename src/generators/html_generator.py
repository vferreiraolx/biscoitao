"""
Gerador de Relatórios HTML Profissionais - Biscoitão
Sistema para consolidar análises em relatórios elegantes com abertura automática
"""

import sys
import os
import webbrowser
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
from io import BytesIO
import warnings

# Imports relativos para nova estrutura
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.generators.visual_assistant import IntelligentReportGenerator

warnings.filterwarnings("ignore")

class HTMLReportGenerator:
    """Gerador de relatórios HTML profissionais e elegantes"""
    
    def __init__(self):
        self.visual_generator = IntelligentReportGenerator()
        # Configuração da paleta viridis profissional
        plt.style.use('default')
        self.setup_viridis_theme()
    
    def setup_viridis_theme(self):
        """Configura tema viridis profissional"""
        # Cores viridis para uso consistente
        self.viridis_colors = ['#440154', '#31688e', '#35b779', '#fde725']
        
        # Configuração global do matplotlib
        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': '#440154',
            'axes.linewidth': 1.2,
            'axes.labelcolor': '#333333',
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
            'xtick.color': '#666666',
            'ytick.color': '#666666',
            'font.size': 10,
            'font.family': 'sans-serif'
        })
        
        # Configuração do seaborn
        sns.set_palette(self.viridis_colors)
    
    def generate_html_report(self, instruction, auto_open=True):
        """
        Gera relatório HTML completo com análise visual e insights
        
        Args:
            instruction (str): Instrução para análise
            auto_open (bool): Se deve abrir automaticamente no navegador
            
        Returns:
            dict: Resultado com caminhos dos arquivos gerados
        """
        print(f"📊 Gerando relatório HTML para: {instruction}")
        print("=" * 60)
        
        # Gera análise visual
        result = self.visual_generator.generate_complete_report(instruction)
        
        if not result:
            print("❌ Não foi possível gerar análise visual")
            return None
        
        # Gera HTML consolidado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_filename = f"relatorio_biscoitao_{timestamp}.html"
        
        html_content = self._create_html_content(result, instruction, timestamp)
        
        # Salva HTML
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'reports')
        os.makedirs(output_dir, exist_ok=True)
        html_path = os.path.join(output_dir, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Relatório HTML gerado: {html_filename}")
        
        # Abre automaticamente se solicitado
        if auto_open:
            webbrowser.open(f'file://{os.path.abspath(html_path)}')
            print(f"🌐 Relatório aberto no navegador")
        
        return {
            'html_file': html_path,
            'chart_file': result.get('chart_file'),
            'analysis_result': result,
            'timestamp': timestamp
        }
    
    def _create_html_content(self, result, instruction, timestamp):
        """Cria conteúdo HTML do relatório"""
        
        # Converte gráfico para base64
        chart_base64 = ""
        if result.get('chart_file') and os.path.exists(result['chart_file']):
            with open(result['chart_file'], 'rb') as f:
                chart_base64 = base64.b64encode(f.read()).decode()
        
        # Template HTML com design profissional
        html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Biscoitão - {datetime.now().strftime('%d/%m/%Y %H:%M')}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>📊 Relatório Biscoitão</h1>
            <p class="subtitle">Análise Inteligente de Dados OLX</p>
        </header>
        
        <div class="metadata">
            <div class="metadata-item">
                <strong>📅 Data:</strong> {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
            </div>
            <div class="metadata-item">
                <strong>🔍 Consulta:</strong> {instruction}
            </div>
            <div class="metadata-item">
                <strong>📊 Registros:</strong> {len(result.get('data', []))} dados analisados
            </div>
            <div class="metadata-item">
                <strong>📈 Tipo:</strong> {result.get('viz_type', 'N/A').replace('_', ' ').title()}
            </div>
        </div>
        
        <div class="content-grid">
            <div class="chart-section">
                <h2>📈 Visualização</h2>
                {f'<img src="data:image/png;base64,{chart_base64}" alt="Gráfico de Análise" class="chart-image">' if chart_base64 else '<p class="no-chart">Gráfico não disponível</p>'}
            </div>
            
            <div class="insights-section">
                <h2>💡 Insights Principais</h2>
                <ul class="insights-list">
                    {''.join([f'<li>{insight}</li>' for insight in result.get('insights', [])])}
                </ul>
            </div>
        </div>
        
        <div class="summary-section">
            <h2>📋 Resumo da Análise</h2>
            <p class="summary-text">{result.get('response', 'Análise não disponível')}</p>
        </div>
        
        <div class="data-section">
            <h2>📊 Dados Analisados</h2>
            <div class="data-table-container">
                {self._format_data_table(result.get('data', []))}
            </div>
        </div>
        
        <footer class="footer">
            <p>🤖 Gerado automaticamente pelo Sistema Biscoitão v2.0</p>
            <p>📧 OLX Data Team | 🕐 {timestamp}</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html_template
    
    def _get_css_styles(self):
        """Retorna estilos CSS profissionais com tema viridis"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #440154 0%, #31688e 25%, #35b779 75%, #fde725 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .header {
            background: linear-gradient(135deg, #440154, #31688e);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .metadata {
            background: #f8f9fa;
            padding: 20px;
            border-left: 5px solid #35b779;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .metadata-item {
            padding: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }
        
        .chart-section, .insights-section {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-top: 4px solid #35b779;
        }
        
        .chart-image {
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        }
        
        .insights-list {
            list-style: none;
        }
        
        .insights-list li {
            padding: 12px;
            margin: 8px 0;
            background: linear-gradient(90deg, rgba(253, 231, 37, 0.1), rgba(53, 183, 121, 0.1));
            border-left: 4px solid #fde725;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        
        .insights-list li:hover {
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        .summary-section, .data-section {
            margin: 0 30px 30px 30px;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-top: 4px solid #31688e;
        }
        
        .summary-text {
            font-size: 1.1em;
            line-height: 1.8;
            color: #555;
            text-align: justify;
        }
        
        .data-table-container {
            overflow-x: auto;
            max-height: 400px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }
        
        .data-table th, .data-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        .data-table th {
            background: linear-gradient(135deg, #440154, #31688e);
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        
        .data-table tr:nth-child(even) {
            background: rgba(53, 183, 121, 0.05);
        }
        
        .data-table tr:hover {
            background: rgba(253, 231, 37, 0.1);
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        h2 {
            color: #440154;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #35b779;
            font-size: 1.4em;
        }
        
        .no-chart {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 50px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        @media (max-width: 768px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                margin: 10px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
        }
        """
    
    def _format_data_table(self, data):
        """Formata dados como tabela HTML"""
        if not data:
            return '<p class="no-chart">Nenhum dado disponível</p>'
        
        # Converte para DataFrame se necessário
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            return '<p class="no-chart">Formato de dados não suportado</p>'
        
        # Limita a 50 linhas para performance
        if len(df) > 50:
            df_display = df.head(50)
            footer_note = f'<p style="margin-top: 10px; color: #666; font-size: 0.9em;">Mostrando primeiras 50 linhas de {len(df)} registros totais.</p>'
        else:
            df_display = df
            footer_note = ""
        
        # Gera HTML da tabela
        table_html = df_display.to_html(
            classes='data-table',
            escape=False,
            index=False,
            table_id='data-table'
        )
        
        return table_html + footer_note

# Para compatibilidade com código existente
ProfessionalHTMLReportGenerator = HTMLReportGenerator
