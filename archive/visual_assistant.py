import sys
import re
from query import execute_query
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from dotenv import load_dotenv
from datetime import datetime
import warnings

# Configurações
load_dotenv()
warnings.filterwarnings("ignore")
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DatabaseExplorer:
    """Explora e mapeia as tabelas e colunas disponíveis no banco de dados"""
    
    def __init__(self):
        self.columns_cache = {}
    
    def get_table_columns(self, table_name):
        """Obtém colunas de uma tabela específica"""
        if table_name in self.columns_cache:
            return self.columns_cache[table_name]
        
        try:
            result = execute_query(f"DESCRIBE {table_name}")
            columns = result['Column'].tolist() if 'Column' in result.columns else []
            self.columns_cache[table_name] = columns
            return columns
        except Exception as e:
            print(f"Erro ao buscar colunas de {table_name}: {e}")
            return []
    
    def find_relevant_columns(self, instruction, table_name):
        """Encontra colunas relevantes baseado na instrução"""
        columns = self.get_table_columns(table_name)
        instruction_lower = instruction.lower()
        
        relevant_columns = []
        
        keyword_mappings = {
            'preço': ['price', 'valor', 'amount', 'cost'],
            'price': ['price', 'valor', 'amount', 'cost'],
            'data': ['date', 'creation_date', 'year', 'month', 'day', 'dt'],
            'mês': ['month', 'mes'],
            'ano': ['year', 'ano'],
            'status': ['status', 'state', 'situation'],
            'usuário': ['user_id', 'user', 'customer_id'],
            'categoria': ['category', 'categoria', 'platform', 'product'],
            'produto': ['product', 'produto', 'item'],
            'receita': ['revenue', 'income', 'price', 'amount'],
            'vendas': ['sales', 'vendas', 'price', 'amount'],
            'faturamento': ['revenue', 'income', 'price', 'amount', 'total']
        }
        
        for word in instruction_lower.split():
            if word in keyword_mappings:
                for col in columns:
                    for mapping in keyword_mappings[word]:
                        if mapping.lower() in col.lower():
                            relevant_columns.append(col)
        
        return list(set(relevant_columns))
    
    def get_numeric_columns(self, table_name):
        """Identifica colunas numéricas da tabela"""
        try:
            # Faz uma query simples para identificar tipos
            result = execute_query(f"SELECT * FROM {table_name} LIMIT 1")
            numeric_columns = []
            
            for col in result.columns:
                if result[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                    numeric_columns.append(col)
            
            return numeric_columns
        except Exception as e:
            print(f"Erro ao identificar colunas numéricas: {e}")
            # Fallback: assume colunas comuns como numéricas
            columns = self.get_table_columns(table_name)
            probable_numeric = []
            for col in columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['price', 'amount', 'value', 'cost', 'revenue', 'total', 'count', 'id']):
                    probable_numeric.append(col)
            return probable_numeric

class AdvancedQueryBuilder:
    """Construtor de queries inteligente com foco em visualização"""
    
    def __init__(self):
        self.explorer = DatabaseExplorer()
        self.month_mapping = {
            "jan": 1, "janeiro": 1, "fev": 2, "fevereiro": 2, "mar": 3, "março": 3,
            "abr": 4, "abril": 4, "mai": 5, "maio": 5, "jun": 6, "junho": 6,
            "jul": 7, "julho": 7, "ago": 8, "agosto": 8, "set": 9, "setembro": 9,
            "out": 10, "outubro": 10, "nov": 11, "novembro": 11, "dez": 12, "dezembro": 12
        }
    
    def detect_visualization_intent(self, instruction):
        """Detecta que tipo de visualização é mais apropriada"""
        instruction_lower = instruction.lower()
        
        viz_intents = {
            'line_chart': ['tendência', 'evolução', 'ao longo', 'temporal', 'crescimento', 'variação'],
            'bar_chart': ['compara', 'comparação', 'categoria', 'ranking', 'top', 'maior', 'menor'],
            'pie_chart': ['distribuição', 'proporção', 'percentual', 'participação'],
            'scatter_plot': ['correlação', 'relação', 'dispersão'],
            'histogram': ['frequência', 'distribuição', 'histograma']
        }
        
        detected_types = []
        for viz_type, keywords in viz_intents.items():
            if any(keyword in instruction_lower for keyword in keywords):
                detected_types.append(viz_type)
        
        # Detecta múltiplas datas = linha temporal
        date_pattern = r"(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)[- ]?\d{2,4}"
        if len(re.findall(date_pattern, instruction_lower)) > 1:
            detected_types.append('line_chart')
        
        return detected_types if detected_types else ['bar_chart']  # default
    
    def extract_date_filters(self, instruction, table_name):
        """Extrai filtros de data otimizados para visualização"""
        columns = self.explorer.get_table_columns(table_name)
        
        date_columns = {}
        for col in columns:
            col_lower = col.lower()
            if any(date_keyword in col_lower for date_keyword in ['year', 'ano']):
                date_columns['year'] = col
            if any(date_keyword in col_lower for date_keyword in ['month', 'mes', 'mês']):
                date_columns['month'] = col
            if any(date_keyword in col_lower for date_keyword in ['date', 'data', 'creation', 'event']):
                date_columns['date'] = col
        
        # Busca por períodos específicos
        date_pattern = r"(jan|janeiro|fev|fevereiro|mar|março|abr|abril|mai|maio|jun|junho|jul|julho|ago|agosto|set|setembro|out|outubro|nov|novembro|dez|dezembro)[- ]?(\d{2,4})"
        matches = re.findall(date_pattern, instruction.lower())
        
        # Busca por ranges temporais (ex: "últimos 6 meses", "2023", "primeiro trimestre")
        year_pattern = r"\b(20\d{2})\b"
        year_matches = re.findall(year_pattern, instruction)
        
        month_range_pattern = r"últimos?\s+(\d+)\s+meses?"
        month_range = re.search(month_range_pattern, instruction.lower())
        
        date_conditions = []
        
        # Períodos específicos
        for month_str, year_str in matches:
            month = self.month_mapping.get(month_str)
            year = int(year_str)
            if year < 100:
                year += 2000
            
            if 'date' in date_columns:
                date_conditions.append(f"(EXTRACT(YEAR FROM {date_columns['date']})={year} AND EXTRACT(MONTH FROM {date_columns['date']})={month})")
        
        # Anos específicos
        for year in year_matches:
            if year not in [match[1] for match in matches]:
                if 'date' in date_columns:
                    date_conditions.append(f"EXTRACT(YEAR FROM {date_columns['date']})={year}")
        
        # Range de meses
        if month_range and 'date' in date_columns:
            months = int(month_range.group(1))
            date_conditions.append(f"{date_columns['date']} >= CURRENT_DATE - INTERVAL '{months}' MONTH")
        
        if len(date_conditions) > 1:
            return [" OR ".join(date_conditions)]
        elif len(date_conditions) == 1:
            return [date_conditions[0]]
        
        return []
    
    def build_visualization_query(self, instruction, table_name="dw.monetization_total"):
        """Constrói query otimizada para visualização"""
        viz_types = self.detect_visualization_intent(instruction)
        relevant_columns = self.explorer.find_relevant_columns(instruction, table_name)
        numeric_columns = self.explorer.get_numeric_columns(table_name)
        date_filters = self.extract_date_filters(instruction, table_name)
        
        # Encontra colunas principais
        main_column = None
        if relevant_columns:
            # Prioriza colunas numéricas relevantes
            numeric_relevant = [col for col in relevant_columns if col in numeric_columns]
            if numeric_relevant:
                price_cols = [col for col in numeric_relevant if any(p in col.lower() for p in ['price', 'amount', 'valor'])]
                main_column = price_cols[0] if price_cols else numeric_relevant[0]
            else:
                # Se não há colunas numéricas relevantes, usa a primeira numérica disponível
                main_column = numeric_columns[0] if numeric_columns else None
        else:
            # Fallback para a primeira coluna numérica
            main_column = numeric_columns[0] if numeric_columns else None
        
        columns = self.explorer.get_table_columns(table_name)
        date_columns = {}
        for col in columns:
            col_lower = col.lower()
            if any(date_keyword in col_lower for date_keyword in ['date', 'data', 'creation', 'event']):
                date_columns['date'] = col
        
        # Query para gráfico de linha temporal
        if 'line_chart' in viz_types and main_column and 'date' in date_columns:
            query = f"""
            SELECT 
                EXTRACT(YEAR FROM {date_columns['date']}) as year,
                EXTRACT(MONTH FROM {date_columns['date']}) as month,
                AVG({main_column}) as avg_value,
                COUNT(*) as record_count,
                STDDEV({main_column}) as stddev_value
            FROM {table_name}
            {f'WHERE {date_filters[0]}' if date_filters else ''}
            GROUP BY EXTRACT(YEAR FROM {date_columns['date']}), EXTRACT(MONTH FROM {date_columns['date']})
            ORDER BY year, month
            """
            return query.strip(), 'line_chart'
        
        # Query para gráfico de barras (comparação categórica)
        elif 'bar_chart' in viz_types and main_column:
            # Busca por colunas categóricas (não numéricas)
            categorical_cols = []
            for col in columns:
                if col not in numeric_columns and any(cat_keyword in col.lower() for cat_keyword in ['category', 'status', 'type', 'platform', 'product']):
                    categorical_cols.append(col)
            
            if categorical_cols:
                cat_col = categorical_cols[0]
                query = f"""
                SELECT 
                    {cat_col} as category,
                    AVG({main_column}) as avg_value,
                    COUNT(*) as record_count
                FROM {table_name}
                {f'WHERE {date_filters[0]}' if date_filters else ''}
                GROUP BY {cat_col}
                ORDER BY avg_value DESC
                LIMIT 15
                """
                return query.strip(), 'bar_chart'
            else:
                # Fallback: usa alguma coluna como categórica, mas apenas contagem
                if columns:
                    cat_col = columns[0]  # Primeira coluna como categoria
                    query = f"""
                    SELECT 
                        {cat_col} as category,
                        COUNT(*) as record_count
                    FROM {table_name}
                    {f'WHERE {date_filters[0]}' if date_filters else ''}
                    GROUP BY {cat_col}
                    ORDER BY record_count DESC
                    LIMIT 15
                    """
                    return query.strip(), 'bar_chart'
        
        # Query fallback (temporal simples)
        if main_column and 'date' in date_columns:
            query = f"""
            SELECT 
                EXTRACT(YEAR FROM {date_columns['date']}) as year,
                EXTRACT(MONTH FROM {date_columns['date']}) as month,
                AVG({main_column}) as avg_value
            FROM {table_name}
            {f'WHERE {date_filters[0]}' if date_filters else ''}
            GROUP BY EXTRACT(YEAR FROM {date_columns['date']}), EXTRACT(MONTH FROM {date_columns['date']})
            ORDER BY year, month
            """
            return query.strip(), 'line_chart'
        
        return None, None

class VisualizationEngine:
    """Engine para geração de gráficos inteligentes"""
    
    def __init__(self):
        self.fig_size = (12, 6)
        self.colors = sns.color_palette("husl", 8)
    
    def create_line_chart(self, data, instruction, filename):
        """Cria gráfico de linha temporal"""
        plt.figure(figsize=self.fig_size)
        
        if 'year' in data.columns and 'month' in data.columns:
            # Cria coluna de data
            data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))
            x_col = 'date'
            x_data = data['date']
            x_label = 'Período'
        else:
            x_col = data.columns[0]
            x_data = data[x_col]
            x_label = x_col
        
        # Identifica coluna de valores
        value_cols = [col for col in data.columns if 'avg_' in col or 'sum_' in col or 'value' in col]
        y_col = value_cols[0] if value_cols else data.columns[1]
        
        plt.plot(x_data, data[y_col], marker='o', linewidth=2.5, markersize=8, color=self.colors[0])
        
        # Adiciona linha de tendência se há múltiplos pontos
        if len(data) > 2:
            z = np.polyfit(range(len(data)), data[y_col], 1)
            p = np.poly1d(z)
            plt.plot(x_data, p(range(len(data))), "--", alpha=0.7, color=self.colors[1], label='Tendência')
            plt.legend()
        
        plt.title(self._generate_chart_title(instruction, 'temporal'), fontsize=14, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(self._extract_metric_name(y_col), fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def create_bar_chart(self, data, instruction, filename):
        """Cria gráfico de barras"""
        plt.figure(figsize=self.fig_size)
        
        # Identifica colunas
        cat_col = data.columns[0]
        value_cols = [col for col in data.columns if 'avg_' in col or 'sum_' in col or 'value' in col]
        value_col = value_cols[0] if value_cols else data.columns[1]
        
        # Limita a 10 categorias para melhor visualização
        if len(data) > 10:
            data = data.head(10)
        
        bars = plt.bar(range(len(data)), data[value_col], color=self.colors[:len(data)])
        
        # Adiciona valores nas barras
        for i, (bar, value) in enumerate(zip(bars, data[value_col])):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(data[value_col])*0.01, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title(self._generate_chart_title(instruction, 'categorical'), fontsize=14, fontweight='bold')
        plt.xlabel(cat_col.replace('_', ' ').title(), fontsize=12)
        plt.ylabel(self._extract_metric_name(value_col), fontsize=12)
        plt.xticks(range(len(data)), data[cat_col], rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filename
    
    def _generate_chart_title(self, instruction, chart_type):
        """Gera título inteligente para o gráfico"""
        if 'média' in instruction.lower():
            metric = 'Média'
        elif 'soma' in instruction.lower() or 'total' in instruction.lower():
            metric = 'Total'
        elif 'quantidade' in instruction.lower():
            metric = 'Quantidade'
        else:
            metric = 'Análise'
        
        if chart_type == 'temporal':
            return f'{metric} ao Longo do Tempo'
        elif chart_type == 'categorical':
            return f'{metric} por Categoria'
        else:
            return f'{metric} - Análise de Dados'
    
    def _extract_metric_name(self, column_name):
        """Extrai nome legível da métrica"""
        if 'price' in column_name.lower():
            return 'Preço (R$)'
        elif 'avg_' in column_name:
            return 'Média'
        elif 'sum_' in column_name:
            return 'Soma Total'
        elif 'count' in column_name:
            return 'Quantidade'
        else:
            return column_name.replace('_', ' ').title()

class IntelligentReportGenerator:
    """Gerador de relatórios completos com análise + visualização"""
    
    def __init__(self):
        self.query_builder = AdvancedQueryBuilder()
        self.viz_engine = VisualizationEngine()
    
    def generate_complete_report(self, instruction, table_name="dw.monetization_total"):
        """Gera relatório completo com dados, gráficos e insights"""
        
        print(f"🎨 Gerando relatório visual para: {instruction}")
        print("=" * 60)
        
        # 1. Constrói e executa query
        query, viz_type = self.query_builder.build_visualization_query(instruction, table_name)
        
        if not query:
            print("❌ Não foi possível gerar query apropriada para visualização.")
            return None
        
        print(f"📊 Tipo de visualização detectado: {viz_type}")
        print(f"📝 Query gerada:")
        print(f"   {query}")
        print()
        
        try:
            data = execute_query(query)
            
            if data.empty:
                print("❌ Nenhum dado encontrado para a consulta.")
                return None
            
            print(f"✅ Dados obtidos: {len(data)} registros")
            print()
            
            # 2. Mostra dados tabulares
            print("📋 Dados encontrados:")
            print(data.to_string(index=False))
            print()
            
            # 3. Gera visualização
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grafico_{viz_type}_{timestamp}.png"
            
            print(f"🎨 Gerando gráfico: {filename}")
            
            if viz_type == 'line_chart':
                chart_file = self.viz_engine.create_line_chart(data, instruction, filename)
            elif viz_type == 'bar_chart':
                chart_file = self.viz_engine.create_bar_chart(data, instruction, filename)
            else:
                chart_file = self.viz_engine.create_line_chart(data, instruction, filename)
            
            # 4. Gera insights automáticos
            insights = self._generate_insights(data, instruction, viz_type)
            
            print(f"💾 Gráfico salvo: {chart_file}")
            print()
            
            if insights:
                print("🔍 Insights automáticos:")
                for insight in insights:
                    print(f"   • {insight}")
                print()
            
            # 5. Resposta conversacional
            response = self._generate_conversational_response(data, instruction, viz_type)
            print(f"💬 Resumo: {response}")
            
            return {
                'data': data,
                'chart_file': chart_file,
                'query': query,
                'viz_type': viz_type,
                'insights': insights,
                'response': response
            }
            
        except Exception as e:
            print(f"❌ Erro ao executar análise: {e}")
            return None
    
    def _generate_insights(self, data, instruction, viz_type):
        """Gera insights automáticos baseados nos dados"""
        insights = []
        
        if len(data) < 2:
            return insights
        
        # Insights para dados temporais
        if viz_type == 'line_chart' and 'avg_value' in data.columns:
            values = data['avg_value'].dropna()
            
            if len(values) > 1:
                # Tendência geral
                first_val = values.iloc[0]
                last_val = values.iloc[-1]
                growth = ((last_val - first_val) / first_val) * 100
                
                if growth > 10:
                    insights.append(f"📈 Tendência de crescimento forte: {growth:.1f}%")
                elif growth > 2:
                    insights.append(f"📊 Crescimento moderado: {growth:.1f}%")
                elif growth < -10:
                    insights.append(f"📉 Declínio significativo: {growth:.1f}%")
                elif growth < -2:
                    insights.append(f"📊 Declínio moderado: {growth:.1f}%")
                else:
                    insights.append(f"📊 Tendência estável: variação de {growth:.1f}%")
                
                # Volatilidade
                std_dev = values.std()
                mean_val = values.mean()
                if std_dev / mean_val > 0.2:
                    insights.append(f"⚠️ Alta volatilidade detectada (CV: {(std_dev/mean_val)*100:.1f}%)")
                
                # Picos e vales
                max_val = values.max()
                min_val = values.min()
                max_idx = values.idxmax()
                min_idx = values.idxmin()
                
                if 'year' in data.columns and 'month' in data.columns:
                    max_period = f"{data.loc[max_idx, 'month']}/{data.loc[max_idx, 'year']}"
                    min_period = f"{data.loc[min_idx, 'month']}/{data.loc[min_idx, 'year']}"
                    insights.append(f"🔝 Pico em {max_period}: {max_val:.2f}")
                    insights.append(f"🔻 Vale em {min_period}: {min_val:.2f}")
        
        # Insights para dados categóricos
        elif viz_type == 'bar_chart' and len(data) > 1:
            value_col = [col for col in data.columns if 'avg_' in col or 'sum_' in col or 'value' in col][0]
            
            if value_col in data.columns:
                top_category = data.iloc[0]
                total_sum = data[value_col].sum()
                top_percentage = (top_category[value_col] / total_sum) * 100
                
                insights.append(f"🥇 Categoria líder: {top_category.iloc[0]} ({top_percentage:.1f}% do total)")
                
                # Concentração
                top_3_sum = data[value_col].head(3).sum()
                top_3_percentage = (top_3_sum / total_sum) * 100
                insights.append(f"📊 Top 3 representam {top_3_percentage:.1f}% do total")
        
        return insights
    
    def _generate_conversational_response(self, data, instruction, viz_type):
        """Gera resposta conversacional baseada na análise"""
        if data.empty:
            return "Não foram encontrados dados para análise."
        
        if viz_type == 'line_chart' and len(data) > 1:
            if 'avg_value' in data.columns:
                first_val = data['avg_value'].iloc[0]
                last_val = data['avg_value'].iloc[-1]
                periods = len(data)
                
                if last_val > first_val:
                    trend = "crescimento"
                elif last_val < first_val:
                    trend = "declínio"
                else:
                    trend = "estabilidade"
                
                return f"Análise de {periods} períodos mostra {trend}. Valor inicial: {first_val:.2f}, final: {last_val:.2f}."
        
        elif viz_type == 'bar_chart':
            categories = len(data)
            value_col = [col for col in data.columns if 'avg_' in col or 'sum_' in col or 'value' in col][0]
            
            if value_col in data.columns:
                top_category = data.iloc[0]
                return f"Análise de {categories} categorias. Líder: {top_category.iloc[0]} com valor {top_category[value_col]:.2f}."
        
        return f"Análise realizada com {len(data)} registros de dados."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python visual_assistant.py 'sua pergunta para gerar gráfico'")
        print("Exemplos:")
        print("  'Mostre a evolução da média do preço nos últimos meses'")
        print("  'Compare as categorias por faturamento'")
        print("  'Gráfico da tendência de jan-24 a jan-25'")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    
    try:
        report_generator = IntelligentReportGenerator()
        result = report_generator.generate_complete_report(instruction)
        
        if result:
            print("\n🎯 Relatório visual gerado com sucesso!")
            print(f"📁 Arquivo: {result['chart_file']}")
        else:
            print("\n❌ Não foi possível gerar o relatório visual.")
    
    except Exception as e:
        print(f"❌ Erro na geração do relatório: {e}")
