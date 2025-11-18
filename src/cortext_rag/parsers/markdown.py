"""Markdown document parser."""

import re
from pathlib import Path
from typing import Any


class MarkdownParser:
    """Parse markdown files, extracting frontmatter and content."""

    @property
    def supported_extensions(self) -> list[str]:
        """Supported file extensions."""
        return [".md", ".markdown"]

    def parse(self, path: Path) -> tuple[str, dict[str, Any]]:
        """Parse markdown file.

        Args:
            path: Path to markdown file

        Returns:
            Tuple of (content, metadata)
        """
        text = path.read_text(encoding="utf-8")
        metadata = {}

        # Extract YAML frontmatter if present
        if text.startswith("---"):
            # Find closing ---
            end_match = re.search(r"\n---\n", text[3:])
            if end_match:
                frontmatter_text = text[3 : end_match.start() + 3]
                content = text[end_match.end() + 3 :].strip()

                # Parse simple YAML frontmatter (key: value pairs)
                metadata = self._parse_frontmatter(frontmatter_text)
            else:
                content = text
        else:
            content = text

        # Clean up markdown for embedding
        # Remove excessive blank lines
        content = re.sub(r"\n{3,}", "\n\n", content)

        return content.strip(), metadata

    def _parse_frontmatter(self, text: str) -> dict[str, Any]:
        """Parse simple YAML frontmatter."""
        metadata = {}
        for line in text.strip().split("\n"):
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                metadata[key] = value
        return metadata
