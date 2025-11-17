"""MCP tool functions for RAG pipeline.

These functions expose RAG capabilities for AI agents.
"""

from pathlib import Path
from typing import Any

from .embedder import Embedder
from .indexer import Indexer
from .retriever import Retriever
from .store import VectorStore


def embed_document(
    path: str, workspace_path: str = None
) -> dict[str, Any]:
    """Embed a specific document or conversation.

    Args:
        path: Path to file or directory to embed
        workspace_path: Optional workspace root path

    Returns:
        Dictionary with embedding results
    """
    ws_path = Path(workspace_path) if workspace_path else Path.cwd()
    doc_path = Path(path)

    if not doc_path.is_absolute():
        doc_path = ws_path / doc_path

    if not doc_path.exists():
        return {"error": f"Path not found: {doc_path}"}

    embedder = Embedder()
    indexer = Indexer(ws_path)
    store = VectorStore(ws_path)

    embedded_count = 0
    skipped_count = 0
    errors = []

    # Find documents to embed
    documents = indexer.find_documents(doc_path)

    for doc_file in documents:
        try:
            doc = indexer.parse_document(doc_file)

            if not indexer.needs_embedding(doc):
                skipped_count += 1
                continue

            # Generate embeddings
            chunk_texts = [chunk.text for chunk in doc.chunks]
            embeddings = embedder.embed(chunk_texts)

            # Store in vector DB (UPSERT)
            store.update_chunks(doc.chunks, embeddings, str(doc_file))

            # Update status
            indexer.update_status(
                doc, embedder.model_name, embedder.embedding_dim
            )

            embedded_count += 1

        except Exception as e:
            errors.append(f"{doc_file}: {str(e)}")

    return {
        "success": True,
        "embedded": embedded_count,
        "skipped": skipped_count,
        "total_files": len(documents),
        "errors": errors if errors else None,
    }


def embed_workspace(workspace_path: str = None) -> dict[str, Any]:
    """Embed all unembedded content in workspace.

    Args:
        workspace_path: Optional workspace root path

    Returns:
        Dictionary with embedding results
    """
    ws_path = Path(workspace_path) if workspace_path else Path.cwd()

    # Get all conversation type directories
    registry_path = ws_path / ".workspace" / "registry.json"
    if not registry_path.exists():
        return {"error": "Not a valid Cortext workspace (no registry.json)"}

    import json

    registry = json.loads(registry_path.read_text())
    conversation_types = registry.get("conversation_types", {})

    total_embedded = 0
    total_skipped = 0
    all_errors = []

    for type_name, config in conversation_types.items():
        folder = config.get("folder", type_name)
        type_dir = ws_path / folder

        if type_dir.exists():
            result = embed_document(str(type_dir), str(ws_path))
            total_embedded += result.get("embedded", 0)
            total_skipped += result.get("skipped", 0)
            if result.get("errors"):
                all_errors.extend(result["errors"])

    return {
        "success": True,
        "embedded": total_embedded,
        "skipped": total_skipped,
        "errors": all_errors if all_errors else None,
    }


def search_semantic(
    query: str,
    workspace_path: str = None,
    n_results: int = 10,
    conversation_type: str = None,
    date_range: str = None,
) -> dict[str, Any]:
    """Semantic search across workspace.

    Args:
        query: Search query text
        workspace_path: Optional workspace root path
        n_results: Maximum number of results
        conversation_type: Filter by type (e.g., "brainstorm")
        date_range: Filter by date (YYYY-MM or YYYY-MM-DD)

    Returns:
        Dictionary with search results
    """
    ws_path = Path(workspace_path) if workspace_path else Path.cwd()
    retriever = Retriever(ws_path)

    try:
        results = retriever.search(
            query=query,
            n_results=n_results,
            conversation_type=conversation_type,
            date_range=date_range,
        )

        return {
            "success": True,
            "query": query,
            "num_results": len(results),
            "results": retriever.format_results_json(results),
        }

    except Exception as e:
        return {"error": str(e)}


def get_similar(
    source_path: str, workspace_path: str = None, n_results: int = 5
) -> dict[str, Any]:
    """Find documents similar to a given source.

    Args:
        source_path: Path to source document
        workspace_path: Optional workspace root path
        n_results: Number of similar documents to return

    Returns:
        Dictionary with similar documents
    """
    ws_path = Path(workspace_path) if workspace_path else Path.cwd()
    retriever = Retriever(ws_path)

    try:
        results = retriever.get_similar(source_path, n_results=n_results)

        return {
            "success": True,
            "source": source_path,
            "num_results": len(results),
            "similar": retriever.format_results_json(results),
        }

    except Exception as e:
        return {"error": str(e)}


def get_embedding_status(workspace_path: str = None) -> dict[str, Any]:
    """Get embedding status and statistics.

    Args:
        workspace_path: Optional workspace root path

    Returns:
        Dictionary with embedding statistics
    """
    ws_path = Path(workspace_path) if workspace_path else Path.cwd()

    indexer = Indexer(ws_path)
    store = VectorStore(ws_path)

    # Get store stats
    store_stats = store.get_stats()

    # Get all status entries
    all_status = indexer.get_all_status()

    # Calculate summary
    recent_embeddings = []
    for path, status in sorted(
        all_status.items(), key=lambda x: x[1].embedded_at, reverse=True
    )[:5]:
        recent_embeddings.append(
            {
                "path": path,
                "chunks": status.num_chunks,
                "embedded_at": status.embedded_at.isoformat(),
            }
        )

    return {
        "success": True,
        "total_chunks": store_stats["total_chunks"],
        "num_documents": store_stats["num_documents"],
        "db_path": store_stats["db_path"],
        "recent_embeddings": recent_embeddings,
    }
