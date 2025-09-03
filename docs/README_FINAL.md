# 📊 Biscoitão v2.0 - Sistema Integrado de Análise com PDF

## 🚀 Visão Geral

O Biscoitão v2.0 é um sistema completo de Business Intelligence conversacional que transforma consultas em linguagem natural em relatórios PDF profissionais com gráficos viridis. A integração permite que você use o Google Sheets como interface principal, obtendo análises visuais automaticamente.

## ✨ Principais Recursos

- 🗣️ **Consultas em Linguagem Natural**: "evolução do preço de jan-24 a jan-25"
- 📊 **Gráficos Automáticos**: Detecta automaticamente o melhor tipo de visualização
- 🎨 **Tema Viridis**: Cores profissionais (#440154 → #31688e → #35b779 → #fde725)
- 📄 **Relatórios PDF**: Geração automática via Markdown
- 📱 **Integração Google Sheets**: Função `=perguntarToqan()` nativa
- 🔍 **Insights Automáticos**: IA identifica padrões e tendências
- ⚡ **Processamento Rápido**: Análise em tempo real

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  Google Sheets  │───▶│  API Toqan      │───▶│  Servidor Flask     │
│  perguntarToqan │    │  (NL→SQL)       │    │  (localhost:5000)   │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                          │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 ▼                                 │
         ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────┐
         │ Visual Assistant │    │ PDF Generator    │    │ Sheets Integrator│    │ Flask Server │
         │ • Query Building │    │ • Markdown       │    │ • Conversations  │    │ • REST API   │
         │ • Chart Creation │    │ • PDF Conversion │    │ • Formatting     │    │ • Health     │
         │ • Insights       │    │ • File Management│    │ • Response       │    │ • Testing    │
         └─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────┘
```

## 🛠️ Instalação e Configuração

### 1️⃣ Preparação do Ambiente Python

```bash
# Verifique se Python 3.8+ está instalado
python --version

# Navegue até o diretório do projeto
cd "g:\Meu Drive\__AUTOMACOES\Biscoitão"

# Instale as dependências obrigatórias
pip install matplotlib seaborn pandas numpy flask flask-cors requests markdown markdown2

# Dependências opcionais para PDF (se quiser PDFs além de Markdown)
pip install pandoc weasyprint  # Podem ter conflitos no Windows
```

### 2️⃣ Configuração do Banco de Dados

Certifique-se de que o arquivo `query.py` está configurado corretamente com:
- Conexão PyHive para Trino
- Acesso à tabela `dw.monetization_total`
- Credenciais de autenticação

### 3️⃣ Inicialização do Servidor

```bash
# Inicie o servidor Flask
python flask_server.py

# O servidor rodará em:
# 🌐 http://localhost:5000
# 🌐 http://127.0.0.1:5000
```

### 4️⃣ Configuração do Google Apps Script

1. **Abra o Google Apps Script** do seu projeto Biscoitão
2. **Substitua o código** pelo conteúdo atualizado do arquivo `biscoitao.gs`
3. **Configure a chave da API Toqan**:
   ```javascript
   configurarChaveToqan("SUA_CHAVE_TOQAN_AQUI")
   ```
4. **Salve e teste** a função

## 📱 Como Usar no Google Sheets

### Sintaxe Básica
```
=perguntarToqan("sua consulta em linguagem natural")
```

### Exemplos de Consultas

```excel
=perguntarToqan("evolução do preço médio de jan-24 a jan-25")
=perguntarToqan("compare categorias por volume de vendas")
=perguntarToqan("top 10 produtos por receita")
=perguntarToqan("tendência mensal dos últimos 6 meses")
=perguntarToqan("distribuição de preços por categoria")
=perguntarToqan("correlação entre preço e volume")
```

### Tipos de Análise Suportados

| Consulta | Tipo de Gráfico | Exemplo |
|----------|----------------|---------|
| Evolução temporal | Line Chart | "preços ao longo do tempo" |
| Comparação categórica | Bar Chart | "vendas por categoria" |
| Distribuição | Histogram | "distribuição de preços" |
| Correlação | Scatter Plot | "preço vs volume" |
| Matriz de correlação | Heatmap | "correlações entre variáveis" |

## 📊 Resultados Gerados

### Para cada consulta, o sistema gera:

1. **📊 Gráfico PNG** - Visualização com tema viridis
2. **📝 Arquivo Markdown** - Relatório estruturado
3. **📄 Arquivo PDF** - Documento profissional (quando possível)
4. **💡 Insights Automáticos** - Padrões identificados pela IA
5. **📱 Resposta Formatada** - Texto otimizado para Google Sheets

### Exemplo de Resposta no Sheets:
```
📊 RELATÓRIO BISCOITÃO GERADO

🔍 Consulta: evolução do preço médio de jan-24 a jan-25
⏰ Gerado em: 28/08/2025 00:39:04

📈 Resultados:
• 2 registros analisados
• Tipo: Line Chart

💡 Principais Insights:
• Crescimento moderado: 3.5%
• Pico em 1/2025: 81.66
• Vale em 1/2024: 78.92

📄 Arquivos Gerados:
• PDF: relatorio_biscoitao_20250828_003904.pdf
• Markdown: relatorio_biscoitao_20250828_003904.md
• Gráfico: chart_line_chart_20250828_003904.png

💬 Resumo: Análise de 2 períodos mostra crescimento...
🔗 ID da Conversação: conv_20250828_003844
```

## 🔧 Testes e Validação

### Teste Rápido do Sistema
```bash
# Teste direto via linha de comando
python sheets_integrator.py "evolução do preço médio de jan-24 a jan-25"

# Teste completo do sistema
python test_system.py
```

### Teste via Navegador
```
# Acesse a interface web
http://localhost:5000

# Teste de health check
http://localhost:5000/api/health
```

### Teste no Google Sheets
```javascript
// No Google Apps Script, execute:
testarBiscoitao()

// Ou use diretamente no Sheets:
=perguntarToqan("teste de funcionamento")
```

## 🎨 Personalização do Tema Viridis

### Cores Principais
- **#440154** - Roxo escuro (dados baixos)
- **#31688e** - Azul médio (dados médios-baixos)  
- **#35b779** - Verde médio (dados médios-altos)
- **#fde725** - Amarelo brilhante (dados altos)

### Customização de Gráficos
O sistema aplica automaticamente:
- Gradientes viridis em todos os gráficos
- Fontes legíveis e profissionais
- Layout otimizado para impressão
- Cores acessíveis para daltônicos

## 📁 Estrutura de Arquivos

```
Biscoitão/
├── 📄 README.md                 # Este arquivo
├── 🐍 visual_assistant.py       # Motor de análise visual
├── 📄 pdf_report_generator.py   # Gerador de relatórios PDF
├── 🔗 sheets_integrator.py      # Integração com Google Sheets
├── 🌐 flask_server.py          # Servidor web Flask
├── 📱 biscoitao.gs             # Google Apps Script atualizado
├── 🧪 test_system.py           # Testes do sistema
├── 🗄️ query.py                # Conexão com banco de dados
├── 📊 data_processor.py        # Processamento de dados
├── 🛠️ schema_utils.py          # Utilitários de schema
└── 📂 outputs/                 # Arquivos gerados
    ├── 📊 graficos_*.png
    ├── 📝 relatorio_*.md
    └── 📄 relatorio_*.pdf
```

## 🐛 Solução de Problemas

### ❌ Erro: "Servidor não encontrado"
**Solução**: Verifique se o Flask está rodando em `localhost:5000`
```bash
python flask_server.py
```

### ❌ Erro: "Chave da API Toqan"
**Solução**: Configure a chave no Google Apps Script
```javascript
configurarChaveToqan("SUA_CHAVE_AQUI")
```

### ❌ Erro: "Módulo não encontrado"
**Solução**: Instale as dependências Python
```bash
pip install matplotlib seaborn pandas flask flask-cors
```

### ❌ Erro: "Falha na conversão PDF"
**Solução**: PDFs são opcionais. O sistema gera Markdown sempre.
- Para Windows: PDFs podem ter problemas de dependências
- Arquivos Markdown contêm o mesmo conteúdo profissional

### ❌ Erro: "Dados não encontrados"
**Solução**: Verifique a conexão com o banco via `query.py`

## 📈 Monitoramento e Logs

### Logs do Servidor Flask
```
📊 Servidor rodando: http://localhost:5000
✅ Consulta processada: "evolução do preço..."
📄 PDF gerado: relatorio_biscoitao_20250828_003904.pdf
```

### Logs do Google Apps Script
```javascript
console.log("🚀 Iniciando pergunta para Biscoitão:", pergunta);
console.log("✅ Conversação criada:", conversationId);
```

## 🔮 Próximas Versões

### Recursos Planejados
- 🤖 **IA Avançada**: GPT integration para insights mais profundos
- 📱 **Mobile App**: Interface móvel nativa
- 🔄 **Cache Inteligente**: Armazenamento de consultas frequentes
- 📧 **Email Reports**: Envio automático de relatórios
- 🎯 **Dashboards**: Painéis interativos personalizáveis
- 🔐 **Multi-tenant**: Suporte a múltiplas organizações

## 👥 Suporte e Contribuição

### Documentação Técnica
- **API Endpoints**: `http://localhost:5000/api/health`
- **Código Fonte**: Comentários detalhados em todos os arquivos
- **Arquitetura**: Diagrama na seção de arquitetura

### Contribuindo
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commite suas mudanças
4. Abra um Pull Request

### Suporte
- 📧 Email: [seu-email@exemplo.com]
- 💬 Issues: GitHub Issues
- 📖 Docs: Este README.md

---

## 🎉 Status do Sistema

```
✅ Funcionando:
   • Integração Google Sheets ↔ API Toqan
   • Geração de gráficos viridis automáticos
   • Análise de linguagem natural
   • Insights automáticos baseados em IA
   • Relatórios Markdown profissionais
   • Servidor Flask com endpoints REST
   • Sistema de arquivos organizado por timestamp

⚠️ Limitações:
   • PDFs podem falhar no Windows (dependências)
   • Requer servidor Flask rodando localmente
   • Conexão com banco via PyHive/Trino necessária

🎯 Pronto para uso em produção com Markdown!
```

---

**Biscoitão v2.0** - Transformando dados em insights visuais desde 2025 🚀
