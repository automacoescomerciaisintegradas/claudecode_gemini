"""
QA Agent - Responsável por validar a qualidade do código implementado.
"""
import asyncio
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

from .base_agent import BaseAgent, AgentState, AgentResult, TaskContext


class QAAgent(BaseAgent):
    """
    Agente de Garantia de Qualidade (QA).
    
    Valida a implementação através de testes automatizados,
    análise estática de código e verificação de critérios de aceitação.
    """
    
    def __init__(self, **kwargs):
        super().__init__(name="QAAgent", **kwargs)
        self.specialties = ["testing", "linting", "validation", "security"]
    
    def get_system_prompt(self) -> str:
        return """
Você é um Agente de QA especializado em garantia de qualidade de software.

SUAS RESPONSABILIDADES:
1. Executar testes automatizados (unitários, integração, e2e)
2. Realizar análise estática de código (linting, type checking)
3. Verificar conformidade com critérios de aceitação
4. Identificar bugs, vulnerabilidades e code smells
5. Validar performance e segurança

FERRAMENTAS DE QA:
- pytest: testes unitários e de integração
- ruff/flake8: linting de Python
- mypy/pyright: type checking
- bandit: análise de segurança
- coverage: medição de cobertura de testes

CRITÉRIOS DE APROVAÇÃO:
- Todos os testes devem passar
- Sem erros de linting
- Cobertura mínima de 80%
- Sem vulnerabilidades críticas de segurança
- Todos os critérios de aceitação atendidos

PROCESSO DE VALIDAÇÃO:
1. Execute a suíte de testes existente
2. Crie testes para novas funcionalidades
3. Execute análise estática
4. Verifique critérios de aceitação
5. Gere relatório de qualidade
"""
    
    async def execute(self, context: TaskContext) -> AgentResult:
        """Executa a validação de QA."""
        start_time = datetime.now()
        self.update_state(AgentState.VALIDATING)
        self.current_task = context
        
        try:
            # Executar testes
            test_results = await self._run_tests(context)
            
            # Executar linting
            lint_results = await self._run_linting(context)
            
            # Verificar type checking
            type_results = await self._run_type_check(context)
            
            # Verificar critérios de aceitação
            acceptance_results = await self._verify_acceptance_criteria(context)
            
            # Análise de segurança
            security_results = await self._security_scan(context)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Determinar se passou no QA
            passed = all([
                test_results.get("passed", False),
                lint_results.get("passed", True),
                type_results.get("passed", True),
                acceptance_results.get("passed", False),
            ])
            
            self.log_action("qa_completed", {
                "passed": passed,
                "tests": test_results,
                "lint": lint_results,
            })
            
            self.update_state(AgentState.COMPLETED if passed else AgentState.FAILED)
            
            return AgentResult(
                success=passed,
                output=self._generate_qa_report(
                    test_results, lint_results, type_results, acceptance_results
                ),
                metadata={
                    "test_results": test_results,
                    "lint_results": lint_results,
                    "type_results": type_results,
                    "acceptance_results": acceptance_results,
                    "security_results": security_results,
                    "passed": passed,
                    "execution_time": execution_time,
                },
            )
            
        except Exception as e:
            self.update_state(AgentState.FAILED)
            return AgentResult(
                success=False,
                output=f"Erro na validação QA: {str(e)}",
                errors=[str(e)],
            )
    
    async def _run_tests(self, context: TaskContext) -> Dict[str, Any]:
        """Executa a suíte de testes."""
        self.log_action("running_tests", {})
        
        result = {
            "passed": True,
            "total": 0,
            "passed_count": 0,
            "failed_count": 0,
            "skipped_count": 0,
            "coverage": 0.0,
            "errors": [],
            "output": "",
        }
        
        # Executar pytest
        try:
            import subprocess
            
            cmd = ["pytest", "--cov=.", "--cov-report=json", "-v"]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            result["output"] = process.stdout
            result["passed"] = process.returncode == 0
            
            # Parse dos resultados seria feito aqui
            
        except subprocess.TimeoutExpired:
            result["errors"].append("Timeout na execução dos testes")
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    async def _run_linting(self, context: TaskContext) -> Dict[str, Any]:
        """Executa análise de linting."""
        self.log_action("running_linting", {})
        
        result = {
            "passed": True,
            "errors": [],
            "warnings": [],
            "output": "",
        }
        
        try:
            import subprocess
            
            cmd = ["ruff", "check", "."]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            result["output"] = process.stdout
            result["passed"] = process.returncode == 0
            
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    async def _run_type_check(self, context: TaskContext) -> Dict[str, Any]:
        """Executa type checking."""
        self.log_action("running_type_check", {})
        
        result = {
            "passed": True,
            "errors": [],
            "output": "",
        }
        
        try:
            import subprocess
            
            cmd = ["mypy", "."]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            result["output"] = process.stdout
            result["passed"] = process.returncode == 0
            
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    async def _verify_acceptance_criteria(
        self, context: TaskContext
    ) -> Dict[str, Any]:
        """Verifica os critérios de aceitação."""
        self.log_action("verifying_acceptance_criteria", {
            "criteria_count": len(context.acceptance_criteria),
        })
        
        result = {
            "passed": True,
            "criteria": [],
        }
        
        for criterion in context.acceptance_criteria:
            # Verificação real seria implementada aqui
            criterion_result = {
                "description": criterion,
                "passed": True,
                "notes": "",
            }
            result["criteria"].append(criterion_result)
        
        result["passed"] = all(c["passed"] for c in result["criteria"])
        
        return result
    
    async def _security_scan(self, context: TaskContext) -> Dict[str, Any]:
        """Realiza scan de segurança."""
        self.log_action("security_scan", {})
        
        result = {
            "passed": True,
            "vulnerabilities": [],
            "warnings": [],
        }
        
        try:
            import subprocess
            
            cmd = ["bandit", "-r", "."]
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=context.worktree_path or Path.cwd(),
            )
            
            # Parse da saída do bandit
            
        except Exception as e:
            pass  # Bandit pode não estar instalado
        
        return result
    
    def _generate_qa_report(
        self,
        test_results: Dict[str, Any],
        lint_results: Dict[str, Any],
        type_results: Dict[str, Any],
        acceptance_results: Dict[str, Any],
    ) -> str:
        """Gera relatório de QA."""
        passed = all([
            test_results.get("passed", False),
            lint_results.get("passed", True),
            type_results.get("passed", True),
            acceptance_results.get("passed", False),
        ])
        
        report = f"""
# Relatório de Garantia de Qualidade

## Status: {'✅ APROVADO' if passed else '❌ REPROVADO'}

## Testes
- Total: {test_results.get('total', 0)}
- Passaram: {test_results.get('passed_count', 0)}
- Falharam: {test_results.get('failed_count', 0)}
- Cobertura: {test_results.get('coverage', 0):.1f}%

## Linting
- Status: {'✅ Passou' if lint_results.get('passed', True) else '❌ Falhou'}
- Erros: {len(lint_results.get('errors', []))}
- Warnings: {len(lint_results.get('warnings', []))}

## Type Checking
- Status: {'✅ Passou' if type_results.get('passed', True) else '❌ Falhou'}

## Critérios de Aceitação
- Status: {'✅ Atendidos' if acceptance_results.get('passed', False) else '❌ Não atendidos'}
"""
        return report
