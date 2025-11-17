"""RAG pipeline for Cortext workspace context management."""

__version__ = "0.1.0"

# Lazy imports to handle missing dependencies gracefully
def _check_dependencies():
    """Check if RAG dependencies are installed."""
    missing = []
    try:
        import sentence_transformers  # noqa: F401
    except ImportError:
        missing.append("sentence-transformers")

    try:
        import chromadb  # noqa: F401
    except ImportError:
        missing.append("chromadb")

    if missing:
        raise ImportError(
            f"RAG dependencies not installed: {', '.join(missing)}. "
            "Install with: pip install cortext-workspace[rag]"
        )


def get_embedder():
    """Get the embedder instance."""
    _check_dependencies()
    from .embedder import Embedder
    return Embedder()


def get_store(workspace_path=None):
    """Get the vector store instance."""
    _check_dependencies()
    from .store import VectorStore
    return VectorStore(workspace_path)


def get_indexer(workspace_path=None):
    """Get the indexer instance."""
    _check_dependencies()
    from .indexer import Indexer
    return Indexer(workspace_path)


def get_retriever(workspace_path=None):
    """Get the retriever instance."""
    _check_dependencies()
    from .retriever import Retriever
    return Retriever(workspace_path)


__all__ = [
    "__version__",
    "get_embedder",
    "get_store",
    "get_indexer",
    "get_retriever",
]
