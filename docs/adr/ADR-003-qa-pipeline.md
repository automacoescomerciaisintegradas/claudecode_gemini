# ADR-003: Pipeline de QA em 5 Estágios

**Status:** Aceito  
**Data:** 2026-03-10  
**Decisão:** Implementar pipeline de QA com 5 estágios sequenciais

## Contexto

Como garantir qualidade consistente do código gerado pelos agentes?

Requisitos:
- Validação automatizada sem intervenção manual
- Múltiplas camadas de verificação
- Feedback rápido para desenvolvedores
- Detecção de problemas de segurança

## Decisão

Implementar pipeline sequencial com 5 estágios:

```
┌─────────┐    ┌─────────┐    ┌────────────┐    ┌─────────┐    ┌───────────┐
│ Linting │ -> │ Testes  │ -> │ Type Check │ -> │ Security│ -> │ Coverage  │
│ (ruff)  │    │ (pytest)│    │   (mypy)   │    │ (bandit)│    │ (pytest)  │
└─────────┘    └─────────┘    └────────────┘    └─────────┘    └───────────┘
     |              |              |                |              |
   Fail?          Fail?          Fail?           Fail?          Fail?
     |              |              |                |              |
     v              v              v                v              v
  Corrigir      Corrigir      Corrigir        Revisar        Adicionar
   Estilo         Bugs           Tipos         Segurança        Testes
```

### Critérios de Aprovação

| Estágio | Ferramenta | Critério |
|---------|-----------|----------|
| Linting | ruff | 0 erros |
| Testes | pytest | 100% dos testes passam |
| Type Check | mypy | 0 erros de tipo |
| Security | bandit | 0 issues de alta severidade |
| Coverage | pytest-cov | Mínimo 80% |

## Consequências

### Positivas
- Qualidade consistente
- Problemas detectados cedo
- Documentação implícita de padrões
- Segurança automatizada

### Negativas
- Tempo adicional (2-5 minutos)
- Falsos positivos possíveis
- Curva de aprendizado das ferramentas

### Configuração

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
```

## Status

- [x] Decisão aprovada
- [x] QAPipeline implementado
- [ ] Configuração de exemplos
- [ ] Documentação de troubleshooting
