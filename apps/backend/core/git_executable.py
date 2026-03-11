"""
Git executable utilities.
"""

import subprocess
from pathlib import Path
from typing import List, Optional


class GitResult:
    """Result of a git command execution."""
    
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def run_git(
    args: List[str],
    cwd: Optional[Path] = None,
    timeout: Optional[int] = None,
    capture_output: bool = True,
) -> GitResult:
    """
    Run a git command.
    
    Args:
        args: Git command arguments
        cwd: Working directory
        timeout: Command timeout in seconds
        capture_output: Whether to capture stdout/stderr
        
    Returns:
        GitResult with returncode, stdout, stderr
    """
    try:
        cmd = ["git"] + args
        result = subprocess.run(
            cmd,
            cwd=cwd,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
        )
        return GitResult(
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    except subprocess.TimeoutExpired:
        return GitResult(returncode=-1, stdout="", stderr="Command timed out")
    except Exception as e:
        return GitResult(returncode=-1, stdout="", stderr=str(e))