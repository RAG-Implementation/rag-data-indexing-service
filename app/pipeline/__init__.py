"""The data indexing pipeline.

Each module implements one stage of the pipeline, in the same order as the
notebooks:

1. `loaders`   - read raw documents from disk (.txt, .md, .pdf)
2. `cleaning`  - normalize text for reliable chunking and embedding
3. `chunking`  - split documents into overlapping chunks
4. `metadata`  - attach retrieval metadata to each chunk
5. `embedding` - turn chunk text into vectors with a local model
6. `indexing`  - store vectors and metadata in Qdrant
"""
