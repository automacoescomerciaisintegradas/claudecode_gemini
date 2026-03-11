"""
Memory Module
=============

Handles session memory storage using dual-layer approach:
- PRIMARY: Graphiti (when enabled) - semantic search, cross-session context
- FALLBACK: File-based memory - zero dependencies, always available
"""

import logging
from pathlib import Path

from core.sentry import capture_exception
from debug import (
    debug,
    debug_detailed,
    debug_error,
    debug_section,
    debug_success,
    debug_warning,
    is_debug_enabled,
)
from graphiti_config import get_graphiti_status, is_graphiti_enabled

# Import from parent memory package
from memory import save_session_insights as save_file_based_memory
from memory.graphiti_helpers import get_graphiti_memory

logger = logging.getLogger(__name__)


def debug_memory_system_status() -> None:
    """Print memory system status for debugging."""
    if not is_debug_enabled():
        return

    debug_section("memory", "Memory System Status")
    graphiti_status = get_graphiti_status()

    debug(
        "memory",
        "Memory system configuration",
        primary_system="Graphiti"
        if graphiti_status.get("available")
        else "File-based (fallback)",
        graphiti_enabled=graphiti_status.get("enabled"),
        graphiti_available=graphiti_status.get("available"),
    )

    if graphiti_status.get("enabled"):
        debug_detailed(
            "memory",
            "Graphiti configuration",
            host=graphiti_status.get("host"),
            port=graphiti_status.get("port"),
            database=graphiti_status.get("database"),
        )
        if not graphiti_status.get("available"):
            debug_warning("memory", "Graphiti not available", reason=graphiti_status.get("reason"))
        else:
            debug_success("memory", "Graphiti ready")


async def get_graphiti_context(spec_dir: Path, project_dir: Path, subtask: dict) -> str | None:
    """Retrieve relevant context from Graphiti."""
    if not is_graphiti_enabled():
        return None

    memory = await get_graphiti_memory(spec_dir, project_dir)
    if memory is None:
        return None

    try:
        subtask_desc = subtask.get("description", "")
        query = f"{subtask_desc}".strip()
        context_items = await memory.get_relevant_context(query, num_results=5)
        
        if not context_items:
            return None

        sections = ["## Graphiti Memory Context\n"]
        for item in context_items:
            content = item.get("content", "")[:500]
            sections.append(f"- {content}\n")
        return "\n".join(sections)
    except Exception as e:
        logger.warning(f"Failed to get Graphiti context: {e}")
        return None
    finally:
        if memory: await memory.close()


async def save_session_memory(spec_dir: Path, project_dir: Path, subtask_id: str, session_num: int, success: bool, subtasks_completed: list[str], discoveries: dict | None = None) -> tuple[bool, str]:
    """Save session insights to memory."""
    insights = {
        "subtasks_completed": subtasks_completed,
        "discoveries": discoveries or {},
        "success": success
    }

    if is_graphiti_enabled():
        memory = await get_graphiti_memory(spec_dir, project_dir)
        if memory and memory.is_enabled:
            try:
                result = await memory.save_session_insights(session_num, insights)
                if result:
                    return True, "graphiti"
            except Exception as e:
                 logger.warning(f"Graphiti save failed: {e}")
            finally:
                await memory.close()

    # Fallback
    try:
        save_file_based_memory(spec_dir, session_num, insights)
        return True, "file"
    except Exception as e:
        logger.error(f"File-based memory save failed: {e}")
        return False, "none"

async def save_session_to_graphiti(**kwargs) -> bool:
    """Compatibility wrapper."""
    res, _ = await save_session_memory(**kwargs)
    return res
