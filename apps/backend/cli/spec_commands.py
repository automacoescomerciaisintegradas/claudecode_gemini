"""
Spec management commands.
"""
import click
from .utils import print_success, print_info

@click.group(name="spec")
def spec_group():
    """Manage task specifications."""
    pass

@spec_group.command(name="list")
def list_specs():
    """List all available specifications."""
    print_info("Listing specifications...")
    # Logic to list specs goes here
    pass

@spec_group.command(name="create")
@click.argument("title")
def create_spec(title):
    """Create a new task specification."""
    print_success(f"Created spec: {title}")
    pass
