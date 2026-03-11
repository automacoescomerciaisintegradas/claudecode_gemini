"""
Verification script for Agents Module refactoring.
"""
import sys
import os
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

def test_imports():
    print("Testing modular imports...")
    try:
        from agents.base import AUTO_CONTINUE_DELAY_SECONDS
        from agents.utils import get_latest_commit
        from agents.memory import save_session_memory
        from agents.session import run_agent_session
        from agents.planner import run_followup_planner
        from agents.coder import run_autonomous_agent
        print("✅ Modular imports successful.")
    except ImportError as e:
        print(f"❌ Modular imports failed: {e}")
        return False

    print("\nTesting Public API (lazy loading)...")
    try:
        import agents
        # Trigger lazy loading
        _ = agents.run_autonomous_agent
        _ = agents.save_session_memory
        _ = agents.get_latest_commit
        _ = agents.LaraAgent
        print("✅ Public API lazy loading successful.")
    except (ImportError, AttributeError) as e:
        print(f"❌ Public API failed: {e}")
        return False

    print("\nTesting Backwards Compatibility facade...")
    try:
        import agent
        _ = agent.run_autonomous_agent
        _ = agent.save_session_memory
        print("✅ Backwards compatibility facade successful.")
    except (ImportError, AttributeError) as e:
        print(f"❌ Backwards compatibility failed: {e}")
        return False

    return True

if __name__ == "__main__":
    if test_imports():
        print("\n✨ Refactoring verification COMPLETE and SUCCESSFUL.")
    else:
        print("\n🚩 Refactoring verification FAILED.")
        sys.exit(1)
