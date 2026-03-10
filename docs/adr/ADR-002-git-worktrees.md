# ADR-002: Git Worktrees para Isolamento de Tarefas

**Status:** Aceito  
**Data:** 2026-03-10  
**Decisão:** Utilizar Git Worktrees para isolamento de desenvolvimento

## Contexto

Cada tarefa precisa ser desenvolvida em isolamento para:
- Prevenir conflitos entre tarefas paralelas
- Permitir rollback seguro
- Manter branch principal limpa

Opções consideradas:
1. Múltiplos clones do repositório
2. Git Worktrees
3. Branches temporárias sem worktree

## Decisão

Utilizar **Git Worktrees** para criar ambientes isolados por tarefa.

### Estrutura

```
repositorio/
├── .git/
├── .worktrees/
│   ├── task-001/          # Worktree isolado
│   │   ├── src/
│   │   └── .git
│   └── task-002/
│       ├── src/
│       └── .git
└── main/                   # Branch principal
```

### Fluxo

1. Criar worktree: `git worktree add -b task-001 .worktrees/task-001 main`
2. Desenvolver no worktree
3. QA valida no worktree
4. Merge para main
5. Remover worktree: `git worktree remove .worktrees/task-001`

## Consequências

### Positivas
- Compartilha objeto database (economia de espaço)
- Checkout independente por worktree
- Fácil de criar e remover
- Performance melhor que clone

### Negativas
- Worktrees órfãos se não limpos
- Conflitos de merge ainda possíveis
- Ferramentas podem não reconhecer worktrees

### Mitigações
- Limpeza automática de worktrees antigos
- Notificação de conflitos
- Documentação para IDEs

## Comandos Úteis

```bash
# Listar worktrees
git worktree list

# Criar worktree
git worktree add -b <branch> <path> <base-branch>

# Remover worktree
git worktree remove <path>

# Limpeza
git worktree prune
```

## Status

- [x] Decisão aprovada
- [x] Implementado em GitManager
- [ ] Testes de integração
