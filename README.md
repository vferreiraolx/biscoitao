# 🍪 Biscoitão

Consolida dados de receita OLX em uma aba única e integra inteligência artificial via API Toqan.

## Como usar

### Consolidação de Receitas
1. **Apps Script:** Cole o código de `biscoitao.gs`
2. **Planilha:** https://docs.google.com/spreadsheets/d/1UZlUinLJOVtMFFGwJu1A8rr-5QNzG0FoFWPtkPTwrSs/edit
3. **Execute:** `consolidarReceita()`

### Assistente IA (Toqan)
1. **Configure a chave:** Execute `configurarChaveToqan("SUA_CHAVE_API")` no editor
2. **Use na planilha:** Digite `=perguntarToqan("sua pergunta")` em qualquer célula
3. **Aguarde:** A resposta aparecerá automaticamente na célula abaixo

## Estrutura

- **Entrada:** Abas com colunas `data` e `receita`
- **Saída:** Aba `Consolidado_Temporal` com totais mensais
- **IA:** Respostas inteligentes via Toqan API

## Funções

- `perguntarToqan(pergunta)` - Consulta o assistente IA
- `configurarChaveToqan(chave)` - Configura autenticação segura
- `testarToqanEditor()` - Diagnóstico de conexão

## Integração Toqan

A conexão com a API Toqan utiliza o padrão:
1. **POST** `/create_conversation` - Inicia conversa
2. **GET** `/get_answer` - Busca resposta via polling com query parameters

**OLX Internal** - 21/08/2025

