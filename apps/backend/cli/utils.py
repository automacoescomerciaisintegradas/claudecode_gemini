"""
Shared utilities for the CLI.
"""
from rich.console import Console

console = Console()

def print_success(message: str):
    console.print(f"[bold green]✔[/bold green] {message}")

def print_error(message: str):
    console.print(f"[bold red]✘[/bold red] {message}")

def print_info(message: str):
    console.print(f"[blue]ℹ[/blue] {message}")

def print_warning(message: str):
    console.print(f"[bold yellow]![/bold yellow] {message}")
