"""Tests for the chunking stage."""

from app.pipeline.chunking import chunk_documents, chunk_text, build_splitter


def test_recursive_chunking_splits_long_text():
    splitter = build_splitter("recursive", chunk_size=50, chunk_overlap=10)
    text = "word " * 100  # 500 chars, well above the chunk size
    chunks = chunk_text(text, splitter)

    assert len(chunks) > 1, "long text should produce multiple chunks"
    assert all(chunk.strip() for chunk in chunks), "no empty chunks"


def test_chunk_documents_adds_chunk_index():
    documents = [
        {"document_id": "doc1", "title": "T", "text": "word " * 100, "source": "s"}
    ]
    chunks = chunk_documents(
        documents, strategy="recursive", chunk_size=50, chunk_overlap=10
    )

    assert len(chunks) > 1
    # chunk_index must start at 0 and increase by 1
    indexes = [c["chunk_index"] for c in chunks]
    assert indexes == list(range(len(chunks)))
    assert all(c["document_id"] == "doc1" for c in chunks)


def test_unknown_strategy_raises():
    import pytest

    with pytest.raises(ValueError):
        build_splitter("nonsense", chunk_size=10, chunk_overlap=0)
