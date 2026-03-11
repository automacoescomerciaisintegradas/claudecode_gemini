"""
Main CLI entry point.
"""
import click
from .spec_commands import spec_group
from .build_commands import build_group
from .workspace_commands import workspace_group
from .qa_commands import qa_group
from .batch_commands import batch_group

@click.group()
@click.version_option(version="1.0.0")
def main():
    """Cleudocode: Autonomous Coding Framework CLI."""
    pass

# Register command groups
main.add_command(spec_group)
main.add_command(build_group)
main.add_command(workspace_group)
main.add_command(qa_group)
main.add_command(batch_group)

if __name__ == "__main__":
    main()
