# tests/fixtures

Reserved directory for small sample files used by tests that need to load real documents from disk. Keeping fixture files here separates test data from test code and makes it easy to add new input scenarios without modifying test files.

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Conventions](#2-conventions)
- [3. Current Contents](#3-current-contents)

## 1. Purpose

Some tests need to exercise the document loading stage (`app/pipeline/loaders/`) with real files rather than in-memory strings. Place those files in this directory so tests can reference them with a relative path.

Example usage in a test:

```python
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures"

def test_load_txt_file():
    docs = load_documents(FIXTURES)
    assert len(docs) > 0
```

## 2. Conventions

- Keep fixture files small (a few kilobytes at most).
- Use descriptive file names that explain what the file represents (e.g., `sample_abstract.txt`, `broken_encoding.md`).
- Do not place real research data or sensitive content here.
- All files in this directory are tracked by git so tests are reproducible.

## 3. Current Contents

This directory is currently empty. Fixture files will be added as tests that need them are introduced.
