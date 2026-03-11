"""
Utils Module
============

Git operations, plan management, and workspace synchronization.
"""
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

def get_latest_commit(project_dir: Path) -> str:
    """Get the latest commit hash (Mock)."""
    return "HEAD"

def get_commit_count(project_dir: Path) -> int:
    """Get the number of commits in the repository (Mock)."""
    return 0

def load_implementation_plan(spec_dir: Path):
    """Load the implementation plan from spec directory."""
    import json
    plan_file = spec_dir / "implementation_plan.json"
    if plan_file.exists():
        try:
            with open(plan_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load plan: {e}")
    return None

def find_subtask_in_plan(plan, subtask_id: str):
    """Find a specific subtask in the implementation plan."""
    if not plan: return None
    for phase in plan.get("phases", []):
        for subtask in phase.get("subtasks", []):
            if subtask.get("id") == subtask_id:
                return subtask
    return None

def find_phase_for_subtask(plan, subtask_id: str):
    """Find the phase containing a specific subtask."""
    if not plan: return None
    for phase in plan.get("phases", []):
        for subtask in phase.get("subtasks", []):
            if subtask.get("id") == subtask_id:
                return phase
    return None

def _sync_directory(source_dir: Path, target_dir: Path):
    """
    Recursively sync a directory.
    
    Args:
        source_dir: Source directory (in worktree)
        target_dir: Target directory (in main project)
    """
    # Create target directory if needed
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.iterdir():
        # Skip symlinks to prevent path traversal attacks
        if item.is_symlink():
            logger.warning(
                f"Skipping symlink during sync: {source_dir.name}/{item.name}"
            )
            continue

        target_item = target_dir / item.name

        if item.is_file():
            shutil.copy2(item, target_item)
            logger.debug(f"Synced {source_dir.name}/{item.name} to source")
        elif item.is_dir():
            # Recurse into subdirectories
            _sync_directory(item, target_item)

def sync_spec_to_source(spec_dir: Path, source_spec_dir: Path | None) -> bool:
    """
    Sync the spec directory back to the main project (for worktree mode).
    """
    if not source_spec_dir or spec_dir == source_spec_dir:
        return False

    if not spec_dir.exists():
        return False

    try:
        _sync_directory(spec_dir, source_spec_dir)
        return True
    except Exception as e:
        logger.error(f"Failed to sync spec to source: {e}")
        return False
