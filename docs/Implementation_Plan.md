# RAG Data Indexing Service - Implementation Plan

This plan outlines the step-by-step execution strategy for building the `rag-data-indexing-service` in two clear stages: first, a series of Jupyter notebooks that demonstrate each pipeline stage interactively; second, a production service layer that packages the proven notebook logic into reusable, tested Python modules exposed through a FastAPI HTTP API and a Typer CLI.

## Table of Contents

- [1. Goal](#1-goal)
- [2. Two-Stage Approach](#2-two-stage-approach)
  - [2.1. Stage 1 — Notebooks (Phases 1-7)](#21-stage-1--notebooks-phases-1-7)
  - [2.2. Stage 2 — Service Layer (Phases 8-11)](#22-stage-2--service-layer-phases-8-11)
- [3. Notebook House Style](#3-notebook-house-style)
- [4. Pipeline Phase Map](#4-pipeline-phase-map)
- [5. Data Flow](#5-data-flow)
- [6. Phase 0 — Cleanup](#6-phase-0--cleanup)
- [7. Phase 3 — Chunking](#7-phase-3--chunking)
- [8. Phase 4 — Metadata Enrichment](#8-phase-4--metadata-enrichment)
- [9. Phase 5 — Embedding](#9-phase-5--embedding)
- [10. Phase 6 — Qdrant Indexing](#10-phase-6--qdrant-indexing)
- [11. Phase 7 — Index Health Report](#11-phase-7--index-health-report)
- [12. Phase 8 — Service Layer Core](#12-phase-8--service-layer-core)
- [13. Phase 9 — FastAPI](#13-phase-9--fastapi)
- [14. Phase 10 — Typer CLI](#14-phase-10--typer-cli)
- [15. Phase 11 — Tests](#15-phase-11--tests)
- [16. Docs (Ongoing)](#16-docs-ongoing)
- [17. Key Decisions](#17-key-decisions)
- [18. Execution Order](#18-execution-order)

## 1. Goal

Finish every goal in `docs/Project_Goal.md` in two clear stages:

- **Notebooks (Phases 1-7):** one numbered notebook per pipeline stage, designed to be read and run cell by cell. Each notebook number equals its pipeline phase.
- **Service layer (Phases 8-11):** refactor the proven notebook logic into reusable `app/` modules, then expose them via FastAPI and Typer CLI, and add automated tests.

## 2. Two-Stage Approach

### 2.1. Stage 1 — Notebooks (Phases 1-7)

Each notebook is self-contained and reads only the output file of the previous one. This makes it possible to understand and run the pipeline one step at a time without reading the entire codebase.

The two notebooks that already exist — `01_download_scifact_corpus.ipynb` and `02_clean_corpus.ipynb` — define the house style that all new notebooks must follow exactly.

### 2.2. Stage 2 — Service Layer (Phases 8-11)

The `app/` layer reuses — not rewrites — the functions already validated in the notebooks. The notebooks remain the source of truth for learning; the `app/` package is the production-ready, testable implementation of the same logic.

## 3. Notebook House Style

Every notebook must follow this structure exactly:

- A title in a markdown `<div>` (no `#` heading) with a "What this does / does NOT do" summary.
- Numbered markdown sections (`## 1.`, `## 2.`, ...), each followed by exactly one code cell.
- Each code cell starts with a step marker comment: `# ── [N / M] Title ──`.
- A final verification cell that re-reads the output file and asserts it is correct.
- A single "Configuration" cell near the top with all hardcoded values.
- Project root auto-detected: `ROOT = _cwd.parent if _cwd.name == "notebooks" else _cwd`.

## 4. Pipeline Phase Map

| Phase | Stage | Notebook | Status |
|---|---|---|---|
| 1 | Document Loading | `01_download_scifact_corpus.ipynb` | Done |
| 2 | Text Cleaning | `02_clean_corpus.ipynb` | Done |
| 3 | Chunking | `03_chunk_corpus.ipynb` | Done |
| 4 | Metadata Enrichment | `04_enrich_metadata.ipynb` | Done |
| 5 | Embedding | `05_generate_embeddings.ipynb` | Done |
| 6 | Qdrant Indexing | `06_index_qdrant.ipynb` | Done |
| 7 | Index Health Report | `07_index_health_report.ipynb` | Done |
| 8 | Service Layer Core | `app/core/`, `app/pipeline/`, `app/services/` | Done |
| 9 | FastAPI | `app/api/`, `app/main.py` | Done |
| 10 | Typer CLI | `app/cli/` | Done |
| 11 | Tests | `tests/` | Done |

## 5. Data Flow

Each notebook reads the previous notebook's output file and writes a new one under `data/processed/`:

```text
data/raw/corpus/corpus.jsonl
  --> 02_clean_corpus.ipynb  -->  data/processed/02_clean_corpus.jsonl
  --> 03_chunk_corpus.ipynb  -->  data/processed/03_chunks.jsonl
  --> 04_enrich_metadata.ipynb  -->  data/processed/04_chunks_with_metadata.jsonl
  --> 05_generate_embeddings.ipynb  -->  data/processed/05_embeddings.npy
                                    -->  data/processed/05_embeddings_meta.jsonl
  --> 06_index_qdrant.ipynb  -->  Qdrant collection: rag_scifact
  --> 07_index_health_report.ipynb  -->  search + filter smoke test (console)
```

## 6. Phase 0 — Cleanup

- Delete the stray empty `Untitled.ipynb` at the project root.
- Confirm `data/processed/` is the standard output folder (already used by notebook 02).

## 7. Phase 3 — Chunking

**Notebook:** `notebooks/03_chunk_corpus.ipynb`

Implements the chunking goal in `Project_Goal.md` section 3: character, recursive, and token-aware strategies.

**10 numbered cells:**

1. Imports: `json`, `pathlib`, `langchain_text_splitters`, tokenizer from `transformers`.
2. Configuration: `CHUNK_SIZE=800`, `CHUNK_OVERLAP=100`, `STRATEGY="recursive"`, input/output paths.
3. Load the cleaned corpus from `02_clean_corpus.jsonl`.
4. Explore document length distribution (characters and token estimate) to motivate chunking.
5. Define all three splitters in one place: character, recursive (`RecursiveCharacterTextSplitter`), and token-aware (Hugging Face tokenizer-based).
6. Test all three strategies on one document and compare chunk counts and sizes side by side.
7. Chunk the whole corpus with the configured strategy. Each chunk keeps `document_id`, `title`, `source`, and adds `chunk_index` and `text`.
8. Inspect the chunk-size distribution (min, mean, max) and total chunk count.
9. Save chunks to `data/processed/03_chunks.jsonl`.
10. Verify: re-read the file, assert no empty chunks, and confirm overlap is applied correctly.

## 8. Phase 4 — Metadata Enrichment

**Notebook:** `notebooks/04_enrich_metadata.ipynb`

Implements the metadata schema from `Project_Goal.md` section 4.

**10 numbered cells:**

1. Imports.
2. Configuration: input `03_chunks.jsonl`, output `04_chunks_with_metadata.jsonl`.
3. Load chunks.
4. Explain the target metadata schema: `document_id`, `source_file`, `chunk_id`, `chunk_index`, `document_type`, `created_at`, optional `chapter`/`section`.
5. Define helper functions: `make_chunk_id` (stable SHA-1 hash) and `build_metadata`.
6. Test both functions on one chunk.
7. Enrich every chunk.
8. Validate every chunk has all required keys and a unique `chunk_id`.
9. Save output to `04_chunks_with_metadata.jsonl`.
10. Verify: count records and check schema.

## 9. Phase 5 — Embedding

**Notebook:** `notebooks/05_generate_embeddings.ipynb`

Implements `Project_Goal.md` section 5: local, free embeddings using `BAAI/bge-small-en-v1.5`.

**10 numbered cells:**

1. Imports: `sentence_transformers`, `numpy`.
2. Configuration: `EMBEDDING_MODEL`, `BATCH_SIZE`.
3. Load enriched chunks from `04_chunks_with_metadata.jsonl`.
4. Load the model and confirm the vector dimension is 384.
5. Embed one chunk to demonstrate the vector shape.
6. Embed all chunk texts in batches with a progress bar.
7. Sanity-check: vector count equals chunk count, no NaN values, norms are close to 1.0.
8. Save vectors to `data/processed/05_embeddings.npy` and aligned metadata to `05_embeddings_meta.jsonl`.
9. Reload both files and verify alignment (same row count, matching `chunk_id`).
10. Verify final shapes.

## 10. Phase 6 — Qdrant Indexing

**Notebook:** `notebooks/06_index_qdrant.ipynb`

Implements `Project_Goal.md` section 6. Qdrant runs at `http://qdrant:6333` via Docker Compose.

**10 numbered cells:**

1. Imports: `qdrant_client`.
2. Configuration: `QDRANT_URL`, `QDRANT_COLLECTION`, vector size 384, distance Cosine.
3. Connect to Qdrant and run a health check.
4. Load vectors and metadata from the embedding files.
5. Create or recreate the collection (implements the collection-reset goal).
6. Upsert all points in batches with the full metadata payload.
7. Confirm `vectors_count` matches the number of chunks.
8. Run one test vector search and print the top results.
9. Run one metadata-filtered search to verify payload filtering works.
10. Verify collection status matches the expected shape from `Project_Goal.md`.

## 11. Phase 7 — Index Health Report

**Notebook:** `notebooks/07_index_health_report.ipynb`

Implements the "Index Health Report" and success-criteria verification from `Project_Goal.md`.

**7 numbered cells:**

1. Imports and configuration.
2. Connect to Qdrant.
3. Retrieve and display collection status: `vectors_count`, indexed document count, embedding model.
4. End-to-end query demo: embed a natural language question, retrieve top-k results, and print chunks with metadata.
5. Metadata filter demo: retrieve only chunks matching a specific `document_type` or `source`.
6. Collection reset and rebuild check (optional — demonstrates the reset goal).
7. Print a final health summary matching the collection-status JSON shape defined in `Project_Goal.md`.

## 12. Phase 8 — Service Layer Core

**Modules:** `app/core/`, `app/pipeline/`, `app/services/`

Refactor the proven notebook functions into importable modules. No logic changes — only productionize.

| Module | Purpose |
|---|---|
| `app/core/config.py` | `pydantic-settings` `Settings` class reading from `.env`: `QDRANT_URL`, `QDRANT_COLLECTION`, `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `CHUNKING_STRATEGY`, `INPUT_DIR`. |
| `app/core/logging.py` | `structlog` setup that logs the metrics listed in `Project_Goal.md`: documents loaded, chunks produced, embed/index time, failed files. |
| `app/pipeline/loaders/` | `.txt` / `.md` loader and `.pdf` via `pypdf`, mirroring the normalization from notebook 01. |
| `app/pipeline/cleaning.py` | Lift the tested cleaning functions from notebook 02. |
| `app/pipeline/chunking/` | Lift the three chunking strategies from notebook 03. |
| `app/pipeline/metadata.py` | Lift `make_chunk_id` and `build_metadata` from notebook 04. |
| `app/pipeline/embedding.py` | `Embedder` class wrapping the `sentence-transformers` model from notebook 05. |
| `app/pipeline/indexing/` | `QdrantIndexer` class wrapping `qdrant-client` from notebooks 06-07. |
| `app/services/ingestion_service.py` | `IngestionService` orchestrating the full pipeline: load → clean → chunk → enrich → embed → index. |

## 13. Phase 9 — FastAPI

**Modules:** `app/api/`, `app/main.py`

Expose the four endpoints defined in `Project_Goal.md`:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness probe |
| `POST` | `/ingest` | Run the full pipeline on a folder |
| `GET` | `/collections/{name}/status` | Collection statistics |
| `DELETE` | `/collections/{name}` | Delete a collection for a clean rebuild |

- `app/api/schemas/` holds all Pydantic request and response models.
- The `api` Docker Compose service already exists with `--profile api`; no `docker-compose.yml` changes needed.

## 14. Phase 10 — Typer CLI

**Module:** `app/cli/`

`python -m app.cli` with three commands that mirror the FastAPI endpoints: `ingest`, `status`, and `reset`. The existing `Makefile` targets `ingest` and `reset-index` are wired to these commands.

## 15. Phase 11 — Tests

**Directory:** `tests/`

`pytest` covering the minimum set required by `Project_Goal.md`:

| Test | Module under test |
|---|---|
| Text cleaning | `app/pipeline/cleaning.py` |
| Chunking | `app/pipeline/chunking/` |
| Metadata creation | `app/pipeline/metadata.py` |
| Embedding interface | `app/pipeline/embedding.py` |
| Qdrant indexing smoke test | `app/pipeline/indexing/` |

## 16. Docs (Ongoing)

Update the relevant `README.md` file after each phase completes (required by the repo rule: every directory must have a README):

- `notebooks/README.md` — add rows to the notebook index table as each notebook is completed.
- `data/README.md` — add entries to the layout table as each `data/processed/` file is created.
- Root `README.md` — update the notebook table and pipeline description.
- `app/README.md` — add when Phase 8 lands.
- `tests/README.md` — add when Phase 11 lands.

## 17. Key Decisions

| Decision | Rationale |
|---|---|
| Notebook numbers equal pipeline phase numbers | Makes the mapping between phases and files immediately obvious without needing a separate index. |
| Each notebook reads only the previous notebook's output | Ensures notebooks are independent units: you can run and understand them one at a time. |
| `app/` reuses notebook functions, does not rewrite them | Notebooks stay the source of truth for learning; `app/` is the production packaging of the same logic. |
| `data/processed/` as the standard intermediate output folder | All intermediate files share the same parent, are easy to list and inspect, and are already excluded from git. |

## 18. Execution Order

The recommended execution order is notebooks first, service layer second:

1. Run Phases 3-7 (notebooks) end to end and confirm a working Qdrant index with real data.
2. Then productionize in Phases 8-11.

This order ensures the pipeline logic is correct and well-understood before it is packaged as a service.
