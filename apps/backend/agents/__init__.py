"""
Sistema Multi-Agent - Framework Autônomo de Codificação

Este módulo implementa o sistema de agentes autônomos que planejam,
constroem e validam software de forma independente.
"""
from .base_agent import BaseAgent, AgentState, AgentResult
from .planning_agent import PlanningAgent
from .coding_agent import CodingAgent
from .qa_agent import QAAgent
from .merge_agent import MergeAgent
from .agent_orchestrator import AgentOrchestrator

__all__ = [
    "BaseAgent",
    "AgentState",
    "AgentResult",
    "PlanningAgent",
    "CodingAgent",
    "QAAgent",
    "MergeAgent",
    "AgentOrchestrator",
]
