# app/services

Orchestration layer that connects all pipeline stages into a single callable service. This package contains one class, `IngestionService`, which is the main entry point used by both the HTTP API and the CLI. It does not implement any pipeline logic itself — it delegates each step to the corresponding module in `app/pipeline/`.

## Table of Contents

- [1. Files](#1-files)
- [2. IngestionService](#2-ingestionservice)
  - [2.1. Constructor](#21-constructor)
  - [2.2. Methods](#22-methods)
- [3. Pipeline Execution Order](#3-pipeline-execution-order)
- [4. Logging](#4-logging)

## 1. Files

| File | Purpose |
|---|---|
| `ingestion_service.py` | `IngestionService` class — orchestrates load, clean, chunk, metadata, embed, index. |
| `__init__.py` | Re-exports `IngestionService` from `app.services`. |

## 2. IngestionService

### 2.1. Constructor

```python
IngestionService(settings: Settings | None = None)
```

Accepts an optional `Settings` instance for dependency injection (useful in tests). When none is provided, `get_settings()` is called to load configuration from the environment. The `Embedder` model is loaded lazily on first use because loading a sentence-transformers model is the most expensive part of startup.

### 2.2. Methods

**`ingest(input_dir, collection_name, chunking_strategy, chunk_size, chunk_overlap) -> dict`**

Runs the full pipeline and returns a summary report. Every parameter is optional and falls back to the configured default when not provided.

Return value:
```python
{
    "collection_name": "rag_scifact",
    "documents": 5183,
    "chunks": 7042,
    "indexed": 7042,
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "embed_seconds": 42.1,
    "index_seconds": 3.8
}
```

If no documents are found in `input_dir`, the method logs a warning and returns counts of zero without hitting Qdrant.

**`status(collection_name=None) -> dict`**

Returns the current status of a Qdrant collection. Delegates to `QdrantIndexer.status()`.

**`reset(collection_name=None) -> dict`**

Deletes a Qdrant collection so it can be rebuilt with a fresh `ingest()` call. Returns `{"collection_name": ..., "deleted": True}`.

## 3. Pipeline Execution Order

```text
1. load_documents(input_dir)
2. clean_text(doc["text"]) for each document
3. chunk_documents(documents, strategy, chunk_size, chunk_overlap)
4. enrich_chunks(chunks, document_type="document")
5. embedder.embed_texts([c["text"] for c in enriched])
6. indexer.recreate_collection(vector_size)
7. indexer.upsert_chunks(vectors, enriched)
```

Steps 5 and 6–7 are each timed separately and reported in `embed_seconds` and `index_seconds`.

## 4. Logging

`IngestionService` logs via `app.core.logging.get_logger("ingestion")`:

| Event | Logged when |
|---|---|
| `no_documents_found` | `input_dir` exists but contains no supported files |
| `ingestion_complete` | The full pipeline finishes, with the summary report as fields |
