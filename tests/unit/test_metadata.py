"""Tests for the metadata enrichment stage."""

from app.pipeline.metadata import REQUIRED_KEYS, enrich_chunks, make_chunk_id


def _sample_chunks():
    return [
        {"document_id": "doc1", "chunk_index": 0, "text": "first", "title": "T", "source": "s"},
        {"document_id": "doc1", "chunk_index": 1, "text": "second", "title": "T", "source": "s"},
    ]


def test_make_chunk_id_is_stable():
    a = make_chunk_id("doc1", 0, "hello")
    b = make_chunk_id("doc1", 0, "hello")
    assert a == b, "same input must produce the same id"


def test_make_chunk_id_differs_for_different_content():
    a = make_chunk_id("doc1", 0, "hello")
    b = make_chunk_id("doc1", 1, "hello")
    assert a != b, "different chunk_index must produce a different id"


def test_enrich_chunks_has_all_required_fields_and_unique_ids():
    enriched = enrich_chunks(_sample_chunks(), document_type="test")

    for record in enriched:
        assert REQUIRED_KEYS.issubset(record.keys())
        assert record["document_type"] == "test"

    ids = [r["chunk_id"] for r in enriched]
    assert len(ids) == len(set(ids)), "chunk ids must be unique"


def test_enrich_chunks_chapter_section_default_empty():
    enriched = enrich_chunks(_sample_chunks())

    for record in enriched:
        assert record["chapter"] == "", "chapter defaults to empty for flat corpora"
        assert record["section"] == "", "section defaults to empty for flat corpora"


def test_enrich_chunks_carries_chapter_and_section():
    chunks = [
        {
            "document_id": "doc1",
            "chunk_index": 0,
            "text": "intro",
            "title": "T",
            "source": "s",
            "chapter": "Chapter 1",
            "section": "1.2 Background",
        }
    ]
    enriched = enrich_chunks(chunks)

    assert enriched[0]["chapter"] == "Chapter 1"
    assert enriched[0]["section"] == "1.2 Background"
