"""Unit tests for data models."""

import pytest
from datetime import datetime


class TestChunk:
    """Tests for Chunk model."""

    def test_chunk_id(self):
        """Test chunk ID generation."""
        from cortext_rag.models import Chunk

        chunk = Chunk(
            text="test content",
            source_path="/path/to/file.md",
            chunk_index=2,
            total_chunks=5,
        )

        assert chunk.chunk_id == "/path/to/file.md::2"

    def test_chunk_metadata(self):
        """Test chunk with metadata."""
        from cortext_rag.models import Chunk

        chunk = Chunk(
            text="test",
            source_path="file.md",
            chunk_index=0,
            total_chunks=1,
            metadata={"start_word": 0, "end_word": 10},
        )

        assert chunk.metadata["start_word"] == 0
        assert chunk.metadata["end_word"] == 10


class TestDocument:
    """Tests for Document model."""

    def test_document_creation(self, tmp_path):
        """Test document creation."""
        from cortext_rag.models import Document
        from pathlib import Path

        doc = Document(
            path=tmp_path / "test.md",
            content="Test content",
            content_hash="abc123",
            doc_type=".md",
        )

        assert doc.path == tmp_path / "test.md"
        assert doc.content == "Test content"
        assert doc.content_hash == "abc123"
        assert doc.doc_type == ".md"
        assert doc.chunks == []
        assert doc.metadata == {}


class TestEmbeddingStatus:
    """Tests for EmbeddingStatus model."""

    def test_to_dict(self):
        """Test serialization to dictionary."""
        from cortext_rag.models import EmbeddingStatus

        now = datetime.now()
        status = EmbeddingStatus(
            source_path="/test/path.md",
            content_hash="hash123",
            num_chunks=5,
            embedded_at=now,
            model_name="test-model",
            embedding_dim=384,
        )

        data = status.to_dict()

        assert data["source_path"] == "/test/path.md"
        assert data["content_hash"] == "hash123"
        assert data["num_chunks"] == 5
        assert data["embedded_at"] == now.isoformat()
        assert data["model_name"] == "test-model"
        assert data["embedding_dim"] == 384

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        from cortext_rag.models import EmbeddingStatus

        data = {
            "source_path": "/test/path.md",
            "content_hash": "hash123",
            "num_chunks": 5,
            "embedded_at": "2025-11-10T10:30:00",
            "model_name": "test-model",
            "embedding_dim": 384,
        }

        status = EmbeddingStatus.from_dict(data)

        assert status.source_path == "/test/path.md"
        assert status.content_hash == "hash123"
        assert status.num_chunks == 5
        assert status.model_name == "test-model"
        assert status.embedding_dim == 384
        assert isinstance(status.embedded_at, datetime)


class TestSearchResult:
    """Tests for SearchResult model."""

    def test_conversation_name_extraction(self):
        """Test extracting conversation name from path."""
        from cortext_rag.models import Chunk, SearchResult

        chunk = Chunk(
            text="test",
            source_path="brainstorm/2025-11-10/001-auth-patterns/conversation.md",
            chunk_index=0,
            total_chunks=1,
        )

        result = SearchResult(chunk=chunk, score=0.85)

        # Should extract "001-auth-patterns" from path
        assert result.conversation_name == "001-auth-patterns"

    def test_conversation_name_fallback(self):
        """Test fallback when path structure is unexpected."""
        from cortext_rag.models import Chunk, SearchResult

        chunk = Chunk(
            text="test",
            source_path="random/file.md",
            chunk_index=0,
            total_chunks=1,
        )

        result = SearchResult(chunk=chunk, score=0.5)

        # Should fallback to filename stem
        assert result.conversation_name == "file"

    def test_score_preservation(self):
        """Test that score is preserved."""
        from cortext_rag.models import Chunk, SearchResult

        chunk = Chunk(
            text="test",
            source_path="test.md",
            chunk_index=0,
            total_chunks=1,
        )

        result = SearchResult(chunk=chunk, score=0.95)

        assert result.score == 0.95
