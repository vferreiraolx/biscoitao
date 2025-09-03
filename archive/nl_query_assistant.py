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
        self.tables_cache = {}
        self.columns_cache = {}
    
    def get_available_tables(self):
        """Descobre tabelas disponíveis no schema dw"""
        try:
            result = execute_query("SHOW TABLES FROM dw")
            tables = result['Table'].tolist() if 'Table' in result.columns else []
            return [f"dw.{table}" for table in tables]
        except Exception as e:
            print(f"Erro ao buscar tabelas: {e}")
            return ["dw.monetization_total"]  # fallback
    
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

class AdvancedNLProcessor:
    """Processador avançado de linguagem natural com detecção de intenções"""
    
    def __init__(self):
        self.intent_patterns = {
            'temporal_comparison': r'(compara|diferença|variação|evolução|tendência|vs|versus| e )',
            'aggregation': r'(total|soma|média|máximo|mínimo|quantidade|count)',
            'filtering': r'(onde|com|que|em|de|durante|entre)',
            'grouping': r'(por|agrupado|separado|dividido)',
            'ranking': r'(melhor|pior|maior|menor|top|primeiro|último)',
            'statistical': r'(desvio|distribuição|estatística|análise|padrão)'
        }
    
    def extract_intent(self, instruction):
        """Identifica múltiplas intenções na instrução"""
        intents = []
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, instruction.lower()):
                intents.append(intent)
        return intents
    
    def detect_business_context(self, instruction):
        """Detecta contexto empresarial"""
        business_contexts = {
            'revenue': ['receita', 'faturamento', 'vendas', 'preço', 'price'],
            'customer': ['cliente', 'usuário', 'comprador', 'user'],
            'product': ['produto', 'item', 'categoria', 'product'],
            'geography': ['região', 'estado', 'cidade', 'local', 'area'],
            'time_analysis': ['sazonal', 'mensal', 'trimestral', 'anual', 'período']
        }
        
        detected = []
        for context, keywords in business_contexts.items():
            if any(kw in instruction.lower() for kw in keywords):
                detected.append(context)
        
        return detected

class InsightGenerator:
    """Gerador automático de insights dos dados"""
    
    def analyze_trends(self, data):
        """Identifica padrões e tendências automaticamente"""
        insights = []
        
        if len(data) < 2:
            return insights
        
        # Análise de crescimento
        if 'growth_percentage' in data.columns:
            growth = data['growth_percentage'].dropna()
            if not growth.empty:
                avg_growth = growth.mean()
                if avg_growth > 10:
                    insights.append(f"📈 Crescimento acelerado: {avg_growth:.1f}% em média")
                elif avg_growth > 2:
                    insights.append(f"📊 Crescimento moderado: {avg_growth:.1f}% em média")
                elif avg_growth < -10:
                    insights.append(f"📉 Declínio acentuado: {avg_growth:.1f}% em média")
                elif avg_growth < -2:
                    insights.append(f"📊 Declínio moderado: {avg_growth:.1f}% em média")
                else:
                    insights.append(f"📊 Estabilidade: variação de {avg_growth:.1f}%")
        
        # Análise de valores
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            if any(keyword in col.lower() for keyword in ['avg_', 'sum_', 'price', 'amount']):
                values = data[col].dropna()
                if len(values) > 1:
                    std_dev = values.std()
                    mean_val = values.mean()
                    if std_dev / mean_val > 0.3:  # Alta variabilidade
                        insights.append(f"⚠️ Alta volatilidade nos dados ({col})")
        
        return insights
    
    def generate_data_visualization(self, data, instruction):
        """Cria visualização textual dos dados"""
        if len(data) < 2:
            return ""
        
        # Encontra coluna de valores
        value_cols = [col for col in data.columns if any(prefix in col for prefix in ['avg_', 'sum_', 'count_', 'max_', 'min_'])]
        if not value_cols:
            return ""
        
        value_col = value_cols[0]
        values = data[value_col].tolist()
        
        if not values or all(pd.isna(values)):
            return ""
        
        max_val = max([v for v in values if not pd.isna(v)])
        min_val = min([v for v in values if not pd.isna(v)])
        
        chart_lines = []
        chart_lines.append("📊 Visualização dos dados:")
        
        for i, val in enumerate(values):
            if pd.isna(val):
                continue
                
            # Calcula proporção para a barra
            if max_val > min_val:
                proportion = (val - min_val) / (max_val - min_val)
            else:
                proportion = 1
            
            bar_length = max(1, int(proportion * 15))
            bar = "█" * bar_length + "░" * (15 - bar_length)
            
            # Tenta identificar o período
            period = ""
            if 'year' in data.columns and 'month' in data.columns:
                year = data.iloc[i]['year']
                month = data.iloc[i]['month']
                month_names = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                period = f"{month_names[int(month)]}-{str(int(year))[2:]}"
            else:
                period = f"P{i+1}"
            
            chart_lines.append(f"  {period:>6}: {bar} {val:,.2f}")
        
        return "\n".join(chart_lines)

class SmartQueryBuilder:
    """Constrói queries SQL inteligentes baseado em instruções conversacionais"""
    
    def __init__(self, explorer):
        self.explorer = explorer
        self.month_mapping = {
            "jan": 1, "janeiro": 1, "fev": 2, "fevereiro": 2, "mar": 3, "março": 3,
            "abr": 4, "abril": 4, "mai": 5, "maio": 5, "jun": 6, "junho": 6,
            "jul": 7, "julho": 7, "ago": 8, "agosto": 8, "set": 9, "setembro": 9,
            "out": 10, "outubro": 10, "nov": 11, "novembro": 11, "dez": 12, "dezembro": 12
        }
    
    def extract_date_filters(self, instruction, table_name):
        """Extrai filtros de data da instrução usando nomes reais das colunas"""
        filters = []
        columns = self.explorer.get_table_columns(table_name)
        
        # Mapeia colunas de data disponíveis
        date_columns = {}
        for col in columns:
            col_lower = col.lower()
            if any(date_keyword in col_lower for date_keyword in ['year', 'ano']):
                date_columns['year'] = col
            if any(date_keyword in col_lower for date_keyword in ['month', 'mes', 'mês']):
                date_columns['month'] = col
            if any(date_keyword in col_lower for date_keyword in ['day', 'dia']):
                date_columns['day'] = col
            if any(date_keyword in col_lower for date_keyword in ['date', 'data', 'creation', 'event']):
                date_columns['date'] = col
        
        # Padrão para múltiplos períodos (ex: jan-24 e jan-25)
        date_pattern = r"(jan|janeiro|fev|fevereiro|mar|março|abr|abril|mai|maio|jun|junho|jul|julho|ago|agosto|set|setembro|out|outubro|nov|novembro|dez|dezembro)[- ]?(\d{2,4})"
        matches = re.findall(date_pattern, instruction.lower())
        
        date_conditions = []
        for month_str, year_str in matches:
            month = self.month_mapping.get(month_str)
            year = int(year_str)
            if year < 100:
                year += 2000
            
            # Usa os nomes reais das colunas se disponíveis
            if 'year' in date_columns and 'month' in date_columns:
                date_conditions.append(f"({date_columns['year']}={year} AND {date_columns['month']}={month})")
            elif 'date' in date_columns:
                # Se há uma coluna de data, tenta usar filtro por período
                date_conditions.append(f"(EXTRACT(YEAR FROM {date_columns['date']})={year} AND EXTRACT(MONTH FROM {date_columns['date']})={month})")
        
        # Se há múltiplas condições de data, usa OR
        if len(date_conditions) > 1:
            filters.append(" OR ".join(date_conditions))
        elif len(date_conditions) == 1:
            filters.append(date_conditions[0])
        
        # Padrão para ano específico
        year_pattern = r"\b(20\d{2})\b"
        year_matches = re.findall(year_pattern, instruction)
        for year in year_matches:
            if year not in [match[1] for match in matches]:  # Evita duplicatas
                if 'year' in date_columns:
                    filters.append(f"{date_columns['year']}={year}")
                elif 'date' in date_columns:
                    filters.append(f"EXTRACT(YEAR FROM {date_columns['date']})={year}")
        
        return filters
    
    def determine_operation(self, instruction):
        """Determina qual operação SQL realizar"""
        instruction_lower = instruction.lower()
        
        if any(word in instruction_lower for word in ["média", "media"]):
            return "AVG"
        elif any(word in instruction_lower for word in ["soma", "total", "somar"]):
            return "SUM"
        elif any(word in instruction_lower for word in ["contagem", "contar", "quantidade"]):
            return "COUNT"
        elif any(word in instruction_lower for word in ["máximo", "maior", "max"]):
            return "MAX"
        elif any(word in instruction_lower for word in ["mínimo", "menor", "min"]):
            return "MIN"
        elif any(word in instruction_lower for word in ["listar", "mostrar", "exibir"]):
            return "SELECT"
        else:
            return "SELECT"
    
    def build_query(self, instruction, table_name="dw.monetization_total"):
        """Constrói uma query SQL baseada na instrução"""
        operation = self.determine_operation(instruction)
        relevant_columns = self.explorer.find_relevant_columns(instruction, table_name)
        date_filters = self.extract_date_filters(instruction, table_name)
        
        # Detecta se é uma comparação/variação
        is_comparison = any(word in instruction.lower() for word in ["variação", "comparar", "diferença", "vs", "versus", " e "])
        
        # Determina a coluna principal para operações agregadas
        main_column = None
        if relevant_columns:
            # Prioriza colunas de preço/valor para operações numéricas
            price_cols = [col for col in relevant_columns if any(p in col.lower() for p in ['price', 'amount', 'valor'])]
            main_column = price_cols[0] if price_cols else relevant_columns[0]
        
        # Para comparações com múltiplas datas, cria query mais complexa
        if is_comparison and len(date_filters) == 1 and " OR " in date_filters[0]:
            # Query para comparação temporal
            if operation in ["AVG", "SUM", "MAX", "MIN"] and main_column:
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
                
                if 'year' in date_columns and 'month' in date_columns:
                    select_part = f"SELECT {date_columns['year']}, {date_columns['month']}, {operation}({main_column}) AS {operation.lower()}_{main_column}"
                    query = f"{select_part} FROM {table_name} WHERE {date_filters[0]} GROUP BY {date_columns['year']}, {date_columns['month']} ORDER BY {date_columns['year']}, {date_columns['month']}"
                elif 'date' in date_columns:
                    select_part = f"SELECT EXTRACT(YEAR FROM {date_columns['date']}) as year, EXTRACT(MONTH FROM {date_columns['date']}) as month, {operation}({main_column}) AS {operation.lower()}_{main_column}"
                    query = f"{select_part} FROM {table_name} WHERE {date_filters[0]} GROUP BY EXTRACT(YEAR FROM {date_columns['date']}), EXTRACT(MONTH FROM {date_columns['date']}) ORDER BY year, month"
                else:
                    # Fallback para query simples
                    select_part = f"SELECT {operation}({main_column}) AS {operation.lower()}_{main_column}"
                    query = f"{select_part} FROM {table_name}"
                    if date_filters:
                        query += f" WHERE {date_filters[0]}"
            else:
                # Para outros tipos de operação
                select_part = f"SELECT {', '.join(relevant_columns[:5])}" if relevant_columns else "SELECT *"
                query = f"{select_part} FROM {table_name}"
                if date_filters:
                    query += f" WHERE {date_filters[0]}"
                query += " LIMIT 20"
        else:
            # Query normal
            if operation in ["AVG", "SUM", "MAX", "MIN"] and main_column:
                select_part = f"SELECT {operation}({main_column}) AS {operation.lower()}_{main_column}"
            elif operation == "COUNT":
                if "únicos" in instruction.lower() or "distinct" in instruction.lower():
                    count_col = main_column or "*"
                    select_part = f"SELECT COUNT(DISTINCT {count_col}) AS unique_count"
                else:
                    select_part = "SELECT COUNT(*) AS total_count"
            else:
                # SELECT básico
                if relevant_columns:
                    select_part = f"SELECT {', '.join(relevant_columns[:5])}"  # Limita a 5 colunas
                else:
                    select_part = "SELECT *"
            
            # Constrói a query completa
            query = f"{select_part} FROM {table_name}"
            
            if date_filters:
                query += f" WHERE {' AND '.join(date_filters)}"
            
            # Adiciona LIMIT para queries SELECT básicas
            if operation == "SELECT" and "LIMIT" not in query:
                query += " LIMIT 10"
        
        return query

class ToqanAIHelper:
    """Integração com API Toqan para interpretação inteligente de queries"""
    
    def __init__(self):
        self.api_key = os.getenv('TOQAN_API_KEY')
        self.base_url = 'https://api.coco.prod.toqan.ai/api'
    
    def enhanced_sql_help(self, instruction, table_schema, business_contexts, intents):
        """Versão melhorada da consulta ao Toqan com contexto empresarial"""
        if not self.api_key:
            return None
        
        # Contexto mais rico para o Toqan
        context = f"""
        Você é um analista de dados especialista em SQL e negócios de marketplace.
        
        CONTEXTO EMPRESARIAL: Marketplace OLX - dados de monetização
        INTENÇÕES DETECTADAS: {', '.join(intents)}
        CONTEXTOS DE NEGÓCIO: {', '.join(business_contexts)}
        
        SCHEMA DA TABELA: {table_schema}
        
        INSTRUÇÃO DO USUÁRIO: {instruction}
        
        Baseado no contexto, retorne um JSON estruturado:
        {{
            "sql_strategy": "estratégia SQL recomendada",
            "business_insight": "insight de negócio a buscar",
            "recommended_metrics": ["métricas complementares"],
            "grouping_suggestion": ["colunas para agrupar"],
            "filter_recommendations": ["filtros importantes"],
            "analysis_type": "comparativo|temporal|agregado|exploratório"
        }}
        """
        
        try:
            # Implementação similar à versão anterior, mas com contexto aprimorado
            create_payload = {"user_message": context}
            create_resp = requests.post(
                f"{self.base_url}/create_conversation",
                headers={"x-api-key": self.api_key},
                json=create_payload,
                timeout=10
            )
            
            if create_resp.status_code != 200:
                return None
            
            create_data = create_resp.json()
            conversation_id = create_data.get('conversation_id')
            request_id = create_data.get('request_id')
            
            if not conversation_id or not request_id:
                return None
            
            # Busca resposta com timeout menor para ser mais responsivo
            for _ in range(10):  # 10 segundos máximo
                import time
                time.sleep(1)
                
                get_url = f"{self.base_url}/get_answer?conversation_id={conversation_id}&request_id={request_id}"
                ans_resp = requests.get(get_url, headers={"x-api-key": self.api_key}, timeout=5)
                
                if ans_resp.status_code == 200:
                    ans_data = ans_resp.json()
                    if ans_data.get('status') in ['completed', 'finished'] and ans_data.get('answer'):
                        answer = ans_data['answer']
                        try:
                            json_match = re.search(r'\{.*\}', answer, re.DOTALL)
                            if json_match:
                                return json.loads(json_match.group())
                        except:
                            pass
                        return {"explanation": answer}
            
            return None
            
        except Exception as e:
            print(f"⚠️ Toqan temporariamente indisponível: {e}")
            return None

class AdaptiveQueryBuilder(SmartQueryBuilder):
    """Construtor de queries adaptativo com fallbacks e análises avançadas"""
    
    def __init__(self, explorer):
        super().__init__(explorer)
        self.nl_processor = AdvancedNLProcessor()
        self.insight_generator = InsightGenerator()
    
    def generate_statistical_query(self, instruction, table_name, intents):
        """Gera query com análises estatísticas automáticas"""
        relevant_columns = self.explorer.find_relevant_columns(instruction, table_name)
        date_filters = self.extract_date_filters(instruction, table_name)
        
        # Encontra coluna principal de valor
        main_column = None
        if relevant_columns:
            price_cols = [col for col in relevant_columns if any(p in col.lower() for p in ['price', 'amount', 'valor'])]
            main_column = price_cols[0] if price_cols else relevant_columns[0]
        
        if not main_column:
            return None
        
        # Detecta colunas de data para agrupamento temporal
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
        
        # Query com análises estatísticas avançadas
        if 'temporal_comparison' in intents and date_columns:
            if 'year' in date_columns and 'month' in date_columns:
                query = f"""
                WITH monthly_stats AS (
                    SELECT 
                        {date_columns['year']} as year,
                        {date_columns['month']} as month,
                        AVG({main_column}) as avg_{main_column},
                        COUNT(*) as record_count,
                        STDDEV({main_column}) as stddev_{main_column},
                        MIN({main_column}) as min_{main_column},
                        MAX({main_column}) as max_{main_column}
                    FROM {table_name}
                    {f'WHERE {date_filters[0]}' if date_filters else ''}
                    GROUP BY {date_columns['year']}, {date_columns['month']}
                ),
                growth_analysis AS (
                    SELECT *,
                        LAG(avg_{main_column}) OVER (ORDER BY year, month) as prev_avg,
                        avg_{main_column} - LAG(avg_{main_column}) OVER (ORDER BY year, month) as absolute_change
                    FROM monthly_stats
                )
                SELECT *,
                    CASE 
                        WHEN prev_avg > 0 AND prev_avg IS NOT NULL 
                        THEN (absolute_change / prev_avg) * 100 
                        ELSE NULL 
                    END as growth_percentage
                FROM growth_analysis
                ORDER BY year, month
                """
            elif 'date' in date_columns:
                query = f"""
                WITH monthly_stats AS (
                    SELECT 
                        EXTRACT(YEAR FROM {date_columns['date']}) as year,
                        EXTRACT(MONTH FROM {date_columns['date']}) as month,
                        AVG({main_column}) as avg_{main_column},
                        COUNT(*) as record_count,
                        STDDEV({main_column}) as stddev_{main_column}
                    FROM {table_name}
                    {f'WHERE {date_filters[0]}' if date_filters else ''}
                    GROUP BY EXTRACT(YEAR FROM {date_columns['date']}), EXTRACT(MONTH FROM {date_columns['date']})
                ),
                growth_analysis AS (
                    SELECT *,
                        LAG(avg_{main_column}) OVER (ORDER BY year, month) as prev_avg,
                        avg_{main_column} - LAG(avg_{main_column}) OVER (ORDER BY year, month) as absolute_change
                    FROM monthly_stats
                )
                SELECT *,
                    CASE 
                        WHEN prev_avg > 0 AND prev_avg IS NOT NULL 
                        THEN (absolute_change / prev_avg) * 100 
                        ELSE NULL 
                    END as growth_percentage
                FROM growth_analysis
                ORDER BY year, month
                """
            else:
                return None
        else:
            # Query estatística simples
            operation = self.determine_operation(instruction)
            query = f"SELECT {operation}({main_column}) AS {operation.lower()}_{main_column} FROM {table_name}"
            if date_filters:
                query += f" WHERE {' AND '.join(date_filters)}"
        
        return query
    
    def build_adaptive_queries(self, instruction, table_name="dw.monetization_total"):
        """Gera múltiplas versões de query com fallbacks"""
        intents = self.nl_processor.extract_intent(instruction)
        business_contexts = self.nl_processor.detect_business_context(instruction)
        
        queries = []
        
        # Query 1: Estatística avançada (se aplicável)
        if 'temporal_comparison' in intents or 'statistical' in intents:
            advanced_query = self.generate_statistical_query(instruction, table_name, intents)
            if advanced_query:
                queries.append(('advanced_statistical', advanced_query))
        
        # Query 2: Comparação temporal (query atual melhorada)
        comparison_query = self.build_query(instruction, table_name)
        queries.append(('temporal_comparison', comparison_query))
        
        # Query 3: Agregação simples (fallback)
        operation = self.determine_operation(instruction)
        relevant_columns = self.explorer.find_relevant_columns(instruction, table_name)
        if relevant_columns:
            main_column = relevant_columns[0]
            simple_query = f"SELECT {operation}({main_column}) AS {operation.lower()}_{main_column} FROM {table_name}"
            date_filters = self.extract_date_filters(instruction, table_name)
            if date_filters:
                # Para fallback, usa apenas o primeiro filtro de data
                first_filter = date_filters[0].split(' OR ')[0] if ' OR ' in date_filters[0] else date_filters[0]
                simple_query += f" WHERE {first_filter}"
            queries.append(('simple_aggregation', simple_query))
        
        # Query 4: Exploratória (último fallback)
        explore_query = f"SELECT * FROM {table_name} LIMIT 5"
        queries.append(('exploration', explore_query))
        
        return queries, intents, business_contexts
    """Processador avançado de linguagem natural com detecção de intenções"""
    
    def __init__(self):
        self.intent_patterns = {
            'temporal_comparison': r'(compara|diferença|variação|evolução|tendência|vs|versus| e )',
            'aggregation': r'(total|soma|média|máximo|mínimo|quantidade|count)',
            'filtering': r'(onde|com|que|em|de|durante|entre)',
            'grouping': r'(por|agrupado|separado|dividido)',
            'ranking': r'(melhor|pior|maior|menor|top|primeiro|último)',
            'statistical': r'(desvio|distribuição|estatística|análise|padrão)'
        }
    
    def extract_intent(self, instruction):
        """Identifica múltiplas intenções na instrução"""
        intents = []
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, instruction.lower()):
                intents.append(intent)
        return intents
    
    def detect_business_context(self, instruction):
        """Detecta contexto empresarial"""
        business_contexts = {
            'revenue': ['receita', 'faturamento', 'vendas', 'preço', 'price'],
            'customer': ['cliente', 'usuário', 'comprador', 'user'],
            'product': ['produto', 'item', 'categoria', 'product'],
            'geography': ['região', 'estado', 'cidade', 'local', 'area'],
            'time_analysis': ['sazonal', 'mensal', 'trimestral', 'anual', 'período']
        }
        
        detected = []
        for context, keywords in business_contexts.items():
            if any(kw in instruction.lower() for kw in keywords):
                detected.append(context)
        
        return detected

class InsightGenerator:
    """Gerador automático de insights dos dados"""
    
    def analyze_trends(self, data):
        """Identifica padrões e tendências automaticamente"""
        insights = []
        
        if len(data) < 2:
            return insights
        
        # Análise de crescimento
        if 'growth_percentage' in data.columns:
            growth = data['growth_percentage'].dropna()
            if not growth.empty:
                avg_growth = growth.mean()
                if avg_growth > 10:
                    insights.append(f"📈 Crescimento acelerado: {avg_growth:.1f}% em média")
                elif avg_growth > 2:
                    insights.append(f"📊 Crescimento moderado: {avg_growth:.1f}% em média")
                elif avg_growth < -10:
                    insights.append(f"📉 Declínio acentuado: {avg_growth:.1f}% em média")
                elif avg_growth < -2:
                    insights.append(f"📊 Declínio moderado: {avg_growth:.1f}% em média")
                else:
                    insights.append(f"📊 Estabilidade: variação de {avg_growth:.1f}%")
        
        # Análise de valores
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            if any(keyword in col.lower() for keyword in ['avg_', 'sum_', 'price', 'amount']):
                values = data[col].dropna()
                if len(values) > 1:
                    std_dev = values.std()
                    mean_val = values.mean()
                    if std_dev / mean_val > 0.3:  # Alta variabilidade
                        insights.append(f"⚠️ Alta volatilidade nos dados ({col})")
        
        return insights
    
    def generate_data_visualization(self, data, instruction):
        """Cria visualização textual dos dados"""
        if len(data) < 2:
            return ""
        
        # Encontra coluna de valores
        value_cols = [col for col in data.columns if any(prefix in col for prefix in ['avg_', 'sum_', 'count_', 'max_', 'min_'])]
        if not value_cols:
            return ""
        
        value_col = value_cols[0]
        values = data[value_col].tolist()
        
        if not values or all(pd.isna(values)):
            return ""
        
        max_val = max([v for v in values if not pd.isna(v)])
        min_val = min([v for v in values if not pd.isna(v)])
        
        chart_lines = []
        chart_lines.append("📊 Visualização dos dados:")
        
        for i, val in enumerate(values):
            if pd.isna(val):
                continue
                
            # Calcula proporção para a barra
            if max_val > min_val:
                proportion = (val - min_val) / (max_val - min_val)
            else:
                proportion = 1
            
            bar_length = max(1, int(proportion * 15))
            bar = "█" * bar_length + "░" * (15 - bar_length)
            
            # Tenta identificar o período
            period = ""
            if 'year' in data.columns and 'month' in data.columns:
                year = data.iloc[i]['year']
                month = data.iloc[i]['month']
                month_names = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                period = f"{month_names[int(month)]}-{str(int(year))[2:]}"
            else:
                period = f"P{i+1}"
            
            chart_lines.append(f"  {period:>6}: {bar} {val:,.2f}")
        
        return "\n".join(chart_lines)
    """Integração com API Toqan para interpretação inteligente de queries"""
    
    def __init__(self):
        self.api_key = os.getenv('TOQAN_API_KEY')
        self.base_url = 'https://api.coco.prod.toqan.ai/api'
    
    def ask_toqan_for_sql_help(self, instruction, table_schema):
        """Usa Toqan para ajudar na conversão NL→SQL"""
        if not self.api_key:
            return None
        
        # Prepara contexto para o Toqan
        context = f"""
        Você é um especialista em SQL. Baseado na instrução em português e no schema da tabela abaixo, 
        me ajude a entender:
        1. Que tipo de operação SQL é necessária (SELECT, AVG, SUM, COUNT, etc.)
        2. Quais colunas são relevantes
        3. Que filtros aplicar
        
        SCHEMA DA TABELA: {table_schema}
        
        INSTRUÇÃO: {instruction}
        
        Responda apenas com um JSON no formato:
        {{
            "operation": "AVG|SUM|COUNT|SELECT|MAX|MIN",
            "columns": ["lista", "de", "colunas"],
            "filters": ["lista de condições WHERE"],
            "explanation": "breve explicação"
        }}
        """
        
        try:
            # Cria conversa
            create_payload = {"user_message": context}
            create_resp = requests.post(
                f"{self.base_url}/create_conversation",
                headers={"x-api-key": self.api_key},
                json=create_payload,
                timeout=10
            )
            
            if create_resp.status_code != 200:
                return None
            
            create_data = create_resp.json()
            conversation_id = create_data.get('conversation_id')
            request_id = create_data.get('request_id')
            
            if not conversation_id or not request_id:
                return None
            
            # Busca resposta
            for _ in range(15):  # Tenta por 15 segundos
                import time
                time.sleep(1)
                
                get_url = f"{self.base_url}/get_answer?conversation_id={conversation_id}&request_id={request_id}"
                ans_resp = requests.get(get_url, headers={"x-api-key": self.api_key}, timeout=5)
                
                if ans_resp.status_code == 200:
                    ans_data = ans_resp.json()
                    if ans_data.get('status') in ['completed', 'finished'] and ans_data.get('answer'):
                        # Tenta extrair JSON da resposta
                        answer = ans_data['answer']
                        try:
                            # Procura por JSON na resposta
                            import re
                            json_match = re.search(r'\{.*\}', answer, re.DOTALL)
                            if json_match:
                                return json.loads(json_match.group())
                        except:
                            pass
                        return {"explanation": answer}  # Fallback
            
            return None
            
        except Exception as e:
            print(f"Erro ao consultar Toqan: {e}")
            return None

def nl_to_sql_adaptive(instruction):
    """Função principal melhorada com queries adaptativas"""
    explorer = DatabaseExplorer()
    builder = AdaptiveQueryBuilder(explorer)
    toqan = ToqanAIHelper()
    
    # Descobre tabela principal
    tables = explorer.get_available_tables()
    main_table = "dw.monetization_total"
    
    for table in tables:
        table_name = table.split('.')[-1]
        if table_name.lower() in instruction.lower():
            main_table = table
            break
    
    # Gera queries adaptativas
    queries, intents, business_contexts = builder.build_adaptive_queries(instruction, main_table)
    
    # Consulta Toqan se disponível
    table_columns = explorer.get_table_columns(main_table)
    toqan_help = toqan.enhanced_sql_help(instruction, table_columns, business_contexts, intents)
    
    if toqan_help and 'business_insight' in toqan_help:
        print(f"🤖 Toqan sugere: {toqan_help.get('business_insight', 'Análise inteligente')}")
    
    return queries

def execute_with_adaptive_fallback(queries):
    """Executa queries com fallback automático e análise de resultados"""
    insight_gen = InsightGenerator()
    
    for query_type, query in queries:
        try:
            print(f"🔄 Tentando estratégia: {query_type}")
            result = execute_query(query)
            
            if not result.empty:
                print(f"✅ Sucesso com estratégia: {query_type}")
                
                # Gera insights automáticos
                insights = insight_gen.analyze_trends(result)
                visualization = insight_gen.generate_data_visualization(result, "")
                
                return result, query_type, query, insights, visualization
                
        except Exception as e:
            print(f"❌ Estratégia {query_type} falhou: {str(e)[:100]}...")
            continue
    
    return None, None, None, [], ""

def generate_natural_response(result_df, instruction, sql_query):
    """Gera uma resposta em linguagem natural baseada no resultado"""
    if result_df.empty:
        return "Não foram encontrados dados para sua consulta."
    
    instruction_lower = instruction.lower()
    columns = result_df.columns.tolist()
    
    # Detecta se é uma comparação temporal
    is_comparison = any(word in instruction_lower for word in ["variação", "comparar", "diferença", "vs", "versus", " e "])
    
    if is_comparison and len(result_df) > 1:
        # Resposta para comparações temporais
        if any('avg_' in col for col in columns):
            avg_col = [col for col in columns if 'avg_' in col][0]
            
            response_parts = []
            for _, row in result_df.iterrows():
                if 'year' in columns and 'month' in columns:
                    year, month = row['year'], row['month']
                    value = row[avg_col]
                    month_name = list(SmartQueryBuilder({}).month_mapping.keys())[month-1]
                    response_parts.append(f"{month_name}-{str(year)[2:]}: {value:,.2f}")
            
            # Calcula variação se há 2 períodos
            if len(result_df) == 2:
                values = result_df[avg_col].tolist()
                variation = ((values[1] - values[0]) / values[0]) * 100
                variation_text = f"aumento de {variation:.1f}%" if variation > 0 else f"redução de {abs(variation):.1f}%"
                return f"Médias: {', '.join(response_parts)}. Variação: {variation_text}."
            else:
                return f"Médias por período: {', '.join(response_parts)}."
    
    # Respostas para operações simples
    if any('avg_' in col for col in columns):
        avg_col = [col for col in columns if 'avg_' in col][0]
        value = result_df[avg_col].iloc[0]
        if pd.isna(value):
            return "Não há dados suficientes para calcular a média solicitada."
        return f"A média é {value:,.2f}."
    
    elif any('sum_' in col for col in columns):
        sum_col = [col for col in columns if 'sum_' in col][0]
        value = result_df[sum_col].iloc[0]
        if pd.isna(value):
            return "Não há dados para somar."
        return f"A soma total é {value:,.2f}."
    
    elif any('max_' in col for col in columns):
        max_col = [col for col in columns if 'max_' in col][0]
        value = result_df[max_col].iloc[0]
        return f"O valor máximo é {value:,.2f}."
    
    elif any('min_' in col for col in columns):
        min_col = [col for col in columns if 'min_' in col][0]
        value = result_df[min_col].iloc[0]
        return f"O valor mínimo é {value:,.2f}."
    
    elif 'unique_count' in columns:
        count = result_df['unique_count'].iloc[0]
        return f"Existem {count} valores únicos."
    
    elif 'total_count' in columns:
        count = result_df['total_count'].iloc[0]
        return f"Total de {count} registros encontrados."
    
    else:
        # Para resultados tabulares, fornece um resumo
        rows = len(result_df)
        cols = len(result_df.columns)
        
        if rows == 1:
            return f"Encontrado 1 registro com {cols} campos."
        else:
            return f"Encontrados {rows} registros com {cols} campos cada."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python nl_query_assistant.py 'sua pergunta em linguagem natural'")
        print("Exemplos:")
        print("  'Qual a média do preço em jan-24?'")
        print("  'Quantos usuários únicos temos?'")
        print("  'Soma das vendas de 2023'")
        print("  'Listar os produtos mais caros'")
        sys.exit(1)
    
    instruction = " ".join(sys.argv[1:])
    
    print(f"🤖 Processando: {instruction}")
    print("=" * 50)
    
    try:
        # Gera queries adaptativas
        queries = nl_to_sql_adaptive(instruction)
        
        if not queries:
            print("❌ Não foi possível interpretar sua solicitação.")
            print("Tente ser mais específico ou usar palavras-chave como: média, soma, quantidade, etc.")
            sys.exit(1)
        
        print(f"🎯 Geradas {len(queries)} estratégias de consulta")
        print()
        
        # Executa com fallback adaptativo
        result_df, strategy_used, sql_query, insights, visualization = execute_with_adaptive_fallback(queries)
        
        if result_df is None:
            print("❌ Todas as estratégias de consulta falharam.")
            print("Verifique a conectividade com o banco de dados ou reformule a pergunta.")
            sys.exit(1)
        
        print(f"📝 Query SQL executada ({strategy_used}):")
        print(f"   {sql_query}")
        print()
        
        # Mostra visualização se disponível
        if visualization:
            print(visualization)
            print()
        
        # Mostra o resultado tabular
        print("📊 Resultado da consulta:")
        print(result_df.to_string(index=False))
        print()
        
        # Gera resposta em linguagem natural
        natural_response = generate_natural_response(result_df, instruction, sql_query)
        print(f"💬 Resposta: {natural_response}")
        
        # Mostra insights automáticos
        if insights:
            print("\n🔍 Insights automáticos:")
            for insight in insights:
                print(f"   • {insight}")
        
    except Exception as e:
        print(f"❌ Erro ao executar a consulta: {e}")
        print("\nPossíveis causas:")
        print("- Problema de conexão com o banco de dados")
        print("- Tabela ou coluna não existe")
        print("- Sintaxe SQL incorreta")
