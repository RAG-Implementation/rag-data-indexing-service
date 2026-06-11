# app/core

Application-wide infrastructure shared by every part of the service. This package contains exactly two modules: one for configuration and one for logging. Both are designed to be imported once at startup and reused everywhere without creating duplicate instances.

## Table of Contents

- [1. Files](#1-files)
  - [1.1. config.py](#11-configpy)
  - [1.2. logging.py](#12-loggingpy)
- [2. Usage](#2-usage)

## 1. Files

### 1.1. config.py

**Purpose:** Single source of truth for all runtime configuration.

Defines a `Settings` class backed by `pydantic-settings`. Every setting maps directly to an environment variable (e.g., `qdrant_url` reads from `QDRANT_URL`). Settings are resolved from three layers, highest priority first: environment variables, the `.env` file, then `config/pipeline.yaml`. Environment variables and `.env` always override the YAML file.

The `get_settings()` function returns a cached singleton so the configuration files are parsed only once per process. Every module in the app imports settings through `get_settings()`.

**Settings defined:**

| Setting | Environment Variable | Default | Description |
|---|---|---|---|
| `qdrant_url` | `QDRANT_URL` | `http://qdrant:6333` | Qdrant server URL |
| `qdrant_collection` | `QDRANT_COLLECTION` | `rag_scifact` | Default collection name |
| `embedding_model` | `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | Local Hugging Face embedding model |
| `chunk_size` | `CHUNK_SIZE` | `800` | Maximum chunk size in characters |
| `chunk_overlap` | `CHUNK_OVERLAP` | `100` | Overlap between consecutive chunks |
| `chunking_strategy` | `CHUNKING_STRATEGY` | `recursive` | Chunking strategy: `character`, `recursive`, or `token` |
| `input_dir` | `INPUT_DIR` | `./data/raw` | Directory to read raw documents from |

### 1.2. logging.py

**Purpose:** Structured logging setup for the entire application.

Configures Python's standard `logging` module and `structlog` together so that all log output is structured, timestamped, and human-readable in the terminal. Uses `structlog.dev.ConsoleRenderer` for clean local output.

**Functions:**

- `configure_logging(level="INFO")` — Sets up both `logging` and `structlog`. Should be called once at startup. Both the API (`main.py`) and the CLI (`app/cli/__init__.py`) call this.
- `get_logger(name=None)` — Returns a bound `structlog` logger, optionally tagged with a component name (e.g., `"indexing"`, `"loaders"`). All pipeline modules use this to log structured events like `documents_loaded`, `chunks_upserted`, and `ingestion_complete`.

## 2. Usage

```python
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger("my_component")

settings = get_settings()
print(settings.qdrant_url)
```
