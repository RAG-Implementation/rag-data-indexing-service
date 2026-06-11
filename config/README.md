# config

Version-controlled YAML configuration for the pipeline. This directory holds `pipeline.yaml`, the lowest-priority configuration layer. Environment variables and the `.env` file always override these values, so this file is a safe place to keep shared project defaults without overriding a developer's local setup.

## Table of Contents

- [1. Files](#1-files)
- [2. How It Works](#2-how-it-works)
- [3. Precedence](#3-precedence)

## 1. Files

| File | Purpose |
|---|---|
| `pipeline.yaml` | Flat key/value defaults for every setting in `app/core/config.py`. |

## 2. How It Works

`app/core/config.py` registers a `YamlConfigSettingsSource` that reads `config/pipeline.yaml`. The keys are flat and match the `Settings` field names exactly:

```yaml
qdrant_url: http://qdrant:6333
qdrant_collection: rag_scifact
embedding_model: BAAI/bge-small-en-v1.5
chunk_size: 800
chunk_overlap: 100
chunking_strategy: recursive
input_dir: ./data/raw
```

## 3. Precedence

Configuration is resolved highest priority first:

```text
1. Environment variables (e.g. QDRANT_URL)
2. .env file
3. config/pipeline.yaml   <-- this directory
4. built-in defaults in app/core/config.py
```

So a value in `.env` always wins over the same key in `pipeline.yaml`. Use `.env` for machine-specific overrides and `pipeline.yaml` for shared team defaults.
