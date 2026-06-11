# data

Holds all data files used and produced by the pipeline. The actual data files are git-ignored. Only this README and the `.gitkeep` placeholder files are tracked by git. This keeps the repository lightweight while preserving the directory structure that the pipeline expects.

## Table of Contents

- [1. Layout](#1-layout)
- [2. Data Flow](#2-data-flow)
- [3. Document Schema](#3-document-schema)
- [4. Recreating the Data](#4-recreating-the-data)

## 1. Layout

| Path | Purpose | Produced by |
|---|---|---|
| `raw/corpus/corpus.jsonl` | Normalized SciFact corpus, one document per line | `notebooks/01_download_scifact_corpus.ipynb` |
| `processed/02_clean_corpus.jsonl` | Corpus after text cleaning | `notebooks/02_clean_corpus.ipynb` |
| `processed/03_chunks.jsonl` | Documents split into overlapping chunks | `notebooks/03_chunk_corpus.ipynb` |
| `processed/04_chunks_with_metadata.jsonl` | Chunks enriched with retrieval metadata | `notebooks/04_enrich_metadata.ipynb` |
| `processed/05_embeddings.npy` | Embedding vectors, one row per chunk | `notebooks/05_generate_embeddings.ipynb` |
| `processed/05_embeddings_meta.jsonl` | Chunk metadata aligned with the vectors | `notebooks/05_generate_embeddings.ipynb` |
| `samples/` | Small sample files for quick experiments | Manual |

## 2. Data Flow

Each pipeline stage reads the previous stage's output file and writes a new one:

```text
raw/corpus/corpus.jsonl
  → processed/02_clean_corpus.jsonl              (cleaning)
  → processed/03_chunks.jsonl                    (chunking)
  → processed/04_chunks_with_metadata.jsonl      (metadata enrichment)
  → processed/05_embeddings.npy + _meta.jsonl    (embedding)
  → Qdrant collection                            (indexing)
```

## 3. Document Schema

Documents in `raw/` and `processed/` share the same base schema:

```json
{
  "document_id": "string",
  "title": "string",
  "text": "string",
  "source": "BeIR/scifact",
  "dataset_config": "corpus"
}
```

Processed files add pipeline-specific fields (e.g., `chunk_index`, `chunk_id`, `created_at`) as each stage enriches the records.

## 4. Recreating the Data

All data can be recreated from scratch by running the notebooks in order:

```bash
make download-data       # runs notebook 01
make up                  # start JupyterLab and Qdrant
# then open http://localhost:8888 and run notebooks 02 through 07
```
