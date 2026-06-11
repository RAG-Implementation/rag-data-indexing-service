# tests/unit

Unit tests for every pipeline stage. Each test file is independent and uses no external services, no network calls, and no Docker. The full suite runs in a few seconds.

## Table of Contents

- [1. Files](#1-files)
  - [1.1. test_cleaning.py](#11-test_cleaningpy)
  - [1.2. test_chunking.py](#12-test_chunkingpy)
  - [1.3. test_metadata.py](#13-test_metadatapy)
  - [1.4. test_embedding.py](#14-test_embeddingpy)
- [2. How to Run](#2-how-to-run)

## 1. Files

### 1.1. test_cleaning.py

Tests for `app.pipeline.cleaning.clean_text`.

| Test | What it verifies |
|---|---|
| `test_clean_text_removes_all_problems` | Tabs, double spaces, excess blank lines, and control characters are all removed |
| `test_clean_text_empty_input_returns_empty_string` | Empty string and `None` both return `""` without raising |
| `test_clean_text_preserves_real_unicode` | Legitimate unicode characters (e.g., Greek beta `β`) survive cleaning |

### 1.2. test_chunking.py

Tests for `app.pipeline.chunking`: `build_splitter`, `chunk_text`, and `chunk_documents`.

| Test | What it verifies |
|---|---|
| `test_recursive_chunking_splits_long_text` | A 500-character string with `chunk_size=50` produces multiple non-empty chunks |
| `test_chunk_documents_adds_chunk_index` | `chunk_index` starts at 0 and increases by 1; `document_id` is preserved |
| `test_unknown_strategy_raises` | Passing an unknown strategy name raises `ValueError` |

### 1.3. test_metadata.py

Tests for `app.pipeline.metadata`: `make_chunk_id` and `enrich_chunks`.

| Test | What it verifies |
|---|---|
| `test_make_chunk_id_is_stable` | The same inputs always produce the same chunk ID |
| `test_make_chunk_id_differs_for_different_content` | Different `chunk_index` values produce different IDs |
| `test_enrich_chunks_has_all_required_fields_and_unique_ids` | All required metadata fields are present and all chunk IDs are unique |

### 1.4. test_embedding.py

Tests for `app.pipeline.embedding.Embedder` using the real `BAAI/bge-small-en-v1.5` model.

| Test | What it verifies |
|---|---|
| `test_vector_dimension_matches_model` | `embedder.vector_size` equals 384 |
| `test_embed_texts_returns_float32_matrix` | Output shape is `(3, 384)` and dtype is `float32` |
| `test_embed_texts_vectors_are_normalized` | All vector norms are close to 1.0 (unit vectors) |
| `test_embed_query_returns_list_of_correct_length` | `embed_query` returns a plain Python list of 384 floats |
| `test_similar_texts_have_higher_score_than_unrelated` | Semantically similar texts score higher than unrelated ones |

The embedding model is loaded once per test module via a `scope="module"` pytest fixture.

## 2. How to Run

```bash
pytest tests/unit/
```

Or with verbose output:

```bash
pytest tests/unit/ -v
```
