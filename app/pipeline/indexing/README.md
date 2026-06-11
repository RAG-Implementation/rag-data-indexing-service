# app/pipeline/indexing

Qdrant indexing stage of the pipeline. Wraps the `qdrant-client` library to manage a collection, insert embedded chunks, run vector searches, and report collection health. Point IDs are deterministic UUIDs derived from each chunk's `chunk_id`, which makes re-indexing idempotent: the same chunk always maps to the same point and updates in place instead of creating duplicates.

## Table of Contents

- [1. Files](#1-files)
- [2. QdrantIndexer Class](#2-qdrantindexer-class)
  - [2.1. Constructor](#21-constructor)
  - [2.2. Methods](#22-methods)
- [3. Point ID Strategy](#3-point-id-strategy)
- [4. Logging](#4-logging)

## 1. Files

| File | Purpose |
|---|---|
| `qdrant_indexer.py` | `QdrantIndexer` class — all Qdrant operations. |
| `__init__.py` | Re-exports `QdrantIndexer` from `app.pipeline.indexing`. |

## 2. QdrantIndexer Class

### 2.1. Constructor

```python
QdrantIndexer(
    url: str | None = None,
    collection: str = "rag_scifact",
    timeout: int = 30,
    client: QdrantClient | None = None,
)
```

The `client` parameter accepts an injected `QdrantClient`. This is used in tests to pass an in-memory client (`QdrantClient(":memory:")`) so tests run without a real Qdrant server.

### 2.2. Methods

| Method | Description |
|---|---|
| `recreate_collection(vector_size)` | Deletes the collection if it exists, then creates a fresh one with cosine distance and the given vector dimension. |
| `upsert_chunks(vectors, metadata, batch_size=256)` | Converts each `(vector, metadata)` pair into a Qdrant `PointStruct` and upserts them in batches. Returns the total number of points inserted. |
| `search(query_vector, limit=5)` | Runs a cosine similarity search and returns the top matching points with their metadata payloads. |
| `count()` | Returns the exact number of points (chunks) in the collection. |
| `count_documents()` | Scrolls the payloads and returns the number of distinct `document_id` values (source documents, not chunks). |
| `exists()` | Returns `True` if the collection currently exists in Qdrant. |
| `delete_collection()` | Deletes the collection if it exists. Used to reset the index before a clean rebuild. |
| `status(embedding_model=None)` | Returns a status dict with `collection_name`, `exists`, `vectors_count`, `indexed_documents`, `vector_size`, `distance`, `embedding_model`, and `status`. |

## 3. Point ID Strategy

Qdrant requires each point to have a UUID. Point IDs are generated deterministically using `uuid.uuid5(namespace, chunk_id)`. Because `chunk_id` is itself a SHA-1 hash of the document ID, chunk index, and text, the same chunk always produces the same point ID. This means:

- Re-indexing the same document updates existing points rather than creating duplicates.
- You can delete a specific chunk by computing its expected point ID without querying first.

## 4. Logging

`QdrantIndexer` logs structured events via `app.core.logging.get_logger("indexing")`:

| Event | Logged when |
|---|---|
| `collection_created` | A new collection is successfully created |
| `chunks_upserted` | A batch upsert completes |
| `collection_deleted` | A collection is deleted |
