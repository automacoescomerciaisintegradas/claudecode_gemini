"""
Workspace and Git management commands.
"""
import click
from .utils import print_success, print_info

@click.group(name="workspace")
def workspace_group():
    """Manage worktrees and branch integration."""
    pass

@workspace_group.command(name="merge")
@click.argument("spec_id")
def merge_workspace(spec_id):
    """Merge completed worktree back to main branch."""
    print_info(f"Merging workspace for: {spec_id}")
    pass
