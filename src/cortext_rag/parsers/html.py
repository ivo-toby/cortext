"""HTML document parser."""

from pathlib import Path
from typing import Any


class HTMLParser:
    """Parse HTML files, stripping tags."""

    @property
    def supported_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".html", ".htm"]

    def parse(self, path: Path) -> tuple[str, dict[str, Any]]:
        """Parse HTML file.

        Args:
            path: Path to HTML file

        Returns:
            Tuple of (content, metadata)
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError(
                "beautifulsoup4 not installed. "
                "Install with: pip install cortext-workspace[rag]"
            )

        html_content = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html_content, "lxml")

        # Extract title if present
        title = ""
        if soup.title:
            title = soup.title.string or ""

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator="\n")

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        metadata = {
            "title": title.strip() if title else path.stem,
            "file_name": path.name,
        }

        return content.strip(), metadata
