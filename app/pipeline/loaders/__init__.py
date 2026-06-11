"""Document loaders that read raw files into the pipeline's document schema."""

from app.pipeline.loaders.document_loader import load_documents, SUPPORTED_EXTENSIONS

__all__ = ["load_documents", "SUPPORTED_EXTENSIONS"]
