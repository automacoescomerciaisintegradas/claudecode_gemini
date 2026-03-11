# Agents Module

Modular agent system for autonomous coding. This module refactors the original monolithic `agent.py` (1,446 lines) into focused, maintainable modules.

## Architecture

The agent system is now organized by concern:

```
apps/backend/agents/
├── __init__.py          # Public API exports
├── base.py              # Shared constants and imports
├── utils.py             # Git operations and plan management
├── memory.py            # Memory management (Graphiti + file-based)
├── session.py           # Agent session execution
├── planner.py           # Follow-up planner logic
└── coder.py             # Main autonomous agent loop
```

## Modules

### `base.py`
- Shared constants (`AUTO_CONTINUE_DELAY_SECONDS`, `HUMAN_INTERVENTION_FILE`)
- Common imports and logging setup
- Error sanitization logic

### `utils.py`
- Git operations: `get_latest_commit()`, `get_commit_count()`
- Plan management: `load_implementation_plan()`, `find_subtask_in_plan()`, `find_phase_for_subtask()`
- Workspace sync: `sync_spec_to_source()`

### `memory.py`
- Dual-layer memory system (Graphiti primary, file-based fallback)
- `debug_memory_system_status()` - Memory system diagnostics
- `get_graphiti_context()` - Retrieve relevant context for subtasks
- `save_session_memory()` - Save session insights to memory
- `save_session_to_graphiti()` - Backwards compatibility wrapper

### `session.py`
- `run_agent_session()` - Execute a single agent session
- `post_session_processing()` - Process results and update memory

### `planner.py`
- `run_followup_planner()` - Add new subtasks to completed specs

### `coder.py`
- `run_autonomous_agent()` - Main autonomous agent loop

## Public API

The `agents` module exports a clean public API:

```python
from agents import (
    # Main functions
    run_autonomous_agent,
    run_followup_planner,

    # Memory functions
    save_session_memory,
    get_graphiti_context,

    # Session management
    run_agent_session,
    post_session_processing,

    # Utilities
    get_latest_commit,
    load_implementation_plan,
    sync_spec_to_source,
)
```

## Backwards Compatibility

The original `agent.py` is now a facade that re-exports everything from the `agents` module:

```python
# Old code still works
from agent import run_autonomous_agent, save_session_memory

# New code can use modular imports
from agents.coder import run_autonomous_agent
from agents.memory import save_session_memory
```

## Benefits

1. **Separation of Concerns**: Each module has a clear, focused responsibility
2. **Maintainability**: Easier to understand and modify individual components
3. **Testability**: Modules can be tested in isolation
4. **Backwards Compatible**: No breaking changes to existing code
5. **Scalability**: Easy to add new agent types or features
