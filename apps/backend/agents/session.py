"""
Agent Session Management
========================

Handles running agent sessions and post-session processing including
memory updates, recovery tracking, and Linear integration.
"""

import logging
from pathlib import Path

from claude_agent_sdk import ClaudeSDKClient
from core.error_utils import (
    is_authentication_error,
    is_rate_limit_error,
    is_tool_concurrency_error,
    safe_receive_messages,
)
from core.file_utils import write_json_atomic
from debug import debug, debug_detailed, debug_error, debug_section, debug_success
from insight_extractor import extract_session_insights
from linear_updater import (
    linear_subtask_completed,
    linear_subtask_failed,
)
from progress import (
    count_subtasks_detailed,
    is_build_complete,
)
from recovery import RecoveryManager, check_and_recover, reset_subtask
from security.tool_input_validator import get_safe_tool_input
from task_logger import (
    LogEntryType,
    LogPhase,
    get_task_logger,
)
from ui import (
    StatusManager,
    muted,
    print_key_value,
    print_status,
)

from .base import sanitize_error_message
from .memory import save_session_memory
from .utils import (
    find_subtask_in_plan,
    get_commit_count,
    get_latest_commit,
    load_implementation_plan,
    sync_spec_to_source,
)

logger = logging.getLogger(__name__)


def _execute_recovery_action(
    recovery_action,
    recovery_manager: RecoveryManager,
    spec_dir: Path,
    project_dir: Path,
    subtask_id: str,
) -> None:
    """Execute a recovery action (rollback/retry/skip/escalate)."""
    if not recovery_action:
        return

    print_status(f"Recovery action: {recovery_action.action}", "info")
    print_status(f"Reason: {recovery_action.reason}", "info")

    if recovery_action.action == "rollback":
        print_status(f"Rolling back to {recovery_action.target[:8]}", "warning")
        if recovery_manager.rollback_to_commit(recovery_action.target):
            print_status("Rollback successful", "success")
        else:
            print_status("Rollback failed", "error")

    elif recovery_action.action == "retry":
        print_status(f"Resetting subtask {subtask_id} for retry", "info")
        reset_subtask(spec_dir, project_dir, subtask_id)
        print_status("Subtask reset - will retry with different approach", "success")

    elif recovery_action.action in ("skip", "escalate"):
        print_status(f"Marking subtask {subtask_id} as stuck", "warning")
        recovery_manager.mark_subtask_stuck(subtask_id, recovery_action.reason)
        print_status("Subtask marked for human intervention", "warning")


async def post_session_processing(
    spec_dir: Path,
    project_dir: Path,
    subtask_id: str,
    session_num: int,
    commit_before: str | None,
    commit_count_before: int,
    recovery_manager: RecoveryManager,
    linear_enabled: bool = False,
    status_manager: StatusManager | None = None,
    source_spec_dir: Path | None = None,
    error_info: dict | None = None,
) -> bool:
    """
    Process session results and update memory automatically.
    """
    print()
    print(muted("--- Post-Session Processing ---"))

    if sync_spec_to_source(spec_dir, source_spec_dir):
        print_status("Implementation plan synced to main project", "success")

    plan = load_implementation_plan(spec_dir)
    if not plan:
        print("  Warning: Could not load implementation plan")
        return False

    subtask = find_subtask_in_plan(plan, subtask_id)
    if not subtask:
        print(f"  Warning: Subtask {subtask_id} not found in plan")
        return False

    subtask_status = subtask.get("status", "pending")
    commit_after = get_latest_commit(project_dir)
    commit_count_after = get_commit_count(project_dir)
    new_commits = commit_count_after - commit_count_before

    print_key_value("Subtask status", subtask_status)
    print_key_value("New commits", str(new_commits))

    if subtask_status == "completed":
        print_status(f"Subtask {subtask_id} completed successfully", "success")

        if status_manager:
            subtasks = count_subtasks_detailed(spec_dir)
            status_manager.update_subtasks(
                completed=subtasks["completed"],
                total=subtasks["total"],
                in_progress=0,
            )

        recovery_manager.record_attempt(
            subtask_id=subtask_id,
            session=session_num,
            success=True,
            approach=f"Implemented: {subtask.get('description', 'subtask')[:100]}",
        )

        if commit_after and commit_after != commit_before:
            recovery_manager.record_good_commit(commit_after, subtask_id)
            print_status(f"Recorded good commit: {commit_after[:8]}", "success")

        if linear_enabled:
            subtasks_detail = count_subtasks_detailed(spec_dir)
            await linear_subtask_completed(
                spec_dir=spec_dir,
                subtask_id=subtask_id,
                completed_count=subtasks_detail["completed"],
                total_count=subtasks_detail["total"],
            )
            print_status("Linear progress recorded", "success")

        try:
            extracted_insights = await extract_session_insights(
                spec_dir=spec_dir,
                project_dir=project_dir,
                subtask_id=subtask_id,
                session_num=session_num,
                commit_before=commit_before,
                commit_after=commit_after,
                success=True,
                recovery_manager=recovery_manager,
            )
        except Exception as e:
            logger.warning(f"Insight extraction failed: {e}")
            extracted_insights = None

        try:
            save_success, storage_type = await save_session_memory(
                spec_dir=spec_dir,
                project_dir=project_dir,
                subtask_id=subtask_id,
                session_num=session_num,
                success=True,
                subtasks_completed=[subtask_id],
                discoveries=extracted_insights,
            )
        except Exception as e:
            logger.warning(f"Error saving session memory: {e}")

        return True

    elif subtask_status == "in_progress":
        print_status(f"Subtask {subtask_id} still in progress", "warning")
        recovery_manager.record_attempt(
            subtask_id=subtask_id,
            session=session_num,
            success=False,
            approach="Session ended with subtask in_progress",
            error="Subtask not marked as completed",
        )

        is_concurrency_error = (
            error_info and error_info.get("type") == "tool_concurrency"
        )

        if is_concurrency_error:
            reset_subtask(spec_dir, project_dir, subtask_id)
            plan = load_implementation_plan(spec_dir)
            if plan:
                subtask_found = False
                for phase in plan.get("phases", []):
                    for subtask in phase.get("subtasks", []):
                        if subtask.get("id") == subtask_id:
                            subtask["status"] = "pending"
                            subtask["started_at"] = None
                            subtask["completed_at"] = None
                            subtask_found = True
                            break
                    if subtask_found: break
                if subtask_found:
                    write_json_atomic(spec_dir / "implementation_plan.json", plan)
        else:
            error_message = error_info.get("message", "Subtask not marked as completed") if error_info else "Subtask not marked as completed"
            recovery_action = check_and_recover(spec_dir=spec_dir, project_dir=project_dir, subtask_id=subtask_id, error=error_message)
            _execute_recovery_action(recovery_action, recovery_manager, spec_dir, project_dir, subtask_id)

        if commit_after and commit_after != commit_before:
            recovery_manager.record_good_commit(commit_after, subtask_id)

        if linear_enabled:
            attempt_count = recovery_manager.get_attempt_count(subtask_id)
            await linear_subtask_failed(spec_dir=spec_dir, subtask_id=subtask_id, attempt=attempt_count, error_summary="Session ended without completion")

        return False

    else:
        print_status(f"Subtask {subtask_id} not completed (status: {subtask_status})", "error")
        recovery_manager.record_attempt(subtask_id=subtask_id, session=session_num, success=False, approach="Session ended without progress", error=f"Subtask status is {subtask_status}")
        error_message = error_info.get("message", f"Subtask status is {subtask_status}") if error_info else f"Subtask status is {subtask_status}"
        recovery_action = check_and_recover(spec_dir=spec_dir, project_dir=project_dir, subtask_id=subtask_id, error=error_message)
        _execute_recovery_action(recovery_action, recovery_manager, spec_dir, project_dir, subtask_id)

        if linear_enabled:
            attempt_count = recovery_manager.get_attempt_count(subtask_id)
            await linear_subtask_failed(spec_dir=spec_dir, subtask_id=subtask_id, attempt=attempt_count, error_summary=f"Subtask status: {subtask_status}")

        return False


async def run_agent_session(
    client: ClaudeSDKClient,
    message: str,
    spec_dir: Path,
    verbose: bool = False,
    phase: LogPhase = LogPhase.CODING,
) -> tuple[str, str, dict]:
    """
    Run a single agent session using Claude Agent SDK.
    """
    debug_section("session", f"Agent Session - {phase.value}")
    print("Sending prompt to Claude Agent SDK...\n")

    task_logger = get_task_logger(spec_dir)
    current_tool = None
    message_count = 0
    tool_count = 0
    response_text = ""

    try:
        await client.query(message)
        async for msg in safe_receive_messages(client, caller="session"):
            msg_type = type(msg).__name__
            message_count += 1

            if msg_type == "AssistantMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    block_type = type(block).__name__
                    if block_type == "TextBlock" and hasattr(block, "text"):
                        response_text += block.text
                        print(block.text, end="", flush=True)
                    elif block_type == "ToolUseBlock" and hasattr(block, "name"):
                        tool_name = block.name
                        tool_count += 1
                        inp = get_safe_tool_input(block)
                        if task_logger:
                            task_logger.tool_start(tool_name, str(inp)[:50], phase, print_to_console=True)
                        else:
                            print(f"\n[Tool: {tool_name}]", flush=True)
                        current_tool = tool_name
            elif msg_type == "UserMessage" and hasattr(msg, "content"):
                for block in msg.content:
                    if type(block).__name__ == "ToolResultBlock":
                        is_error = getattr(block, "is_error", False)
                        if is_error:
                            print(f"   [Error] {str(getattr(block, 'content', ''))[:100]}", flush=True)
                        else:
                            print("   [Done]", flush=True)
                        current_tool = None

        print("\n" + "-" * 70 + "\n")
        if is_build_complete(spec_dir):
            return "complete", response_text, {}
        return "continue", response_text, {}

    except Exception as e:
        sanitized_error = sanitize_error_message(str(e))
        error_type = "tool_concurrency" if is_tool_concurrency_error(e) else "other"
        print(f"Error during agent session: {sanitized_error}")
        return "error", sanitized_error, {"type": error_type, "message": sanitized_error}
