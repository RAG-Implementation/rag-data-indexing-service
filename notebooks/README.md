<div style="font-size:2.5em; font-weight:bold; text-align:center; margin-top:20px;">Notebooks</div>

Step-by-step Jupyter notebooks that implement the RAG data indexing pipeline.

# 1. Overview

Each notebook covers exactly one stage of the pipeline and is designed to be run
cell by cell. Every notebook follows the same structure:

- A titled markdown cell explaining what the notebook does (and does not) do.
- Numbered step markers (`# ── [N / M] ... ──`) on each code cell.
- A markdown explanation before every code cell.
- A verification cell at the end that checks the output before you move on.

Notebooks are meant to be run in order, because each one reads the output file
produced by the previous one.

# 2. Notebook Index

| Notebook | Stage | Reads | Writes |
|---|---|---|---|
| `01_download_scifact_corpus.ipynb` | Download & normalize the SciFact corpus | Hugging Face | `data/raw/corpus/corpus.jsonl` |
| `02_clean_corpus.ipynb` | Clean & normalize document text | `data/raw/corpus/corpus.jsonl` | `data/processed/02_clean_corpus.jsonl` |

# 3. How to Run

All notebooks run inside the JupyterLab container.

Start the stack and open JupyterLab at `http://localhost:8888`:

```bash
make up
```

Then open a notebook and run it cell by cell. To run a notebook non-interactively
(for example in CI), use `nbconvert`:

```bash
docker compose exec jupyter jupyter nbconvert \
    --to notebook --execute --inplace notebooks/02_clean_corpus.ipynb
```

# 4. Conventions

- Markdown titles use an inline `<div>` (not a `#` heading).
- Configuration values live in a single "Configuration" cell near the top.
- The project root is detected automatically, so notebooks work whether they are
  launched from `notebooks/` or from the project root.
