"""Collection status and reset endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_ingestion_service
from app.api.schemas import ResetResponse, StatusResponse
from app.services import IngestionService

router = APIRouter(tags=["collections"])


@router.get("/collections/{collection_name}/status", response_model=StatusResponse)
def collection_status(
    collection_name: str,
    service: IngestionService = Depends(get_ingestion_service),
) -> StatusResponse:
    """Return basic statistics for a collection."""
    status = service.status(collection_name)
    if not status.get("exists"):
        raise HTTPException(
            status_code=404, detail=f"Collection '{collection_name}' not found"
        )
    return StatusResponse(**status)


@router.delete("/collections/{collection_name}", response_model=ResetResponse)
def reset_collection(
    collection_name: str,
    service: IngestionService = Depends(get_ingestion_service),
) -> ResetResponse:
    """Delete a collection so it can be rebuilt from scratch."""
    result = service.reset(collection_name)
    return ResetResponse(**result)
