<div style="font-size:2.5em; font-weight:bold; text-align:center; margin-top:20px;">rag-data-indexing-service</div>

Production-style data ingestion and indexing service for RAG systems.

# 1. Overview

This repository prepares raw documents for retrieval: loading, cleaning, chunking, metadata enrichment, embedding, and Qdrant indexing.

# 2. Quick Start with Docker

Everything runs inside Docker — no local Python environment needed.

**Prerequisites:** Docker and Docker Compose must be installed.

**Step 1 — Copy the environment file:**

```bash
cp .env.example .env
```

**Step 2 — Build and start the containers:**

```bash
make up
```

This builds the image and starts two services:

| Service | URL | Purpose |
|---|---|---|
| JupyterLab | http://localhost:8888 | Run and edit notebooks |
| Qdrant | http://localhost:6333 | Vector database (used in later steps) |

**Step 3 — Download the dataset (inside Docker):**

```bash
make download-data
```

**Step 4 — Open JupyterLab** in your browser at http://localhost:8888 and run any notebook cell by cell.

**Stop everything:**

```bash
make down
```

> The Hugging Face dataset cache and Qdrant data are stored in named Docker volumes,
> so they persist across container restarts.
> To also delete the volumes, run: `docker compose down -v`

# 3. Dataset

This project uses the BEIR SciFact corpus as a compact public dataset for testing RAG ingestion and indexing.

To download and normalize the corpus from Hugging Face, run:

```bash
make download-data
```

This executes `notebooks/01_download_scifact_corpus.ipynb` and saves a normalized JSONL file to:

```text
data/raw/corpus/corpus.jsonl
```

Each line is one document with these fields:

```json
{
  "document_id": "<_id>",
  "title": "<title>",
  "text": "<text>",
  "source": "BeIR/scifact",
  "dataset_config": "corpus"
}
```

Project 1 only imports the corpus documents because this repository focuses on document loading, cleaning, chunking, embedding, and vector indexing.

Queries and qrels are intentionally not used in this repository. They belong to the retrieval benchmark and answering API repositories.

# 3. Notebooks

All pipeline steps are implemented as Jupyter notebooks in the `notebooks/` folder.
Each notebook covers one step of the pipeline and can be run cell by cell.

| Notebook | Description |
|---|---|
| `01_download_scifact_corpus.ipynb` | Download and normalize the SciFact corpus from Hugging Face |
| `02_clean_corpus.ipynb` | Clean and normalize the corpus text (whitespace, control chars, unicode) |

# 4. License

MIT License. See [LICENSE](LICENSE).


