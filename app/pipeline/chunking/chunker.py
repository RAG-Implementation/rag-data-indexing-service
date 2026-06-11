"""Chunking stage.

Splits documents into smaller, overlapping chunks using one of three strategies:
`character`, `recursive`, or `token`. This is the same logic explored in
`notebooks/03_chunk_corpus.ipynb`, refactored into reusable functions.
"""

from __future__ import annotations

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# Cache tokenizers so the token strategy loads each model at most once.
_TOKENIZER_CACHE: dict[str, object] = {}


def _get_tokenizer(model_name: str):
    """Load (and cache) a Hugging Face tokenizer for token-aware splitting."""
    if model_name not in _TOKENIZER_CACHE:
        from transformers import AutoTokenizer  # imported lazily

        _TOKENIZER_CACHE[model_name] = AutoTokenizer.from_pretrained(model_name)
    return _TOKENIZER_CACHE[model_name]


def build_splitter(
    strategy: str,
    chunk_size: int,
    chunk_overlap: int,
    tokenizer_model: str = "BAAI/bge-small-en-v1.5",
):
    """Return a LangChain splitter for the requested strategy.

    For the `token` strategy, `chunk_size` and `chunk_overlap` are interpreted as
    token counts; for `character` and `recursive` they are character counts.
    """
    if strategy == "character":
        return CharacterTextSplitter(
            separator="", chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
    if strategy == "recursive":
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
    if strategy == "token":
        return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            _get_tokenizer(tokenizer_model),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    raise ValueError(f"Unknown chunking strategy: {strategy!r}")


def chunk_text(text: str, splitter) -> list[str]:
    """Split one text into non-empty, trimmed chunks."""
    return [piece.strip() for piece in splitter.split_text(text) if piece.strip()]


def chunk_documents(
    documents: list[dict],
    strategy: str,
    chunk_size: int,
    chunk_overlap: int,
    tokenizer_model: str = "BAAI/bge-small-en-v1.5",
) -> list[dict]:
    """Split every document into chunks.

    Each chunk keeps the original document fields and adds a `chunk_index`
    (0, 1, 2, ... within that document).
    """
    splitter = build_splitter(strategy, chunk_size, chunk_overlap, tokenizer_model)

    chunks: list[dict] = []
    for doc in documents:
        pieces = chunk_text(doc.get("text", "") or "", splitter)
        for index, piece in enumerate(pieces):
            chunks.append(
                {
                    "document_id": doc["document_id"],
                    "chunk_index": index,
                    "text": piece,
                    "title": doc.get("title", ""),
                    "source": doc.get("source", ""),
                }
            )
    return chunks
