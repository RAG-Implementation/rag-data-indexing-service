# app

The production service layer for the RAG data indexing pipeline. This package reuses the exact pipeline logic that the `notebooks/` demonstrate step by step, but organizes it as importable Python modules exposed through a FastAPI HTTP API and a Typer CLI. Everything in this package is tested, typed, and ready to run inside Docker.

## Table of Contents

- [1. Layout](#1-layout)
- [2. Pipeline Order](#2-pipeline-order)
- [3. Entry Points](#3-entry-points)
  - [3.1. FastAPI Application](#31-fastapi-application)
  - [3.2. CLI](#32-cli)
- [4. HTTP API](#4-http-api)
- [5. Configuration](#5-configuration)

## 1. Layout

| Path | Purpose |
|---|---|
| `main.py` | FastAPI application entry point. Creates the `app` instance and registers all routers. |
| `__init__.py` | Marks `app` as a Python package. |
| `core/` | Application-wide configuration (`config.py`) and structured logging (`logging.py`). |
| `pipeline/` | One module per pipeline stage: loaders, cleaning, chunking, metadata, embedding, indexing. |
| `services/` | `IngestionService` — orchestrates the full pipeline end to end. |
| `api/` | FastAPI routers and Pydantic request/response schemas. |
| `cli/` | Typer CLI (`python -m app.cli`) that wraps the same service. |

## 2. Pipeline Order

```text
load → clean → chunk → enrich metadata → embed → index
```

The notebooks in `notebooks/` are the place to learn each stage in detail. This package is the reusable, testable implementation of the same logic.

## 3. Entry Points

### 3.1. FastAPI Application

Start the API server (requires the Qdrant container to be running):

```bash
docker compose --profile api up
```

Or run locally:

```bash
uvicorn app.main:app --reload
```

Interactive API docs are available at http://localhost:8000/docs.

### 3.2. CLI

```bash
python -m app.cli ingest --input-dir ./data/raw --collection rag_scifact
python -m app.cli status --collection rag_scifact
python -m app.cli reset  --collection rag_scifact
```

## 4. HTTP API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check — returns `{"status": "ok"}` |
| `POST` | `/ingest` | Runs the full pipeline on a folder and returns a summary |
| `GET` | `/collections/{name}/status` | Returns vector count and collection statistics |
| `DELETE` | `/collections/{name}` | Deletes a collection so it can be rebuilt from scratch |

## 5. Configuration

All settings are loaded from environment variables (and an optional `.env` file) via `pydantic-settings`. See `core/config.py` for the full list of settings and their defaults. The `.env.example` file at the project root documents every variable.
