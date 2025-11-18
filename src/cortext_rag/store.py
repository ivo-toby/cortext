"""Vector store using ChromaDB."""

from pathlib import Path
from typing import Any

from .models import Chunk, SearchResult


class VectorStore:
    """Persistent vector store using ChromaDB."""

    def __init__(self, workspace_path: Path = None):
        """Initialize vector store.

        Args:
            workspace_path: Path to workspace root
        """
        self.workspace_path = Path(workspace_path or Path.cwd())
        self.db_path = self.workspace_path / ".workspace" / "embeddings" / "chroma"
        self._client = None
        self._collection = None

    def _ensure_client(self) -> None:
        """Ensure ChromaDB client is initialized."""
        if self._client is not None:
            return

        try:
            import chromadb
        except ImportError:
            raise ImportError(
                "chromadb not installed. "
                "Install with: pip install cortext-workspace[rag]"
            )

        # Create database directory
        self.db_path.mkdir(parents=True, exist_ok=True)

        # Initialize persistent client
        self._client = chromadb.PersistentClient(path=str(self.db_path))

        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name="cortext_chunks",
            metadata={"description": "Cortext workspace document chunks"},
        )

    @property
    def collection(self):
        """Get the ChromaDB collection."""
        self._ensure_client()
        return self._collection

    def add_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        source_path: str,
    ) -> None:
        """Add chunks with embeddings to store.

        Args:
            chunks: List of chunks to add
            embeddings: Corresponding embeddings
            source_path: Source document path
        """
        if not chunks:
            return

        self._ensure_client()

        # Prepare data for ChromaDB
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [
            {
                "source_path": chunk.source_path,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                **{k: str(v) for k, v in chunk.metadata.items()},
            }
            for chunk in chunks
        ]

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def update_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        source_path: str,
    ) -> None:
        """Update chunks for a document (UPSERT).

        Deletes old chunks and adds new ones.

        Args:
            chunks: New chunks
            embeddings: New embeddings
            source_path: Source document path
        """
        # Delete old chunks for this source
        self.delete_by_source(source_path)

        # Add new chunks
        self.add_chunks(chunks, embeddings, source_path)

    def delete_by_source(self, source_path: str) -> None:
        """Delete all chunks from a source document.

        Args:
            source_path: Source document path
        """
        self._ensure_client()

        # Query for all chunks from this source
        results = self.collection.get(where={"source_path": source_path})

        if results["ids"]:
            self.collection.delete(ids=results["ids"])

    def search(
        self,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict[str, Any] = None,
    ) -> list[SearchResult]:
        """Search for similar chunks.

        Args:
            query_embedding: Query vector
            n_results: Maximum number of results
            where: Optional filter conditions

        Returns:
            List of SearchResult objects
        """
        self._ensure_client()

        # Perform search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        # Convert to SearchResult objects
        search_results = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                # Extract metadata
                metadata = results["metadatas"][0][i]
                text = results["documents"][0][i]
                distance = results["distances"][0][i]

                # Convert distance to similarity score (ChromaDB uses L2 by default)
                # Lower distance = more similar
                score = 1.0 / (1.0 + distance)

                chunk = Chunk(
                    text=text,
                    source_path=metadata.get("source_path", ""),
                    chunk_index=int(metadata.get("chunk_index", 0)),
                    total_chunks=int(metadata.get("total_chunks", 1)),
                    metadata={
                        k: v
                        for k, v in metadata.items()
                        if k not in ["source_path", "chunk_index", "total_chunks"]
                    },
                )

                search_results.append(SearchResult(chunk=chunk, score=score))

        return search_results

    def get_stats(self) -> dict[str, Any]:
        """Get statistics about the vector store.

        Returns:
            Dictionary with store statistics
        """
        self._ensure_client()

        count = self.collection.count()

        # Get unique sources
        if count > 0:
            results = self.collection.get(include=["metadatas"])
            sources = set()
            for metadata in results["metadatas"]:
                if "source_path" in metadata:
                    sources.add(metadata["source_path"])
            num_documents = len(sources)
        else:
            num_documents = 0

        return {
            "total_chunks": count,
            "num_documents": num_documents,
            "db_path": str(self.db_path),
        }

    def clear(self) -> None:
        """Clear all data from the store."""
        self._ensure_client()
        # Delete and recreate collection
        self._client.delete_collection("cortext_chunks")
        self._collection = self._client.create_collection(
            name="cortext_chunks",
            metadata={"description": "Cortext workspace document chunks"},
        )
