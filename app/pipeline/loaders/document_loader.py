"""Load raw documents from a directory into the pipeline's document schema.

Supported formats: `.txt`, `.md`, and `.pdf` (via `pypdf`). Each loaded document
is a dict with the same shape used throughout the pipeline:

```python
{"document_id": str, "title": str, "text": str, "source": str}
```
"""

from __future__ import annotations

from pathlib import Path

from app.core.logging import get_logger

logger = get_logger("loaders")

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def _read_text_file(path: Path) -> str:
    """Read a plain-text or markdown file."""
    return path.read_text(encoding="utf-8", errors="replace")


def _read_pdf_file(path: Path) -> str:
    """Extract text from a PDF using pypdf, page by page."""
    from pypdf import PdfReader  # imported lazily so .txt/.md work without pypdf

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def load_document(path: Path) -> dict:
    """Load a single supported file into the document schema."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _read_pdf_file(path)
    else:
        text = _read_text_file(path)

    return {
        "document_id": path.stem,
        "title": path.stem,
        "text": text,
        "source": str(path),
    }


def load_documents(input_dir: str | Path) -> list[dict]:
    """Load every supported document under `input_dir` (recursively).

    Files that fail to load are logged and skipped so one bad file never stops
    the whole ingestion run.
    """
    root = Path(input_dir)
    if not root.exists():
        raise FileNotFoundError(f"Input directory not found: {root}")

    documents: list[dict] = []
    failed: list[str] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            documents.append(load_document(path))
        except Exception as exc:  # noqa: BLE001 - skip and report bad files
            failed.append(str(path))
            logger.warning("failed_to_load_file", file=str(path), error=str(exc))

    logger.info(
        "documents_loaded",
        loaded=len(documents),
        failed=len(failed),
        input_dir=str(root),
    )
    return documents
