# 🍪 Biscoitão

Sistema de consolidação de dados de receita do Grupo OLX para consultas via IA Toqan.

## O que faz

Pega dados de receita espalhados em várias abas de uma planilha e consolida tudo em uma aba única, organizados por mês, para a IA conseguir responder perguntas sobre receita de forma rápida e precisa.

## Como funciona

1. **Detecta automaticamente** abas com dados de receita na planilha
2. **Consolida os dados** em formato mensal na aba "Consolidado_Temporal"  
3. **Prepara tudo** para a IA Toqan consultar via API
4. **Roda diariamente** de forma automática
5. **Envia notificação** quando termina ou dá erro

## Setup rápido

### 1. Configure no Google Apps Script

- Acesse [script.google.com](https://script.google.com)
- Novo projeto → cole o código de `src/main.gs` e `config/constants.gs`

### 2. Configure os IDs

Edite em `constants.gs`:

```javascript
const RECURSOS_OLX = {
  SPREADSHEET_DADOS_RECEITA: 'COLE_ID_DA_PLANILHA_AQUI',
  // outros IDs conforme necessário
};
```

### 3. Configure propriedades do script

No Apps Script → Configurações → Propriedades do script:

```text
EMAIL_ADMIN = seu.email@grupoolx.com
TOQAN_API_TOKEN = seu_token_aqui
```

### 4. Teste

Execute no Apps Script:

```javascript
// Validar sistema
validarSistemaOLX();

// Primeira consolidação  
funcaoPrincipal();
```

## Estrutura dos dados

### Entrada (suas abas)

Qualquer aba com colunas como: data, receita, produto, região, etc.

### Saída (aba "Consolidado_Temporal")

Uma linha por mês com todas as métricas consolidadas:

```text
mes_ano | data_atualizacao | rec_receita | rec_produto | reg_regiao | ...
2024-01 | 21/08/2025       | 180000      | 100000      | 80000      | ...
```

## Principais funções

- `funcaoPrincipal()` - Executa consolidação completa
- `detectarAbasReceita()` - Encontra abas com dados
- `validarSistemaOLX()` - Verifica se está tudo configurado
- `logarExecucao(nivel, msg)` - Sistema de logs

## Automação

O sistema roda automaticamente todo dia. Para configurar:

```javascript
// No Apps Script
ScriptApp.newTrigger('funcaoPrincipal')
  .timeBased()
  .everyDays(1)
  .atHour(8)
  .create();
```

## Se der erro

1. Execute `validarSistemaOLX()` para ver o que está faltando
2. Verifique os logs no console do Apps Script
3. Confirme se os IDs das planilhas estão corretos

---

**Projeto interno Grupo OLX** - Última atualização: 21/08/2025

