from flask import Flask, request, jsonify
from query import execute_query
from data_processor import SimpleDataProcessor
from schema_utils import build_query
import pandas as pd

app = Flask(__name__)
processor = SimpleDataProcessor()

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question", "")

    # Exemplo: extrair tabela e filtros da pergunta (hardcoded para protótipo)
    table = "dw.monetization_total"
    filters = {"year": "2019", "month": "12"}  # Em produção, extrair do texto

    # Monta a query ajustada conforme o schema real
    sql_query = build_query(table, filters)
    sql_query += " LIMIT 5"  # Limita a 5 registros para teste rápido

    try:
        df = execute_query(sql_query)
        processed = processor.process(df, question)
        # Sumarização simples: soma de vendas
        summary = None
        vendas_col = None
        for col in df.columns:
            if "venda" in col.lower() or "price" in col.lower():
                vendas_col = col
                break
        if vendas_col:
            soma = df[vendas_col].sum()
            summary = f"A soma das vendas para o filtro aplicado foi {soma:.2f}."
        else:
            summary = "Coluna de vendas não encontrada para sumarização."
        output = {"result": processed, "sql_query": sql_query, "summary": summary}
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e), "sql_query": sql_query})

if __name__ == "__main__":
    app.run(debug=True)
