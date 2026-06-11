# app/api

FastAPI layer for the RAG data indexing service. This package wires together the HTTP interface: route handlers that call the `IngestionService` and Pydantic schemas that define what the API accepts and returns. The API is thin by design — all business logic lives in `app/services/` and `app/pipeline/`.

## Table of Contents

- [1. Layout](#1-layout)
- [2. Files](#2-files)
  - [2.1. deps.py](#21-depspy)
  - [2.2. routes/](#22-routes)
  - [2.3. schemas/](#23-schemas)
- [3. Endpoints Summary](#3-endpoints-summary)

## 1. Layout

| Path | Purpose |
|---|---|
| `deps.py` | Shared FastAPI dependencies (singleton `IngestionService`). |
| `routes/` | One router module per resource group: `health`, `ingest`, `collections`. |
| `schemas/` | Pydantic models for all request bodies and response payloads. |
| `__init__.py` | Marks `app/api` as a Python package. |

## 2. Files

### 2.1. deps.py

**Purpose:** Manages expensive shared objects across requests.

Defines `get_ingestion_service()`, a `FastAPI` dependency decorated with `@lru_cache`. Because the `IngestionService` loads an embedding model on first use (which is expensive), this pattern ensures the model is loaded only once per process and reused for every subsequent request.

### 2.2. routes/

See [routes/README.md](routes/README.md) for details on each route file.

| File | Endpoints |
|---|---|
| `health.py` | `GET /health` |
| `ingest.py` | `POST /ingest` |
| `collections.py` | `GET /collections/{name}/status`, `DELETE /collections/{name}` |
| `__init__.py` | Imports and re-exports all three router modules. |

### 2.3. schemas/

See [schemas/README.md](schemas/README.md) for details.

Defines all Pydantic models used by the API:

| Model | Used by |
|---|---|
| `HealthResponse` | `GET /health` |
| `IngestRequest` | `POST /ingest` (request body) |
| `IngestResponse` | `POST /ingest` (response) |
| `StatusResponse` | `GET /collections/{name}/status` |
| `ResetResponse` | `DELETE /collections/{name}` |

## 3. Endpoints Summary

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness probe. Returns `{"status": "ok", "service": "rag-data-indexing-service"}`. |
| `POST` | `/ingest` | Runs the full pipeline on a document folder and returns a summary report. |
| `GET` | `/collections/{collection_name}/status` | Returns vector count, distance metric, and model info for a collection. Returns 404 if the collection does not exist. |
| `DELETE` | `/collections/{collection_name}` | Deletes a collection so it can be rebuilt from scratch. |
