"""
Utilitários Git para gerenciamento de worktrees e branches.
"""
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorktreeInfo:
    """Informações sobre um worktree."""
    path: Path
    branch: str
    is_current: bool
    head: str


class GitManager:
    """
    Gerenciador de operações Git.
    
    Fornece utilitários para criação e gerenciamento de worktrees
    isolados para cada tarefa.
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
    
    def is_git_repo(self) -> bool:
        """Verifica se o diretório é um repositório git."""
        git_dir = self.repo_path / ".git"
        return git_dir.exists()
    
    def get_current_branch(self) -> str:
        """Retorna a branch atual."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"
    
    def get_main_branch(self) -> str:
        """Retorna a branch principal (main ou master)."""
        branches = ["main", "master"]
        for branch in branches:
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--verify", branch],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                )
                if result.returncode == 0:
                    return branch
            except Exception:
                continue
        return "main"
    
    def create_worktree(
        self,
        branch_name: str,
        worktree_path: Path,
        base_branch: Optional[str] = None,
    ) -> bool:
        """
        Cria um worktree isolado para uma tarefa.
        
        Args:
            branch_name: Nome da branch para o worktree.
            worktree_path: Caminho onde o worktree será criado.
            base_branch: Branch base para o worktree (padrão: main).
            
        Returns:
            True se sucesso, False caso contrário.
        """
        base_branch = base_branch or self.get_main_branch()
        
        try:
            # Criar branch e worktree
            cmd = [
                "git", "worktree", "add",
                "-b", branch_name,
                str(worktree_path),
                base_branch,
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def remove_worktree(self, worktree_path: Path, force: bool = False) -> bool:
        """Remove um worktree."""
        try:
            cmd = ["git", "worktree", "remove"]
            if force:
                cmd.append("-f")
            cmd.append(str(worktree_path))
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def list_worktrees(self) -> List[WorktreeInfo]:
        """Lista todos os worktrees."""
        worktrees = []
        
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            if result.returncode == 0:
                current_worktree = None
                
                for line in result.stdout.split("\n"):
                    if line.startswith("worktree "):
                        if current_worktree:
                            worktrees.append(current_worktree)
                        current_worktree = WorktreeInfo(
                            path=Path(line.split(" ", 1)[1]),
                            branch="",
                            is_current=False,
                            head="",
                        )
                    elif line.startswith("branch ") and current_worktree:
                        current_worktree.branch = line.split(" ", 1)[1]
                    elif line.startswith("HEAD ") and current_worktree:
                        current_worktree.head = line.split(" ", 1)[1]
                    elif line.startswith("current") and current_worktree:
                        current_worktree.is_current = True
                
                if current_worktree:
                    worktrees.append(current_worktree)
            
        except Exception:
            pass
        
        return worktrees
    
    def create_branch(
        self,
        branch_name: str,
        base_branch: Optional[str] = None,
        start_point: Optional[str] = None,
    ) -> bool:
        """Cria uma nova branch."""
        base_branch = base_branch or self.get_main_branch()
        
        try:
            cmd = ["git", "checkout", "-b", branch_name, base_branch]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def checkout_branch(self, branch_name: str) -> bool:
        """Faz checkout de uma branch."""
        try:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def commit_changes(
        self,
        message: str,
        files: Optional[List[str]] = None,
        all_files: bool = False,
    ) -> bool:
        """Faz commit das mudanças."""
        try:
            # Stage files
            if all_files:
                subprocess.run(
                    ["git", "add", "-A"],
                    capture_output=True,
                    cwd=self.repo_path,
                )
            elif files:
                for file in files:
                    subprocess.run(
                        ["git", "add", file],
                        capture_output=True,
                        cwd=self.repo_path,
                    )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def push_branch(self, branch_name: str, remote: str = "origin") -> bool:
        """Push de uma branch para o remote."""
        try:
            result = subprocess.run(
                ["git", "push", "-u", remote, branch_name],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_diff(self, branch1: str, branch2: str) -> str:
        """Retorna o diff entre duas branches."""
        try:
            result = subprocess.run(
                ["git", "diff", f"{branch1}..{branch2}"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.stdout
        except Exception:
            return ""
    
    def get_changed_files(
        self,
        branch1: str,
        branch2: str,
    ) -> List[str]:
        """Retorna lista de arquivos modificados entre branches."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{branch1}..{branch2}"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            return []
    
    def has_conflicts(self, branch_name: str) -> bool:
        """Verifica se há conflitos no merge."""
        try:
            # Tentar merge dry-run
            result = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", branch_name],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            # Abortar merge
            subprocess.run(
                ["git", "merge", "--abort"],
                capture_output=True,
                cwd=self.repo_path,
            )
            
            return "conflict" in result.stdout.lower() or result.returncode != 0
            
        except Exception:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do repositório."""
        status = {
            "branch": self.get_current_branch(),
            "is_clean": True,
            "uncommitted_files": [],
            "ahead_behind": {"ahead": 0, "behind": 0},
        }
        
        try:
            # Verificar se há mudanças não commitadas
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            if result.stdout.strip():
                status["is_clean"] = False
                status["uncommitted_files"] = [
                    line.split()[1] 
                    for line in result.stdout.strip().split("\n")
                    if line.strip()
                ]
            
            # Verificar ahead/behind
            main_branch = self.get_main_branch()
            result = subprocess.run(
                ["git", "rev-list", "--left-right", "--count", f"{main_branch}...HEAD"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) == 2:
                    status["ahead_behind"] = {
                        "ahead": int(parts[0]),
                        "behind": int(parts[1]),
                    }
            
        except Exception:
            pass
        
        return status
