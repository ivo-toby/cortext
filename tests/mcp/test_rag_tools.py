"""Tests for MCP server RAG tool handlers."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cortext_mcp.server import CortextMCPServer


class TestMCPRAGTools:
    """Test RAG tools integration in MCP server."""

    @pytest.fixture
    def server(self, tmp_path):
        """Create test MCP server instance."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()

        # Create basic workspace structure
        workspace_dir = workspace / ".workspace"
        workspace_dir.mkdir()

        registry = {
            "version": "1.0",
            "conversation_types": {
                "brainstorm": {"folder": "brainstorm"},
            },
        }
        (workspace_dir / "registry.json").write_text(json.dumps(registry))

        return CortextMCPServer(workspace)

    def test_list_tools_includes_rag_tools(self, server):
        """Test that RAG tools are included in tool list."""
        result = server.list_tools()

        assert "tools" in result
        tool_names = [tool["name"] for tool in result["tools"]]

        # Check all RAG tools are present
        assert "embed_document" in tool_names
        assert "embed_workspace" in tool_names
        assert "search_semantic" in tool_names
        assert "get_similar" in tool_names
        assert "get_embedding_status" in tool_names

    def test_embed_document_tool_schema(self, server):
        """Test embed_document tool has correct schema."""
        result = server.list_tools()

        embed_doc_tool = next(
            (t for t in result["tools"] if t["name"] == "embed_document"), None
        )

        assert embed_doc_tool is not None
        assert "inputSchema" in embed_doc_tool
        assert embed_doc_tool["inputSchema"]["type"] == "object"
        assert "path" in embed_doc_tool["inputSchema"]["properties"]
        assert "path" in embed_doc_tool["inputSchema"]["required"]

    def test_search_semantic_tool_schema(self, server):
        """Test search_semantic tool has correct schema."""
        result = server.list_tools()

        search_tool = next(
            (t for t in result["tools"] if t["name"] == "search_semantic"), None
        )

        assert search_tool is not None
        schema = search_tool["inputSchema"]

        assert "query" in schema["properties"]
        assert "n_results" in schema["properties"]
        assert "conversation_type" in schema["properties"]
        assert "date_range" in schema["properties"]
        assert "query" in schema["required"]

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_embed_document(self, mock_mcp_tools, server):
        """Test calling embed_document tool."""
        mock_mcp_tools.embed_document.return_value = {
            "success": True,
            "embedded": 1,
            "skipped": 0,
            "total_files": 1,
        }

        result = server.call_tool("embed_document", {"path": "test.md"})

        assert "content" in result
        assert len(result["content"]) > 0
        mock_mcp_tools.embed_document.assert_called_once_with(path="test.md")

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_search_semantic(self, mock_mcp_tools, server):
        """Test calling search_semantic tool."""
        mock_mcp_tools.search_semantic.return_value = {
            "success": True,
            "query": "test query",
            "num_results": 2,
            "results": [
                {
                    "conversation": "001-test",
                    "score": 0.9,
                    "text": "test content",
                    "source_path": "brainstorm/001-test/conversation.md",
                }
            ],
        }

        result = server.call_tool(
            "search_semantic",
            {"query": "test query", "n_results": 10},
        )

        assert "content" in result
        mock_mcp_tools.search_semantic.assert_called_once()

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_rag_tool_handles_errors(self, mock_mcp_tools, server):
        """Test RAG tool error handling."""
        mock_mcp_tools.embed_document.return_value = {
            "error": "Document not found"
        }

        result = server.call_tool("embed_document", {"path": "nonexistent.md"})

        assert "content" in result
        assert "Error:" in result["content"][0]["text"]

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_rag_tool_exception_handling(self, mock_mcp_tools, server):
        """Test RAG tool exception handling."""
        mock_mcp_tools.search_semantic.side_effect = Exception("Test error")

        result = server.call_tool("search_semantic", {"query": "test"})

        assert "content" in result
        assert "Error calling RAG tool" in result["content"][0]["text"]

    @patch("cortext_mcp.server.RAG_AVAILABLE", False)
    def test_rag_tools_not_available(self, server):
        """Test behavior when RAG is not available."""
        result = server.list_tools()

        tool_names = [tool["name"] for tool in result["tools"]]

        # RAG tools should not be present
        assert "embed_document" not in tool_names
        assert "search_semantic" not in tool_names

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_get_embedding_status(self, mock_mcp_tools, server):
        """Test calling get_embedding_status tool."""
        mock_mcp_tools.get_embedding_status.return_value = {
            "success": True,
            "total_chunks": 100,
            "num_documents": 10,
            "db_path": "/path/to/db",
            "recent_embeddings": [],
        }

        result = server.call_tool("get_embedding_status", {})

        assert "content" in result
        mock_mcp_tools.get_embedding_status.assert_called_once()

    @patch("cortext_mcp.server.RAG_AVAILABLE", True)
    @patch("cortext_mcp.server.mcp_tools")
    def test_call_get_similar(self, mock_mcp_tools, server):
        """Test calling get_similar tool."""
        mock_mcp_tools.get_similar.return_value = {
            "success": True,
            "source": "test.md",
            "num_results": 3,
            "similar": [],
        }

        result = server.call_tool(
            "get_similar",
            {"source_path": "test.md", "n_results": 5},
        )

        assert "content" in result
        mock_mcp_tools.get_similar.assert_called_once()
