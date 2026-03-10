"""
Planning Agent - Responsável por analisar requisitos e criar especificações.
"""
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext


class PlanningAgent(BaseAgent):
    """
    Agente de Planejamento.
    
    Analisa os requisitos da tarefa e cria um plano detalhado de implementação,
    incluindo especificações técnicas, arquitetura e critérios de aceitação.
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="PlanningAgent", **kwargs)
        self.specialties = ["architecture", "requirements", "planning"]
    
    def get_system_prompt(self) -> str:
        return """
Você é um Agente de Planejamento especializado em análise de requisitos e arquitetura de software.

SUAS RESPONSABILIDADES:
1. Analisar cuidadosamente os requisitos fornecidos
2. Identificar dependências e riscos potenciais
3. Criar um plano de implementação detalhado e executável
4. Definir critérios de aceitação claros e testáveis
5. Sugerir a melhor arquitetura e padrões de design

DIRETRIZES:
- Sempre considere a simplicidade e manutenibilidade
- Identifique oportunidades de reutilização de código existente
- Considere aspectos de segurança e performance
- Documente decisões técnicas importantes
- Quebre tarefas complexas em passos menores e gerenciáveis

FORMATO DE SAÍDA:
Retorne um plano estruturado com:
- Visão geral da solução
- Lista de arquivos a serem criados/modificados
- Passo a passo da implementação
- Critérios de aceitação
- Riscos e mitigação
"""
    
    async def execute(self, context: TaskContext) -> AgentResult:
        """Executa o planejamento da tarefa."""
        start_time = datetime.now()
        self.update_state(AgentState.PLANNING)
        self.current_task = context
        
        try:
            # Analisar requisitos
            analysis = await self._analyze_requirements(context)
            
            # Criar plano de implementação
            plan = await self._create_implementation_plan(context, analysis)
            
            # Gerar especificação técnica
            spec = await self._generate_technical_spec(context, plan)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.log_action("planning_completed", {
                "analysis": analysis,
                "plan_steps": len(plan),
                "spec_generated": spec is not None,
            })
            
            self.update_state(AgentState.COMPLETED)
            
            return AgentResult(
                success=True,
                output=f"Planejamento concluído para tarefa: {context.title}",
                artifacts=[spec] if spec else [],
                metadata={
                    "analysis": analysis,
                    "plan": plan,
                    "execution_time": execution_time,
                },
            )
            
        except Exception as e:
            self.update_state(AgentState.FAILED)
            return AgentResult(
                success=False,
                output=f"Erro no planejamento: {str(e)}",
                errors=[str(e)],
            )
    
    async def _analyze_requirements(self, context: TaskContext) -> Dict[str, Any]:
        """Analisa os requisitos da tarefa."""
        self.log_action("analyzing_requirements", {
            "title": context.title,
            "requirements_count": len(context.requirements),
        })
        
        # Análise dos requisitos
        analysis = {
            "complexity": self._assess_complexity(context),
            "estimated_effort": self._estimate_effort(context),
            "dependencies": await self._identify_dependencies(context),
            "risks": await self._identify_risks(context),
            "tech_stack": await self._detect_tech_stack(context),
        }
        
        return analysis
    
    async def _create_implementation_plan(
        self, 
        context: TaskContext, 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Cria o plano de implementação detalhado."""
        self.log_action("creating_implementation_plan", {})
        
        # Plano base estruturado
        plan = [
            {
                "step": 1,
                "phase": "setup",
                "description": "Preparar ambiente e dependências",
                "actions": ["Verificar estrutura do projeto", "Instalar dependências necessárias"],
            },
            {
                "step": 2,
                "phase": "implementation",
                "description": "Implementar funcionalidade principal",
                "actions": [],  # Preenchido dinamicamente
            },
            {
                "step": 3,
                "phase": "testing",
                "description": "Criar e executar testes",
                "actions": ["Criar testes unitários", "Executar testes existentes"],
            },
            {
                "step": 4,
                "phase": "validation",
                "description": "Validar implementação",
                "actions": ["Revisar código", "Verificar critérios de aceitação"],
            },
        ]
        
        return plan
    
    async def _generate_technical_spec(
        self, 
        context: TaskContext, 
        plan: List[Dict[str, Any]]
    ) -> Optional[Path]:
        """Gera o arquivo de especificação técnica."""
        spec_dir = Path(__file__).parent.parent / "specs"
        spec_dir.mkdir(exist_ok=True)
        
        spec_file = spec_dir / f"spec_{context.task_id}.md"
        
        content = f"""# Especificação Técnica: {context.title}

## ID da Tarefa
{context.task_id}

## Data de Criação
{datetime.now().isoformat()}

## Visão Geral
{context.description}

## Requisitos
{chr(10).join(f'- {r}' for r in context.requirements)}

## Restrições
{chr(10).join(f'- {c}' for c in context.constraints)}

## Critérios de Aceitação
{chr(10).join(f'- {a}' for a in context.acceptance_criteria)}

## Plano de Implementação
{self._format_plan(plan)}

## Arquivos Relacionados
{chr(10).join(f'- `{f}`' for f in context.related_files)}

## Notas Técnicas
[Espaço para notas técnicas adicionais]
"""
        
        spec_file.write_text(content, encoding="utf-8")
        return spec_file
    
    def _format_plan(self, plan: List[Dict[str, Any]]) -> str:
        """Formata o plano para exibição."""
        lines = []
        for step in plan:
            lines.append(f"\n### Passo {step['step']}: {step['phase']}")
            lines.append(f"**Descrição:** {step['description']}")
            lines.append("**Ações:**")
            for action in step.get("actions", []):
                lines.append(f"- {action}")
        return chr(10).join(lines)
    
    def _assess_complexity(self, context: TaskContext) -> str:
        """Avalia a complexidade da tarefa."""
        score = 0
        score += len(context.requirements) * 2
        score += len(context.related_files)
        score += len(context.description) // 100
        
        if score < 10:
            return "baixa"
        elif score < 25:
            return "média"
        else:
            return "alta"
    
    def _estimate_effort(self, context: TaskContext) -> str:
        """Estima o esforço necessário."""
        complexity = self._assess_complexity(context)
        effort_map = {
            "baixa": "1-2 horas",
            "média": "2-4 horas",
            "alta": "4+ horas",
        }
        return effort_map.get(complexity, "desconhecido")
    
    async def _identify_dependencies(self, context: TaskContext) -> List[str]:
        """Identifica dependências da tarefa."""
        # Implementação real analisaria o código
        return []
    
    async def _identify_risks(self, context: TaskContext) -> List[Dict[str, str]]:
        """Identifica riscos potenciais."""
        return []
    
    async def _detect_tech_stack(self, context: TaskContext) -> List[str]:
        """Detecta o stack tecnológico do projeto."""
        # Implementação real analisaria arquivos de configuração
        return []
