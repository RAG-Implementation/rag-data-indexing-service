"""Ingestion service.

Orchestrates the full pipeline end to end:

    load -> clean -> chunk -> enrich metadata -> embed -> index

It reuses the same stage functions that the notebooks demonstrate, so the service
and the notebooks stay in sync.
"""

from __future__ import annotations

import time

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.pipeline.chunking import chunk_documents
from app.pipeline.cleaning import clean_text
from app.pipeline.embedding import Embedder
from app.pipeline.indexing import QdrantIndexer
from app.pipeline.loaders import load_documents
from app.pipeline.metadata import enrich_chunks

logger = get_logger("ingestion")


class IngestionService:
    """High-level entry point for indexing a folder of documents."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        # The embedder is created lazily on first use because loading the model
        # is the most expensive part of startup.
        self._embedder: Embedder | None = None

    @property
    def embedder(self) -> Embedder:
        if self._embedder is None:
            self._embedder = Embedder(self.settings.embedding_model)
        return self._embedder

    def _indexer(self, collection: str) -> QdrantIndexer:
        return QdrantIndexer(self.settings.qdrant_url, collection)

    def ingest(
        self,
        input_dir: str | None = None,
        collection_name: str | None = None,
        chunking_strategy: str | None = None,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> dict:
        """Run the full pipeline and return a summary report.

        Any argument left as `None` falls back to the configured default.
        """
        input_dir = input_dir or self.settings.input_dir
        collection = collection_name or self.settings.qdrant_collection
        strategy = chunking_strategy or self.settings.chunking_strategy
        size = chunk_size or self.settings.chunk_size
        overlap = chunk_overlap if chunk_overlap is not None else self.settings.chunk_overlap

        # 1. Load
        documents = load_documents(input_dir)
        if not documents:
            logger.warning("no_documents_found", input_dir=input_dir)
            return {
                "collection_name": collection,
                "documents": 0,
                "chunks": 0,
                "indexed": 0,
            }

        # 2. Clean
        for doc in documents:
            doc["text"] = clean_text(doc.get("text", "") or "")
            doc["title"] = clean_text(doc.get("title", "") or "")
        documents = [d for d in documents if d["text"]]

        # 3. Chunk
        chunks = chunk_documents(
            documents,
            strategy=strategy,
            chunk_size=size,
            chunk_overlap=overlap,
            tokenizer_model=self.settings.embedding_model,
        )

        # 4. Enrich metadata
        enriched = enrich_chunks(chunks, document_type="document")

        # 5. Embed
        embed_start = time.perf_counter()
        vectors = self.embedder.embed_texts([c["text"] for c in enriched])
        embed_seconds = round(time.perf_counter() - embed_start, 2)

        # 6. Index
        index_start = time.perf_counter()
        indexer = self._indexer(collection)
        indexer.recreate_collection(self.embedder.vector_size)
        indexed = indexer.upsert_chunks(vectors, enriched)
        index_seconds = round(time.perf_counter() - index_start, 2)

        report = {
            "collection_name": collection,
            "documents": len(documents),
            "chunks": len(chunks),
            "indexed": indexed,
            "embedding_model": self.settings.embedding_model,
            "embed_seconds": embed_seconds,
            "index_seconds": index_seconds,
        }
        logger.info("ingestion_complete", **report)
        return report

    def status(self, collection_name: str | None = None) -> dict:
        """Return the status of a collection."""
        collection = collection_name or self.settings.qdrant_collection
        return self._indexer(collection).status(self.settings.embedding_model)

    def reset(self, collection_name: str | None = None) -> dict:
        """Delete a collection so it can be rebuilt from scratch."""
        collection = collection_name or self.settings.qdrant_collection
        self._indexer(collection).delete_collection()
        return {"collection_name": collection, "deleted": True}
