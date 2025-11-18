"""Document parsers for different file types."""

from pathlib import Path
from typing import Protocol


class Parser(Protocol):
    """Protocol for document parsers."""

    def parse(self, path: Path) -> tuple[str, dict]:
        """Parse document and return (content, metadata)."""
        ...

    @property
    def supported_extensions(self) -> list[str]:
        """List of supported file extensions."""
        ...


def get_parser(path: Path) -> Parser:
    """Get appropriate parser for file type."""
    ext = path.suffix.lower()

    if ext in [".md", ".markdown"]:
        from .markdown import MarkdownParser
        return MarkdownParser()
    elif ext in [".txt"]:
        from .text import TextParser
        return TextParser()
    elif ext in [".pdf"]:
        from .pdf import PDFParser
        return PDFParser()
    elif ext in [".docx"]:
        from .docx import DOCXParser
        return DOCXParser()
    elif ext in [".html", ".htm"]:
        from .html import HTMLParser
        return HTMLParser()
    else:
        raise ValueError(
            f"Unsupported file type: {ext}. "
            f"Supported: .md, .txt, .pdf, .docx, .html"
        )


__all__ = ["Parser", "get_parser"]
