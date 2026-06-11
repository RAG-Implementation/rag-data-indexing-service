# app/pipeline/chunking

Chunking stage of the pipeline. Splits cleaned document text into smaller, overlapping pieces so that each piece fits within the embedding model's context window and carries enough surrounding context for meaningful retrieval. Three strategies are supported so their impact on retrieval quality can be compared later.

## Table of Contents

- [1. Files](#1-files)
- [2. Chunking Strategies](#2-chunking-strategies)
- [3. Key Functions](#3-key-functions)
- [4. Output Schema](#4-output-schema)
- [5. Configuration](#5-configuration)

## 1. Files

| File | Purpose |
|---|---|
| `chunker.py` | All chunking logic: `build_splitter()`, `chunk_text()`, and `chunk_documents()`. |
| `__init__.py` | Re-exports the public functions so other modules import from `app.pipeline.chunking`. |

## 2. Chunking Strategies

| Strategy | Implementation | Units | Best for |
|---|---|---|---|
| `character` | `LangChain CharacterTextSplitter` | Characters | Simple, fast splitting when semantic boundaries do not matter |
| `recursive` | `LangChain RecursiveCharacterTextSplitter` | Characters | Default — tries paragraph, sentence, then word boundaries |
| `token` | `RecursiveCharacterTextSplitter.from_huggingface_tokenizer` | Tokens | Guarantees chunks fit the embedding model's token limit |

For the `token` strategy, `chunk_size` and `chunk_overlap` are interpreted as **token counts**. For `character` and `recursive` they are **character counts**.

## 3. Key Functions

**`build_splitter(strategy, chunk_size, chunk_overlap, tokenizer_model) -> splitter`**

Returns the appropriate LangChain splitter object. For the `token` strategy, the tokenizer is loaded from Hugging Face and cached so repeated calls do not reload it. Raises `ValueError` for an unknown strategy.

**`chunk_text(text: str, splitter) -> list[str]`**

Splits a single text string using the given splitter. Returns non-empty, trimmed chunks only.

**`chunk_documents(documents, strategy, chunk_size, chunk_overlap, tokenizer_model) -> list[dict]`**

Iterates over all documents, splits each one, and returns a flat list of chunk dicts. Each chunk keeps the original document fields and adds `chunk_index` (0, 1, 2, ... within that document).

## 4. Output Schema

Each chunk produced by `chunk_documents` is a dict:

```python
{
    "document_id":  "source_document_id",
    "chunk_index":  0,          # position within the document, 0-based
    "text":         "chunk text content",
    "title":        "document title",
    "source":       "source file path"
}
```

## 5. Configuration

Default values used throughout the pipeline:

| Parameter | Default | Description |
|---|---|---|
| `chunk_size` | `800` | Maximum chunk size |
| `chunk_overlap` | `100` | Number of characters (or tokens) shared between adjacent chunks |
| `strategy` | `recursive` | Splitting strategy |
| `tokenizer_model` | `BAAI/bge-small-en-v1.5` | Hugging Face tokenizer used by the `token` strategy |
