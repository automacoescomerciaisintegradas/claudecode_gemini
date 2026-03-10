# Arquitetura do Multi-Agent Framework

## Visão Geral da Estrutura

```
/code/
├── 📄 README.md                          # Documentação principal
├── 📄 LICENSE                            # Licença AGPL-3.0
├── 📄 package.json                       # Configuração NPM principal
├── 📄 run.py                             # CLI principal do framework
├── 📄 .gitignore                         # Arquivos ignorados pelo Git
├── 📄 .env.example                       # Exemplo de variáveis de ambiente
├── 📄 ruff.toml                          # Configuração do linter Python
├── 📄 mypy.ini                           # Configuração do type checker
├── 📄 pyproject.toml                     # Configuração pytest e coverage
├── 📄 .pre-commit-config.yaml            # Hooks de pre-commit
│
├── 📁 scripts/                           # Scripts de automação
│   ├── install.sh                        # Instalação completa
│   ├── build.sh                          # Build do projeto
│   ├── start.sh                          # Inicialização
│   └── test.sh                           # Execução de testes
│
├── 📁 docs/                              # Documentação
│   ├── requisitos/
│   │   └── REQUISITOS.md                 # Requisitos funcionais e não funcionais
│   ├── adr/                              # Architecture Decision Records
│   │   ├── DECISOES_TECNICAS.md          # Visão geral das decisões
│   │   ├── ADR-001-arquitetura-multi-agent.md
│   │   ├── ADR-002-git-worktrees.md
│   │   └── ADR-003-qa-pipeline.md
│   └── rfc/                              # Requests for Comments
│       └── RFC-001-Sistema-Plugins.md
│
├── 📁 apps/                              # Aplicações principais
│   │
│   ├── 📁 backend/                       # Backend Python
│   │   ├── agents/                       # Sistema multi-agente
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py             # Classe base para agentes
│   │   │   ├── planning_agent.py         # Agente de planejamento
│   │   │   ├── coding_agent.py           # Agente de codificação
│   │   │   ├── qa_agent.py               # Agente de QA
│   │   │   ├── merge_agent.py            # Agente de merge
│   │   │   └── agent_orchestrator.py     # Orquestrador de agentes
│   │   │
│   │   ├── qa_pipeline/                  # Pipeline de QA
│   │   │   ├── __init__.py
│   │   │   └── pipeline.py               # Pipeline automatizado de QA
│   │   │
│   │   ├── config/                       # Configurações
│   │   │   ├── __init__.py
│   │   │   └── settings.py               # Configurações do ambiente
│   │   │
│   │   ├── utils/                        # Utilitários
│   │   │   ├── __init__.py
│   │   │   └── git.py                    # Gerenciador Git
│   │   │
│   │   ├── specs/                        # Especificações (gerado)
│   │   ├── results/                      # Resultados (gerado)
│   │   ├── .worktrees/                   # Worktrees Git (gerado)
│   │   │
│   │   ├── requirements.txt              # Dependências Python
│   │   └── spec_runner.py                # CLI de gerenciamento de specs
│   │
│   └── 📁 frontend/                      # Frontend Electron
│       ├── electron/                     # Configuração Electron
│       │   ├── main.ts                   # Processo principal
│       │   └── preload.ts                # Script de preload
│       │
│       ├── src/                          # Código React
│       │   ├── components/               # Componentes React
│       │   │   ├── KanbanBoard.tsx       # Quadro Kanban
│       │   │   ├── KanbanColumn.tsx      # Coluna do Kanban
│       │   │   ├── KanbanCard.tsx        # Card de tarefa
│       │   │   ├── AgentTerminal.tsx     # Terminal de agente
│       │   │   ├── AgentTerminals.tsx    # Grid de terminais
│       │   │   ├── AgentsView.tsx        # View de agentes
│       │   │   ├── Sidebar.tsx           # Sidebar de navegação
│       │   │   ├── CreateTaskModal.tsx   # Modal de criação
│       │   │   └── TaskDetailPanel.tsx   # Painel de detalhes
│       │   │
│       │   ├── store/                    # Gerenciamento de estado
│       │   │   └── appStore.ts           # Zustand store
│       │   │
│       │   ├── types/                    # Tipos TypeScript
│       │   │   └── index.ts              # Definições de tipos
│       │   │
│       │   ├── App.tsx                   # Componente principal
│       │   ├── main.tsx                  # Ponto de entrada React
│       │   └── index.css                 # Estilos globais
│       │
│       ├── package.json                  # Dependências frontend
│       ├── tsconfig.json                 # Config TypeScript
│       ├── vite.config.ts                # Config Vite
│       ├── tailwind.config.js            # Config TailwindCSS
│       └── postcss.config.js             # Config PostCSS
│
├── 📁 tests/                             # Testes
│   ├── unit/                             # Testes unitários
│   └── integration/                      # Testes de integração
│
└── 📁 .github/                           # Configuração GitHub
    ├── workflows/                        # GitHub Actions
    └── ISSUE_TEMPLATE/                   # Templates de issue
```

---

## Fluxo de Execução

### 1. Criação de Tarefa
```
Usuário → Kanban Board → CreateTaskModal → appStore → Task criada
```

### 2. Execução do Pipeline
```
Task → Orchestrator → Planning Agent → Coding Agent → QA Agent → Merge Agent
```

### 3. Pipeline de QA
```
Código → Linting (ruff) → Testes (pytest) → Type Check (mypy) → Security (bandit) → Coverage
```

---

## Componentes Principais

### Backend Python

| Componente | Descrição |
|------------|-----------|
| `BaseAgent` | Classe abstrata base para todos os agentes |
| `PlanningAgent` | Analisa requisitos e cria especificações |
| `CodingAgent` | Implementa código baseado em specs |
| `QAAgent` | Valida qualidade do código |
| `MergeAgent` | Integra mudanças para branch principal |
| `AgentOrchestrator` | Coordena múltiplos agentes |
| `QAPipeline` | Pipeline automatizado de validação |
| `GitManager` | Gerencia worktrees e operações Git |
| `SpecRunner` | CLI para gerenciamento de tarefas |

### Frontend React

| Componente | Descrição |
|------------|-----------|
| `KanbanBoard` | Quadro visual de tarefas |
| `KanbanColumn` | Coluna com tarefas de um status |
| `KanbanCard` | Card individual de tarefa |
| `AgentTerminal` | Terminal Xterm.js para output |
| `AgentTerminals` | Grid de múltiplos terminais |
| `AgentsView` | Monitoramento de agentes |
| `Sidebar` | Navegação lateral |
| `CreateTaskModal` | Formulário de criação |
| `TaskDetailPanel` | Detalhes da tarefa |
| `appStore` | Estado global com Zustand |

---

## Tecnologias por Camada

### Frontend
```
Electron (Desktop)
  └── React 18 (UI)
      ├── TypeScript (Tipagem)
      ├── TailwindCSS (Estilos)
      ├── Zustand (Estado)
      ├── Xterm.js (Terminais)
      └── React DnD (Drag-and-drop)
```

### Backend
```
Python 3.10+
  ├── Anthropic SDK (IA)
  ├── Pydantic (Validação)
  ├── Click (CLI)
  ├── Rich (Output)
  ├── GitPython (Git)
  ├── pytest (Testes)
  ├── ruff (Linting)
  └── mypy (Type Check)
```

---

## Comandos Disponíveis

```bash
# Instalação
./scripts/install.sh

# Desenvolvimento
npm run dev

# Build
./scripts/build.sh

# Testes
./scripts/test.sh

# CLI Python
python run.py create --interactive
python run.py run --spec 001
python run.py list
python run.py status
```

---

## Variáveis de Ambiente

```bash
# Obrigatórias
ANTHROPIC_API_KEY=sk-...

# Opcionais
MAX_PARALLEL_AGENTS=12
AGENT_TIMEOUT_MINUTES=60
DEFAULT_MODEL=claude-sonnet-4-20250514
MAIN_BRANCH=main
AUTO_COMMIT=true
RUN_TESTS=true
ENABLE_MEMORY_LAYER=true
```

---

## Decisões de Arquitetura (ADRs)

1. **ADR-001**: Arquitetura Multi-Agent com Orquestração Centralizada
2. **ADR-002**: Git Worktrees para Isolamento de Tarefas
3. **ADR-003**: Pipeline de QA em 5 Estágios

---

## RFCs Ativas

1. **RFC-001**: Sistema de Plugins para Extensibilidade (Em Discussão)

---

## Próximos Passos

1. Instalar dependências: `./scripts/install.sh`
2. Configurar `.env` com API key
3. Iniciar aplicação: `npm start`
4. Criar primeira tarefa no Kanban
5. Acompanhar execução nos Terminais
