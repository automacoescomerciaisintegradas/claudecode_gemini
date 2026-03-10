"""
Agente Base - Classe abstrata para todos os agentes do sistema.
"""
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path
import uuid


class AgentState(Enum):
    """Estados possíveis de um agente."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentResult:
    """Resultado da execução de um agente."""
    success: bool
    output: str
    artifacts: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0


@dataclass
class TaskContext:
    """Contexto da tarefa para injeção no agente."""
    task_id: str
    title: str
    description: str
    requirements: List[str]
    constraints: List[str]
    acceptance_criteria: List[str]
    related_files: List[Path] = field(default_factory=list)
    worktree_path: Optional[Path] = None
    branch_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Classe base abstrata para todos os agentes.
    
    Cada agente é responsável por uma fase específica do ciclo
    de desenvolvimento autônomo.
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_iterations: int = 10,
    ):
        self.agent_id = agent_id or str(uuid.uuid4())[:8]
        self.name = name or self.__class__.__name__
        self.model = model
        self.max_iterations = max_iterations
        self.state = AgentState.IDLE
        self.current_task: Optional[TaskContext] = None
        self.history: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        
    @abstractmethod
    async def execute(self, context: TaskContext) -> AgentResult:
        """
        Executa a tarefa do agente.
        
        Args:
            context: Contexto da tarefa com todas as informações necessárias.
            
        Returns:
            Resultado da execução com output, artifacts e erros.
        """
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Retorna o prompt de sistema que define o comportamento do agente.
        """
        pass
    
    async def plan(self, context: TaskContext) -> List[Dict[str, Any]]:
        """
        Planeja os passos necessários para executar a tarefa.
        
        Args:
            context: Contexto da tarefa.
            
        Returns:
            Lista de passos planejados.
        """
        self.state = AgentState.PLANNING
        # Implementação base - pode ser sobrescrita
        return []
    
    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa um único passo do plano.
        
        Args:
            step: Dicionário com informações do passo.
            
        Returns:
            Resultado da execução do passo.
        """
        self.state = AgentState.EXECUTING
        # Implementação base - deve ser sobrescrita
        return {"success": False, "output": "Not implemented"}
    
    async def validate(self, result: AgentResult) -> bool:
        """
        Valida o resultado da execução.
        
        Args:
            result: Resultado da execução.
            
        Returns:
            True se válido, False caso contrário.
        """
        self.state = AgentState.VALIDATING
        return result.success and len(result.errors) == 0
    
    def update_state(self, new_state: AgentState) -> None:
        """Atualiza o estado do agente."""
        old_state = self.state
        self.state = new_state
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "event": "state_change",
            "from": old_state.value,
            "to": new_state.value,
        })
    
    def log_action(self, action: str, details: Dict[str, Any]) -> None:
        """Registra uma ação no histórico do agente."""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "event": "action",
            "action": action,
            "details": details,
        })
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do agente."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state.value,
            "current_task": self.current_task.task_id if self.current_task else None,
            "created_at": self.created_at.isoformat(),
            "history_length": len(self.history),
        }
    
    async def cancel(self) -> None:
        """Cancela a execução do agente."""
        self.state = AgentState.CANCELLED
        self.log_action("cancel", {"reason": "User requested"})
