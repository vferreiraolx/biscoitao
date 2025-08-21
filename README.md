# 🍪 Biscoitão

Sistema de consolidação de dados de receita do Grupo OLX para interface conversacional com IA.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração Inicial](#configuração-inicial)
- [Como Usar](#como-usar)
- [Desenvolvimento](#desenvolvimento)
- [Contribuição](#contribuição)
- [Recursos Úteis](#recursos-úteis)

## 📝 Sobre o Projeto

O Biscoitão consolida informações de receita espalhadas em múltiplas fontes de dados, criando uma base unificada para consultas conversacionais via IA (Toqan).

### Principais Funcionalidades

- **Consolidação Automática**: Unifica dados de múltiplas abas em formato temporal mensal
- **Validação Inteligente**: Sistema autônomo de verificação de qualidade dos dados
- **Interface com IA**: Preparação de dados para consumo pela LLM Toqan
- **Monitoramento Proativo**: Detecção automática de mudanças e notificações
- **Integração APIs**: Conexão com sistemas externos (CRMs, ERPs)

## 🏗️ Estrutura do Projeto

```
Biscoitão/
├── 📁 src/               # Código-fonte principal
│   └── main.gs          # Arquivo principal do Apps Script
├── 📁 config/           # Arquivos de configuração
├── 📁 docs/             # Documentação detalhada
├── 📄 appsscript.json   # Manifest do Google Apps Script
├── 📄 README.md         # Documentação principal (este arquivo)
└── 📄 .gitignore        # Arquivos ignorados pelo Git
```

### Descrição das Pastas

| Pasta | Descrição |
|-------|-----------|
| `src/` | Contém todo o código-fonte do projeto |
| `config/` | Arquivos de configuração, templates e constantes |
| `docs/` | Documentação técnica detalhada |

## ⚙️ Configuração Inicial

### Pré-requisitos

- Conta Google com privilégios administrativos
- Acesso às planilhas de dados de receita do Grupo OLX
- Tokens de API da LLM Toqan
- Permissões para integração com sistemas externos

### Instalação

1. **Clone o repositório**

   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd Biscoitão
   ```

2. **Configure o Google Apps Script**
   - Acesse [script.google.com](https://script.google.com)
   - Crie um novo projeto
   - Copie o conteúdo dos arquivos da pasta `src/`

3. **Configure as integrações**
   - APIs: Google Sheets, Drive, Gmail
   - Tokens da LLM Toqan
   - Credenciais de sistemas externos

## 🚀 Como Usar

### Fluxo Principal

1. **Consolidação Automática**: Sistema processa abas de dados diariamente
2. **Validação**: Verificação automática de qualidade e consistência
3. **Interface IA**: Dados preparados para consultas via Toqan
4. **Monitoramento**: Notificações sobre status e atualizações

### Execução Manual

- Acesse Google Apps Script
- Execute `funcaoPrincipal()` para consolidação completa
- Execute `executarTestes()` para validação do sistema

## 👨‍💻 Desenvolvimento

### Estrutura de Código

O projeto segue as seguintes convenções:

- **Nomenclatura**: camelCase para funções e variáveis
- **Constantes**: UPPER_SNAKE_CASE
- **Arquivos**: Organizados por funcionalidade

### Adicionando Nova Funcionalidade

1. Crie uma nova função em `src/main.gs`
2. Documente a função com comentários JSDoc
3. Teste a funcionalidade
4. Atualize esta documentação

### Estrutura de Dados

- **Abas de Entrada**: Dados de receita por produto, região, período
- **Aba Consolidada**: Fluxo temporal mensal unificado
- **Logs**: Registro de execuções e validações
- **Configurações**: Parâmetros e credenciais do sistema

### Integração com IA

- **Toqan LLM**: Interface conversacional para consultas
- **Contexto Expandido**: Suporte a planilhas, PDFs, documentos
- **API Bidirecional**: Leitura e escrita em Google Workspace

## 🔧 Troubleshooting

### Problemas Comuns

| Problema | Solução |
|----------|---------|
| Erro de permissão | Verifique se as APIs necessárias estão habilitadas |
| Timeout de execução | Otimize o código ou use execução assíncrona |
| Limite de cota | Verifique os limites do Google Apps Script |

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📚 Recursos Úteis

- [Documentação Google Apps Script](https://developers.google.com/apps-script)
- [Referência da API](https://developers.google.com/apps-script/reference)
- [Guia de Melhores Práticas](https://developers.google.com/apps-script/guides/support/best-practices)
- [Google Apps Script CLI (clasp)](https://github.com/google/clasp)

## 📄 Licença

Projeto interno do Grupo OLX

---

**📧 Contato**: Equipe de Dados OLX  
**🔗 Repositório**: https://github.com/vferreiraolx/biscoitao  
**📅 Última atualização**: 21 de agosto de 2025

## 🎯 Status do Projeto

### ✅ Implementado
- Estrutura completa de documentação
- Sistema de detecção automática de abas
- Consolidação temporal mensal
- Integração com IA Toqan
- Sistema de logging e notificações
- Validação automônoma de dados

### 🔄 Em Desenvolvimento
- Conexões com APIs externas (CRM, ERP)
- Notificações via Slack
- Sistema de backup automático
- Dashboard de monitoramento

### 📋 Próximos Passos
1. Configurar IDs das planilhas OLX
2. Configurar token da API Toqan
3. Testar detecção de abas
4. Executar primeira consolidação
5. Integrar com sistema de notificações
