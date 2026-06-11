# scripts

Reserved directory for standalone utility scripts. These are one-off or maintenance scripts that do not belong inside the `app/` package but are useful for development, data management, or operational tasks.

## Table of Contents

- [1. Current State](#1-current-state)
- [2. Planned Use](#2-planned-use)
- [3. Conventions](#3-conventions)

## 1. Current State

| File | Purpose |
|---|---|
| `README.md` | This file — documents the scripts directory |

Day-to-day automation is handled through `Makefile` targets.

## 2. Planned Use

Scripts that may be added here in the future:

| Script | Purpose |
|---|---|
| `export_collection.py` | Export all vectors and metadata from a Qdrant collection to a JSONL file |
| `validate_corpus.py` | Check a JSONL corpus file for missing fields, duplicates, or encoding issues |
| `benchmark_chunking.py` | Compare chunk count and size distribution across the three chunking strategies |
| `seed_sample_data.py` | Populate `data/samples/` with a small subset of the SciFact corpus for quick testing |

## 3. Conventions

- Scripts must be runnable standalone: `python scripts/my_script.py`.
- Each script should print a usage message when called with `--help`.
- Scripts import from `app/` where possible to avoid duplicating logic.
- Do not add scripts that require the Docker environment to run; they should work with a plain `pip install -r requirements.txt`.
