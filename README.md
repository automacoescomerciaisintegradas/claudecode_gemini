# Multi-Agent Framework

<div align="center">

![Multi-Agent Framework](https://img.shields.io/badge/Multi--Agent-Framework-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Node](https://img.shields.io/badge/Node-18+-brightgreen)
![License](https://img.shields.io/badge/License-AGPL--3.0-orange)

**Framework Autônomo de Codificação Multi-Agente**

Planeja, constrói e valida software de forma autônoma

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Documentação](#-documentação)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **Multi-Agent Framework** é um sistema autônomo que utiliza múltiplos agentes de IA especializados para automatizar o ciclo completo de desenvolvimento de software.

### O que ele faz?

1. **Analisa requisitos** e cria especificações técnicas detalhadas
2. **Implementa código** seguindo boas práticas e padrões
3. **Valida qualidade** através de testes automatizados e análise estática
4. **Integra mudanças** de forma segura com resolução de conflitos

### Quando usar?

- ✅ Automatizar tarefas repetitivas de desenvolvimento
- ✅ Acelerar prototipagem de novas funcionalidades
- ✅ Gerar código boilerplate automaticamente
- ✅ Validar qualidade de código consistentemente
- ✅ Gerenciar múltiplas tarefas em paralelo

---

## ✨ Funcionalidades

### Quadro Kanban
- Gerenciamento visual de tarefas do planejamento até a conclusão
- Drag-and-drop entre colunas de status
- Acompanhamento em tempo real do progresso dos agentes

### Terminais de Agente
- Múltiplos terminais alimentados por IA
- Injeção de contexto de tarefa em um clique
- Geração de múltiplos agentes para trabalho paralelo
- Output em tempo real com syntax highlighting

### Sistema Multi-Agent
| Agente | Responsabilidade |
|--------|-----------------|
| 📝 Planning Agent | Análise de requisitos e planejamento |
| 💻 Coding Agent | Implementação de código |
| 🔍 QA Agent | Validação de qualidade |
| 🔀 Merge Agent | Integração de mudanças |
| 🎯 Orchestrator | Coordenação de agentes |

### Pipeline de QA
- **Linting** (ruff) - Verificação de estilo de código
- **Testes** (pytest) - Execução de testes automatizados
- **Type Checking** (mypy) - Verificação de tipos
- **Security** (bandit) - Scan de vulnerabilidades
- **Coverage** - Medição de cobertura de testes

### Memory Layer
- Retém insights entre sessões
- Identifica problemas comuns
- Sugere otimizações
- Calcula taxa de sucesso

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Electron Desktop App                      │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────────┐  │
│  │   Kanban    │ │  Terminais   │ │    Agents View      │  │
│  │    Board    │ │   de Agente  │ │   (Monitoramento)   │  │
│  └─────────────┘ └──────────────┘ └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Python Backend                            │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────────┐  │
│  │  Planning   │ │   Coding     │ │       QA            │  │
│  │   Agent     │ │   Agent      │ │      Agent          │  │
│  └─────────────┘ └──────────────┘ └─────────────────────┘  │
│  ┌─────────────┐ ┌──────────────┐                          │
│  │   Merge     │ │ Orchestrator │                          │
│  │   Agent     │ │   (Coordena) │                          │
│  └─────────────┘ └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude Code CLI + Git Worktrees + QA Tools                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Instalação

### Pré-requisitos

- **Python 3.10+**
- **Node.js 18+**
- **Git**
- **Claude Pro/Max** (para API key)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/automacoescomerciaisintegradas/multi-agent-framework.git
cd multi-agent-framework

# Execute o script de instalação
chmod +x scripts/install.sh
./scripts/install.sh

# Configure suas variáveis de ambiente
cp .env.example .env
# Edite .env e adicione sua ANTHROPIC_API_KEY
```

### Instalação Manual

```bash
# Backend Python
cd apps/backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend Electron
cd ../frontend
npm install

# Raiz
cd ../..
npm install
```

---

## 🚀 Uso

### Iniciar a Aplicação

```bash
# Modo desenvolvimento (hot reload)
npm run dev

# Modo produção
npm start
```

### Via CLI

```bash
# Criar nova tarefa
python run.py create --interactive

# Executar tarefa
python run.py run --spec 001

# Listar tarefas
python run.py list

# Ver status do sistema
python run.py status
```

### Exemplo de Fluxo

1. **Criar Tarefa no Kanban**
   - Clique em "Nova Tarefa"
   - Preencha título, descrição e requisitos
   - A tarefa aparece na coluna "Pendentes"

2. **Executar Agentes**
   - Arraste a tarefa para "Planejamento"
   - Os agentes começam a trabalhar automaticamente
   - Acompanhe o progresso nos Terminais

3. **Revisar Resultado**
   - Clique na tarefa para ver detalhes
   - Revise o código gerado
   - Aprovar ou solicitar mudanças

---

## 📚 Documentação

### Documentos Principais

| Documento | Descrição |
|-----------|-----------|
| [Requisitos](docs/requisitos/REQUISITOS.md) | Requisitos funcionais e não funcionais |
| [Decisões Técnicas](docs/adr/DECISOES_TECNICAS.md) | Decisões de arquitetura e tecnologia |
| [ADRs](docs/adr/) | Architecture Decision Records |
| [RFCs](docs/rfc/) | Requests for Comments |

### ADRs Disponíveis

- [ADR-001](docs/adr/ADR-001-arquitetura-multi-agent.md) - Arquitetura Multi-Agent
- [ADR-002](docs/adr/ADR-002-git-worktrees.md) - Git Worktrees para Isolamento
- [ADR-003](docs/adr/ADR-003-qa-pipeline.md) - Pipeline de QA em 5 Estágios

### RFCs Ativas

- [RFC-001](docs/rfc/RFC-001-Sistema-Plugins.md) - Sistema de Plugins (Em Discussão)

---

## 🧪 Testes

```bash
# Rodar todos os testes
./scripts/test.sh

# Apenas backend
cd apps/backend && pytest

# Apenas frontend
cd apps/frontend && npm test
```

---

## 🛠️ Tecnologias

### Frontend
- Electron, React 18, TypeScript
- TailwindCSS, Zustand
- Xterm.js, React DnD

### Backend
- Python 3.10+, Anthropic SDK
- Pydantic, Click, Rich
- GitPython, pytest, ruff, mypy

---

## 🤝 Contribuição

Contribuições são bem-vindas! Veja nosso guia:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Desenvolvendo

```bash
# Setup de desenvolvimento
./scripts/install.sh

# Rodar em modo desenvolvimento
npm run dev

# Rodar linters
npm run lint
cd apps/backend && ruff check .
```

---

## 📄 Licença

Este projeto está sob a licença **AGPL-3.0**. Veja [LICENSE](LICENSE) para detalhes.

---

## 🔗 Links

- [Repositório](https://github.com/automacoescomerciaisintegradas/multi-agent-framework)
- [Issues](https://github.com/automacoescomerciaisintegradas/multi-agent-framework/issues)
- [Discord](#) (em breve)

---

<div align="center">

**Multi-Agent Framework** - Automatizando o desenvolvimento de software

Feito com ❤️ por [Automacoes Comerciais Integradas](https://github.com/automacoescomerciaisintegradas)

</div>
