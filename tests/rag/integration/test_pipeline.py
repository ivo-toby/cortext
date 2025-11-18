"""Integration tests for RAG pipeline."""

import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    not pytest.importorskip("chromadb", reason="chromadb not installed"),
    reason="chromadb not installed",
)
class TestVectorStoreIntegration:
    """Integration tests for ChromaDB vector store."""

    def test_add_and_search_chunks(self, sample_workspace, mock_embedder):
        """Test adding chunks and searching."""
        from cortext_rag.store import VectorStore
        from cortext_rag.models import Chunk

        store = VectorStore(sample_workspace)

        # Create test chunks
        chunks = [
            Chunk(
                text="Authentication using JWT tokens",
                source_path="test1.md",
                chunk_index=0,
                total_chunks=1,
            ),
            Chunk(
                text="Database query optimization",
                source_path="test2.md",
                chunk_index=0,
                total_chunks=1,
            ),
        ]

        # Generate embeddings
        embeddings = mock_embedder.embed([c.text for c in chunks])

        # Add to store
        store.add_chunks(chunks, embeddings, "test1.md")

        # Search
        query_embedding = mock_embedder.embed_single("JWT authentication")
        results = store.search(query_embedding, n_results=2)

        assert len(results) >= 1
        assert results[0].chunk.text in [c.text for c in chunks]

    def test_update_chunks_upsert(self, sample_workspace, mock_embedder):
        """Test UPSERT behavior."""
        from cortext_rag.store import VectorStore
        from cortext_rag.models import Chunk

        store = VectorStore(sample_workspace)

        # Add initial chunk
        chunk1 = Chunk(
            text="Original content",
            source_path="doc.md",
            chunk_index=0,
            total_chunks=1,
        )

        embedding1 = mock_embedder.embed([chunk1.text])
        store.add_chunks([chunk1], embedding1, "doc.md")

        # Update with new content
        chunk2 = Chunk(
            text="Updated content",
            source_path="doc.md",
            chunk_index=0,
            total_chunks=1,
        )

        embedding2 = mock_embedder.embed([chunk2.text])
        store.update_chunks([chunk2], embedding2, "doc.md")

        # Verify old content is gone
        stats = store.get_stats()
        assert stats["total_chunks"] == 1

        # Verify new content is searchable
        query_emb = mock_embedder.embed_single("Updated")
        results = store.search(query_emb)
        assert any("Updated" in r.chunk.text for r in results)

    def test_delete_by_source(self, sample_workspace, mock_embedder):
        """Test deleting chunks by source."""
        from cortext_rag.store import VectorStore
        from cortext_rag.models import Chunk

        store = VectorStore(sample_workspace)

        # Add chunks from two sources
        chunk1 = Chunk(
            text="Source A content", source_path="a.md", chunk_index=0, total_chunks=1
        )
        chunk2 = Chunk(
            text="Source B content", source_path="b.md", chunk_index=0, total_chunks=1
        )

        embeddings = mock_embedder.embed([chunk1.text, chunk2.text])
        store.add_chunks([chunk1], [embeddings[0]], "a.md")
        store.add_chunks([chunk2], [embeddings[1]], "b.md")

        # Delete source A
        store.delete_by_source("a.md")

        # Only source B should remain
        stats = store.get_stats()
        assert stats["total_chunks"] == 1

    def test_get_stats(self, sample_workspace, mock_embedder):
        """Test getting store statistics."""
        from cortext_rag.store import VectorStore
        from cortext_rag.models import Chunk

        store = VectorStore(sample_workspace)

        # Add some chunks
        chunks = [
            Chunk(text=f"Content {i}", source_path=f"doc{i}.md", chunk_index=0, total_chunks=1)
            for i in range(3)
        ]
        embeddings = mock_embedder.embed([c.text for c in chunks])

        for i, chunk in enumerate(chunks):
            store.add_chunks([chunk], [embeddings[i]], chunk.source_path)

        stats = store.get_stats()

        assert stats["total_chunks"] == 3
        assert stats["num_documents"] == 3
        assert "chroma" in stats["db_path"]


@pytest.mark.integration
@pytest.mark.skipif(
    not pytest.importorskip("chromadb", reason="chromadb not installed"),
    reason="chromadb not installed",
)
class TestFullPipeline:
    """Integration tests for full embedding pipeline."""

    def test_embed_workspace(self, sample_workspace, monkeypatch):
        """Test embedding entire workspace."""
        from cortext_rag import mcp_tools

        # Use mock embedder by monkeypatching
        from tests.rag.conftest import mock_embedder as _mock_embedder

        result = mcp_tools.embed_workspace(str(sample_workspace))

        assert result["success"] is True
        # Should embed all sample conversations (3 conversations)
        assert result["embedded"] >= 3

    def test_incremental_embedding(self, sample_workspace, monkeypatch):
        """Test that unchanged files are skipped."""
        from cortext_rag import mcp_tools

        # First embedding
        result1 = mcp_tools.embed_workspace(str(sample_workspace))
        first_embedded = result1["embedded"]

        # Second embedding should skip all
        result2 = mcp_tools.embed_workspace(str(sample_workspace))

        assert result2["embedded"] == 0
        assert result2["skipped"] >= first_embedded

    def test_semantic_search(self, sample_workspace, monkeypatch):
        """Test semantic search after embedding."""
        from cortext_rag import mcp_tools

        # Embed workspace
        mcp_tools.embed_workspace(str(sample_workspace))

        # Search for authentication topics
        result = mcp_tools.search_semantic("authentication tokens", str(sample_workspace))

        assert result["success"] is True
        assert result["num_results"] > 0
        # Should find auth-related content
        assert any("auth" in str(r).lower() for r in result["results"])

    def test_search_with_type_filter(self, sample_workspace, monkeypatch):
        """Test filtering search by conversation type."""
        from cortext_rag import mcp_tools

        # Embed workspace
        mcp_tools.embed_workspace(str(sample_workspace))

        # Search only in brainstorm conversations
        result = mcp_tools.search_semantic(
            "patterns", str(sample_workspace), conversation_type="brainstorm"
        )

        assert result["success"] is True
        # Results should only be from brainstorm folder
        for r in result["results"]:
            assert "brainstorm" in r["source_path"]

    def test_get_embedding_status(self, sample_workspace, monkeypatch):
        """Test getting embedding status."""
        from cortext_rag import mcp_tools

        # Embed workspace
        mcp_tools.embed_workspace(str(sample_workspace))

        # Get status
        result = mcp_tools.get_embedding_status(str(sample_workspace))

        assert result["success"] is True
        assert result["total_chunks"] > 0
        assert result["num_documents"] >= 3
        assert len(result["recent_embeddings"]) > 0

    def test_get_similar(self, sample_workspace, monkeypatch):
        """Test finding similar documents."""
        from cortext_rag import mcp_tools

        # Embed workspace
        mcp_tools.embed_workspace(str(sample_workspace))

        # Get similar to auth-patterns conversation
        source_path = str(
            sample_workspace
            / "brainstorm"
            / "2025-11-10"
            / "001-auth-patterns"
            / "conversation.md"
        )

        result = mcp_tools.get_similar(source_path, str(sample_workspace))

        assert result["success"] is True
        # Should find other conversations
        assert result["num_results"] > 0
        # Should not include source itself
        for similar in result["similar"]:
            assert similar["source_path"] != source_path
