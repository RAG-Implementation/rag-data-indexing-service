# rag-data-indexing-service

## Project Goal

`rag-data-indexing-service` is a production-style data ingestion and indexing service for Retrieval-Augmented Generation (RAG) systems.

The goal of this project is to show that RAG quality starts before retrieval and generation. A reliable RAG system needs clean documents, well-designed chunks, useful metadata, consistent embeddings, and a searchable vector index.

This project focuses only on the data preparation and indexing layer of a RAG pipeline.

## What This Project Does

The service takes raw documents, preprocesses them, splits them into chunks, enriches each chunk with metadata, generates embeddings, and stores the indexed chunks in Qdrant.

The output of this project is a ready-to-query vector index that can be used by downstream retrieval and answering services.

## Core Pipeline

```text
Raw Documents
→ Document Loading
→ Text Cleaning
→ Chunking
→ Metadata Enrichment
→ Embedding
→ Qdrant Indexing
→ Index Health Report
```

## Main Features

### 1. Document Loading

Supported input formats:

```text
.txt
.md
.pdf
```

The initial implementation should focus on `.txt` and `.md` files for simplicity. PDF support can be added through `pypdf` or `unstructured`.

### 2. Text Cleaning

The cleaning layer normalizes text before chunking.

It handles:

```text
extra whitespace
broken line breaks
repeated empty lines
basic formatting artifacts
invalid or empty documents
```

The goal is not heavy NLP preprocessing. The goal is to make the text clean enough for reliable chunking and embedding.

### 3. Chunking Strategies

The service supports multiple chunking strategies so their impact can be compared later.

Supported strategies:

```text
character chunking
recursive character chunking
token-aware chunking
```

Configurable parameters:

```text
chunk_size
chunk_overlap
chunking_strategy
```

Example configuration:

```yaml
chunking:
  strategy: recursive
  chunk_size: 800
  chunk_overlap: 100
```

### 4. Metadata Enrichment

Each chunk should include metadata that makes retrieval easier and more trustworthy.

Recommended metadata:

```json
{
  "document_id": "string",
  "source_file": "string",
  "chunk_id": "string",
  "chunk_index": 0,
  "chapter": "string",
  "section": "string",
  "document_type": "book_chapter",
  "created_at": "datetime"
}
```

Metadata is important because later retrieval services can filter, rank, debug, and cite chunks more effectively.

### 5. Embedding Generation

The project should use free/local embedding models.

Recommended default model:

```text
BAAI/bge-small-en-v1.5
```

Alternative models:

```text
sentence-transformers/all-MiniLM-L6-v2
intfloat/e5-small-v2
intfloat/multilingual-e5-small
```

For this project, `BAAI/bge-small-en-v1.5` is the best default because it is lightweight, free, strong enough for English technical documents, and easy to run locally.

### 6. Vector Indexing

The project uses Qdrant as the vector database.

Qdrant should run locally through Docker Compose.

The service should create or refresh a Qdrant collection and insert embedded chunks with metadata payloads.

The collection should support:

```text
vector search
metadata filtering
collection reset
index refresh
basic health checks
```

## Technology Stack

### Core Language

```text
Python 3.11+
```

### API

```text
FastAPI
Uvicorn
```

Used for exposing ingestion and health-check endpoints.

### CLI

```text
Typer
```

Used for local batch indexing from the terminal.

Example:

```bash
python -m app.cli ingest --input-dir ./data/raw --collection rag_book
```

### Vector Database

```text
Qdrant
qdrant-client
```

Qdrant runs locally with Docker Compose.

### Embeddings

```text
sentence-transformers
BAAI/bge-small-en-v1.5
```

No paid embedding API is required.

### Document Parsing

```text
pypdf
unstructured optional
```

Use `pypdf` for basic PDF support. Keep `unstructured` optional because it can add extra dependencies.

### Chunking

```text
LangChain text splitters
transformers tokenizer
```

Use LangChain splitters for fast implementation and tokenizer-based splitting where needed.

### Configuration

```text
pydantic-settings
.env
YAML config
```

Configuration should control:

```text
Qdrant URL
collection name
embedding model
chunk size
chunk overlap
chunking strategy
input directory
```

### Logging

```text
structlog
```

Logs should include:

```text
number of loaded documents
number of generated chunks
embedding time
indexing time
failed files
Qdrant collection status
```

### Testing

```text
pytest
```

Minimum tests:

```text
text cleaning test
chunking test
metadata creation test
embedding interface test
Qdrant indexing smoke test
```

### Code Quality

```text
ruff
black
mypy optional
```

### Deployment

```text
Docker
Docker Compose
```

Services:

```text
api
qdrant
```

## API Endpoints

### Health Check

```http
GET /health
```

Returns service status.

### Ingest Documents

```http
POST /ingest
```

Indexes documents from a configured input directory.

Request example:

```json
{
  "input_dir": "./data/raw",
  "collection_name": "rag_book",
  "chunking_strategy": "recursive",
  "chunk_size": 800,
  "chunk_overlap": 100
}
```

### Collection Status

```http
GET /collections/{collection_name}/status
```

Returns basic index statistics.

Example response:

```json
{
  "collection_name": "rag_book",
  "vectors_count": 245,
  "indexed_documents": 6,
  "embedding_model": "BAAI/bge-small-en-v1.5"
}
```

### Reset Collection

```http
DELETE /collections/{collection_name}
```

Deletes a collection for clean re-indexing.

## CLI Commands

```bash
make up
make ingest
make test
make lint
make reset-index
```

Expected commands:

```bash
python -m app.cli ingest --input-dir ./data/raw --collection rag_book
python -m app.cli status --collection rag_book
python -m app.cli reset --collection rag_book
```

## What This Project Intentionally Does Not Do

This project does not implement answer generation.

It does not call an LLM.

It does not implement hybrid retrieval, reranking, query rewriting, or observability dashboards.

Those belong to the next repositories:

```text
rag-retrieval-benchmark
production-rag-answering-api
```

Keeping this repository focused makes the system easier to understand, test, and reuse.

## Success Criteria

The project is complete when:

```text
documents can be loaded from a folder
text is cleaned and split into chunks
metadata is attached to every chunk
embeddings are generated locally for free
chunks are stored in Qdrant
the index can be reset and rebuilt
the service runs with Docker Compose
basic tests pass
README explains the pipeline clearly
```

## Branding Message

This repository demonstrates the data engineering foundation of a production-style RAG system.

It shows how raw documents become clean, metadata-rich, embedded, and searchable chunks that downstream RAG services can use reliably.
