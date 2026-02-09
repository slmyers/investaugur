"""
Basic RAG Module

Local Retrieval-Augmented Generation using LlamaIndex.
This is a stub implementation for Week 1. Full integration in Week 2.
"""
from pathlib import Path
from typing import List


def load_docs(dir_path: str) -> List:
    """
    Load documents from a directory.

    Args:
        dir_path: Path to directory containing PDF documents

    Returns:
        List of loaded documents

    Note: This is a stub. Full implementation will use LlamaIndex SimpleDirectoryReader.
    """
    # Stub: Return empty list for now
    path = Path(dir_path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    return []


def build_index(docs: List, persist_dir: str = "./local_rag_db"):
    """
    Build vector index from documents and persist to disk.

    Args:
        docs: List of documents to index
        persist_dir: Directory to persist the index

    Returns:
        Index object

    Note: This is a stub. Full implementation will use LlamaIndex with Chroma.
    """
    # Stub: Create persist directory if needed
    Path(persist_dir).mkdir(exist_ok=True)
    return None


def query_rag(index, query: str, top_k: int = 5) -> str:
    """
    Query the RAG index and return response.

    Args:
        index: Vector store index
        query: Query string
        top_k: Number of top results to retrieve

    Returns:
        Generated response with retrieved context

    Note: This is a stub. Full implementation will use LlamaIndex query engine.
    """
    # Stub: Return mock response
    return f"Mock RAG response for query: {query}"


# Placeholder for future implementation:
# - HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
# - Chroma vector store setup
# - LlamaIndex VectorStoreIndex
# - Metadata handling (stock, sector, decade)
# - Query engine configuration
