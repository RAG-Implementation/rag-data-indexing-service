# app/api/schemas

Pydantic models that define the shape of every request body and response payload in the API. Keeping schemas in a dedicated folder separates the data contract from routing logic and makes it easy to see what the API accepts and returns without reading route code.

## Table of Contents

- [1. Files](#1-files)
- [2. Models](#2-models)
  - [2.1. HealthResponse](#21-healthresponse)
  - [2.2. IngestRequest](#22-ingestrequest)
  - [2.3. IngestResponse](#23-ingestresponse)
  - [2.4. StatusResponse](#24-statusresponse)
  - [2.5. ResetResponse](#25-resetresponse)

## 1. Files

| File | Purpose |
|---|---|
| `ingest.py` | All request and response Pydantic models for the API. |
| `__init__.py` | Re-exports all models so routes can import from `app.api.schemas` directly. |

## 2. Models

### 2.1. HealthResponse

Returned by `GET /health`.

| Field | Type | Value |
|---|---|---|
| `status` | `str` | Always `"ok"` |
| `service` | `str` | Always `"rag-data-indexing-service"` |

### 2.2. IngestRequest

Request body for `POST /ingest`. Every field is optional. Fields left as `null` fall back to the configured defaults in `app/core/config.py`.

| Field | Type | Example | Description |
|---|---|---|---|
| `input_dir` | `str \| null` | `"./data/raw"` | Directory to load documents from |
| `collection_name` | `str \| null` | `"rag_scifact"` | Qdrant collection name |
| `chunking_strategy` | `str \| null` | `"recursive"` | `character`, `recursive`, or `token` |
| `chunk_size` | `int \| null` | `800` | Maximum chunk size in characters |
| `chunk_overlap` | `int \| null` | `100` | Overlap between consecutive chunks |

### 2.3. IngestResponse

Returned by `POST /ingest` with a summary of the completed pipeline run.

| Field | Type | Description |
|---|---|---|
| `collection_name` | `str` | Name of the indexed collection |
| `documents` | `int` | Number of documents loaded |
| `chunks` | `int` | Total number of chunks produced |
| `indexed` | `int` | Number of vectors upserted into Qdrant |
| `embedding_model` | `str \| null` | Model used to generate embeddings |
| `embed_seconds` | `float \| null` | Time spent generating embeddings |
| `index_seconds` | `float \| null` | Time spent upserting into Qdrant |

### 2.4. StatusResponse

Returned by `GET /collections/{collection_name}/status`.

| Field | Type | Description |
|---|---|---|
| `collection_name` | `str` | Name of the collection |
| `exists` | `bool` | Whether the collection exists in Qdrant |
| `vectors_count` | `int \| null` | Number of vectors stored |
| `vector_size` | `int \| null` | Dimension of each vector (e.g., 384) |
| `distance` | `str \| null` | Distance metric (e.g., `"COSINE"`) |
| `embedding_model` | `str \| null` | Model that produced the vectors |
| `status` | `str \| null` | Qdrant collection status string |

### 2.5. ResetResponse

Returned by `DELETE /collections/{collection_name}`.

| Field | Type | Description |
|---|---|---|
| `collection_name` | `str` | Name of the deleted collection |
| `deleted` | `bool` | Always `true` after a successful delete |
