# config

Reserved directory for YAML configuration files. The project currently reads all runtime settings from environment variables via `app/core/config.py`. This directory is the intended home for future file-based configuration if YAML config files are introduced (for example, per-environment pipeline profiles or chunking strategy presets).

## Table of Contents

- [1. Current State](#1-current-state)
- [2. Planned Use](#2-planned-use)

## 1. Current State

This directory is empty. All configuration is handled through environment variables defined in `.env.example` and loaded by `app/core/config.py`. The `.gitkeep` file preserves the directory in git so the structure is visible to new contributors.

## 2. Planned Use

If YAML configuration files are added in the future, they should follow this pattern:

```yaml
# config/pipeline.yaml
chunking:
  strategy: recursive
  chunk_size: 800
  chunk_overlap: 100

embedding:
  model: BAAI/bge-small-en-v1.5

qdrant:
  url: http://qdrant:6333
  collection: rag_scifact
```

For now, use `.env` and `.env.example` at the project root to configure the service.
