"""
Task-specific logging.
"""
from enum import Enum

class LogPhase(Enum):
    PLANNING = "planning"
    CODING = "coding"
    QA = "qa"

class LogEntryType(Enum):
    TEXT = "text"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    ERROR = "error"

def get_task_logger(spec_dir):
    class MockLogger:
        def start_phase(self, phase, msg): pass
        def end_phase(self, phase, **kwargs): pass
        def set_session(self, num): pass
        def set_subtask(self, id): pass
        def log_error(self, msg, phase): pass
        def log(self, text, type, phase, **kwargs): pass
        def tool_start(self, name, input, phase, **kwargs): pass
        def tool_end(self, name, success, **kwargs): pass
    return MockLogger()
