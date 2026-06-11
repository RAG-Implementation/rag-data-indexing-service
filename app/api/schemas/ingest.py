"""Request and response models for the ingestion and health endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Returned by GET /health."""

    status: str = "ok"
    service: str = "rag-data-indexing-service"


class IngestRequest(BaseModel):
    """Body for POST /ingest. Every field is optional and falls back to config."""

    input_dir: str | None = Field(default=None, examples=["./data/raw"])
    collection_name: str | None = Field(default=None, examples=["rag_scifact"])
    chunking_strategy: str | None = Field(default=None, examples=["recursive"])
    chunk_size: int | None = Field(default=None, examples=[800])
    chunk_overlap: int | None = Field(default=None, examples=[100])


class IngestResponse(BaseModel):
    """Summary of an ingestion run."""

    collection_name: str
    documents: int
    chunks: int
    indexed: int
    embedding_model: str | None = None
    embed_seconds: float | None = None
    index_seconds: float | None = None


class StatusResponse(BaseModel):
    """Status of a Qdrant collection."""

    collection_name: str
    exists: bool
    vectors_count: int | None = None
    indexed_documents: int | None = None
    vector_size: int | None = None
    distance: str | None = None
    embedding_model: str | None = None
    status: str | None = None


class ResetResponse(BaseModel):
    """Result of deleting a collection."""

    collection_name: str
    deleted: bool
