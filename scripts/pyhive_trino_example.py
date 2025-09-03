import warnings

# Suprimir aviso do pandas sobre SQLAlchemy
warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable*")

from pyhive import trino
import pandas as pd
import os
from dotenv import load_dotenv
import shutil
from rich.console import Console
from rich.panel import Panel
from tabulate import tabulate

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



# Exemplo usando pandas
df = pd.read_sql(
    'SELECT * FROM hive.dw.monetization_total WHERE year=2019 AND month=12 AND day=25 LIMIT 1',
    conn
)

# Configurar pandas para exibir mais colunas e ajustar largura
df = df.head(10)  # Exibir apenas as 10 primeiras linhas para legibilidade
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Exibir saída padrão do pandas
print(df)

# Executar um DESCRIBE na tabela para obter informações sobre as colunas
describe_query = "DESCRIBE hive.dw.monetization_total"
describe_df = pd.read_sql(describe_query, conn)

# Salvar o DataFrame original em um arquivo CSV
output_csv = __file__.replace('.py', '.csv')
df.to_csv(output_csv, index=False)
print(f"Dados salvos em: {output_csv}")

# Exibir descritivo das colunas no terminal
print("Descritivo das colunas:")
for _, row in describe_df.iterrows():
    print(f"- {row['Column']}: {row['Type']}")

def execute_query(query):
    """
    Executa uma query no Trino e retorna o resultado como um DataFrame.

    Args:
        query (str): A query SQL a ser executada.

    Returns:
        pd.DataFrame: Resultado da query em formato DataFrame.
    """
    return pd.read_sql(query, conn)

# Exemplo de uso da função
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result_df = execute_query(query)
        print(result_df)
    else:
        print("Por favor, forneça uma query como argumento ao executar o script.")
