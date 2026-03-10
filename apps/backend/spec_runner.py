#!/usr/bin/env python3
"""
Spec Runner - Gerenciador de especificações e execução de tarefas autônomas.

Este script permite criar, gerenciar e executar especificações de tarefas
para o sistema multi-agente.
"""
import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent))

from agents import (
    PlanningAgent,
    CodingAgent,
    QAAgent,
    MergeAgent,
    AgentOrchestrator,
    TaskContext,
)
from qa_pipeline import QAPipeline
from config import settings


console = Console()
specs_dir = Path(__file__).parent / "specs"
specs_dir.mkdir(exist_ok=True)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(verbose: bool = False):
    """Spec Runner - Gerenciador de especificações e tarefas autônomas."""
    if verbose:
        console.print("[blue]Verbose mode enabled[/blue]")


@cli.command()
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
@click.option("--title", "-t", help="Task title")
@click.option("--description", "-d", help="Task description")
@click.option("--requirement", "-r", multiple=True, help="Task requirements")
def create(interactive: bool, title: Optional[str], description: Optional[str], requirement: tuple):
    """Cria uma nova especificação de tarefa."""
    if interactive:
        spec_data = _interactive_create()
    else:
        spec_data = {
            "title": title or "Nova Tarefa",
            "description": description or "",
            "requirements": list(requirement) or [],
        }
    
    # Gerar ID único
    spec_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Salvar especificação
    spec_file = specs_dir / f"spec_{spec_id}.json"
    spec_data["id"] = spec_id
    spec_data["created_at"] = datetime.now().isoformat()
    spec_data["status"] = "pending"
    
    spec_file.write_text(json.dumps(spec_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    console.print(Panel(
        f"[green]Especificação criada com sucesso![/green]\n\n"
        f"ID: [cyan]{spec_id}[/cyan]\n"
        f"Arquivo: [yellow]{spec_file}[/yellow]",
        title="✅ Especificação Criada",
    ))
    
    return spec_id


def _interactive_create() -> dict:
    """Criação interativa de especificação."""
    console.print("\n[bold]Criar Nova Especificação[/bold]\n")
    
    title = click.prompt("Título da tarefa", type=str)
    description = click.prompt("Descrição", type=str, default="")
    
    requirements = []
    while True:
        req = click.prompt(
            f"Requisito {len(requirements) + 1} (Enter para pular)",
            type=str,
            default="",
            show_default=False,
        )
        if not req:
            break
        requirements.append(req)
    
    constraints = []
    while True:
        constraint = click.prompt(
            f"Restrição {len(constraints) + 1} (Enter para pular)",
            type=str,
            default="",
            show_default=False,
        )
        if not constraint:
            break
        constraints.append(constraint)
    
    acceptance = []
    while True:
        criterion = click.prompt(
            f"Critério de aceitação {len(acceptance) + 1} (Enter para pular)",
            type=str,
            default="",
            show_default=False,
        )
        if not criterion:
            break
        acceptance.append(criterion)
    
    return {
        "title": title,
        "description": description,
        "requirements": requirements,
        "constraints": constraints,
        "acceptance_criteria": acceptance,
    }


@cli.command()
@click.argument("spec_id")
@click.option("--phase", "-p", type=click.Choice(["planning", "coding", "qa", "merge", "all"]), default="all")
@click.option("--parallel", is_flag=True, help="Run in parallel mode")
def run(spec_id: str, phase: str, parallel: bool):
    """Executa uma especificação através do pipeline de agentes."""
    console.print(f"\n[bold]Executando especificação: {spec_id}[/bold]\n")
    
    # Carregar especificação
    spec_file = specs_dir / f"spec_{spec_id}.json"
    if not spec_file.exists():
        # Tentar sem prefixo
        spec_file = specs_dir / f"{spec_id}.json"
    
    if not spec_file.exists():
        console.print(f"[red]Especificação não encontrada: {spec_id}[/red]")
        return
    
    spec_data = json.loads(spec_file.read_text())
    
    # Criar contexto da tarefa
    context = TaskContext(
        task_id=spec_data.get("id", spec_id),
        title=spec_data.get("title", "Tarefa"),
        description=spec_data.get("description", ""),
        requirements=spec_data.get("requirements", []),
        constraints=spec_data.get("constraints", []),
        acceptance_criteria=spec_data.get("acceptance_criteria", []),
    )
    
    # Executar pipeline
    if phase == "all":
        result = asyncio.run(_run_full_pipeline(context))
    else:
        result = asyncio.run(_run_single_phase(context, phase))
    
    # Atualizar status da especificação
    spec_data["status"] = "completed" if result.success else "failed"
    spec_data["last_run"] = datetime.now().isoformat()
    spec_data["result"] = {
        "success": result.success,
        "output": result.output,
        "errors": result.errors,
    }
    spec_file.write_text(json.dumps(spec_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    # Mostrar resultado
    if result.success:
        console.print(Panel(
            f"[green]{result.output}[/green]",
            title="✅ Tarefa Concluída",
        ))
    else:
        console.print(Panel(
            f"[red]{result.output}[/red]\n\n"
            f"Erros: {', '.join(result.errors)}",
            title="❌ Tarefa Falhou",
        ))


async def _run_full_pipeline(context: TaskContext) -> "AgentResult":
    """Executa o pipeline completo."""
    orchestrator = AgentOrchestrator()
    return await orchestrator.execute_task(context)


async def _run_single_phase(context: TaskContext, phase: str) -> "AgentResult":
    """Executa uma fase específica."""
    from agents import PlanningAgent, CodingAgent, QAAgent, MergeAgent
    
    agents = {
        "planning": PlanningAgent(),
        "coding": CodingAgent(),
        "qa": QAAgent(),
        "merge": MergeAgent(),
    }
    
    agent = agents.get(phase)
    if not agent:
        return AgentResult(
            success=False,
            output=f"Fase desconhecida: {phase}",
            errors=[f"Fase {phase} não encontrada"],
        )
    
    return await agent.execute(context)


@cli.command()
def list():
    """Lista todas as especificações."""
    console.print("\n[bold]Especificações[/bold]\n")
    
    if not specs_dir.exists():
        console.print("[yellow]Nenhuma especificação encontrada[/yellow]")
        return
    
    specs = list(specs_dir.glob("spec_*.json"))
    
    if not specs:
        console.print("[yellow]Nenhuma especificação encontrada[/yellow]")
        return
    
    table = Table(title="Especificações")
    table.add_column("ID", style="cyan")
    table.add_column("Título", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Criado em", style="blue")
    
    for spec_file in sorted(specs, reverse=True):
        spec_data = json.loads(spec_file.read_text())
        
        status_colors = {
            "pending": "yellow",
            "in_progress": "blue",
            "completed": "green",
            "failed": "red",
        }
        
        table.add_row(
            spec_data.get("id", "N/A"),
            spec_data.get("title", "Sem título"),
            f"[{status_colors.get(spec_data.get('status', 'pending'), 'white')}]{spec_data.get('status', 'pending')}[/{status_colors.get(spec_data.get('status', 'pending'), 'white')}]",
            spec_data.get("created_at", "N/A")[:10],
        )
    
    console.print(table)


@cli.command()
@click.argument("spec_id")
def show(spec_id: str):
    """Mostra detalhes de uma especificação."""
    spec_file = specs_dir / f"spec_{spec_id}.json"
    
    if not spec_file.exists():
        spec_file = specs_dir / f"{spec_id}.json"
    
    if not spec_file.exists():
        console.print(f"[red]Especificação não encontrada: {spec_id}[/red]")
        return
    
    spec_data = json.loads(spec_file.read_text())
    
    console.print(Panel(
        f"[bold]Título:[/bold] {spec_data.get('title', 'N/A')}\n\n"
        f"[bold]ID:[/bold] {spec_data.get('id', 'N/A')}\n"
        f"[bold]Status:[/bold] {spec_data.get('status', 'pending')}\n"
        f"[bold]Criado em:[/bold] {spec_data.get('created_at', 'N/A')}\n\n"
        f"[bold]Descrição:[/bold]\n{spec_data.get('description', 'Sem descrição')}\n\n"
        f"[bold]Requisitos:[/bold]\n" + 
        "\n".join(f"  • {r}" for r in spec_data.get('requirements', [])) + "\n\n"
        f"[bold]Critérios de Aceitação:[/bold]\n" +
        "\n".join(f"  ✓ {a}" for a in spec_data.get('acceptance_criteria', [])),
        title=f"📋 Especificação: {spec_id}",
    ))


@cli.command()
@click.argument("spec_id")
def delete(spec_id: str):
    """Deleta uma especificação."""
    spec_file = specs_dir / f"spec_{spec_id}.json"
    
    if not spec_file.exists():
        spec_file = specs_dir / f"{spec_id}.json"
    
    if not spec_file.exists():
        console.print(f"[red]Especificação não encontrada: {spec_id}[/red]")
        return
    
    if click.confirm(f"Tem certeza que deseja deletar a especificação {spec_id}?"):
        spec_file.unlink()
        console.print(f"[green]Especificação {spec_id} deletada com sucesso[/green]")


@cli.command()
def status():
    """Mostra status do sistema de agentes."""
    console.print("\n[bold]Status do Sistema[/bold]\n")
    
    orchestrator = AgentOrchestrator()
    agents_status = orchestrator.get_all_agents_status()
    
    table = Table(title="Agentes")
    table.add_column("Nome", style="cyan")
    table.add_column("ID", style="magenta")
    table.add_column("Estado", style="green")
    table.add_column("Tarefa Atual", style="blue")
    
    for name, status in agents_status.items():
        table.add_row(
            name,
            status.get("agent_id", "N/A"),
            status.get("state", "unknown"),
            status.get("current_task", "-"),
        )
    
    console.print(table)
    
    # Memory layer
    memory = orchestrator.get_memory_layer()
    console.print(Panel(
        f"[bold]Total de Tarefas:[/bold] {memory.get('total_tasks', 0)}\n"
        f"[bold]Taxa de Sucesso:[/bold] {memory.get('success_rate', 0):.1%}\n"
        f"[bold]Otimizações Sugeridas:[/bold]\n" +
        "\n".join(f"  • {o}" for o in memory.get('optimizations', [])),
        title="🧠 Memory Layer",
    ))


if __name__ == "__main__":
    cli()
