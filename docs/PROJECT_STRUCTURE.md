# 📁 Biscoitão - Estrutura Organizada

## 📋 Estrutura do Projeto

```
Biscoitão/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 core/                     # Módulos centrais
│   │   ├── query.py                 # Conexão com banco (PyHive/Trino)
│   │   ├── data_processor.py        # Processamento de dados
│   │   └── __init__.py
│   ├── 📁 generators/               # Geradores de relatórios
│   │   ├── visual_assistant.py      # Geração de gráficos
│   │   ├── html_generator.py        # Relatórios HTML
│   │   ├── pdf_generator.py         # Relatórios PDF
│   │   └── __init__.py
│   ├── 📁 integrations/             # Integrações externas
│   │   ├── sheets_integrator.py     # Google Sheets
│   │   ├── toqan_api.py            # API Toqan
│   │   └── __init__.py
│   └── 📁 api/                      # APIs e serviços web
│       ├── flask_app.py             # Servidor Flask
│       └── __init__.py
├── 📁 scripts/                      # Scripts executáveis
│   ├── biscoitao_cli.py            # Interface de linha de comando
│   ├── demo_reports.py             # Demonstrações
│   └── setup.py                    # Configuração inicial
├── 📁 google_apps_script/           # Código Google Apps Script
│   ├── biscoitao.gs                # Função principal
│   ├── appsscript.json            # Configuração
│   └── .clasp.json                # Deploy config
├── 📁 tests/                        # Testes
│   ├── test_core.py
│   ├── test_generators.py
│   └── test_integration.py
├── 📁 docs/                         # Documentação
│   ├── README.md                   # Documentação principal
│   ├── ARCHITECTURE.md            # Arquitetura
│   └── API_GUIDE.md               # Guia da API
├── 📁 output/                       # Arquivos gerados
│   ├── reports/                    # Relatórios
│   ├── charts/                     # Gráficos
│   └── temp/                       # Temporários
├── 📁 archive/                      # Arquivos obsoletos
│   └── [arquivos antigos]
├── .env                            # Variáveis de ambiente
├── .gitignore                      # Git ignore
├── requirements.txt                # Dependências Python
└── pyproject.toml                  # Configuração do projeto
```

## 🔄 Organização Implementada

### ✅ Arquivos Ativos (Movidos para nova estrutura):
- **Core:** `query.py`, `data_processor.py`
- **Generators:** `visual_assistant.py`, `html_report_generator.py`, `pdf_report_generator.py`
- **Integrations:** `sheets_integrator.py`
- **Scripts:** `biscoitao_direto.py` → `biscoitao_cli.py`
- **Google Apps Script:** `biscoitao.gs`, `appsscript.json`

### 📦 Arquivos Obsoletos (Movidos para archive/):
- `nl_query_assistant.py` (v1 - obsoleto)
- `nl_query_assistant_v2.py` (substituído)
- `app.py` (substituído por flask_app.py)
- `master_biscoitao.py` (funcionalidade integrada)
- `flask_server.py` (refatorado)
- `visual_api.py` (não usado)
- Documentação duplicada/obsoleta

### 🧹 Limpeza Realizada:
- Removidas duplicidades entre arquivos similares
- Consolidadas funcionalidades espalhadas
- Padronizada estrutura de imports
- Criados `__init__.py` para módulos Python
- Movido `__pycache__/` para .gitignore

## 🚀 Benefícios da Nova Estrutura

1. **Modularidade:** Separação clara de responsabilidades
2. **Manutenibilidade:** Código organizado e fácil de encontrar
3. **Escalabilidade:** Estrutura preparada para crescimento
4. **Padrões:** Seguindo boas práticas Python
5. **Deploy:** Separação clara entre código e configuração

## 📱 Como Usar

### Desenvolvimento Local:
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar CLI
python scripts/biscoitao_cli.py "sua consulta"

# Demonstração
python scripts/demo_reports.py
```

### Google Apps Script:
```javascript
// No Google Sheets
=perguntarToqan("sua consulta")
```

### API Web:
```bash
# Iniciar servidor
python src/api/flask_app.py

# Acessar
http://localhost:5000
```
