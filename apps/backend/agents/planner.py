"""
Planner Module
==============

Follow-up planner logic for completed specs.
"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

async def run_followup_planner(spec_dir: Path, project_dir: Path) -> bool:
    """Plan follow-up tasks for a completed spec."""
    print(f"Planning follow-ups for {spec_dir.name}...")
    return True
