"""Plain text document parser."""

from pathlib import Path
from typing import Any


class TextParser:
    """Parse plain text files."""

    @property
    def supported_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".txt"]

    def parse(self, path: Path) -> tuple[str, dict[str, Any]]:
        """Parse text file.

        Args:
            path: Path to text file

        Returns:
            Tuple of (content, metadata)
        """
        content = path.read_text(encoding="utf-8")
        metadata = {
            "file_name": path.name,
            "file_size": path.stat().st_size,
        }
        return content.strip(), metadata
