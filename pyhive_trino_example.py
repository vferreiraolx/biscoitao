"""
pyhive_trino_example.py

Exemplo de conexão ao Trino Gateway OLX via PyHive.
Guarde aqui todos os scripts e testes relacionados ao acesso ao Data Lake via Trino.

Requisitos:
- pip install "pyhive>=0.6.5" requests pandas

Configuração:
- Solicite acesso ao Trino Gateway para o time de Engenharia de Dados.
- Use seu usuário AD (sem @olxbr.com) e senha.

Autor: OLX Data Engineering
Data: 2025-08-21
"""

from pyhive import trino
import pandas as pd

from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
USUARIO_OLX = os.getenv('USUARIO_OLX')
SENHA_OLX = os.getenv('SENHA_OLX')

conn = trino.connect(
    host='data-lake.olx.com.br',
    port=443,
    username=USUARIO_OLX,
    password=SENHA_OLX,
    http_scheme='https',
    catalog='hive',
    schema='default'
)

# Substitua pelos seus dados de AD
db_user = 'SEU_USUARIO_AD'      # sem @olxbr.com
db_pass = 'SUA_SENHA_AD'

conn = trino.connect(
    host='trino-gateway.dataeng.bigdata.olxbr.io',
    port=443,
    protocol='https',
    source='dataeng-trino-api',
    username=db_user,
    password=db_pass
)

# Exemplo de consulta simples
cursor = conn.cursor()
cursor.execute('SELECT * FROM ods.ad WHERE year=2019 AND month=12 AND day=25 LIMIT 10')
for row in cursor.fetchall():
    print(row)

# Exemplo usando pandas
df = pd.read_sql(
    'SELECT * FROM ods.ad WHERE year=2019 AND month=12 AND day=25 LIMIT 10',
    conn
)
print(df.head())
