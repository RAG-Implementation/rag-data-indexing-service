"""FastAPI application entry point.

Run locally with:

    uvicorn app.main:app --reload

Or via Docker Compose:

    docker compose --profile api up
"""

from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import collections, health, ingest
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="RAG Data Indexing Service",
    description="Loads, cleans, chunks, embeds, and indexes documents into Qdrant.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(collections.router)
