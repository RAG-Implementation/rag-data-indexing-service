"""Embedding stage.

Wraps a free, local `sentence-transformers` model so the rest of the app can
turn text into vectors without knowing the model details. This is the same logic
validated in `notebooks/05_generate_embeddings.ipynb`.
"""

from __future__ import annotations

import numpy as np


def _best_device() -> str:
    """Return 'cuda' if a GPU is available, otherwise 'cpu'."""
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


class Embedder:
    """Loads an embedding model once and reuses it for every call.

    The device is selected automatically: GPU when available, CPU otherwise.
    Override by passing `device="cpu"` or `device="cuda"` explicitly.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        normalize: bool = True,
        device: str | None = None,
    ):
        # Imported lazily so importing this module is cheap (e.g. for tests).
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self.normalize = normalize
        self.device = device or _best_device()
        self.model = SentenceTransformer(model_name, device=self.device)
        self.vector_size = self.model.get_embedding_dimension()

    def embed_texts(self, texts: list[str], batch_size: int = 64) -> np.ndarray:
        """Embed a list of texts and return a float32 matrix of vectors."""
        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=self.normalize,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vectors.astype(np.float32)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query string and return it as a plain Python list."""
        vector = self.model.encode(text, normalize_embeddings=self.normalize)
        return vector.astype(np.float32).tolist()
