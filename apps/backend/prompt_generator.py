"""
Prompt generation logic.
"""
def generate_planner_prompt(spec_dir, project_dir): return "Plan the implementation."
def generate_subtask_prompt(**kwargs): return "Implement the subtask."
def load_subtask_context(spec_dir, project_dir, subtask): return {}
def format_context_for_prompt(context): return ""
