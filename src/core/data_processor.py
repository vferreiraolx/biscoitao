import pandas as pd
from typing import Any, Dict

class SimpleDataProcessor:
    """
    Processa DataFrames para consumo por LLM, usando formatação direta ou chunking básico.
    """
    SMALL_THRESHOLD = 50000
    CHUNK_SIZE = 25000

    def process(self, df: pd.DataFrame, user_query: str = "") -> Dict[str, Any]:
        rows = len(df)
        if rows <= self.SMALL_THRESHOLD:
            return self._format_direct(df)
        else:
            return self._format_chunked(df, user_query)

    def _format_direct(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "metadata": {
                "rows": len(df),
                "columns": len(df.columns),
                "strategy": "direct"
            },
            "schema": dict(df.dtypes.astype(str)),
            "data": df.to_csv(index=False)
        }

    def _format_chunked(self, df: pd.DataFrame, user_query: str = "") -> Dict[str, Any]:
        chunks = self._create_chunks(df)
        return {
            "metadata": {
                "total_rows": len(df),
                "chunks": len(chunks),
                "strategy": "chunked",
                "chunk_size": self.CHUNK_SIZE
            },
            "schema": dict(df.dtypes.astype(str)),
            "chunks": [chunk.to_csv(index=False) for chunk in chunks]
        }

    def _create_chunks(self, df: pd.DataFrame):
        # Chunking simples por tamanho
        return [df[i:i+self.CHUNK_SIZE] for i in range(0, len(df), self.CHUNK_SIZE)]
