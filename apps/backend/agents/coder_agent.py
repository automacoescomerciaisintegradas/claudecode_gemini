"""
Coder Agent Module
==================

Main autonomous agent loop that runs the coder agent to implement subtasks.
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

from context.constants import SKIP_DIRS
from core.client import create_client
from core.file_utils import write_json_atomic
from linear_updater import (
    LinearTaskState,
    is_linear_enabled,
    linear_build_complete,
    linear_task_started,
    linear_task_stuck,
)
from phase_config import (
    get_fast_mode,
    get_phase_client_thinking_kwargs,
    get_phase_model,
    get_phase_model_betas,
)
from phase_event import ExecutionPhase, emit_phase
from progress import (
    count_subtasks,
    count_subtasks_detailed,
    get_current_phase,
    get_next_subtask,
    is_build_complete,
    print_build_complete_banner,
    print_progress_summary,
    print_session_header,
)
from prompt_generator import (
    format_context_for_prompt,
    generate_planner_prompt,
    generate_subtask_prompt,
    load_subtask_context,
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
    Icons,
    StatusManager,
    bold,
    box,
    highlight,
    icon,
    muted,
    print_key_value,
    print_status,
)

from .base import (
    AUTH_FAILURE_PAUSE_FILE,
    AUTH_RESUME_CHECK_INTERVAL_SECONDS,
    AUTH_RESUME_MAX_WAIT_SECONDS,
    AUTO_CONTINUE_DELAY_SECONDS,
    HUMAN_INTERVENTION_FILE,
    INITIAL_RETRY_DELAY_SECONDS,
    MAX_CONCURRENCY_RETRIES,
    MAX_RATE_LIMIT_WAIT_SECONDS,
    MAX_RETRY_DELAY_SECONDS,
    MAX_SUBTASK_RETRIES,
    RATE_LIMIT_CHECK_INTERVAL_SECONDS,
    RATE_LIMIT_PAUSE_FILE,
    RESUME_FILE,
    sanitize_error_message,
)
from .memory_manager import debug_memory_system_status, get_graphiti_context
from .session import post_session_processing, run_agent_session
from .utils import (
    find_phase_for_subtask,
    find_subtask_in_plan,
    get_commit_count,
    get_latest_commit,
    load_implementation_plan,
    sync_spec_to_source,
)

logger = logging.getLogger(__name__)

_EXCLUDE_DIRS = frozenset(SKIP_DIRS | {".auto-claude", ".tox", "out"})

def _build_file_index(project_dir: Path, suffixes: set[str]) -> dict[str, list[tuple[str, Path]]]:
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
            stem_part = filename[:ext_idx]
            if stem_part == "index":
                dir_name = os.path.basename(root)
                key = f"__dir_stem__:{dir_name}{file_suffix}"
                index.setdefault(key, []).append((rel_str, rel_path))
    return index

def _score_and_select(candidates: list[tuple[str, float]]) -> str | None:
    if not candidates: return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    best_path, best_score = candidates[0]
    if best_score < 8.0: return None
    if len(candidates) > 1:
        if best_score - candidates[1][1] < 3.0: return None
    return best_path

def _find_correct_path_indexed(missing_path: str, parent_parts: tuple[str, ...], file_index: dict[str, list[tuple[str, Path]]]) -> str | None:
    missing = Path(missing_path)
    basename = missing.name
    stem = missing.stem
    suffix = missing.suffix
    if not suffix: return None
    candidates: list[tuple[str, float]] = []
    for rel_str, rel_path in file_index.get(basename, []):
        score = 10.0
        candidate_parts = rel_path.parent.parts
        for i, part in enumerate(parent_parts):
            if i < len(candidate_parts) and candidate_parts[i] == part: score += 3.0
        score -= 0.5 * abs(len(candidate_parts) - len(parent_parts))
        candidates.append((rel_str, score))
    stem_key = f"__dir_stem__:{stem}{suffix}"
    for rel_str, rel_path in file_index.get(stem_key, []):
        score = 8.0
        candidate_parts = rel_path.parent.parts
        for i, part in enumerate(parent_parts):
            if i < len(candidate_parts) and candidate_parts[i] == part: score += 3.0
        score -= 0.5 * abs(len(candidate_parts) - len(parent_parts))
        candidates.append((rel_str, score))
    return _score_and_select(candidates)

def _auto_correct_subtask_files(subtask: dict, missing_files: list[str], project_dir: Path, spec_dir: Path) -> list[str]:
    corrections: dict[str, str] = {}
    still_missing: list[str] = []
    suffixes_needed = {Path(f).suffix for f in missing_files if Path(f).suffix}
    file_index = _build_file_index(project_dir, suffixes_needed) if suffixes_needed else {}
    for missing_path in missing_files:
        corrected = _find_correct_path_indexed(missing_path, Path(missing_path).parent.parts, file_index)
        if corrected:
            corrections[missing_path] = corrected
            print_status(f"Auto-corrected: {missing_path} -> {corrected}", "success")
        else:
            still_missing.append(missing_path)
    if corrections:
        subtask["files_to_modify"] = [corrections.get(f, f) for f in subtask.get("files_to_modify", [])]
        plan_file = spec_dir / "implementation_plan.json"
        if plan_file.exists():
            try:
                with open(plan_file, encoding="utf-8") as f: plan = json.load(f)
                sub_id = subtask.get("id")
                plan_sub = find_subtask_in_plan(plan, sub_id)
                if plan_sub: plan_sub["files_to_modify"] = [corrections.get(f, f) for f in plan_sub.get("files_to_modify", [])]
                write_json_atomic(plan_file, plan)
            except Exception as e: logger.warning(f"Failed to persist path corrections: {e}")
    return still_missing

def _validate_plan_file_paths(spec_dir: Path, project_dir: Path) -> str | None:
    plan_file = spec_dir / "implementation_plan.json"
    if not plan_file.exists(): return None
    try:
        with open(plan_file, encoding="utf-8") as f: plan = json.load(f)
    except: return None
    resolved_project = project_dir.resolve()
    missing_entries: list[tuple[list[str], int, str]] = []
    suffixes_needed: set[str] = set()
    for phase in plan.get("phases", []):
        for subtask in phase.get("subtasks", []):
            files = subtask.get("files_to_modify", [])
            for i, f_path in enumerate(files):
                full = (resolved_project / f_path).resolve()
                if not full.is_relative_to(resolved_project): continue
                if full.exists(): continue
                if Path(f_path).suffix:
                    suffixes_needed.add(Path(f_path).suffix)
                    missing_entries.append((files, i, f_path))
    if not missing_entries: return None
    file_index = _build_file_index(project_dir, suffixes_needed)
    all_missing: list[str] = []
    for flist, idx, fpath in missing_entries:
        corrected = _find_correct_path_indexed(fpath, Path(fpath).parent.parts, file_index)
        if corrected:
            flist[idx] = corrected
            print_status(f"Auto-corrected: {fpath} -> {corrected}", "success")
        else: all_missing.append(fpath)
    if any(m[0][m[1]] != m[2] for m in missing_entries):
        try: write_json_atomic(plan_file, plan)
        except: pass
    if not all_missing: return None
    return "## FILE PATH VALIDATION ERRORS\n\nFiles not found:\n" + "\n".join(f"- `{p}`" for p in all_missing)

def validate_subtask_files(subtask: dict, project_dir: Path, spec_dir: Path | None = None) -> dict:
    missing, invalid = [], []
    res_proj = Path(project_dir).resolve()
    for f in subtask.get("files_to_modify", []):
        full = (res_proj / f).resolve()
        if not full.is_relative_to(res_proj): invalid.append(f)
        elif not full.exists(): missing.append(f)
    if invalid: return {"success": False, "error": f"Invalid paths: {invalid}", "suggestion": "Fix paths"}
    if missing:
        if spec_dir:
            missing = _auto_correct_subtask_files(subtask, missing, project_dir, spec_dir)
            if not missing: return {"success": True}
        return {"success": False, "error": f"Missing files: {missing}", "suggestion": "Correct filenames"}
    return {"success": True}

async def run_autonomous_agent(project_dir: Path, spec_dir: Path, model: str, max_iterations: int | None = None, verbose: bool = False, source_spec_dir: Path | None = None) -> None:
    os.environ[PROJECT_DIR_ENV_VAR] = str(project_dir.resolve())
    recovery = RecoveryManager(spec_dir, project_dir)
    status_mgr = StatusManager(project_dir)
    status_mgr.set_active(spec_dir.name, BuildState.BUILDING)
    debug_memory_system_status()
    first_run = is_first_run(spec_dir)
    is_planning = first_run
    retry_context = None
    
    while True:
        subtask = None if first_run else get_next_subtask(spec_dir)
        if not first_run and not subtask:
            if is_build_complete(spec_dir): break
            await asyncio.sleep(2); continue
            
        phase_model = get_phase_model(spec_dir, "planning" if is_planning else "coding", model)
        client = create_client(project_dir, spec_dir, phase_model, agent_type="planner" if is_planning else "coder")
        
        async with client:
            # Simplified loop for tool-calling limit fix
            prompt = generate_planner_prompt(spec_dir, project_dir) if is_planning else generate_subtask_prompt(spec_dir=spec_dir, project_dir=project_dir, subtask=subtask)
            if retry_context: prompt += "\n\n" + retry_context
            
            status, response, err = await run_agent_session(client, prompt, spec_dir, verbose)
            
            if is_planning and status != "error":
                retry_context = _validate_plan_file_paths(spec_dir, project_dir)
                if not retry_context:
                    is_planning = False
                    first_run = False
                continue
            
            if status == "complete": break
            await asyncio.sleep(AUTO_CONTINUE_DELAY_SECONDS)
