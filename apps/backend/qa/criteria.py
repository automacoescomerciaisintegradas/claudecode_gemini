"""
QA Approval Criteria.
"""
from pathlib import Path

def is_fixes_applied(spec_dir: Path) -> bool:
    """Check if fixes were applied to the spec."""
    return (spec_dir / "fixes_applied.json").exists()

def is_qa_approved(spec_dir: Path) -> bool:
    """Check if the task was approved by QA."""
    return (spec_dir / "qa_approved").exists()

def is_qa_rejected(spec_dir: Path) -> bool:
    """Check if the task was rejected by QA."""
    return (spec_dir / "qa_rejected").exists()
