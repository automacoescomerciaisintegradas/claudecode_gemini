"""
UI utilities for CLI status.
"""
from enum import Enum

class Icons:
    GEAR = "⚙️"
    SESSION = "🕒"
    ARROW_RIGHT = "➡️"
    ERROR = "❌"
    SUCCESS = "✅"
    PLAY = "▶️"

class BuildState(Enum):
    BUILDING = "building"
    PLANNING = "planning"
    COMPLETE = "complete"
    ERROR = "error"
    PAUSED = "paused"

class StatusManager:
    def __init__(self, project_dir): pass
    def set_active(self, spec_name, state): pass
    def update_subtasks(self, **kwargs): pass
    def update(self, **kwargs): pass
    def update_session(self, n): pass
    def update_phase(self, name, current, total): pass

def bold(t): return f"**{t}**"
def box(content, **kwargs): return "\n".join(content)
def highlight(t): return f"`{t}`"
def icon(i): return i
def muted(t): return t
def print_key_value(k, v): print(f"{k}: {v}")
def print_status(msg, type="info"): print(f"[{type}] {msg}")
