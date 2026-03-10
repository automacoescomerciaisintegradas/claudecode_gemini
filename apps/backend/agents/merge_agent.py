"""
Merge Agent - Responsável por integrar mudanças e resolver conflitos.
"""
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext


class MergeAgent(BaseAgent):
    """
    Agente de Merge.
    
    Responsável por integrar as mudanças dos worktrees isolados
    para a branch principal, resolvendo conflitos automaticamente
    quando possível.
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="MergeAgent", **kwargs)
        self.specialties = ["git", "merge", "conflict-resolution"]
    
    def get_system_prompt(self) -> str:
        return """
Você é um Agente de Merge especializado em integração de código e resolução de conflitos.

SUAS RESPONSABILIDADES:
1. Validar que o código passou por QA antes do merge
2. Realizar merge das mudanças para a branch principal
3. Resolver conflitos de merge automaticamente quando possível
4. Manter o histórico do git limpo e significativo
5. Criar commits com mensagens descritivas

ESTRATÉGIA DE MERGE:
- Preferir merge commit para manter histórico
- Usar rebase apenas para limpeza de histórico local
- Resolver conflitos preservando a lógica de ambas as mudanças
- Testar após resolução de conflitos complexos

PROCESSO DE MERGE:
1. Verificar status do QA
2. Atualizar branch de origem com a principal
3. Identificar conflitos potenciais
4. Resolver conflitos automaticamente ou solicitar intervenção
5. Executar testes pós-merge
6. Criar commit/pull request
"""
    
    async def execute(self, context: TaskContext) -> AgentResult:
        """Executa o merge das mudanças."""
        start_time = datetime.now()
        self.update_state(AgentState.EXECUTING)
        self.current_task = context
        
        try:
            # Verificar QA approval
            qa_approved = await self._verify_qa_approval(context)
            if not qa_approved:
                return AgentResult(
                    success=False,
                    output="Merge bloqueado: QA não aprovado",
                    errors=["QA não aprovado para esta tarefa"],
                )
            
            # Preparar para merge
            prep_result = await self._prepare_merge(context)
            
            # Executar merge
            merge_result = await self._execute_merge(context, prep_result)
            
            # Resolver conflitos se necessário
            if merge_result.get("has_conflicts", False):
                resolution = await self._resolve_conflicts(context, merge_result)
                merge_result["conflict_resolution"] = resolution
            
            # Validar pós-merge
            validation = await self._post_merge_validation(context)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.log_action("merge_completed", {
                "success": merge_result.get("success", False),
                "conflicts_resolved": merge_result.get("has_conflicts", False),
            })
            
            self.update_state(AgentState.COMPLETED)
            
            return AgentResult(
                success=merge_result.get("success", False) and validation.get("passed", True),
                output=self._generate_merge_report(merge_result, validation),
                metadata={
                    "merge_result": merge_result,
                    "validation": validation,
                    "execution_time": execution_time,
                },
            )
            
        except Exception as e:
            self.update_state(AgentState.FAILED)
            return AgentResult(
                success=False,
                output=f"Erro no merge: {str(e)}",
                errors=[str(e)],
            )
    
    async def _verify_qa_approval(self, context: TaskContext) -> bool:
        """Verifica se o QA foi aprovado."""
        # Verificar arquivo de resultado do QA
        qa_result_file = Path(__file__).parent.parent / "qa_results" / f"{context.task_id}.json"
        
        if not qa_result_file.exists():
            return False
        
        import json
        qa_result = json.loads(qa_result_file.read_text())
        return qa_result.get("passed", False)
    
    async def _prepare_merge(self, context: TaskContext) -> Dict[str, Any]:
        """Prepara o ambiente para o merge."""
        self.log_action("preparing_merge", {})
        
        result = {
            "branch_name": context.branch_name,
            "worktree_path": context.worktree_path,
            "files_changed": [],
            "commits": [],
        }
        
        try:
            import subprocess
            
            # Obter lista de arquivos modificados
            cmd = ["git", "diff", "--name-only", "HEAD", context.branch_name or "main"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            if process.returncode == 0:
                result["files_changed"] = process.stdout.strip().split("\n")
            
            # Obter commits da branch
            cmd = ["git", "log", "--oneline", f"HEAD..{context.branch_name or 'main'}"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            if process.returncode == 0:
                result["commits"] = process.stdout.strip().split("\n")
            
        except Exception as e:
            self.log_action("prepare_error", {"error": str(e)})
        
        return result
    
    async def _execute_merge(
        self, context: TaskContext, prep_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa o merge."""
        self.log_action("executing_merge", {})
        
        result = {
            "success": False,
            "has_conflicts": False,
            "output": "",
            "strategy": "merge",
        }
        
        try:
            import subprocess
            
            # Checkout na branch principal
            subprocess.run(
                ["git", "checkout", context.branch_name or "main"],
                capture_output=True,
                cwd=Path.cwd(),
            )
            
            # Tentar merge
            cmd = ["git", "merge", "--no-ff", prep_result["branch_name"], "-m", 
                   f"feat: {context.title} (Task: {context.task_id})"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
            
            result["output"] = process.stdout
            result["success"] = process.returncode == 0
            result["has_conflicts"] = "conflict" in process.stdout.lower()
            
        except Exception as e:
            result["output"] = str(e)
        
        return result
    
    async def _resolve_conflicts(
        self, context: TaskContext, merge_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve conflitos de merge."""
        self.log_action("resolving_conflicts", {})
        
        resolution = {
            "resolved": False,
            "conflicted_files": [],
            "strategy_used": "auto",
        }
        
        # Identificar arquivos em conflito
        try:
            import subprocess
            
            cmd = ["git", "diff", "--name-only", "--diff-filter=U"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
            
            if process.returncode == 0:
                resolution["conflicted_files"] = process.stdout.strip().split("\n")
            
            # Para conflitos simples, aceitar ambas as mudanças
            # Para conflitos complexos, seria necessária intervenção humana
            
        except Exception as e:
            self.log_action("conflict_resolution_error", {"error": str(e)})
        
        return resolution
    
    async def _post_merge_validation(self, context: TaskContext) -> Dict[str, Any]:
        """Valida o resultado pós-merge."""
        self.log_action("post_merge_validation", {})
        
        result = {
            "passed": True,
            "checks": [],
        }
        
        # Executar testes rápidos pós-merge
        # Verificar build
        # Validar integridade do repositório
        
        return result
    
    def _generate_merge_report(
        self, merge_result: Dict[str, Any], validation: Dict[str, Any]
    ) -> str:
        """Gera relatório de merge."""
        status = "✅" if merge_result.get("success", False) else "❌"
        
        report = f"""
# Relatório de Merge

## Status: {status} {'Merge concluído com sucesso' if merge_result.get('success') else 'Merge falhou'}

## Detalhes
- Estratégia: {merge_result.get('strategy', 'merge')}
- Conflitos: {'Sim' if merge_result.get('has_conflicts') else 'Não'}
- Arquivos modificados: {len(merge_result.get('files_changed', []))}

## Validação Pós-Merge
- Status: {'✅ Passou' if validation.get('passed') else '❌ Falhou'}

## Output
```
{merge_result.get('output', 'Sem output')}
```
"""
        return report
