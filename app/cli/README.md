# app/cli

Typer-based command-line interface for running the RAG indexing pipeline locally without starting the HTTP server. The CLI wraps the same `IngestionService` used by the API, so every CLI command produces identical results to the equivalent API call.

## Table of Contents

- [1. Files](#1-files)
- [2. Commands](#2-commands)
  - [2.1. ingest](#21-ingest)
  - [2.2. status](#22-status)
  - [2.3. reset](#23-reset)
- [3. How to Run](#3-how-to-run)

## 1. Files

| File | Purpose |
|---|---|
| `__init__.py` | Defines the Typer `app` object and all CLI commands (`ingest`, `status`, `reset`). |
| `__main__.py` | Entry point so the CLI can be invoked with `python -m app.cli`. Calls `app()`. |

## 2. Commands

### 2.1. ingest

Runs the full pipeline on a folder of documents: load, clean, chunk, enrich metadata, embed, and index into Qdrant. Prints a JSON summary report when done.

```bash
python -m app.cli ingest [OPTIONS]
```

| Option | Description | Default (from config) |
|---|---|---|
| `--input-dir` | Folder containing raw documents | `INPUT_DIR` env var |
| `--collection` | Qdrant collection name | `QDRANT_COLLECTION` env var |
| `--strategy` | Chunking strategy: `character`, `recursive`, or `token` | `CHUNKING_STRATEGY` env var |
| `--chunk-size` | Maximum chunk size in characters | `CHUNK_SIZE` env var |
| `--chunk-overlap` | Overlap between consecutive chunks | `CHUNK_OVERLAP` env var |

**Example output:**
```json
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

### 2.2. status

Shows basic statistics for an existing Qdrant collection.

```bash
python -m app.cli status [OPTIONS]
```

| Option | Description |
|---|---|
| `--collection` | Qdrant collection name (defaults to `QDRANT_COLLECTION`) |

**Example output:**
```json
{
  "collection_name": "rag_scifact",
  "exists": true,
  "vectors_count": 7042,
  "vector_size": 384,
  "distance": "COSINE",
  "embedding_model": "BAAI/bge-small-en-v1.5",
  "status": "CollectionStatus.GREEN"
}
```

### 2.3. reset

Deletes a Qdrant collection so it can be rebuilt from scratch with a fresh `ingest` run.

```bash
python -m app.cli reset [OPTIONS]
```

| Option | Description |
|---|---|
| `--collection` | Qdrant collection name (defaults to `QDRANT_COLLECTION`) |

**Example output:**
```json
{
  "collection_name": "rag_scifact",
  "deleted": true
}
```

## 3. How to Run

Inside the Docker container (recommended):

```bash
make ingest
make reset-index
```

Or directly after `pip install -r requirements.txt`:

```bash
python -m app.cli ingest --input-dir ./data/raw --collection rag_scifact
python -m app.cli status --collection rag_scifact
python -m app.cli reset  --collection rag_scifact
```
