"""API route modules grouped by responsibility."""

from app.api.routes import collections, health, ingest

__all__ = ["collections", "health", "ingest"]
