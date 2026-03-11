"""
Agents Module
=============

Modular agent system for autonomous coding.

This module provides:
- run_autonomous_agent: Main coder agent loop
- run_followup_planner: Follow-up planner for completed specs
- Memory management (Graphiti + file-based fallback)
- Session management and post-processing
- Utility functions for git and plan management

Uses lazy imports to avoid circular dependencies.
"""

# Explicit import required by CodeQL static analysis
from .utils import sync_spec_to_source

__all__ = [
    # Main API
    "run_autonomous_agent",
    "run_followup_planner",
    "run_pr_template_filler",
    # Memory
    "debug_memory_system_status",
    "get_graphiti_context",
    "save_session_memory",
    "save_session_to_graphiti",
    # Session
    "run_agent_session",
    "post_session_processing",
    # Utils
    "get_latest_commit",
    "get_commit_count",
    "load_implementation_plan",
    "find_subtask_in_plan",
    "find_phase_for_subtask",
    "sync_spec_to_source",
    # Constants
    "AUTO_CONTINUE_DELAY_SECONDS",
    "HUMAN_INTERVENTION_FILE",
    # Agents (Existing)
    "BaseAgent",
    "AgentState",
    "AgentResult",
    "TaskContext",
    "PlanningAgent",
    "CodingAgent",
    "QAAgent",
    "MergeAgent",
    "LaraAgent",
]

def __getattr__(name):
    """Lazy imports to avoid circular dependencies."""
    if name in ("AUTO_CONTINUE_DELAY_SECONDS", "HUMAN_INTERVENTION_FILE"):
        from .base import AUTO_CONTINUE_DELAY_SECONDS, HUMAN_INTERVENTION_FILE
        return locals()[name]
    elif name == "run_autonomous_agent":
        from .coder import run_autonomous_agent
        return run_autonomous_agent
    elif name in (
        "debug_memory_system_status",
        "get_graphiti_context",
        "save_session_memory",
        "save_session_to_graphiti",
    ):
        from .memory import (
            debug_memory_system_status,
            get_graphiti_context,
            save_session_memory,
            save_session_to_graphiti,
        )
        return locals()[name]
    elif name == "run_followup_planner":
        from .planner import run_followup_planner

        return run_followup_planner
    elif name == "run_pr_template_filler":
        from .pr_template_filler import run_pr_template_filler

        return run_pr_template_filler
    elif name in ("post_session_processing", "run_agent_session"):
        from .session import post_session_processing, run_agent_session
        return locals()[name]
    elif name in (
        "find_phase_for_subtask",
        "find_subtask_in_plan",
        "get_commit_count",
        "get_latest_commit",
        "load_implementation_plan",
        "sync_spec_to_source",
    ):
        from .utils import (
            find_phase_for_subtask,
            find_subtask_in_plan,
            get_commit_count,
            get_latest_commit,
            load_implementation_plan,
            sync_spec_to_source,
        )
        return locals()[name]
    elif name in ("BaseAgent", "AgentState", "AgentResult", "TaskContext"):
        from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext
        return locals()[name]
    elif name == "PlanningAgent":
        from .planning_agent import PlanningAgent
        return PlanningAgent
    elif name == "CodingAgent":
        from .coding_agent import CodingAgent
        return CodingAgent
    elif name == "QAAgent":
        from .qa_agent import QAAgent
        return QAAgent
    elif name == "MergeAgent":
        from .merge_agent import MergeAgent
        return MergeAgent
    elif name == "LaraAgent":
        from .lara_agent import LaraAgent
        return LaraAgent
    
    raise AttributeError(f"module 'agents' has no attribute '{name}'")
