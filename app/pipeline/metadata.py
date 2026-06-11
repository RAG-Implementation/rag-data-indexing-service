"""Metadata enrichment stage.

Attaches the retrieval metadata recommended in the project goal to each chunk.
This is the same logic validated in `notebooks/04_enrich_metadata.ipynb`.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

REQUIRED_KEYS = {
    "chunk_id",
    "document_id",
    "chunk_index",
    "source_file",
    "document_type",
    "title",
    "created_at",
    "text",
}


def make_chunk_id(document_id: str, chunk_index: int, text: str) -> str:
    """Build a stable, unique id from the document id, chunk index, and text.

    Hashing the content makes re-indexing idempotent: the same chunk always maps
    to the same id, so it updates in place instead of creating duplicates.
    """
    raw = f"{document_id}:{chunk_index}:{text}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def build_metadata(chunk: dict, document_type: str, created_at: str) -> dict:
    """Convert a raw chunk into a full enriched record with metadata.

    `chapter` and `section` are optional structural fields. They stay empty for
    flat corpora (like SciFact abstracts) but are carried through when the source
    chunk provides them, so structured documents (book chapters, manuals) keep
    that context for downstream filtering and citation.
    """
    return {
        "chunk_id": make_chunk_id(
            chunk["document_id"], chunk["chunk_index"], chunk["text"]
        ),
        "document_id": chunk["document_id"],
        "chunk_index": chunk["chunk_index"],
        "source_file": chunk.get("source", ""),
        "document_type": document_type,
        "title": chunk.get("title", ""),
        "chapter": chunk.get("chapter", ""),
        "section": chunk.get("section", ""),
        "created_at": created_at,
        "text": chunk["text"],
    }


def enrich_chunks(chunks: list[dict], document_type: str = "document") -> list[dict]:
    """Attach metadata to every chunk using a single timestamp for the run."""
    created_at = datetime.now(timezone.utc).isoformat()
    return [build_metadata(chunk, document_type, created_at) for chunk in chunks]
