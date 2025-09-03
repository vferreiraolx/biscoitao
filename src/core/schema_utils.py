from query import execute_query
from typing import List, Dict, Optional
import pandas as pd
import re

def get_table_schema(table_name: str) -> List[str]:
    """
    Executa DESCRIBE na tabela e retorna lista de colunas em lower case.
    """
    df = execute_query(f"DESCRIBE {table_name}")
    return [str(col).lower() for col in df['Column']]

def map_field(desired_field: str, schema: List[str]) -> Optional[str]:
    """
    Busca campo equivalente no schema usando heurísticas simples.
    """
    desired_field = desired_field.lower()
    # Busca exata
    if desired_field in schema:
        return desired_field
    # Busca por substring
    for col in schema:
        if desired_field in col:
            return col
    # Busca por sinônimos comuns
    synonyms = {
        'year': ['ano', 'data', 'dt'],
        'month': ['mes', 'mês', 'data', 'dt'],
        'day': ['dia', 'data', 'dt']
    }
    for syn in synonyms.get(desired_field, []):
        for col in schema:
            if syn in col:
                return col
    # Busca por regex (ex: data_ano, dt_ano)
    for col in schema:
        if re.search(rf"{desired_field}", col):
            return col
    return None

def build_query(table: str, filters: Dict[str, str]) -> str:
    """
    Monta query SQL ajustando campos conforme schema da tabela.
    """
    schema = get_table_schema(table)
    query_filters = []
    for field, value in filters.items():
        real_field = map_field(field, schema)
        if real_field:
            query_filters.append(f"{real_field}={value}")
    where_clause = " AND ".join(query_filters) if query_filters else ""
    query = f"SELECT * FROM {table}"
    if where_clause:
        query += f" WHERE {where_clause}"
    return query
