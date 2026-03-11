"""
Phase event types and emission.
"""
from enum import Enum

class ExecutionPhase(Enum):
    PLANNING = "planning"
    CODING = "coding"
    QA = "qa"
    MERGE = "merge"
    COMPLETE = "complete"
    FAILED = "failed"
    RATE_LIMIT_PAUSED = "rate_limit_paused"
    AUTH_FAILURE_PAUSED = "auth_failure_paused"

def emit_phase(phase, message, **kwargs):
    print(f"[PHASE][{phase.value}] {message}")
