"""Typer command-line interface for local batch indexing.

Usage:

    python -m app.cli ingest --input-dir ./data/raw --collection rag_scifact
    python -m app.cli status --collection rag_scifact
    python -m app.cli reset  --collection rag_scifact
"""

from __future__ import annotations

import json

import typer

from app.core.logging import configure_logging
from app.services import IngestionService

app = typer.Typer(help="RAG data indexing CLI: ingest, status, and reset commands.")


def _service() -> IngestionService:
    configure_logging()
    return IngestionService()


@app.command()
def ingest(
    input_dir: str = typer.Option(None, "--input-dir", help="Folder of raw documents."),
    collection: str = typer.Option(None, "--collection", help="Qdrant collection name."),
    strategy: str = typer.Option(None, "--strategy", help="character | recursive | token."),
    chunk_size: int = typer.Option(None, "--chunk-size", help="Chunk size."),
    chunk_overlap: int = typer.Option(None, "--chunk-overlap", help="Chunk overlap."),
) -> None:
    """Load, clean, chunk, embed, and index documents into Qdrant."""
    report = _service().ingest(
        input_dir=input_dir,
        collection_name=collection,
        chunking_strategy=strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    typer.echo(json.dumps(report, indent=2))


@app.command()
def status(
    collection: str = typer.Option(None, "--collection", help="Qdrant collection name."),
) -> None:
    """Show basic statistics for a collection."""
    report = _service().status(collection_name=collection)
    typer.echo(json.dumps(report, indent=2))


@app.command()
def reset(
    collection: str = typer.Option(None, "--collection", help="Qdrant collection name."),
) -> None:
    """Delete a collection so it can be rebuilt from scratch."""
    report = _service().reset(collection_name=collection)
    typer.echo(json.dumps(report, indent=2))
