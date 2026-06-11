<div style="font-size:2.5em; font-weight:bold; text-align:center; margin-top:20px;">Data</div>

Holds all data used and produced by the pipeline. The actual data files are
git-ignored; only this README and `.gitkeep` placeholders are tracked.

# 1. Folder Layout

| Path | Purpose | Produced by |
|---|---|---|
| `raw/corpus/corpus.jsonl` | Normalized SciFact corpus (one document per line) | `notebooks/01_download_scifact_corpus.ipynb` |
| `processed/02_clean_corpus.jsonl` | Corpus after text cleaning | `notebooks/02_clean_corpus.ipynb` |
| `samples/` | Small sample files for quick experiments | manual |

# 2. Data Flow

Each pipeline stage reads the previous stage's output file and writes a new one:

```text
raw/corpus/corpus.jsonl
  → processed/02_clean_corpus.jsonl   (cleaning)
  → ... (chunking, metadata, embedding in later notebooks)
```

# 3. Document Schema

Documents in `raw/` and `processed/` share the same schema:

```json
{
  "document_id": "string",
  "title": "string",
  "text": "string",
  "source": "BeIR/scifact",
  "dataset_config": "corpus"
}
```
