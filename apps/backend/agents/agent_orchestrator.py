"""
Agent Orchestrator - Gerencia a orquestração de múltiplos agentes em paralelo.
"""
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime
import uuid

from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext
from .planning_agent import PlanningAgent
from .coding_agent import CodingAgent
from .qa_agent import QAAgent
from .merge_agent import MergeAgent


class AgentOrchestrator:
    """
    Orquestrador de Agentes.
    
    Gerencia o ciclo de vida completo de uma tarefa, coordenando
    múltiplos agentes em paralelo quando possível e garantindo
    que cada fase seja completada antes de prosseguir.
    """
    
    def __init__(self, max_parallel_agents: int = 12):
        self.max_parallel_agents = max_parallel_agents
        self.agents: Dict[str, BaseAgent] = {}
        self.active_tasks: Dict[str, TaskContext] = {}
        self.task_results: Dict[str, AgentResult] = {}
        self.created_at = datetime.now()
        
        # Registrar agentes disponíveis
        self._register_default_agents()
    
    def _register_default_agents(self) -> None:
        """Registra os agentes padrão do sistema."""
        self.agents["planning"] = PlanningAgent()
        self.agents["coding"] = CodingAgent()
        self.agents["qa"] = QAAgent()
        self.agents["merge"] = MergeAgent()
    
    async def execute_task(self, context: TaskContext) -> AgentResult:
        """
        Executa uma tarefa completa através de todas as fases.
        
        Fases:
        1. Planning - Analisar requisitos e criar plano
        2. Coding - Implementar solução
        3. QA - Validar qualidade
        4. Merge - Integrar mudanças
        """
        self.active_tasks[context.task_id] = context
        task_start = datetime.now()
        
        try:
            # Fase 1: Planning
            planning_result = await self._run_phase(
                "planning", context, "Executando planejamento..."
            )
            if not planning_result.success:
                return self._finalize_task(context, planning_result, task_start)
            
            # Fase 2: Coding (pode ser paralelo para múltiplos arquivos)
            coding_result = await self._run_phase(
                "coding", context, "Implementando solução..."
            )
            if not coding_result.success:
                return self._finalize_task(context, coding_result, task_start)
            
            # Fase 3: QA
            qa_result = await self._run_phase(
                "qa", context, "Validando qualidade..."
            )
            if not qa_result.success:
                return self._finalize_task(context, qa_result, task_start)
            
            # Fase 4: Merge (opcional, baseado em configuração)
            merge_result = await self._run_phase(
                "merge", context, "Integrando mudanças..."
            )
            
            return self._finalize_task(context, merge_result, task_start)
            
        except Exception as e:
            return AgentResult(
                success=False,
                output=f"Erro na orquestração: {str(e)}",
                errors=[str(e)],
            )
        finally:
            if context.task_id in self.active_tasks:
                del self.active_tasks[context.task_id]
    
    async def _run_phase(
        self, 
        phase: str, 
        context: TaskContext, 
        status_message: str
    ) -> AgentResult:
        """Executa uma fase específica usando o agente apropriado."""
        print(f"[{context.task_id}] {status_message}")
        
        agent = self.agents.get(phase)
        if not agent:
            return AgentResult(
                success=False,
                output=f"Agente não encontrado para fase: {phase}",
                errors=[f"Agente {phase} não registrado"],
            )
        
        result = await agent.execute(context)
        self.task_results[f"{context.task_id}_{phase}"] = result
        
        return result
    
    async def execute_parallel(
        self, 
        contexts: List[TaskContext]
    ) -> Dict[str, AgentResult]:
        """
        Executa múltiplas tarefas em paralelo.
        
        Args:
            contexts: Lista de contextos de tarefa para execução paralela.
            
        Returns:
            Dicionário mapeando task_id para resultado.
        """
        # Limitar número de tarefas paralelas
        semaphore = asyncio.Semaphore(self.max_parallel_agents)
        
        async def run_with_semaphore(context: TaskContext) -> tuple[str, AgentResult]:
            async with semaphore:
                result = await self.execute_task(context)
                return (context.task_id, result)
        
        # Executar todas as tarefas em paralelo (limitado pelo semaphore)
        tasks = [run_with_semaphore(ctx) for ctx in contexts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados
        processed_results = {}
        for item in results:
            if isinstance(item, Exception):
                processed_results["unknown"] = AgentResult(
                    success=False,
                    output=f"Erro: {str(item)}",
                    errors=[str(item)],
                )
            else:
                task_id, result = item
                processed_results[task_id] = result
        
        return processed_results
    
    def _finalize_task(
        self, 
        context: TaskContext, 
        final_result: AgentResult,
        start_time: datetime
    ) -> AgentResult:
        """Finaliza o processamento de uma tarefa."""
        total_time = (datetime.now() - start_time).total_seconds()
        
        # Salvar resultado
        self.task_results[context.task_id] = final_result
        
        # Adicionar metadata de tempo total
        final_result.metadata["total_execution_time"] = total_time
        final_result.metadata["phases_completed"] = len([
            k for k in self.task_results.keys() 
            if k.startswith(context.task_id)
        ])
        
        return final_result
    
    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Retorna o status de um agente específico."""
        agent = self.agents.get(agent_name)
        if agent:
            return agent.get_status()
        return None
    
    def get_all_agents_status(self) -> Dict[str, Dict[str, Any]]:
        """Retorna o status de todos os agentes."""
        return {
            name: agent.get_status() 
            for name, agent in self.agents.items()
        }
    
    def get_task_progress(self, task_id: str) -> Dict[str, Any]:
        """Retorna o progresso de uma tarefa específica."""
        context = self.active_tasks.get(task_id)
        if not context:
            return {"status": "not_found", "task_id": task_id}
        
        # Contar fases completadas
        phases = ["planning", "coding", "qa", "merge"]
        completed_phases = []
        failed_phases = []
        
        for phase in phases:
            result = self.task_results.get(f"{task_id}_{phase}")
            if result:
                if result.success:
                    completed_phases.append(phase)
                else:
                    failed_phases.append(phase)
        
        current_phase = None
        if not failed_phases and len(completed_phases) < len(phases):
            current_phase = phases[len(completed_phases)]
        
        return {
            "task_id": task_id,
            "status": "completed" if not failed_phases and len(completed_phases) == len(phases) else "in_progress",
            "completed_phases": completed_phases,
            "failed_phases": failed_phases,
            "current_phase": current_phase,
            "progress_percent": (len(completed_phases) / len(phases)) * 100,
        }
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancela uma tarefa em execução."""
        context = self.active_tasks.get(task_id)
        if not context:
            return False
        
        # Cancelar todos os agentes que processaram esta tarefa
        for agent in self.agents.values():
            if agent.current_task and agent.current_task.task_id == task_id:
                await agent.cancel()
        
        return True
    
    def get_memory_layer(self) -> Dict[str, Any]:
        """
        Retorna a camada de memória com insights acumulados.
        
        A memória layer armazena aprendizados de execuções anteriores
        para melhorar futuras iterações.
        """
        memory = {
            "total_tasks": len(self.task_results),
            "success_rate": self._calculate_success_rate(),
            "common_issues": self._identify_common_issues(),
            "optimizations": self._suggest_optimizations(),
        }
        return memory
    
    def _calculate_success_rate(self) -> float:
        """Calcula taxa de sucesso das tarefas."""
        if not self.task_results:
            return 0.0
        
        successful = sum(1 for r in self.task_results.values() if r.success)
        return successful / len(self.task_results)
    
    def _identify_common_issues(self) -> List[Dict[str, Any]]:
        """Identifica problemas comuns nas execuções."""
        issues = {}
        
        for result in self.task_results.values():
            for error in result.errors:
                issues[error] = issues.get(error, 0) + 1
        
        return [
            {"issue": issue, "count": count}
            for issue, count in sorted(issues.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
    
    def _suggest_optimizations(self) -> List[str]:
        """Sugere otimizações baseadas no histórico de execuções."""
        optimizations = []
        
        success_rate = self._calculate_success_rate()
        if success_rate < 0.8:
            optimizations.append("Melhorar validação de requisitos antes do planejamento")
        
        avg_time = self._calculate_average_execution_time()
        if avg_time > 300:  # 5 minutos
            optimizations.append("Considerar paralelização adicional de tarefas")
        
        return optimizations
    
    def _calculate_average_execution_time(self) -> float:
        """Calcula tempo médio de execução."""
        times = [
            r.metadata.get("total_execution_time", 0)
            for r in self.task_results.values()
            if r.metadata.get("total_execution_time")
        ]
        
        if not times:
            return 0.0
        
        return sum(times) / len(times)
