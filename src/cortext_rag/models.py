"""Data models for RAG pipeline."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Chunk:
    """A chunk of text with metadata."""

    text: str
    source_path: str
    chunk_index: int
    total_chunks: int
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def chunk_id(self) -> str:
        """Generate unique ID for this chunk."""
        return f"{self.source_path}::{self.chunk_index}"


@dataclass
class Document:
    """A document with parsed content and metadata."""

    path: Path
    content: str
    content_hash: str
    doc_type: str
    metadata: dict[str, Any] = field(default_factory=dict)
    chunks: list[Chunk] = field(default_factory=list)


@dataclass
class EmbeddingStatus:
    """Status of embedded content."""

    source_path: str
    content_hash: str
    num_chunks: int
    embedded_at: datetime
    model_name: str
    embedding_dim: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "source_path": self.source_path,
            "content_hash": self.content_hash,
            "num_chunks": self.num_chunks,
            "embedded_at": self.embedded_at.isoformat(),
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EmbeddingStatus":
        """Create from dictionary."""
        return cls(
            source_path=data["source_path"],
            content_hash=data["content_hash"],
            num_chunks=data["num_chunks"],
            embedded_at=datetime.fromisoformat(data["embedded_at"]),
            model_name=data["model_name"],
            embedding_dim=data["embedding_dim"],
        )


@dataclass
class SearchResult:
    """A search result with relevance score."""

    chunk: Chunk
    score: float
    embedding: list[float] | None = None

    @property
    def conversation_name(self) -> str:
        """Extract conversation name from source path."""
        parts = Path(self.chunk.source_path).parts
        # Look for pattern: {type}/YYYY-MM-DD/###-name/
        for i, part in enumerate(parts):
            if len(part) >= 10 and part[4] == "-" and part[7] == "-":
                # Found date directory, next part is conversation name
                if i + 1 < len(parts):
                    return parts[i + 1]
        return Path(self.chunk.source_path).stem
