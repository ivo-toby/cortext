"""Semantic search and context retrieval."""

from pathlib import Path
from typing import Any

from .embedder import Embedder
from .models import SearchResult
from .store import VectorStore


class Retriever:
    """Semantic search across embedded workspace content."""

    def __init__(self, workspace_path: Path = None):
        """Initialize retriever.

        Args:
            workspace_path: Path to workspace root
        """
        self.workspace_path = Path(workspace_path or Path.cwd())
        self.embedder = Embedder()
        self.store = VectorStore(workspace_path)

    def search(
        self,
        query: str,
        n_results: int = 10,
        conversation_type: str = None,
        date_range: str = None,
    ) -> list[SearchResult]:
        """Semantic search across workspace.

        Args:
            query: Search query text
            n_results: Maximum number of results
            conversation_type: Filter by conversation type (e.g., "brainstorm")
            date_range: Filter by date (YYYY-MM or YYYY-MM-DD)

        Returns:
            List of SearchResult objects sorted by relevance
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_single(query)

        # Build filter
        where_filter = self._build_filter(conversation_type, date_range)

        # Search vector store
        results = self.store.search(
            query_embedding=query_embedding,
            n_results=n_results,
            where=where_filter,
        )

        return results

    def get_similar(
        self, source_path: str, n_results: int = 5
    ) -> list[SearchResult]:
        """Find documents similar to given source.

        Args:
            source_path: Path to source document
            n_results: Number of similar documents to return

        Returns:
            List of similar documents (excluding source)
        """
        # Get chunks from source document
        store_results = self.store.collection.get(
            where={"source_path": source_path},
            include=["embeddings", "documents"],
        )

        if not store_results["embeddings"]:
            return []

        # Use first chunk's embedding as representative
        source_embedding = store_results["embeddings"][0]

        # Search for similar (get extra to filter out source)
        results = self.store.search(
            query_embedding=source_embedding,
            n_results=n_results + 10,  # Get extra to filter
        )

        # Filter out results from same source and deduplicate by source
        seen_sources = {source_path}
        filtered_results = []

        for result in results:
            if result.chunk.source_path not in seen_sources:
                seen_sources.add(result.chunk.source_path)
                filtered_results.append(result)
                if len(filtered_results) >= n_results:
                    break

        return filtered_results

    def _build_filter(
        self, conversation_type: str = None, date_range: str = None
    ) -> dict[str, Any] | None:
        """Build ChromaDB filter from parameters.

        Args:
            conversation_type: Filter by type (e.g., "brainstorm")
            date_range: Filter by date (YYYY-MM or YYYY-MM-DD)

        Returns:
            ChromaDB where filter or None
        """
        conditions = []

        if conversation_type:
            # Filter by path containing conversation type
            conditions.append(
                {"source_path": {"$contains": f"/{conversation_type}/"}}
            )

        if date_range:
            # Filter by date in path
            conditions.append({"source_path": {"$contains": f"/{date_range}"}})

        if not conditions:
            return None

        if len(conditions) == 1:
            return conditions[0]

        # Combine with AND
        return {"$and": conditions}

    def format_results(self, results: list[SearchResult]) -> str:
        """Format search results for display.

        Args:
            results: List of SearchResult objects

        Returns:
            Formatted string for CLI display
        """
        if not results:
            return "No results found."

        output = f"Found {len(results)} result(s):\n\n"

        for i, result in enumerate(results, 1):
            conv_name = result.conversation_name
            score_pct = int(result.score * 100)

            # Truncate text if too long
            text = result.chunk.text
            if len(text) > 200:
                text = text[:197] + "..."

            output += f"{i}. **{conv_name}** (score: {score_pct}%)\n"
            output += f"   {text}\n"
            output += f"   Source: {result.chunk.source_path}\n\n"

        return output

    def format_results_json(self, results: list[SearchResult]) -> list[dict]:
        """Format search results as JSON-serializable dicts.

        Args:
            results: List of SearchResult objects

        Returns:
            List of dictionaries
        """
        return [
            {
                "conversation": result.conversation_name,
                "score": result.score,
                "text": result.chunk.text,
                "source_path": result.chunk.source_path,
                "chunk_index": result.chunk.chunk_index,
            }
            for result in results
        ]
