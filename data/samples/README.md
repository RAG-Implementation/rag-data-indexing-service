# data/samples

Small sample files for quick local experiments and manual testing. Unlike the full corpus in `data/raw/corpus/`, files here are meant to be tiny so you can run the pipeline end to end in seconds without downloading the full dataset.

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. How to Use](#2-how-to-use)
- [3. Conventions](#3-conventions)
- [4. Current Contents](#4-current-contents)

## 1. Purpose

Use this directory when you want to:

- Test a change to the pipeline quickly without waiting for the full corpus to process.
- Try a specific chunking strategy or embedding model on a small, controlled input.
- Provide a minimal reproducible example when debugging.

## 2. How to Use

Run the pipeline on this directory:

```bash
python -m app.cli ingest --input-dir ./data/samples --collection sample_test
```

Or point the API at it via `POST /ingest`:

```json
{
  "input_dir": "./data/samples",
  "collection_name": "sample_test"
}
```

## 3. Conventions

- Keep files small: a few paragraphs per file is enough.
- Use plain `.txt` or `.md` format for readability.
- Commit sample files to git so they are available to everyone without a download step.
- Do not place sensitive or proprietary content here.

## 4. Current Contents

This directory is currently empty. Add your own sample `.txt` or `.md` files to test the pipeline without the full SciFact corpus.
