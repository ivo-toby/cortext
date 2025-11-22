"""RAG pipeline for Cortext workspace context management."""


def get_embedder():
    """Get the embedder instance."""
    from .embedder import Embedder
    return Embedder()


def get_store(workspace_path=None):
    """Get the vector store instance."""
    from .store import VectorStore
    return VectorStore(workspace_path)


def get_indexer(workspace_path=None):
    """Get the indexer instance."""
    from .indexer import Indexer
    return Indexer(workspace_path)


def get_retriever(workspace_path=None):
    """Get the retriever instance."""
    from .retriever import Retriever
    return Retriever(workspace_path)


__all__ = [
    "get_embedder",
    "get_store",
    "get_indexer",
    "get_retriever",
]
