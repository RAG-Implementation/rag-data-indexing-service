# tests

Automated test suite for the service layer. Tests are split into unit tests (fast, no external dependencies) and integration tests (require Qdrant and the embedding model). The full unit suite runs in seconds without a network connection or a running Qdrant container.

## Table of Contents

- [1. Layout](#1-layout)
- [2. Files](#2-files)
  - [2.1. conftest.py](#21-conftestpy)
  - [2.2. unit/](#22-unit)
  - [2.3. integration/](#23-integration)
  - [2.4. fixtures/](#24-fixtures)
- [3. How to Run](#3-how-to-run)
  - [3.1. Unit Tests Only](#31-unit-tests-only)
  - [3.2. All Tests Including Integration](#32-all-tests-including-integration)
- [4. Design Notes](#4-design-notes)

## 1. Layout

| Path | Purpose |
|---|---|
| `conftest.py` | Makes the project root importable so `import app...` works everywhere |
| `unit/` | Fast tests that need no network and no running Qdrant |
| `integration/` | End-to-end tests that use the real Qdrant server |
| `fixtures/` | Small sample files for tests that need real input data |

## 2. Files

### 2.1. conftest.py

Shared pytest configuration. Adds the project root directory to `sys.path` so that `import app.pipeline.cleaning` and similar imports work when running pytest both inside and outside Docker.

### 2.2. unit/

See [unit/README.md](unit/README.md).

| File | What it tests |
|---|---|
| `test_cleaning.py` | `clean_text()` removes whitespace, control chars, and unicode artifacts |
| `test_chunking.py` | `chunk_documents()` splits long text and assigns correct `chunk_index` values |
| `test_metadata.py` | `make_chunk_id()` is stable and unique; `enrich_chunks()` produces all required fields |
| `test_embedding.py` | `Embedder` produces float32 vectors of the correct dimension with unit norms |

### 2.3. integration/

See [integration/README.md](integration/README.md).

| File | What it tests |
|---|---|
| `test_qdrant_indexing.py` | Full index → count → search → reset cycle against a real Qdrant server |

### 2.4. fixtures/

See [fixtures/README.md](fixtures/README.md).

Reserved for small sample files (text, markdown, PDF) used by tests that need to load real documents from disk. Currently empty.

## 3. How to Run

### 3.1. Unit Tests Only

Inside Docker (recommended):

```bash
make test
```

Outside Docker (after `pip install -r requirements.txt`):

```bash
pytest tests/unit/
```

### 3.2. All Tests Including Integration

Integration tests require the Qdrant container to be running:

```bash
make up
docker compose exec jupyter pytest
```

## 4. Design Notes

- `test_embedding.py` loads the real `BAAI/bge-small-en-v1.5` model. The model must already be cached from running notebook 05. If the cache is missing, the test will download the model on first run.
- `test_qdrant_indexing.py` connects to `http://qdrant:6333` inside Docker. Outside Docker, set `QDRANT_URL=http://localhost:6333` before running.
- Each integration test creates a dedicated test collection (`test_integration_collection`) and deletes it in the pytest fixture teardown.
