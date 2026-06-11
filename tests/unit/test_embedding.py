"""Tests for the embedding stage using the real model.

Loads BAAI/bge-small-en-v1.5 from the Hugging Face cache (no download needed
when the model is already cached from running the notebooks).
"""

import numpy as np
import pytest

from app.pipeline.embedding import Embedder

MODEL = "BAAI/bge-small-en-v1.5"
EXPECTED_DIM = 384


@pytest.fixture(scope="module")
def embedder():
    """Load the real model once for all tests in this module."""
    return Embedder(model_name=MODEL)


def test_vector_dimension_matches_model(embedder):
    assert embedder.vector_size == EXPECTED_DIM


def test_embed_texts_returns_float32_matrix(embedder):
    vectors = embedder.embed_texts(["hello world", "diffusion tensor MRI", "Qdrant"])

    assert vectors.shape == (3, EXPECTED_DIM)
    assert vectors.dtype == np.float32


def test_embed_texts_vectors_are_normalized(embedder):
    vectors = embedder.embed_texts(["science", "medicine"])
    norms = np.linalg.norm(vectors, axis=1)

    assert np.allclose(norms, 1.0, atol=1e-3), "vectors should be unit length"


def test_embed_query_returns_list_of_correct_length(embedder):
    vector = embedder.embed_query("What is white matter development?")

    assert isinstance(vector, list)
    assert len(vector) == EXPECTED_DIM


def test_similar_texts_have_higher_score_than_unrelated(embedder):
    """Semantically similar texts should produce more similar vectors."""
    v_mri     = embedder.embed_texts(["diffusion tensor MRI white matter"])[0]
    v_related = embedder.embed_texts(["white matter brain imaging"])[0]
    v_unrelated = embedder.embed_texts(["stock market trading profits"])[0]

    score_related   = float(np.dot(v_mri, v_related))
    score_unrelated = float(np.dot(v_mri, v_unrelated))

    assert score_related > score_unrelated, (
        "semantically related texts should have a higher cosine score"
    )
