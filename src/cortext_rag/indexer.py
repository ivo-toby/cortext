"""Document indexing with chunking and UPSERT logic."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import Chunk, Document, EmbeddingStatus
from .parsers import get_parser


class Indexer:
    """Index documents with chunking and change detection."""

    def __init__(
        self,
        workspace_path: Path = None,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ):
        """Initialize indexer.

        Args:
            workspace_path: Path to workspace root
            chunk_size: Target chunk size in tokens (approximate)
            chunk_overlap: Overlap between chunks in tokens
        """
        self.workspace_path = Path(workspace_path or Path.cwd())
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.status_file = (
            self.workspace_path / ".workspace" / "embeddings" / "status.json"
        )

    def parse_document(self, path: Path) -> Document:
        """Parse a document file.

        Args:
            path: Path to document

        Returns:
            Document with parsed content and metadata
        """
        parser = get_parser(path)
        content, metadata = parser.parse(path)
        content_hash = self._compute_hash(content)

        doc = Document(
            path=path,
            content=content,
            content_hash=content_hash,
            doc_type=path.suffix.lower(),
            metadata=metadata,
        )

        # Generate chunks
        doc.chunks = self._chunk_content(content, str(path))

        return doc

    def _chunk_content(self, content: str, source_path: str) -> list[Chunk]:
        """Split content into overlapping chunks.

        Uses simple word-based chunking (tokens ≈ words * 1.3).

        Args:
            content: Text content to chunk
            source_path: Source file path for metadata

        Returns:
            List of Chunk objects
        """
        if not content.strip():
            return []

        # Approximate tokens as words (rough estimate)
        words = content.split()
        if not words:
            return []

        # Convert token counts to word counts (approximate)
        words_per_chunk = int(self.chunk_size / 1.3)
        overlap_words = int(self.chunk_overlap / 1.3)

        chunks = []
        start = 0

        while start < len(words):
            end = min(start + words_per_chunk, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append(
                Chunk(
                    text=chunk_text,
                    source_path=source_path,
                    chunk_index=len(chunks),
                    total_chunks=0,  # Will update after
                    metadata={"start_word": start, "end_word": end},
                )
            )

            # Move start with overlap
            start = end - overlap_words
            if start >= len(words) - overlap_words:
                break

        # Update total_chunks
        for chunk in chunks:
            chunk.total_chunks = len(chunks)

        return chunks

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def needs_embedding(self, doc: Document) -> bool:
        """Check if document needs (re-)embedding.

        Args:
            doc: Document to check

        Returns:
            True if document needs embedding, False if unchanged
        """
        status = self.get_status(str(doc.path))
        if status is None:
            return True
        return status.content_hash != doc.content_hash

    def update_status(
        self, doc: Document, model_name: str, embedding_dim: int
    ) -> None:
        """Update embedding status for document.

        Args:
            doc: Document that was embedded
            model_name: Name of embedding model used
            embedding_dim: Dimension of embeddings
        """
        # Load existing status
        all_status = self._load_all_status()

        # Update with new status
        status = EmbeddingStatus(
            source_path=str(doc.path),
            content_hash=doc.content_hash,
            num_chunks=len(doc.chunks),
            embedded_at=datetime.now(),
            model_name=model_name,
            embedding_dim=embedding_dim,
        )

        all_status[str(doc.path)] = status.to_dict()

        # Save status
        self._save_all_status(all_status)

    def get_status(self, source_path: str) -> EmbeddingStatus | None:
        """Get embedding status for a document.

        Args:
            source_path: Path to source document

        Returns:
            EmbeddingStatus if exists, None otherwise
        """
        all_status = self._load_all_status()
        if source_path in all_status:
            return EmbeddingStatus.from_dict(all_status[source_path])
        return None

    def get_all_status(self) -> dict[str, EmbeddingStatus]:
        """Get all embedding statuses."""
        all_status = self._load_all_status()
        return {
            path: EmbeddingStatus.from_dict(data) for path, data in all_status.items()
        }

    def _load_all_status(self) -> dict[str, Any]:
        """Load all status from file."""
        if not self.status_file.exists():
            return {}
        try:
            return json.loads(self.status_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_all_status(self, status: dict[str, Any]) -> None:
        """Save all status to file."""
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        self.status_file.write_text(json.dumps(status, indent=2))

    def remove_status(self, source_path: str) -> None:
        """Remove embedding status for a document."""
        all_status = self._load_all_status()
        if source_path in all_status:
            del all_status[source_path]
            self._save_all_status(all_status)

    def find_documents(
        self, path: Path, extensions: list[str] = None
    ) -> list[Path]:
        """Find all documents in path.

        Args:
            path: Directory to search
            extensions: List of extensions to include (default: all supported)

        Returns:
            List of document paths
        """
        if extensions is None:
            extensions = [".md", ".txt", ".pdf", ".docx", ".html", ".htm"]

        if path.is_file():
            if path.suffix.lower() in extensions:
                return [path]
            return []

        documents = []
        for ext in extensions:
            documents.extend(path.rglob(f"*{ext}"))

        return sorted(documents)
