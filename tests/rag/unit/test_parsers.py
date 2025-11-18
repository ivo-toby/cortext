"""Unit tests for document parsers."""

import pytest
from pathlib import Path


class TestMarkdownParser:
    """Tests for markdown parser."""

    def test_parse_with_frontmatter(self, sample_markdown_file):
        """Test parsing markdown with YAML frontmatter."""
        from cortext_rag.parsers.markdown import MarkdownParser

        parser = MarkdownParser()
        content, metadata = parser.parse(sample_markdown_file)

        assert "Sample Document" in content
        assert "Section 1" in content
        assert metadata.get("title") == "Sample Document"
        assert metadata.get("author") == "Test User"
        assert metadata.get("date") == "2025-11-10"
        # Frontmatter should be removed from content
        assert "---" not in content

    def test_parse_without_frontmatter(self, tmp_path):
        """Test parsing markdown without frontmatter."""
        from cortext_rag.parsers.markdown import MarkdownParser

        md_file = tmp_path / "no_frontmatter.md"
        md_file.write_text("# Just a heading\n\nSome content here.")

        parser = MarkdownParser()
        content, metadata = parser.parse(md_file)

        assert "Just a heading" in content
        assert "Some content here" in content
        assert metadata == {}

    def test_supported_extensions(self):
        """Test supported file extensions."""
        from cortext_rag.parsers.markdown import MarkdownParser

        parser = MarkdownParser()
        assert ".md" in parser.supported_extensions
        assert ".markdown" in parser.supported_extensions


class TestTextParser:
    """Tests for text parser."""

    def test_parse_text_file(self, sample_text_file):
        """Test parsing plain text file."""
        from cortext_rag.parsers.text import TextParser

        parser = TextParser()
        content, metadata = parser.parse(sample_text_file)

        assert "plain text file" in content
        assert "multiple lines" in content
        assert metadata.get("file_name") == "sample.txt"
        assert metadata.get("file_size") > 0

    def test_supported_extensions(self):
        """Test supported file extensions."""
        from cortext_rag.parsers.text import TextParser

        parser = TextParser()
        assert ".txt" in parser.supported_extensions


class TestHTMLParser:
    """Tests for HTML parser."""

    @pytest.mark.skipif(
        not pytest.importorskip("bs4", reason="beautifulsoup4 not installed"),
        reason="beautifulsoup4 not installed",
    )
    def test_parse_html_file(self, sample_html_file):
        """Test parsing HTML file."""
        from cortext_rag.parsers.html import HTMLParser

        parser = HTMLParser()
        content, metadata = parser.parse(sample_html_file)

        assert "Main Heading" in content
        assert "This is a paragraph" in content
        assert "Nested content" in content
        # Tags should be stripped
        assert "<h1>" not in content
        assert "<p>" not in content
        assert metadata.get("title") == "Sample Page"

    def test_supported_extensions(self):
        """Test supported file extensions."""
        from cortext_rag.parsers.html import HTMLParser

        parser = HTMLParser()
        assert ".html" in parser.supported_extensions
        assert ".htm" in parser.supported_extensions


class TestParserFactory:
    """Tests for parser factory."""

    def test_get_markdown_parser(self, tmp_path):
        """Test getting parser for markdown files."""
        from cortext_rag.parsers import get_parser
        from cortext_rag.parsers.markdown import MarkdownParser

        md_file = tmp_path / "test.md"
        parser = get_parser(md_file)
        assert isinstance(parser, MarkdownParser)

    def test_get_text_parser(self, tmp_path):
        """Test getting parser for text files."""
        from cortext_rag.parsers import get_parser
        from cortext_rag.parsers.text import TextParser

        txt_file = tmp_path / "test.txt"
        parser = get_parser(txt_file)
        assert isinstance(parser, TextParser)

    def test_unsupported_extension(self, tmp_path):
        """Test error for unsupported file type."""
        from cortext_rag.parsers import get_parser

        unknown_file = tmp_path / "test.xyz"
        with pytest.raises(ValueError, match="Unsupported file type"):
            get_parser(unknown_file)
