# Arquitetura LLM + Datalake - Processamento Escalável

## VISÃO GERAL
Sistema que conecta LLM ao datalake via PyHive, processa dados tabulares de forma escalável (100k → 1M+ linhas) e entrega contexto otimizado para LLM.

## ARQUITETURA PRINCIPAL

```
Datalake (PyHive) → DataProcessor → FormatLayer → LLM Context
```

## COMPONENTE CENTRAL: DataProcessor

### Classe Principal
```python
class DataProcessor:
    def __init__(self):
        self.small_threshold = 50000      # JSON direto
        self.medium_threshold = 500000    # Chunking
        self.large_threshold = 1000000    # RAG
    
    def process(self, dataframe, user_query=""):
        rows = len(dataframe)
        
        if rows <= self.small_threshold:
            return self._direct_format(dataframe)
        elif rows <= self.medium_threshold:
            return self._chunked_format(dataframe, user_query)
        else:
            return self._rag_format(dataframe, user_query)
```

## ESTRATÉGIAS POR VOLUME

### 1. PEQUENO (≤ 50k linhas): JSON Direto
```python
def _direct_format(self, df):
    return {
        "metadata": {
            "rows": len(df),
            "columns": len(df.columns),
            "strategy": "direct"
        },
        "schema": dict(df.dtypes.astype(str)),
        "data": df.to_csv(index=False)  # CSV é mais eficiente em tokens
    }
```

### 2. MÉDIO (50k-500k linhas): Chunking Inteligente
```python
def _chunked_format(self, df, user_query):
    # Determinar estratégia de chunk baseada nos dados
    strategy = self._determine_chunk_strategy(df, user_query)
    chunks = self._create_chunks(df, strategy)
    
    return {
        "metadata": {
            "total_rows": len(df),
            "chunks": len(chunks),
            "strategy": "chunked",
            "chunk_type": strategy
        },
        "summary": self._create_summary(df),
        "chunks": chunks
    }

def _determine_chunk_strategy(self, df, user_query):
    # Prioridade: temporal > categórico > size-based
    if any(df.dtypes == 'datetime64[ns]'):
        return "temporal"
    elif df.select_dtypes(include=['object']).shape[1] > 0:
        return "categorical"
    else:
        return "size_based"

def _create_chunks(self, df, strategy):
    if strategy == "temporal":
        date_col = df.select_dtypes(include=['datetime64[ns]']).columns[0]
        return df.groupby(pd.Grouper(key=date_col, freq='M'))
    elif strategy == "categorical":
        cat_col = df.select_dtypes(include=['object']).columns[0]
        return df.groupby(cat_col)
    else:  # size_based
        chunk_size = 25000
        return [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
```

### 3. GRANDE (500k+ linhas): RAG Preparado
```python
def _rag_format(self, df, user_query):
    # Criar embeddings dos chunks para busca semântica
    embeddings = self._create_embeddings(df)
    
    return {
        "metadata": {
            "total_rows": len(df),
            "strategy": "rag",
            "indexed": True
        },
        "summary": self._create_summary(df),
        "search_context": {
            "embeddings_ready": True,
            "query_examples": self._generate_query_examples(df.columns)
        }
    }
```

## OTIMIZAÇÕES DE FORMATO

### Context Filtering
```python
def optimize_context(self, df, user_query):
    # Filtrar colunas relevantes baseado na query
    relevant_columns = self._extract_relevant_columns(user_query, df.columns)
    if relevant_columns:
        df = df[relevant_columns]
    
    # Filtrar por período se mencionado
    time_filter = self._extract_time_filter(user_query)
    if time_filter:
        df = self._apply_time_filter(df, time_filter)
    
    return df
```

### Token Optimization
```python
def optimize_for_tokens(self, df):
    # Reduzir precisão de floats
    float_cols = df.select_dtypes(include=['float']).columns
    df[float_cols] = df[float_cols].round(4)
    
    # Formato compacto para datas
    date_cols = df.select_dtypes(include=['datetime']).columns
    df[date_cols] = df[date_cols].dt.strftime('%Y-%m-%d')
    
    return df
```

## IMPLEMENTAÇÃO PRINCIPAL

### Agent Class
```python
class DataLakeAgent:
    def __init__(self, hive_connection):
        self.connection = hive_connection
        self.processor = DataProcessor()
    
    def query_and_process(self, sql_query, user_context=""):
        # 1. Executar query no datalake
        result = self.connection.execute(sql_query)
        df = pd.DataFrame(result)
        
        # 2. Otimizar contexto baseado na query do usuário
        df = self.processor.optimize_context(df, user_context)
        df = self.processor.optimize_for_tokens(df)
        
        # 3. Processar baseado no volume
        formatted_data = self.processor.process(df, user_context)
        
        return formatted_data
```

## FORMATO DE SAÍDA PADRONIZADO

### Estrutura JSON Universal
```json
{
  "metadata": {
    "total_rows": int,
    "total_columns": int,
    "strategy": "direct|chunked|rag",
    "processing_info": {...}
  },
  "schema": {
    "column_name": "data_type"
  },
  "summary": {
    "aggregations": {...},
    "key_insights": [...]
  },
  "data_payload": {
    // Varia conforme estratégia
  }
}
```

## CONFIGURAÇÃO

### Parâmetros Principais
```python
CONFIG = {
    "thresholds": {
        "small_data": 50000,
        "medium_data": 500000,
        "large_data": 1000000
    },
    "chunking": {
        "chunk_size": 25000,
        "temporal_frequency": "M",  # Monthly
        "max_chunks": 20
    },
    "optimization": {
        "float_precision": 4,
        "date_format": "%Y-%m-%d",
        "max_sample_rows": 5
    }
}
```

## DEPENDÊNCIAS

```python
# requirements.txt
pandas>=1.5.0
pyhive>=0.6.0
numpy>=1.20.0
chromadb>=0.4.0  # Para RAG (opcional)
```

## IMPLEMENTAÇÃO FASEADA

### Fase 1: Base (até 100k linhas)
- DataProcessor com estratégia "direct"
- Otimizações básicas de token
- Context filtering simples

### Fase 2: Escalabilidade (100k-500k linhas)  
- Chunking inteligente
- Estratégias múltiplas (temporal, categórico, size-based)
- Agregações prévias

### Fase 3: RAG (500k+ linhas)
- Vector database integration
- Embedding pipeline
- Semantic search
