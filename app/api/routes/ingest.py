"""Document ingestion endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_ingestion_service
from app.api.schemas import IngestRequest, IngestResponse
from app.services import IngestionService

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=IngestResponse)
def ingest(
    request: IngestRequest,
    service: IngestionService = Depends(get_ingestion_service),
) -> IngestResponse:
    """Load, clean, chunk, embed, and index documents from a directory."""
    try:
        report = service.ingest(
            input_dir=request.input_dir,
            collection_name=request.collection_name,
            chunking_strategy=request.chunking_strategy,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return IngestResponse(**report)
