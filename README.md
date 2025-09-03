# 🍪 Biscoitão

Assistente inteligente que conecta analistas OLX ao datalake via consultas conversacionais, permitindo análises de receita e métricas através de perguntas em linguagem natural.

## Visão Geral

O Biscoitão integra:

- **Frontend:** Google Sheets + Apps Script (interface familiar aos analistas)
- **Backend:** Flask + PyHive (conexão direta ao datalake OLX via Trino)
- **IA:** API Toqan (interpretação de perguntas e formatação de respostas)
- **Dados:** Acesso direto às tabelas do datalake (dw.monetization_total, etc.)

## Como usar

### Configuração Inicial

1. **Configure credenciais:** Adicione `.env` com suas credenciais do Trino
2. **Instale dependências:** `pip install flask pyhive pandas python-dotenv`
3. **Inicie o backend:** `python app.py` (roda na porta 5000)
4. **Configure Apps Script:** Execute `configurarChaveToqan("SUA_CHAVE_API")` no editor

### Fazendo Consultas

1. **Na planilha:** Digite `=perguntarToqan("sua pergunta")` em qualquer célula
2. **Exemplos de perguntas:**
   - "Qual foi a receita de dezembro de 2023?"
   - "Compare receita Q1 vs Q2 deste ano"
   - "Mostre a tendência dos últimos 6 meses"
   - "Quais categorias tiveram maior crescimento?"

### Tipos de Resposta

- **Respostas textuais:** Análises e insights em linguagem natural
- **Tabelas condensadas:** Dados relevantes formatados e sumarizados
- **Gráficos:** Visualizações quando apropriado (futuro)
- **Sumarização automática:** O backend interpreta perguntas sobre soma de vendas e retorna o resultado textual no campo `summary` da resposta JSON

## Arquitetura Técnica

### Fluxo de Dados

```text
Pergunta (Sheets) → Toqan (interpretação) → Flask (PyHive) → Datalake → 
DataProcessor (otimização) → Sumarização automática → Toqan (formatação) → Resposta (Sheets)
```

### Processamento de Dados

- **≤50k linhas:** Envio direto para LLM
- **50k-500k linhas:** Chunking inteligente (temporal/categórico)
- **Otimizações:** Context filtering, token optimization, precisão de floats
- **Sumarização:** Backend calcula e retorna respostas textuais para perguntas de soma de vendas

### Infraestrutura

- **Atual:** Notebook corporativo local (desenvolvimento/protótipo)
- **Futuro:** AWS (produção, conforme sucesso do protótipo)

## Funções

- `perguntarToqan(pergunta)` - Consulta conversacional ao datalake
- `configurarChaveToqan(chave)` - Configura autenticação segura
- `testarToqanEditor()` - Diagnóstico de conexão

## Integração APIs

### Toqan (IA Conversacional)

1. **POST** `/create_conversation` - Inicia conversa
2. **GET** `/get_answer` - Busca resposta via polling

### Backend Flask (Datalake)

1. **POST** `/query` - Executa consultas no datalake
2. **Payload:** `{"question": "pergunta do usuário"}`
3. **Response:** Dados otimizados para contexto LLM, incluindo campo `summary` com resposta interpretativa

**OLX Internal** - 22/08/2025

