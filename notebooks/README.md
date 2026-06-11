# notebooks

Step-by-step Jupyter notebooks that implement the RAG data indexing pipeline. Each notebook covers exactly one stage and is designed to be run cell by cell. The notebooks are the primary place to learn and understand each stage. The production code in `app/pipeline/` implements the same logic as reusable, tested Python modules.

## Table of Contents

- [1. Overview](#1-overview)
- [2. Notebook Index](#2-notebook-index)
- [3. How to Run](#3-how-to-run)
- [4. Conventions](#4-conventions)

## 1. Overview

Notebooks are numbered to match the pipeline order. Each notebook reads the output file produced by the previous one, so they must be run in sequence. Running them out of order will fail because the expected input file will not exist.

Every notebook follows the same internal structure:

- A titled cell explaining what the notebook does and does not do.
- Numbered step markers (`# ── [N / M] ... ──`) on each code cell.
- A markdown explanation before every code cell.
- A verification cell at the end that checks the output before you move on.

## 2. Notebook Index

| Notebook | Phase | Reads | Writes |
|---|---|---|---|
| `01_download_scifact_corpus.ipynb` | Download and normalize the SciFact corpus from Hugging Face | Hugging Face Hub | `data/raw/corpus/corpus.jsonl` |
| `02_clean_corpus.ipynb` | Clean and normalize document text (whitespace, control chars, unicode) | `data/raw/corpus/corpus.jsonl` | `data/processed/02_clean_corpus.jsonl` |
| `03_chunk_corpus.ipynb` | Split documents into overlapping chunks using character, recursive, and token strategies | `data/processed/02_clean_corpus.jsonl` | `data/processed/03_chunks.jsonl` |
| `04_enrich_metadata.ipynb` | Attach a stable `chunk_id` and retrieval metadata to each chunk | `data/processed/03_chunks.jsonl` | `data/processed/04_chunks_with_metadata.jsonl` |
| `05_generate_embeddings.ipynb` | Embed chunks locally with `BAAI/bge-small-en-v1.5` | `data/processed/04_chunks_with_metadata.jsonl` | `data/processed/05_embeddings.npy` and `05_embeddings_meta.jsonl` |
| `06_index_qdrant.ipynb` | Create or reset the Qdrant collection and upsert the embedded vectors | `05_embeddings.npy` and `05_embeddings_meta.jsonl` | Qdrant collection |
| `07_index_health_report.ipynb` | Run an end-to-end query demo and produce a final index health report | Qdrant collection | Console report |

## 3. How to Run

All notebooks run inside the JupyterLab container. Start the stack and open JupyterLab at http://localhost:8888:

```bash
make up
```

Open any notebook and run it cell by cell using the JupyterLab interface.

To run a notebook non-interactively (for example in CI), use `nbconvert`:

```bash
docker compose exec jupyter jupyter nbconvert \
    --to notebook --execute --inplace notebooks/02_clean_corpus.ipynb
```

To download the corpus data automatically without opening JupyterLab:

```bash
make download-data
```

## 4. Conventions

- Configuration values (file paths, chunk sizes, model names) live in a single dedicated "Configuration" cell near the top of each notebook. Change them there only.
- The project root is detected automatically using `pathlib`, so notebooks work whether they are launched from the `notebooks/` directory or from the project root.
- Notebooks do not import from `app/`. They reimplement the same logic inline so each notebook is self-contained and easy to follow.
