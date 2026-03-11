"""
Phase-specific configuration.
"""
def get_phase_model(spec_dir, phase, default_model): return default_model
def get_phase_model_betas(spec_dir, phase, model): return []
def get_phase_client_thinking_kwargs(spec_dir, phase, model): return {}
def get_fast_mode(spec_dir): return False
