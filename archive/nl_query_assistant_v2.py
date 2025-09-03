import sys
import re
from query import execute_query
import pandas as pd
import json
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

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
        
        # Mapeamento de palavras-chave para possíveis colunas
        keyword_mappings = {
            'preço': ['price', 'valor', 'amount', 'cost'],
            'price': ['price', 'valor', 'amount', 'cost'],
            'data': ['date', 'creation_date', 'year', 'month', 'day', 'dt'],
            'mês': ['month', 'mes'],
            'ano': ['year', 'ano'],
            'status': ['status', 'state', 'situation'],
            'usuário': ['user_id', 'user', 'customer_id'],
            'categoria': ['category', 'categoria'],
            'produto': ['product', 'produto', 'item'],
            'receita': ['revenue', 'income', 'price', 'amount'],
            'vendas': ['sales', 'vendas', 'price', 'amount']
        }
        
        for word in instruction_lower.split():
            if word in keyword_mappings:
                for col in columns:
                    for mapping in keyword_mappings[word]:
                        if mapping.lower() in col.lower():
                            relevant_columns.append(col)
        
        return list(set(relevant_columns))

class AdvancedQueryBuilder:
    """Construtor de queries inteligente com múltiplas estratégias"""
    
    def __init__(self):
        self.explorer = DatabaseExplorer()
        self.month_mapping = {
            "jan": 1, "janeiro": 1, "fev": 2, "fevereiro": 2, "mar": 3, "março": 3,
            "abr": 4, "abril": 4, "mai": 5, "maio": 5, "jun": 6, "junho": 6,
            "jul": 7, "julho": 7, "ago": 8, "agosto": 8, "set": 9, "setembro": 9,
            "out": 10, "outubro": 10, "nov": 11, "novembro": 11, "dez": 12, "dezembro": 12
        }
    
    def detect_intent(self, instruction):
        """Detecta intenções na instrução"""
        instruction_lower = instruction.lower()
        intents = []
        
        if any(word in instruction_lower for word in ["compara", "diferença", "variação", "evolução", "vs", "versus", " e "]):
            intents.append("comparison")
        if any(word in instruction_lower for word in ["média", "media"]):
            intents.append("average")
        if any(word in instruction_lower for word in ["soma", "total"]):
            intents.append("sum")
        if any(word in instruction_lower for word in ["contagem", "quantidade"]):
            intents.append("count")
        
        return intents
    
    def extract_date_filters(self, instruction, table_name):
        """Extrai filtros de data melhorados"""
        columns = self.explorer.get_table_columns(table_name)
        
        # Mapeia colunas de data disponíveis
        date_columns = {}
        for col in columns:
            col_lower = col.lower()
            if any(date_keyword in col_lower for date_keyword in ['year', 'ano']):
                date_columns['year'] = col
            if any(date_keyword in col_lower for date_keyword in ['month', 'mes', 'mês']):
                date_columns['month'] = col
            if any(date_keyword in col_lower for date_keyword in ['date', 'data', 'creation', 'event']):
                date_columns['date'] = col
        
        # Padrão para múltiplos períodos
        date_pattern = r"(jan|janeiro|fev|fevereiro|mar|março|abr|abril|mai|maio|jun|junho|jul|julho|ago|agosto|set|setembro|out|outubro|nov|novembro|dez|dezembro)[- ]?(\d{2,4})"
        matches = re.findall(date_pattern, instruction.lower())
        
        if not matches:
            return []
        
        date_conditions = []
        for month_str, year_str in matches:
            month = self.month_mapping.get(month_str)
            year = int(year_str)
            if year < 100:
                year += 2000
            
            if 'year' in date_columns and 'month' in date_columns:
                date_conditions.append(f"({date_columns['year']}={year} AND {date_columns['month']}={month})")
            elif 'date' in date_columns:
                date_conditions.append(f"(EXTRACT(YEAR FROM {date_columns['date']})={year} AND EXTRACT(MONTH FROM {date_columns['date']})={month})")
        
        if len(date_conditions) > 1:
            return [" OR ".join(date_conditions)]
        elif len(date_conditions) == 1:
            return [date_conditions[0]]
        
        return []
    
    def build_adaptive_queries(self, instruction, table_name="dw.monetization_total"):
        """Constrói múltiplas estratégias de query"""
        intents = self.detect_intent(instruction)
        relevant_columns = self.explorer.find_relevant_columns(instruction, table_name)
        date_filters = self.extract_date_filters(instruction, table_name)
        
        queries = []
        
        # Encontra coluna principal
        main_column = None
        if relevant_columns:
            price_cols = [col for col in relevant_columns if any(p in col.lower() for p in ['price', 'amount', 'valor'])]
            main_column = price_cols[0] if price_cols else relevant_columns[0]
        
        # Verifica se há múltiplas datas na instrução
        date_pattern = r"(jan|janeiro|fev|fevereiro|mar|março|abr|abril|mai|maio|jun|junho|jul|julho|ago|agosto|set|setembro|out|outubro|nov|novembro|dez|dezembro)[- ]?(\d{2,4})"
        multiple_dates = len(re.findall(date_pattern, instruction.lower())) > 1
        
        # Estratégia 1: Análise temporal comparativa (se há múltiplas datas ou palavra "compara")
        if ("comparison" in intents or multiple_dates) and date_filters and main_column:
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
            
            if 'date' in date_columns:  # Usando coluna de data real
                query = f"""
                WITH monthly_data AS (
                    SELECT EXTRACT(YEAR FROM {date_columns['date']}) as year, 
                           EXTRACT(MONTH FROM {date_columns['date']}) as month,
                           AVG({main_column}) as avg_{main_column},
                           COUNT(*) as record_count
                    FROM {table_name}
                    WHERE {date_filters[0]}
                    GROUP BY EXTRACT(YEAR FROM {date_columns['date']}), EXTRACT(MONTH FROM {date_columns['date']})
                ),
                growth_calc AS (
                    SELECT *, 
                           LAG(avg_{main_column}) OVER (ORDER BY year, month) as prev_avg,
                           avg_{main_column} - LAG(avg_{main_column}) OVER (ORDER BY year, month) as absolute_change
                    FROM monthly_data
                )
                SELECT *, 
                       CASE WHEN prev_avg > 0 AND prev_avg IS NOT NULL 
                            THEN (absolute_change / prev_avg) * 100 
                            ELSE NULL END as growth_percentage
                FROM growth_calc
                ORDER BY year, month
                """
                queries.append(("temporal_analysis", query.strip()))
        
        # Estratégia 2: Agregação simples
        if "average" in intents and main_column:
            query = f"SELECT AVG({main_column}) AS avg_{main_column} FROM {table_name}"
            if date_filters:
                query += f" WHERE {date_filters[0]}"
            queries.append(("simple_average", query))
        
        elif "sum" in intents and main_column:
            query = f"SELECT SUM({main_column}) AS sum_{main_column} FROM {table_name}"
            if date_filters:
                query += f" WHERE {date_filters[0]}"
            queries.append(("simple_sum", query))
        
        elif "count" in intents:
            query = f"SELECT COUNT(*) AS total_count FROM {table_name}"
            if date_filters:
                query += f" WHERE {date_filters[0]}"
            queries.append(("simple_count", query))
        
        # Estratégia 3: Fallback explorativo
        if not queries:
            if main_column:
                query = f"SELECT AVG({main_column}) AS avg_{main_column} FROM {table_name}"
                if date_filters:
                    query += f" WHERE {date_filters[0]}"
                queries.append(("fallback_avg", query))
            else:
                query = f"SELECT COUNT(*) AS total_count FROM {table_name} LIMIT 5"
                queries.append(("fallback_count", query))
        
        return queries

class InsightGenerator:
    """Gerador de insights automáticos"""
    
    def analyze_data(self, data, instruction):
        """Analisa dados e gera insights"""
        insights = []
        
        if len(data) < 2:
            return insights
        
        # Análise de crescimento
        if 'growth_percentage' in data.columns:
            growth = data['growth_percentage'].dropna()
            if not growth.empty:
                avg_growth = growth.mean()
                if avg_growth > 10:
                    insights.append(f"📈 Crescimento forte: {avg_growth:.1f}% em média")
                elif avg_growth > 2:
                    insights.append(f"📊 Crescimento moderado: {avg_growth:.1f}% em média")
                elif avg_growth < -10:
                    insights.append(f"📉 Declínio acentuado: {avg_growth:.1f}% em média")
                elif avg_growth < -2:
                    insights.append(f"📊 Declínio moderado: {avg_growth:.1f}% em média")
                else:
                    insights.append(f"📊 Estabilidade: variação de {avg_growth:.1f}%")
        
        return insights
    
    def create_visualization(self, data):
        """Cria visualização textual"""
        if len(data) < 2:
            return ""
        
        # Encontra coluna de valores
        value_cols = [col for col in data.columns if any(prefix in col for prefix in ['avg_', 'sum_', 'count_'])]
        if not value_cols:
            return ""
        
        value_col = value_cols[0]
        values = data[value_col].tolist()
        
        if not values or all(pd.isna(values)):
            return ""
        
        max_val = max([v for v in values if not pd.isna(v)])
        min_val = min([v for v in values if not pd.isna(v)])
        
        chart_lines = ["📊 Visualização:"]
        
        for i, val in enumerate(values):
            if pd.isna(val):
                continue
            
            if max_val > min_val:
                proportion = (val - min_val) / (max_val - min_val)
            else:
                proportion = 1
            
            bar_length = max(1, int(proportion * 15))
            bar = "█" * bar_length + "░" * (15 - bar_length)
            
            # Identifica período
            period = f"P{i+1}"
            if 'year' in data.columns and 'month' in data.columns:
                year = data.iloc[i]['year']
                month = data.iloc[i]['month']
                month_names = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                period = f"{month_names[int(month)]}-{str(int(year))[2:]}"
            
            chart_lines.append(f"  {period:>6}: {bar} {val:,.2f}")
        
        return "\n".join(chart_lines)

def execute_adaptive_queries(queries):
    """Executa queries com fallback"""
    insight_gen = InsightGenerator()
    
    for strategy, query in queries:
        try:
            print(f"🔄 Estratégia: {strategy}")
            result = execute_query(query)
            
            if not result.empty:
                print(f"✅ Sucesso com: {strategy}")
                insights = insight_gen.analyze_data(result, "")
                visualization = insight_gen.create_visualization(result)
                return result, strategy, query, insights, visualization
                
        except Exception as e:
            print(f"❌ {strategy} falhou: {str(e)[:80]}...")
            continue
    
    return None, None, None, [], ""

def generate_response(result_df, instruction, strategy):
    """Gera resposta em linguagem natural"""
    if result_df.empty:
        return "Não foram encontrados dados."
    
    columns = result_df.columns.tolist()
    
    # Detecta tipo de resposta
    if strategy == "temporal_analysis" and len(result_df) > 1:
        if any('avg_' in col for col in columns):
            avg_col = [col for col in columns if 'avg_' in col][0]
            response_parts = []
            
            for _, row in result_df.iterrows():
                if 'year' in columns and 'month' in columns:
                    year, month = row['year'], row['month']
                    value = row[avg_col]
                    month_names = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                    month_name = month_names[int(month)]
                    response_parts.append(f"{month_name}-{str(int(year))[2:]}: {value:,.2f}")
            
            # Calcula variação
            if len(result_df) == 2:
                values = result_df[avg_col].tolist()
                if values[0] > 0:
                    variation = ((values[1] - values[0]) / values[0]) * 100
                    variation_text = f"aumento de {variation:.1f}%" if variation > 0 else f"redução de {abs(variation):.1f}%"
                    return f"Médias: {', '.join(response_parts)}. Variação: {variation_text}."
            
            return f"Médias por período: {', '.join(response_parts)}."
    
    # Respostas simples
    if any('avg_' in col for col in columns):
        avg_col = [col for col in columns if 'avg_' in col][0]
        value = result_df[avg_col].iloc[0]
        return f"A média é {value:,.2f}."
    
    elif any('sum_' in col for col in columns):
        sum_col = [col for col in columns if 'sum_' in col][0]
        value = result_df[sum_col].iloc[0]
        return f"A soma total é {value:,.2f}."
    
    elif 'total_count' in columns:
        count = result_df['total_count'].iloc[0]
        return f"Total de {count} registros."
    
    return "Consulta executada com sucesso."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python nl_query_assistant_v2.py 'sua pergunta'")
        print("Exemplos:")
        print("  'Qual a média do preço em jan-24?'")
        print("  'Qual a média do preço em jan-24 e jan-25, bem como sua variação?'")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    
    print(f"🤖 Processando: {instruction}")
    print("=" * 50)
    
    try:
        builder = AdvancedQueryBuilder()
        queries = builder.build_adaptive_queries(instruction)
        
        if not queries:
            print("❌ Não foi possível gerar queries para sua solicitação.")
            sys.exit(1)
        
        print(f"🎯 Geradas {len(queries)} estratégias")
        
        result_df, strategy, sql_query, insights, visualization = execute_adaptive_queries(queries)
        
        if result_df is None:
            print("❌ Todas as estratégias falharam.")
            sys.exit(1)
        
        print(f"\n📝 Query executada ({strategy}):")
        print(f"   {sql_query}")
        print()
        
        if visualization:
            print(visualization)
            print()
        
        print("📊 Resultado:")
        print(result_df.to_string(index=False))
        print()
        
        response = generate_response(result_df, instruction, strategy)
        print(f"💬 Resposta: {response}")
        
        if insights:
            print("\n🔍 Insights:")
            for insight in insights:
                print(f"   • {insight}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
