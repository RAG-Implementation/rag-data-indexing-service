# app/api/routes

FastAPI router modules. Each file owns one group of related endpoints. All routers are registered in `app/main.py`. Route handlers are intentionally thin: they validate input via Pydantic schemas, delegate all work to `IngestionService`, and map exceptions to HTTP error codes.

## Table of Contents

- [1. Files](#1-files)
  - [1.1. health.py](#11-healthpy)
  - [1.2. ingest.py](#12-ingestpy)
  - [1.3. collections.py](#13-collectionspy)
  - [1.4. __init__.py](#14-__init__py)
- [2. Error Handling](#2-error-handling)

## 1. Files

### 1.1. health.py

**Endpoint:** `GET /health`

Returns a simple liveness response to confirm the service is running. Does not check Qdrant connectivity — it is a process-level probe only.

**Response:**
```json
{
  "status": "ok",
  "service": "rag-data-indexing-service"
}
```

### 1.2. ingest.py

**Endpoint:** `POST /ingest`

Accepts an `IngestRequest` body and runs the full pipeline through `IngestionService.ingest()`. Every field in the request is optional and falls back to the value in `app/core/config.py`.

**Request body (all fields optional):**
```json
{
  "input_dir": "./data/raw",
  "collection_name": "rag_scifact",
  "chunking_strategy": "recursive",
  "chunk_size": 800,
  "chunk_overlap": 100
}
```

**Response:**
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

Returns HTTP 400 if the `input_dir` does not exist.

### 1.3. collections.py

**Endpoints:**

- `GET /collections/{collection_name}/status` — Returns statistics for a Qdrant collection. Returns HTTP 404 if the collection does not exist.
- `DELETE /collections/{collection_name}` — Deletes a collection so it can be rebuilt from scratch.

**Status response:**
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

**Reset response:**
```json
{
  "collection_name": "rag_scifact",
  "deleted": true
}
```

### 1.4. __init__.py

Imports and re-exports the `collections`, `health`, and `ingest` router modules so `app/main.py` can import them from a single location.

## 2. Error Handling

| Condition | HTTP Status |
|---|---|
| `input_dir` not found | 400 Bad Request |
| Collection does not exist (status endpoint) | 404 Not Found |
