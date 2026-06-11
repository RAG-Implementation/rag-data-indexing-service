"""Qdrant indexing integration test.

Uses the real Qdrant server (http://qdrant:6333) and the real embedding model
to verify the full pipeline: embed -> index -> count -> search -> reset.

Requires:
- Qdrant container running (make up)
- BAAI/bge-small-en-v1.5 cached from running notebook 05
"""

import os

import numpy as np
import pytest

from app.pipeline.embedding import Embedder
from app.pipeline.indexing import QdrantIndexer

QDRANT_URL  = os.environ.get("QDRANT_URL", "http://qdrant:6333")
COLLECTION  = "test_integration_collection"
MODEL       = "BAAI/bge-small-en-v1.5"

SAMPLE_TEXTS = [
    "Diffusion tensor MRI reveals white matter microstructure.",
    "Myelodysplastic syndromes are age-dependent stem cell malignancies.",
    "BC1 RNA is derived from the single copy BC1 RNA gene.",
    "Cerebral white matter development in preterm infants.",
    "Adaptive immune response and ineffective hematopoiesis.",
]

SAMPLE_METADATA = [
    {
        "chunk_id": f"test-chunk-{i}",
        "document_id": f"doc{i}",
        "chunk_index": 0,
        "source_file": "test",
        "document_type": "test",
        "title": f"Test Document {i}",
        "created_at": "2026-01-01T00:00:00+00:00",
        "text": text,
    }
    for i, text in enumerate(SAMPLE_TEXTS)
]


@pytest.fixture(scope="module")
def embedder():
    return Embedder(model_name=MODEL)


@pytest.fixture(scope="module")
def vectors(embedder):
    return embedder.embed_texts(SAMPLE_TEXTS)


@pytest.fixture
def indexer():
    """Fresh indexer pointing at the real Qdrant server."""
    idx = QdrantIndexer(url=QDRANT_URL, collection=COLLECTION)
    yield idx
    # Clean up the test collection after each test
    idx.delete_collection()


def test_vectors_are_real_embeddings(vectors):
    """Confirm real embeddings were generated — not zeros or random noise."""
    assert vectors.shape == (len(SAMPLE_TEXTS), 384)
    assert vectors.dtype == np.float32
    norms = np.linalg.norm(vectors, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-3)


def test_index_and_count(indexer, vectors):
    indexer.recreate_collection(vector_size=384)
    indexed = indexer.upsert_chunks(vectors, SAMPLE_METADATA)

    assert indexed == len(SAMPLE_TEXTS)
    assert indexer.count() == len(SAMPLE_TEXTS)


def test_search_returns_relevant_result(indexer, embedder, vectors):
    """The most relevant chunk for a query should rank first."""
    indexer.recreate_collection(vector_size=384)
    indexer.upsert_chunks(vectors, SAMPLE_METADATA)

    query_vector = embedder.embed_query("MRI white matter brain imaging")
    hits = indexer.search(query_vector, limit=3)

    assert len(hits) == 3
    # The MRI-related chunk should be the top hit
    assert hits[0].payload["document_id"] == "doc0"


def test_reset_deletes_collection(indexer, vectors):
    indexer.recreate_collection(vector_size=384)
    indexer.upsert_chunks(vectors, SAMPLE_METADATA)

    assert indexer.exists() is True
    indexer.delete_collection()
    assert indexer.exists() is False
