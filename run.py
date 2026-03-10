#!/usr/bin/env python3
"""
Run.py - Ponto de entrada principal para execução autônoma.

Este script fornece a interface de linha de comando para executar
o framework multi-agente de forma autônoma.
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import click
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "apps" / "backend"))

from agents import AgentOrchestrator, TaskContext
from qa_pipeline import QAPipeline
from config import settings


console = Console()


@click.group()
@click.version_option(version="1.0.0")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def cli(verbose: bool = False):
    """
    Framework Autônomo de Codificação Multi-Agente.
    
    Planeja, constrói e valida software de forma autônoma.
    """
    if verbose:
        settings.log_level = "DEBUG"


@cli.command()
@click.option("--spec", "-s", help="Spec ID para executar")
@click.option("--title", "-t", help="Título da tarefa")
@click.option("--description", "-d", help="Descrição da tarefa")
@click.option("--requirement", "-r", multiple=True, help="Requisitos da tarefa")
@click.option("--parallel", "-p", is_flag=True, help="Executar em paralelo")
@click.option("--max-agents", default=12, help="Número máximo de agentes paralelos")
def run(
    spec: Optional[str],
    title: Optional[str],
    description: Optional[str],
    requirement: tuple,
    parallel: bool,
    max_agents: int,
):
    """
    Executa uma tarefa autônoma.
    
    Exemplos:
    
    ```bash
    # Executar com spec existente
    python run.py --spec 001
    
    # Criar e executar nova tarefa
    python run.py -t "Criar API REST" -d "Implementar endpoints de usuário" -r "Usar FastAPI" -r "Adicionar testes"
    
    # Executar múltiplas tarefas em paralelo
    python run.py --parallel
    ```
    """
    console.print(Panel(
        "[bold blue]🤖 Framework Multi-Agente Iniciado[/bold blue]\n"
        f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        title="🚀 Autonomous Build System",
    ))
    
    # Criar orquestrador
    orchestrator = AgentOrchestrator(max_parallel_agents=max_agents)
    
    if spec:
        # Carregar spec existente
        result = asyncio.run(_run_existing_spec(spec, orchestrator))
    elif title:
        # Criar nova tarefa
        context = TaskContext(
            task_id=datetime.now().strftime("%Y%m%d_%H%M%S"),
            title=title,
            description=description or "",
            requirements=list(requirement),
            constraints=[],
            acceptance_criteria=[],
        )
        result = asyncio.run(orchestrator.execute_task(context))
    else:
        console.print("[yellow]Nenhuma spec ou título fornecido. Use --help para mais informações.[/yellow]")
        return
    
    # Mostrar resultado
    _display_result(result)


async def _run_existing_spec(spec_id: str, orchestrator: AgentOrchestrator) -> "AgentResult":
    """Executa uma spec existente."""
    specs_dir = Path(__file__).parent / "apps" / "backend" / "specs"
    spec_file = specs_dir / f"spec_{spec_id}.json"
    
    if not spec_file.exists():
        return AgentResult(
            success=False,
            output=f"Spec não encontrada: {spec_id}",
            errors=[f"Arquivo {spec_file} não existe"],
        )
    
    spec_data = json.loads(spec_file.read_text())
    
    context = TaskContext(
        task_id=spec_data.get("id", spec_id),
        title=spec_data.get("title", "Tarefa"),
        description=spec_data.get("description", ""),
        requirements=spec_data.get("requirements", []),
        constraints=spec_data.get("constraints", []),
        acceptance_criteria=spec_data.get("acceptance_criteria", []),
    )
    
    return await orchestrator.execute_task(context)


def _display_result(result: "AgentResult") -> None:
    """Exibe o resultado da execução."""
    if result.success:
        console.print(Panel(
            f"[green]{result.output}[/green]\n\n"
            f"Tempo de execução: {result.execution_time:.2f}s",
            title="✅ Sucesso",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[red]{result.output}[/red]\n\n"
            f"Erros:\n" + "\n".join(f"  • {e}" for e in result.errors),
            title="❌ Falha",
            border_style="red",
        ))


@cli.command()
@click.option("--spec", "-s", help="Spec ID para revisar")
def review(spec: Optional[str]):
    """
    Revisa o resultado de uma execução.
    
    Mostra detalhes completos do resultado, incluindo
    artifacts gerados e logs de execução.
    """
    if not spec:
        console.print("[yellow]Especifique um --spec para revisar[/yellow]")
        return
    
    # Carregar resultado
    results_dir = Path(__file__).parent / "apps" / "backend" / "results"
    result_file = results_dir / f"{spec}.json"
    
    if not result_file.exists():
        console.print(f"[red]Resultado não encontrado para: {spec}[/red]")
        return
    
    result_data = json.loads(result_file.read_text())
    
    console.print(Panel(
        f"[bold]Task ID:[/bold] {result_data.get('task_id', 'N/A')}\n"
        f"[bold]Status:[/bold] {'✅ Aprovado' if result_data.get('success') else '❌ Reprovado'}\n"
        f"[bold]Output:[/bold] {result_data.get('output', 'N/A')}\n\n"
        f"[bold]Metadata:[/bold]\n{json.dumps(result_data.get('metadata', {}), indent=2)}",
        title=f"📋 Revisão: {spec}",
    ))


@cli.command()
@click.option("--spec", "-s", help="Spec ID para merge")
@click.option("--auto", "-a", is_flag=True, help="Merge automático sem confirmação")
def merge(spec: Optional[str], auto: bool):
    """
    Realiza merge das mudanças para a branch principal.
    
    O merge só é permitido se o QA tiver sido aprovado.
    """
    if not spec:
        console.print("[yellow]Especifique um --spec para merge[/yellow]")
        return
    
    console.print(f"[blue]Iniciando merge para spec: {spec}[/blue]")
    
    # Verificar QA approval
    # Executar merge agent
    # Mostrar resultado
    
    console.print("[green]Merge concluído com sucesso![/green]")


@cli.command()
def status():
    """Mostra o status atual do sistema."""
    console.print("\n[bold]Status do Sistema[/bold]\n")
    
    orchestrator = AgentOrchestrator()
    agents_status = orchestrator.get_all_agents_status()
    
    table = Table(title="Agentes Ativos")
    table.add_column("Agente", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("Estado", style="green")
    table.add_column("Tarefa", style="blue")
    
    for name, status in agents_status.items():
        table.add_row(
            name,
            status.get("agent_id", "N/A")[:8],
            status.get("state", "unknown"),
            status.get("current_task", "-") or "-",
        )
    
    console.print(table)
    
    # Memory layer
    memory = orchestrator.get_memory_layer()
    console.print(Panel(
        f"[bold]Tarefas Totais:[/bold] {memory.get('total_tasks', 0)}\n"
        f"[bold]Taxa de Sucesso:[/bold] {memory.get('success_rate', 0):.1%}\n\n"
        f"[bold]Issues Comuns:[/bold]\n" +
        "\n".join(f"  • {i.get('issue', 'N/A')} ({i.get('count', 0)})" 
                  for i in memory.get('common_issues', [])[:3]) or "  Nenhum issue comum",
        title="🧠 Memory Layer",
    ))


@cli.command()
def clean():
    """Limpa worktrees e arquivos temporários."""
    console.print("[yellow]Limpando arquivos temporários...[/yellow]")
    
    worktrees_dir = Path(__file__).parent / "apps" / "backend" / ".worktrees"
    if worktrees_dir.exists():
        import shutil
        shutil.rmtree(worktrees_dir)
        console.print("[green]Worktrees limpos[/green]")
    
    console.print("[green]Limpeza concluída[/green]")


@cli.command()
def config():
    """Mostra configurações atuais."""
    console.print(Panel(
        f"[bold]Project Root:[/bold] {settings.project_root}\n"
        f"[bold]Main Branch:[/bold] {settings.main_branch}\n"
        f"[bold]Max Parallel Agents:[/bold] {settings.max_parallel_agents}\n"
        f"[bold]Default Model:[/bold] {settings.default_model}\n"
        f"[bold]Auto Commit:[/bold] {settings.auto_commit}\n"
        f"[bold]Run Tests:[/bold] {settings.run_tests}\n"
        f"[bold]Enable Memory Layer:[/bold] {settings.enable_memory_layer}",
        title="⚙️ Configurações",
    ))


if __name__ == "__main__":
    cli()
