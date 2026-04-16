from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "dev"

    context_max_chars: int = 8000
    top_k_default: int = 5
    retrieval_max_candidates: int = 8000

    data_dir: Path = Path("data/corpus")


def get_settings() -> Settings:
    return Settings()
