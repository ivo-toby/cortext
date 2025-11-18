"""PDF document parser."""

from pathlib import Path
from typing import Any


class PDFParser:
    """Parse PDF files using pypdf."""

    @property
    def supported_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".pdf"]

    def parse(self, path: Path) -> tuple[str, dict[str, Any]]:
        """Parse PDF file.

        Args:
            path: Path to PDF file

        Returns:
            Tuple of (content, metadata)
        """
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError(
                "pypdf not installed. Install with: pip install cortext-workspace[rag]"
            )

        reader = PdfReader(path)

        # Extract text from all pages
        pages_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                pages_text.append(f"[Page {i + 1}]\n{page_text}")

        content = "\n\n".join(pages_text)

        # Extract metadata
        metadata = {
            "num_pages": len(reader.pages),
            "file_name": path.name,
        }

        # Add PDF metadata if available
        if reader.metadata:
            if reader.metadata.title:
                metadata["title"] = reader.metadata.title
            if reader.metadata.author:
                metadata["author"] = reader.metadata.author

        return content.strip(), metadata
