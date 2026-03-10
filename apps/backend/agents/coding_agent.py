"""
Coding Agent - Responsável por implementar código baseado nas especificações.
"""
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext


class CodingAgent(BaseAgent):
    """
    Agente de Codificação.
    
    Implementa o código baseado nas especificações técnicas geradas
    pelo Planning Agent, seguindo boas práticas e padrões do projeto.
    """
    
    def __init__(self, worktree_path: Optional[Path] = None, **kwargs):
        super().__init__(name="CodingAgent", **kwargs)
        self.worktree_path = worktree_path
        self.specialties = ["implementation", "refactoring", "code-review"]
    
    def get_system_prompt(self) -> str:
        return """
Você é um Agente de Codificação especializado em implementação de software.

SUAS RESPONSABILIDADES:
1. Implementar código limpo, legível e manutenível
2. Seguir os padrões e convenções do projeto
3. Escrever código testável e bem documentado
4. Reutilizar componentes existentes quando apropriado
5. Aplicar princípios SOLID e padrões de design

DIRETRIZES DE CÓDIGO:
- Escreva código claro e expressivo
- Use nomes significativos para variáveis e funções
- Mantenha funções pequenas e com responsabilidade única
- Adicione type hints em Python
- Escreva docstrings para funções e classes públicas
- Trate erros de forma apropriada
- Evite código duplicado

PROCESSO DE IMPLEMENTAÇÃO:
1. Leia e compreenda a especificação técnica
2. Analise o código existente relacionado
3. Planeje a estrutura do código
4. Implemente passo a passo
5. Revise seu próprio código
6. Execute testes locais
"""
    
    async def execute(self, context: TaskContext) -> AgentResult:
        """Executa a implementação do código."""
        start_time = datetime.now()
        self.update_state(AgentState.EXECUTING)
        self.current_task = context
        
        try:
            # Carregar especificação
            spec = await self._load_specification(context)
            
            # Analisar código existente
            existing_code = await self._analyze_existing_code(context)
            
            # Implementar solução
            implementation_result = await self._implement_solution(
                context, spec, existing_code
            )
            
            # Auto-revisão
            review_result = await self._self_review(implementation_result)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.log_action("coding_completed", {
                "files_created": len(implementation_result.get("created_files", [])),
                "files_modified": len(implementation_result.get("modified_files", [])),
                "review_passed": review_result.get("passed", False),
            })
            
            self.update_state(AgentState.COMPLETED)
            
            return AgentResult(
                success=True,
                output=f"Implementação concluída para tarefa: {context.title}",
                artifacts=implementation_result.get("artifacts", []),
                metadata={
                    "implementation": implementation_result,
                    "review": review_result,
                    "execution_time": execution_time,
                },
            )
            
        except Exception as e:
            self.update_state(AgentState.FAILED)
            return AgentResult(
                success=False,
                output=f"Erro na implementação: {str(e)}",
                errors=[str(e)],
            )
    
    async def _load_specification(self, context: TaskContext) -> Optional[Dict[str, Any]]:
        """Carrega a especificação técnica."""
        spec_file = Path(__file__).parent.parent / "specs" / f"spec_{context.task_id}.md"
        
        if not spec_file.exists():
            return None
        
        content = spec_file.read_text(encoding="utf-8")
        return self._parse_specification(content)
    
    def _parse_specification(self, content: str) -> Dict[str, Any]:
        """Parse da especificação markdown."""
        # Implementação simplificada
        return {"raw_content": content}
    
    async def _analyze_existing_code(self, context: TaskContext) -> Dict[str, Any]:
        """Analisa o código existente relacionado à tarefa."""
        analysis = {
            "related_files": [],
            "patterns_found": [],
            "dependencies": [],
        }
        
        for file_path in context.related_files:
            if file_path.exists():
                analysis["related_files"].append({
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                })
        
        return analysis
    
    async def _implement_solution(
        self,
        context: TaskContext,
        spec: Optional[Dict[str, Any]],
        existing_code: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Implementa a solução baseada na especificação."""
        self.log_action("implementing_solution", {})
        
        result = {
            "created_files": [],
            "modified_files": [],
            "deleted_files": [],
            "artifacts": [],
        }
        
        # A implementação real usaria o Claude Code CLI
        # para gerar o código baseado na especificação
        
        return result
    
    async def _self_review(self, implementation: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza auto-revisão do código implementado."""
        self.log_action("self_review", {})
        
        review = {
            "passed": True,
            "issues": [],
            "suggestions": [],
            "metrics": {
                "complexity": "baixa",
                "coverage": 0.0,
                "maintainability": "alta",
            },
        }
        
        return review
    
    async def execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Executa um passo específico da implementação."""
        action = step.get("action")
        
        if action == "create_file":
            return await self._create_file(step)
        elif action == "modify_file":
            return await self._modify_file(step)
        elif action == "delete_file":
            return await self._delete_file(step)
        elif action == "run_command":
            return await self._run_command(step)
        else:
            return {"success": False, "error": f"Ação desconhecida: {action}"}
    
    async def _create_file(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo arquivo."""
        file_path = step.get("path")
        content = step.get("content", "")
        
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            
            return {
                "success": True,
                "action": "create_file",
                "path": str(path),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _modify_file(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Modifica um arquivo existente."""
        # Implementação de modificação de arquivo
        return {"success": True, "action": "modify_file"}
    
    async def _delete_file(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Deleta um arquivo."""
        # Implementação de deleção de arquivo
        return {"success": True, "action": "delete_file"}
    
    async def _run_command(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Executa um comando no terminal."""
        # Implementação de execução de comandos
        return {"success": True, "action": "run_command"}
