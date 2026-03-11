"""
Recovery and retry state management.
"""
class RecoveryManager:
    def __init__(self, spec_dir, project_dir):
        self.spec_dir = spec_dir
    def get_attempt_count(self, subtask_id): return 0
    def record_attempt(self, **kwargs): pass
    def get_recovery_hints(self, subtask_id): return None
    def mark_subtask_stuck(self, subtask_id, reason): pass
    def record_good_commit(self, commit, subtask_id): pass
    def rollback_to_commit(self, commit): return True

def check_and_recover(spec_dir, project_dir, subtask_id, error):
    class RecoveryAction:
        def __init__(self):
            self.action = "retry"
            self.reason = "Automated recovery"
            self.target = None
    return RecoveryAction()

def reset_subtask(spec_dir, project_dir, subtask_id): pass
