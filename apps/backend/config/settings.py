"""
Configurações centrais do framework multi-agente.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List


class Settings(BaseSettings):
    """Configurações do ambiente e do sistema."""
    
    # API Keys
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    
    # Paths
    project_root: Path = Field(default=Path.cwd())
    backend_dir: Path = Field(default=Path(__file__).parent.parent)
    specs_dir: Path = Field(default=Path(__file__).parent.parent / "specs")
    worktrees_dir: Path = Field(default=Path(__file__).parent.parent / ".worktrees")
    
    # Agent Configuration
    max_parallel_agents: int = Field(default=12, env="MAX_PARALLEL_AGENTS")
    agent_timeout_minutes: int = Field(default=60, env="AGENT_TIMEOUT_MINUTES")
    default_model: str = Field(default="claude-sonnet-4-20250514", env="DEFAULT_MODEL")
    max_model: str = Field(default="claude-3-7-sonnet-20250219", env="MAX_MODEL")
    
    # Git Configuration
    main_branch: str = Field(default="main", env="MAIN_BRANCH")
    auto_commit: bool = Field(default=True, env="AUTO_COMMIT")
    
    # QA Pipeline
    run_tests: bool = Field(default=True, env="RUN_TESTS")
    run_linting: bool = Field(default=True, env="RUN_LINTING")
    run_type_check: bool = Field(default=True, env="RUN_TYPE_CHECK")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[Path] = Field(default=None, env="LOG_FILE")
    
    # Feature Flags
    enable_memory_layer: bool = Field(default=True, env="ENABLE_MEMORY_LAYER")
    enable_auto_merge: bool = Field(default=False, env="ENABLE_AUTO_MERGE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Instância global de configurações
settings = Settings()


def get_settings() -> Settings:
    """Retorna as configurações atuais."""
    return settings
