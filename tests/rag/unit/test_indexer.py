"""Unit tests for indexer."""

import pytest
from pathlib import Path


class TestIndexer:
    """Tests for indexer functionality."""

    def test_chunk_content(self, sample_workspace):
        """Test content chunking."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        # Create long content
        words = ["word"] * 1000
        content = " ".join(words)

        chunks = indexer._chunk_content(content, "test.md")

        # Should have multiple chunks
        assert len(chunks) > 1

        # Each chunk should have correct metadata
        for i, chunk in enumerate(chunks):
            assert chunk.source_path == "test.md"
            assert chunk.chunk_index == i
            assert chunk.total_chunks == len(chunks)
            assert len(chunk.text.split()) > 0

    def test_chunk_short_content(self, sample_workspace):
        """Test chunking short content."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)
        content = "This is a short piece of content."

        chunks = indexer._chunk_content(content, "short.md")

        # Should have single chunk
        assert len(chunks) == 1
        assert chunks[0].text == content

    def test_compute_hash(self, sample_workspace):
        """Test content hashing."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        # Same content should produce same hash
        hash1 = indexer._compute_hash("test content")
        hash2 = indexer._compute_hash("test content")
        assert hash1 == hash2

        # Different content should produce different hash
        hash3 = indexer._compute_hash("different content")
        assert hash1 != hash3

    def test_parse_document(self, sample_workspace):
        """Test parsing a document."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        # Parse one of the sample conversations
        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        assert doc.path == conv_file
        assert "Authentication Patterns" in doc.content
        assert doc.content_hash
        assert doc.doc_type == ".md"
        assert len(doc.chunks) > 0

    def test_needs_embedding_new_file(self, sample_workspace):
        """Test detecting new file needs embedding."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        # New file should need embedding
        assert indexer.needs_embedding(doc) is True

    def test_needs_embedding_unchanged_file(self, sample_workspace):
        """Test detecting unchanged file doesn't need embedding."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        # Simulate that file was embedded
        indexer.update_status(doc, "test-model", 384)

        # Unchanged file should not need embedding
        assert indexer.needs_embedding(doc) is False

    def test_needs_embedding_modified_file(self, sample_workspace):
        """Test detecting modified file needs embedding."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        # Simulate that file was embedded
        indexer.update_status(doc, "test-model", 384)

        # Modify the file
        conv_file.write_text("# Modified content\n\nNew stuff here.")

        # Re-parse
        doc2 = indexer.parse_document(conv_file)

        # Modified file should need embedding
        assert indexer.needs_embedding(doc2) is True

    def test_find_documents(self, sample_workspace):
        """Test finding documents in workspace."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        docs = indexer.find_documents(sample_workspace / "brainstorm")

        # Should find the conversation.md file
        assert len(docs) > 0
        assert any("conversation.md" in str(d) for d in docs)

    def test_status_tracking(self, sample_workspace):
        """Test embedding status tracking."""
        from cortext_rag.indexer import Indexer
        from datetime import datetime

        indexer = Indexer(sample_workspace)

        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        # Update status
        indexer.update_status(doc, "test-model", 384)

        # Get status back
        status = indexer.get_status(str(conv_file))

        assert status is not None
        assert status.source_path == str(conv_file)
        assert status.content_hash == doc.content_hash
        assert status.num_chunks == len(doc.chunks)
        assert status.model_name == "test-model"
        assert status.embedding_dim == 384
        assert isinstance(status.embedded_at, datetime)

    def test_remove_status(self, sample_workspace):
        """Test removing embedding status."""
        from cortext_rag.indexer import Indexer

        indexer = Indexer(sample_workspace)

        conv_file = (
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        doc = indexer.parse_document(conv_file)

        # Update status
        indexer.update_status(doc, "test-model", 384)
        assert indexer.get_status(str(conv_file)) is not None

        # Remove status
        indexer.remove_status(str(conv_file))
        assert indexer.get_status(str(conv_file)) is None
