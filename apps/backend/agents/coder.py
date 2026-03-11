"""
Coder Module
============

Main autonomous agent loop that runs the coder agent to implement subtasks.
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

from context.constants import SKIP_DIRS
from core.client import create_client
from core.file_utils import write_json_atomic
from linear_updater import (
    is_linear_enabled,
    linear_subtask_completed,
    linear_subtask_failed,
)
from phase_config import (
    get_phase_model,
)
from phase_event import ExecutionPhase, emit_phase
from progress import (
    count_subtasks_detailed,
    get_next_subtask,
    is_build_complete,
    print_build_complete_banner,
)
from prompt_generator import (
    generate_planner_prompt,
    generate_subtask_prompt,
)
from prompts import is_first_run
from recovery import RecoveryManager
from security.constants import PROJECT_DIR_ENV_VAR
from task_logger import (
    LogPhase,
    get_task_logger,
)
from ui import (
    BuildState,
    StatusManager,
    print_status,
)

from .base import (
    AUTO_CONTINUE_DELAY_SECONDS,
    INITIAL_RETRY_DELAY_SECONDS,
    MAX_RETRY_DELAY_SECONDS,
    MAX_SUBTASK_RETRIES,
)
from .memory import debug_memory_system_status
from .session import post_session_processing, run_agent_session
from .utils import (
    find_subtask_in_plan,
    get_commit_count,
    get_latest_commit,
    load_implementation_plan,
    sync_spec_to_source,
)

logger = logging.getLogger(__name__)

_EXCLUDE_DIRS = frozenset(SKIP_DIRS | {".auto-claude", ".tox", "out"})

def _build_file_index(project_dir: Path, suffixes: set[str]) -> dict[str, list[tuple[str, Path]]]:
    """Build a search index of files in the project."""
    index: dict[str, list[tuple[str, Path]]] = {}
    resolved_str = str(project_dir.resolve())
    for root, dirs, files in os.walk(project_dir.resolve()):
        dirs[:] = [d for d in dirs if d not in _EXCLUDE_DIRS]
        for filename in files:
            ext_idx = filename.rfind(".")
            if ext_idx == -1: continue
            file_suffix = filename[ext_idx:]
            if file_suffix not in suffixes: continue
            
            full_path = os.path.join(root, filename)
            rel_str = os.path.relpath(full_path, resolved_str).replace(os.sep, "/")
            rel_path = Path(rel_str)
            index.setdefault(filename, []).append((rel_str, rel_path))
            
            # Index index.js/ts by directory name
            stem_part = filename[:ext_idx]
            if stem_part == "index":
                dir_name = os.path.basename(root)
                key = f"__dir_stem__:{dir_name}{file_suffix}"
                index.setdefault(key, []).append((rel_str, rel_path))
    return index

def _find_correct_path_indexed(missing_path: str, parent_parts: tuple[str, ...], file_index: dict[str, list[tuple[str, Path]]]) -> str | None:
    """Find the most likely correct path for a missing file."""
    missing = Path(missing_path)
    basename = missing.name
    candidates: list[tuple[str, float]] = []
    
    for rel_str, rel_path in file_index.get(basename, []):
        score = 10.0
        candidate_parts = rel_path.parent.parts
        for i, part in enumerate(parent_parts):
            if i < len(candidate_parts) and candidate_parts[i] == part: score += 3.0
        score -= 0.5 * abs(len(candidate_parts) - len(parent_parts))
        candidates.append((rel_str, score))
        
    if not candidates: return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0] if candidates[0][1] > 8.0 else None

def _validate_plan_file_paths(spec_dir: Path, project_dir: Path) -> str | None:
    """Validate and auto-correct file paths in the implementation plan."""
    plan_path = spec_dir / "implementation_plan.json"
    if not plan_path.exists(): return None
    try:
        with open(plan_path, encoding="utf-8") as f: plan = json.load(f)
    except: return None
    
    suffixes_needed = set()
    missing_entries = []
    project_root = project_dir.resolve()
    
    for phase in plan.get("phases", []):
        for subtask in phase.get("subtasks", []):
            files = subtask.get("files_to_modify", [])
            for i, f_path in enumerate(files):
                full = (project_root / f_path).resolve()
                if not full.exists() and Path(f_path).suffix:
                    suffixes_needed.add(Path(f_path).suffix)
                    missing_entries.append((files, i, f_path))
                    
    if not missing_entries: return None
    
    file_index = _build_file_index(project_dir, suffixes_needed)
    all_missing = []
    
    for flist, idx, fpath in missing_entries:
        corrected = _find_correct_path_indexed(fpath, Path(fpath).parent.parts, file_index)
        if corrected:
            flist[idx] = corrected
            print_status(f"Auto-corrected: {fpath} -> {corrected}", "success")
        else:
            all_missing.append(fpath)
            
    if any(m[0][m[1]] != m[2] for m in missing_entries):
        write_json_atomic(plan_path, plan)
        
    if not all_missing: return None
    return "## FILE PATH VALIDATION ERRORS\nFiles not found:\n" + "\n".join(f"- `{p}`" for p in all_missing)

async def run_autonomous_agent(
    project_dir: Path,
    spec_dir: Path,
    model: str,
    max_iterations: int | None = None,
    verbose: bool = False,
    source_spec_dir: Path | None = None
) -> None:
    """Main autonomous agent loop."""
    os.environ[PROJECT_DIR_ENV_VAR] = str(project_dir.resolve())
    recovery = RecoveryManager(spec_dir, project_dir)
    status_mgr = StatusManager(project_dir)
    status_mgr.set_active(spec_dir.name, BuildState.BUILDING)
    
    debug_memory_system_status()
    
    linear_enabled = is_linear_enabled()
    execution_count = 0
    first_run = is_first_run(spec_dir)
    is_planning = first_run
    retry_context = None
    
    while True:
        if max_iterations and execution_count >= max_iterations:
            print_status("Max iterations reached", "warning")
            break
            
        if is_build_complete(spec_dir):
            print_build_complete_banner(spec_dir)
            emit_phase(ExecutionPhase.COMPLETE, "Build complete")
            break
            
        subtask = None if first_run else get_next_subtask(spec_dir)
        if not first_run and not subtask:
            print_status("Waiting for subtasks...", "info")
            await asyncio.sleep(5)
            continue
            
        phase = LogPhase.PLANNING if is_planning else LogPhase.CODING
        phase_model = get_phase_model(spec_dir, phase.value, model)
        
        client = create_client(project_dir, spec_dir, phase_model, agent_type="planner" if is_planning else "coder")
        
        async with client:
            prompt = generate_planner_prompt(spec_dir, project_dir) if is_planning else generate_subtask_prompt(spec_dir=spec_dir, project_dir=project_dir, subtask=subtask)
            if retry_context:
                prompt += "\n\n" + retry_context
                retry_context = None
                
            execution_count += 1
            session_num = execution_count
            
            commit_before = get_latest_commit(project_dir)
            commit_count_before = get_commit_count(project_dir)
            
            status, response, error_info = await run_agent_session(client, prompt, spec_dir, verbose, phase=phase)
            
            if status == "error":
                print_status(f"Session failed: {error_info.get('message')}", "error")
                # Handle retries with backoff
                delay = min(INITIAL_RETRY_DELAY_SECONDS * (2 ** (recovery.get_attempt_count(subtask.get("id") if subtask else "plan"))), MAX_RETRY_DELAY_SECONDS)
                await asyncio.sleep(delay)
                continue
                
            # Post-session processing (Memory, Linear, Recovery)
            success = await post_session_processing(
                spec_dir=spec_dir,
                project_dir=project_dir,
                subtask_id=subtask.get("id") if subtask else "planning",
                session_num=session_num,
                commit_before=commit_before,
                commit_count_before=commit_count_before,
                recovery_manager=recovery,
                linear_enabled=linear_enabled,
                status_manager=status_mgr,
                source_spec_dir=source_spec_dir,
                error_info=error_info
            )
            
            if is_planning and success:
                retry_context = _validate_plan_file_paths(spec_dir, project_dir)
                if not retry_context:
                    is_planning = False
                    first_run = False
                continue
            
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)
