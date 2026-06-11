# app/pipeline

The core data processing stages of the RAG indexing pipeline. Each module in this package implements exactly one stage. The stages are pure functions or simple classes with no hidden state — they take data in, transform it, and return data out. This design makes them easy to test in isolation and easy to reuse in both the service layer and the notebooks.

## Table of Contents

- [1. Pipeline Stages](#1-pipeline-stages)
- [2. Files and Modules](#2-files-and-modules)
  - [2.1. loaders/](#21-loaders)
  - [2.2. cleaning.py](#22-cleaningpy)
  - [2.3. chunking/](#23-chunking)
  - [2.4. metadata.py](#24-metadatapy)
  - [2.5. embedding.py](#25-embeddingpy)
  - [2.6. indexing/](#26-indexing)
- [3. Data Flow](#3-data-flow)

## 1. Pipeline Stages

```text
Raw Documents
  → loaders/         — Load .txt / .md / .pdf files from disk
  → cleaning.py      — Fix unicode, strip control chars, normalize whitespace
  → chunking/        — Split documents into overlapping text chunks
  → metadata.py      — Attach a stable chunk_id and retrieval metadata
  → embedding.py     — Generate float32 vectors with a local sentence-transformers model
  → indexing/        — Create a Qdrant collection and upsert the vectors
```

## 2. Files and Modules

### 2.1. loaders/

See [loaders/README.md](loaders/README.md).

Loads raw documents from a directory into a standard dict schema:

```python
{"document_id": str, "title": str, "text": str, "source": str}
```

Supported file formats: `.txt`, `.md`, `.pdf`. Files that fail to load are skipped and logged so one bad file never stops the whole run.

### 2.2. cleaning.py

Normalizes raw text before chunking. Handles:

- Garbled unicode and encoding artifacts (via `ftfy`)
- Non-printable control characters (keeps `\n` and `\t`)
- Runs of multiple spaces and trailing whitespace on each line
- Three or more consecutive blank lines collapsed to one

**Key function:** `clean_text(text: str) -> str` — runs the full cleaning pipeline on a single string.

### 2.3. chunking/

See [chunking/README.md](chunking/README.md).

Splits cleaned document text into smaller overlapping chunks using one of three strategies:

| Strategy | How it splits |
|---|---|
| `character` | Fixed character count, no semantic awareness |
| `recursive` | Tries to split on paragraph/sentence/word boundaries (default) |
| `token` | Counts tokens with a Hugging Face tokenizer (respects model limits) |

**Key function:** `chunk_documents(documents, strategy, chunk_size, chunk_overlap)` — splits every document and adds a `chunk_index` field to each chunk.

### 2.4. metadata.py

Enriches each raw chunk with the metadata fields needed for reliable retrieval:

| Field | Description |
|---|---|
| `chunk_id` | Stable SHA-1 hash of `document_id + chunk_index + text`. Idempotent re-indexing. |
| `document_id` | ID of the source document |
| `chunk_index` | Position of this chunk within its document (0-based) |
| `source_file` | File path of the original document |
| `document_type` | Label for the document category |
| `title` | Document title |
| `created_at` | ISO 8601 UTC timestamp of the indexing run |
| `text` | The chunk text itself |

**Key function:** `enrich_chunks(chunks, document_type) -> list[dict]`

### 2.5. embedding.py

Wraps a local `sentence-transformers` model so the rest of the pipeline does not need to know model details.

**Class:** `Embedder(model_name, normalize, device)`

- Loads the model once and reuses it for all calls.
- Automatically selects GPU if available, falls back to CPU.
- Default model: `BAAI/bge-small-en-v1.5` (384-dimensional, free, no API key).

**Key methods:**

- `embed_texts(texts, batch_size) -> np.ndarray` — returns a float32 matrix of shape `(N, 384)`.
- `embed_query(text) -> list[float]` — embeds a single string for use in a vector search query.

### 2.6. indexing/

See [indexing/README.md](indexing/README.md).

Wraps `qdrant-client` to manage a Qdrant collection and insert embedded chunks.

**Class:** `QdrantIndexer(url, collection, timeout, client)`

Key operations: `recreate_collection`, `upsert_chunks`, `search`, `count`, `exists`, `delete_collection`, `status`.

Point IDs are deterministic UUIDs derived from each chunk's `chunk_id`, making re-indexing idempotent.

## 3. Data Flow

```text
load_documents(input_dir)
    → list[{"document_id", "title", "text", "source"}]

clean_text(doc["text"]) applied to each document

chunk_documents(documents, strategy, chunk_size, chunk_overlap)
    → list[{"document_id", "chunk_index", "text", "title", "source"}]

enrich_chunks(chunks, document_type)
    → list[{"chunk_id", "document_id", "chunk_index", "source_file",
             "document_type", "title", "created_at", "text"}]

embedder.embed_texts([c["text"] for c in enriched])
    → np.ndarray of shape (N, 384)

indexer.recreate_collection(vector_size=384)
indexer.upsert_chunks(vectors, enriched)
    → Qdrant collection ready for vector search
```
