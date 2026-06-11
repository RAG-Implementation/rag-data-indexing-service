"""Qdrant indexing stage.

Wraps `qdrant-client` to create/reset a collection, upsert embedded chunks, run
vector searches, and report collection status. This is the same logic validated
in `notebooks/06_index_qdrant.ipynb` and `notebooks/07_index_health_report.ipynb`.
"""

from __future__ import annotations

import uuid

import numpy as np
from qdrant_client import QdrantClient, models

from app.core.logging import get_logger

logger = get_logger("indexing")

# Fixed namespace -> deterministic point ids derived from each chunk_id.
_UUID_NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def _point_id_for(chunk_id: str) -> str:
    """Map a SHA-1 chunk_id to a Qdrant-compatible, deterministic UUID string."""
    return str(uuid.uuid5(_UUID_NAMESPACE, chunk_id))


class QdrantIndexer:
    """Thin wrapper around a Qdrant collection used by the ingestion service."""

    def __init__(
        self,
        url: str | None = None,
        collection: str = "rag_scifact",
        timeout: int = 30,
        client: QdrantClient | None = None,
    ):
        # `client` can be injected (e.g. an in-memory client for tests).
        self.client = client or QdrantClient(url=url, timeout=timeout)
        self.collection = collection

    def recreate_collection(self, vector_size: int) -> None:
        """Create the collection, deleting any existing one first (clean rebuild)."""
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )
        logger.info("collection_created", collection=self.collection, vector_size=vector_size)

    def upsert_chunks(
        self, vectors: np.ndarray, metadata: list[dict], batch_size: int = 256
    ) -> int:
        """Upsert embedded chunks (vector + metadata payload) in batches."""
        points = [
            models.PointStruct(
                id=_point_id_for(meta["chunk_id"]),
                vector=vector.tolist(),
                payload=meta,
            )
            for vector, meta in zip(vectors, metadata)
        ]

        for start in range(0, len(points), batch_size):
            self.client.upsert(
                collection_name=self.collection,
                points=points[start:start + batch_size],
                wait=True,
            )

        logger.info("chunks_upserted", collection=self.collection, count=len(points))
        return len(points)

    def search(self, query_vector: list[float], limit: int = 5):
        """Run a vector similarity search and return the matching points."""
        return self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

    def count(self) -> int:
        """Return the exact number of points stored in the collection."""
        return self.client.count(collection_name=self.collection, exact=True).count

    def exists(self) -> bool:
        """Return True if the collection exists."""
        return self.client.collection_exists(self.collection)

    def delete_collection(self) -> None:
        """Delete the collection for a clean re-index."""
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
            logger.info("collection_deleted", collection=self.collection)

    def status(self, embedding_model: str | None = None) -> dict:
        """Return a status report matching the project goal's collection-status shape."""
        if not self.client.collection_exists(self.collection):
            return {"collection_name": self.collection, "exists": False}

        info = self.client.get_collection(self.collection)
        vector_params = info.config.params.vectors
        return {
            "collection_name": self.collection,
            "exists": True,
            "vectors_count": self.count(),
            "vector_size": vector_params.size,
            "distance": vector_params.distance.name,
            "embedding_model": embedding_model,
            "status": str(info.status),
        }
