"""Application configuration.

Settings come from three layers, highest priority first:

1. Environment variables (e.g. `QDRANT_URL`)
2. The `.env` file
3. The optional `config/pipeline.yaml` file

Environment variables and `.env` always win, so the YAML file is a convenient
place to keep project defaults in version control without overriding a
developer's local `.env`. `pydantic-settings` is the single typed source of
truth, mirroring the values documented in `.env.example`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class Settings(BaseSettings):
    """Strongly-typed application settings.

    Field names map to upper-case environment variables automatically, so
    `qdrant_url` is read from the `QDRANT_URL` environment variable.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        yaml_file="config/pipeline.yaml",
        yaml_file_encoding="utf-8",
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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Add the YAML file as the lowest-priority configuration source.

        Order is highest priority first, so environment variables and `.env`
        override anything set in `config/pipeline.yaml`.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    Caching means the configuration files are parsed once per process instead of
    on every call, and every part of the app sees the same configuration object.
    """
    return Settings()
