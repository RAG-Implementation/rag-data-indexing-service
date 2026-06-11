"""Application configuration.

All settings are read from environment variables (and an optional `.env` file)
using `pydantic-settings`. This is the single source of truth for runtime
configuration, mirroring the values defined in `.env.example`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings.

    Field names map to upper-case environment variables automatically, so
    `qdrant_url` is read from the `QDRANT_URL` environment variable.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Qdrant vector database
    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection: str = "rag_scifact"

    # Embedding model (free, local)
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Chunking defaults
    chunk_size: int = 800
    chunk_overlap: int = 100
    chunking_strategy: str = "recursive"

    # Where raw documents are read from
    input_dir: str = "./data/raw"


@lru_cache
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    Caching means the `.env` file is parsed once per process instead of on
    every call, and every part of the app sees the same configuration object.
    """
    return Settings()
