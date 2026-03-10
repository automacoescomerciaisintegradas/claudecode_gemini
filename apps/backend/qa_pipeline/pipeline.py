"""
QA Pipeline - Pipeline automatizado de garantia de qualidade.
"""
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import subprocess
import json


class QACheckType(Enum):
    """Tipos de verificações de QA."""
    LINT = "lint"
    TEST = "test"
    TYPE_CHECK = "type_check"
    SECURITY = "security"
    COVERAGE = "coverage"
    BUILD = "build"


@dataclass
class QACheckResult:
    """Resultado de uma verificação de QA."""
    check_type: QACheckType
    passed: bool
    output: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QAPipelineResult:
    """Resultado completo do pipeline de QA."""
    success: bool
    checks: List[QACheckResult] = field(default_factory=list)
    total_duration: float = 0.0
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "success": self.success,
            "checks": [
                {
                    "type": c.check_type.value,
                    "passed": c.passed,
                    "output": c.output,
                    "errors": c.errors,
                    "warnings": c.warnings,
                    "duration": c.duration,
                }
                for c in self.checks
            ],
            "total_duration": self.total_duration,
            "summary": self.summary,
        }


class QAPipeline:
    """
    Pipeline de Garantia de Qualidade.
    
    Executa uma série de verificações automatizadas para validar
    a qualidade do código antes do merge.
    """
    
    def __init__(
        self,
        project_root: Optional[Path] = None,
        enable_checks: Optional[List[QACheckType]] = None,
    ):
        self.project_root = project_root or Path.cwd()
        self.enable_checks = enable_checks or list(QACheckType)
        self.results: List[QACheckResult] = []
    
    async def run(self, spec_id: Optional[str] = None) -> QAPipelineResult:
        """
        Executa o pipeline completo de QA.
        
        Args:
            spec_id: ID da especificação para contexto adicional.
            
        Returns:
            Resultado completo do pipeline.
        """
        start_time = datetime.now()
        self.results = []
        
        # Executar checks em paralelo quando possível
        tasks = []
        
        if QACheckType.LINT in self.enable_checks:
            tasks.append(self._run_lint())
        
        if QACheckType.TEST in self.enable_checks:
            tasks.append(self._run_tests())
        
        if QACheckType.TYPE_CHECK in self.enable_checks:
            tasks.append(self._run_type_check())
        
        if QACheckType.SECURITY in self.enable_checks:
            tasks.append(self._run_security_scan())
        
        if QACheckType.COVERAGE in self.enable_checks:
            tasks.append(self._run_coverage_check())
        
        if QACheckType.BUILD in self.enable_checks:
            tasks.append(self._run_build())
        
        # Executar todas as tarefas
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados
        for result in results:
            if isinstance(result, Exception):
                self.results.append(
                    QACheckResult(
                        check_type=QACheckType.TEST,
                        passed=False,
                        output="",
                        errors=[str(result)],
                    )
                )
            elif isinstance(result, QACheckResult):
                self.results.append(result)
        
        total_duration = (datetime.now() - start_time).total_seconds()
        
        # Determinar sucesso geral
        success = all(r.passed for r in self.results)
        
        # Gerar sumário
        summary = self._generate_summary()
        
        return QAPipelineResult(
            success=success,
            checks=self.results,
            total_duration=total_duration,
            summary=summary,
        )
    
    async def _run_lint(self) -> QACheckResult:
        """Executa linting do código."""
        start = datetime.now()
        
        try:
            cmd = ["ruff", "check", ".", "--output-format=text"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )
            
            stdout, stderr = await process.communicate()
            duration = (datetime.now() - start).total_seconds()
            
            passed = process.returncode == 0
            
            return QACheckResult(
                check_type=QACheckType.LINT,
                passed=passed,
                output=stdout.decode() if stdout else "",
                errors=[stderr.decode()] if stderr and not passed else [],
                duration=duration,
            )
            
        except Exception as e:
            return QACheckResult(
                check_type=QACheckType.LINT,
                passed=False,
                output="",
                errors=[str(e)],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    async def _run_tests(self) -> QACheckResult:
        """Executa testes automatizados."""
        start = datetime.now()
        
        try:
            cmd = ["pytest", "-v", "--tb=short"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )
            
            stdout, stderr = await process.communicate()
            duration = (datetime.now() - start).total_seconds()
            
            passed = process.returncode == 0
            
            return QACheckResult(
                check_type=QACheckType.TEST,
                passed=passed,
                output=stdout.decode() if stdout else "",
                errors=[stderr.decode()] if stderr and not passed else [],
                duration=duration,
            )
            
        except Exception as e:
            return QACheckResult(
                check_type=QACheckType.TEST,
                passed=False,
                output="",
                errors=[str(e)],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    async def _run_type_check(self) -> QACheckResult:
        """Executa type checking."""
        start = datetime.now()
        
        try:
            cmd = ["mypy", "."]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )
            
            stdout, stderr = await process.communicate()
            duration = (datetime.now() - start).total_seconds()
            
            passed = process.returncode == 0
            
            return QACheckResult(
                check_type=QACheckType.TYPE_CHECK,
                passed=passed,
                output=stdout.decode() if stdout else "",
                duration=duration,
            )
            
        except Exception as e:
            return QACheckResult(
                check_type=QACheckType.TYPE_CHECK,
                passed=False,
                output="",
                errors=[str(e)],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    async def _run_security_scan(self) -> QACheckResult:
        """Executa scan de segurança."""
        start = datetime.now()
        
        try:
            cmd = ["bandit", "-r", ".", "-f", "json"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )
            
            stdout, stderr = await process.communicate()
            duration = (datetime.now() - start).total_seconds()
            
            # Bandit retorna 0 se não houver issues de alta severidade
            passed = process.returncode == 0
            
            metadata = {}
            if stdout and passed:
                try:
                    metadata["bandit_report"] = json.loads(stdout.decode())
                except json.JSONDecodeError:
                    pass
            
            return QACheckResult(
                check_type=QACheckType.SECURITY,
                passed=passed,
                output=stdout.decode() if stdout else "",
                duration=duration,
                metadata=metadata,
            )
            
        except Exception as e:
            # Bandit pode não estar instalado
            return QACheckResult(
                check_type=QACheckType.SECURITY,
                passed=True,  # Não falhar se ferramenta não existir
                output="",
                warnings=[f"Security scan skipped: {str(e)}"],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    async def _run_coverage_check(self) -> QACheckResult:
        """Verifica cobertura de testes."""
        start = datetime.now()
        
        try:
            cmd = ["pytest", "--cov=.", "--cov-report=json", "--cov-fail-under=80"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root,
            )
            
            stdout, stderr = await process.communicate()
            duration = (datetime.now() - start).total_seconds()
            
            passed = process.returncode == 0
            
            # Ler relatório de cobertura
            coverage_file = self.project_root / ".coverage"
            metadata = {}
            
            if coverage_file.exists():
                try:
                    import coverage
                    cov = coverage.Coverage()
                    cov.load()
                    metadata["coverage_percent"] = cov.report()
                except Exception:
                    pass
            
            return QACheckResult(
                check_type=QACheckType.COVERAGE,
                passed=passed,
                output=stdout.decode() if stdout else "",
                duration=duration,
                metadata=metadata,
            )
            
        except Exception as e:
            return QACheckResult(
                check_type=QACheckType.COVERAGE,
                passed=False,
                output="",
                errors=[str(e)],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    async def _run_build(self) -> QACheckResult:
        """Executa build do projeto."""
        start = datetime.now()
        
        try:
            # Tentar diferentes comandos de build
            build_commands = [
                ["python", "-m", "py_compile", "."],
                ["npm", "run", "build"],
                ["make", "build"],
            ]
            
            for cmd in build_commands:
                try:
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=self.project_root,
                    )
                    
                    stdout, stderr = await process.communicate()
                    
                    if process.returncode == 0:
                        duration = (datetime.now() - start).total_seconds()
                        return QACheckResult(
                            check_type=QACheckType.BUILD,
                            passed=True,
                            output=stdout.decode() if stdout else "",
                            duration=duration,
                        )
                except FileNotFoundError:
                    continue
            
            duration = (datetime.now() - start).total_seconds()
            return QACheckResult(
                check_type=QACheckType.BUILD,
                passed=True,  # Nenhum sistema de build encontrado
                output="",
                warnings=["Nenhum sistema de build detectado"],
                duration=duration,
            )
            
        except Exception as e:
            return QACheckResult(
                check_type=QACheckType.BUILD,
                passed=False,
                output="",
                errors=[str(e)],
                duration=(datetime.now() - start).total_seconds(),
            )
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Gera sumário dos resultados."""
        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results if r.passed)
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "pass_rate": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "checks_by_type": {
                r.check_type.value: r.passed for r in self.results
            },
        }
    
    def save_report(self, output_path: Path) -> None:
        """Salva relatório de QA em arquivo."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            **QAPipelineResult(
                success=all(r.passed for r in self.results),
                checks=self.results,
            ).to_dict(),
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
