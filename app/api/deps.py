"""Shared FastAPI dependencies.

The `IngestionService` loads an embedding model, which is expensive, so we create
it once and reuse it across requests.
"""

from __future__ import annotations

from functools import lru_cache

from app.services import IngestionService


@lru_cache
def get_ingestion_service() -> IngestionService:
    """Return a process-wide singleton ingestion service."""
    return IngestionService()
