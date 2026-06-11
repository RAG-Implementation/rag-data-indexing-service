# tests/integration

Integration tests that verify the full indexing pipeline against a real Qdrant server. These tests load the real embedding model, generate real vectors, insert them into a live Qdrant collection, and verify that vector search returns the expected results.

## Table of Contents

- [1. Files](#1-files)
  - [1.1. test_qdrant_indexing.py](#11-test_qdrant_indexingpy)
- [2. Prerequisites](#2-prerequisites)
- [3. How to Run](#3-how-to-run)
- [4. Test Collection Cleanup](#4-test-collection-cleanup)

## 1. Files

### 1.1. test_qdrant_indexing.py

End-to-end test for the embedding and indexing stages together.

**What it does:**

1. Loads `BAAI/bge-small-en-v1.5` and embeds 5 sample scientific sentences.
2. Creates a fresh Qdrant collection named `test_integration_collection`.
3. Upserts the vectors with metadata payloads.
4. Verifies the point count matches the number of inputs.
5. Runs a vector search and asserts the top result is the most semantically relevant document.
6. Deletes the collection and confirms it no longer exists.

**Tests:**

| Test | What it verifies |
|---|---|
| `test_vectors_are_real_embeddings` | Embeddings have the correct shape `(5, 384)`, dtype `float32`, and unit norms |
| `test_index_and_count` | After upsert, `indexer.count()` equals the number of input documents |
| `test_search_returns_relevant_result` | A search for "MRI white matter brain imaging" returns the MRI document as the top hit |
| `test_reset_deletes_collection` | After `delete_collection()`, `indexer.exists()` returns `False` |

**Fixtures:**

- `embedder` — loads the real model once per test module (`scope="module"`).
- `vectors` — computes embeddings once per module and reuses them across tests.
- `indexer` — creates a fresh `QdrantIndexer` for each test and deletes the test collection in teardown.

## 2. Prerequisites

- Qdrant container is running at `http://qdrant:6333` (inside Docker) or at the URL set by `QDRANT_URL`.
- `BAAI/bge-small-en-v1.5` is already cached in the Hugging Face model cache. Run notebook 05 first if the model is not yet downloaded.

## 3. How to Run

Inside Docker (after `make up`):

```bash
docker compose exec jupyter pytest tests/integration/
```

Outside Docker (set `QDRANT_URL` if needed):

```bash
QDRANT_URL=http://localhost:6333 pytest tests/integration/
```

## 4. Test Collection Cleanup

The `indexer` fixture uses pytest teardown (`yield`) to call `delete_collection()` after each test. This ensures the test collection `test_integration_collection` is always removed, even if the test fails partway through.
