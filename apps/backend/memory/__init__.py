"""
Memory package initialization.
"""

def save_session_insights(spec_dir, session_num, insights):
    """Placeholder for file-based memory save."""
    import json
    memory_dir = spec_dir / "memory" / "session_insights"
    memory_dir.mkdir(parents=True, exist_ok=True)
    file_path = memory_dir / f"session_{session_num:03d}.json"
    file_path.write_text(json.dumps(insights, indent=2), encoding="utf-8")
