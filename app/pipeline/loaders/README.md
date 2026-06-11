# app/pipeline/loaders

Document loading stage of the pipeline. Reads raw files from a directory and converts them into the standard document dict that all other pipeline stages expect. Files that fail to load are logged as warnings and skipped so one bad file never stops a full ingestion run.

## Table of Contents

- [1. Files](#1-files)
- [2. Supported File Formats](#2-supported-file-formats)
- [3. Output Schema](#3-output-schema)
- [4. Key Functions](#4-key-functions)
- [5. Error Handling](#5-error-handling)

## 1. Files

| File | Purpose |
|---|---|
| `document_loader.py` | All loading logic: `load_document()` for a single file, `load_documents()` for a directory. |
| `__init__.py` | Re-exports `load_documents` and `load_document` so other modules import from `app.pipeline.loaders`. |

## 2. Supported File Formats

| Extension | How it is read |
|---|---|
| `.txt` | `Path.read_text(encoding="utf-8")` |
| `.md` | `Path.read_text(encoding="utf-8")` |
| `.pdf` | `pypdf.PdfReader` — extracts text page by page, joined with newlines |

`pypdf` is imported lazily so `.txt` and `.md` files work even without the `pypdf` package installed.

## 3. Output Schema

Each loaded document is a plain Python dict:

```python
{
    "document_id": "filename_without_extension",
    "title":       "filename_without_extension",
    "text":        "full text content of the file",
    "source":      "absolute or relative path to the file"
}
```

This schema is used by every downstream stage: cleaning, chunking, metadata enrichment, embedding, and indexing.

## 4. Key Functions

**`load_document(path: Path) -> dict`**

Loads a single file. Dispatches to the correct reader based on the file extension. Returns one document dict.

**`load_documents(input_dir: str | Path) -> list[dict]`**

Recursively scans `input_dir` for all supported files (`.txt`, `.md`, `.pdf`). Loads each one, skipping files that raise exceptions. Logs a structured summary at the end:

```
documents_loaded | loaded=42 failed=1 input_dir=./data/raw
```

Raises `FileNotFoundError` if `input_dir` does not exist.

## 5. Error Handling

- **Directory not found:** raises `FileNotFoundError` immediately.
- **Individual file fails:** logged as a `WARNING` with the file path and error message. The run continues with the remaining files.
- **Unsupported extension:** the file is silently skipped (not logged as an error).
