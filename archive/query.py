import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pandas as pd
from pyhive import trino
import os
from dotenv import load_dotenv

def execute_query(query):
    """
    Executa uma query na tabela dw.monetization_total e retorna o resultado como um DataFrame.

    Args:
        query (str): A query SQL a ser executada.

    Returns:
        pd.DataFrame: Resultado da query em formato DataFrame.
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    USUARIO_OLX = os.getenv('USUARIO_OLX')
    SENHA_OLX = os.getenv('SENHA_OLX')

    conn = trino.connect(
        host='trino-gateway.dataeng.bigdata.olxbr.io',
        port=443,
        protocol='https',
        source='dataeng-trino-api',
        username=USUARIO_OLX,
        password=SENHA_OLX
    )

    return pd.read_sql(query, conn)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        try:
            result_df = execute_query(query)
            print(result_df)
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
    else:
        print("Por favor, forneça uma query como argumento ao executar o script.")
