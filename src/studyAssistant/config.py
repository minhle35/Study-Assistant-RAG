import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Set


class Settings(BaseSettings):
    """Application settings"""

    # App info
    app_name: str = "RAG StudyAssistant"
    version: str = "1.0.0"
    debug: bool = False

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7

    # Paths
    documents_dir: Path = Path("documents")
    vector_db_dir: Path = Path("vector_db")

    # RAG settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_sources: int = 3
    supported_extensions: Set[str] = {".pdf", ".txt", ".md"}

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # CORS settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_prefix = "STUDYBUDDY_"

    def __post_init__(self):
        """Create directories if they don't exist"""
        self.documents_dir.mkdir(exist_ok=True)
        self.vector_db_dir.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
