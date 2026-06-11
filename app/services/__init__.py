"""Service layer that orchestrates the pipeline stages into a single workflow."""

from app.services.ingestion_service import IngestionService

__all__ = ["IngestionService"]
