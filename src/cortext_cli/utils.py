"""Utility functions and classes for Cortext."""

import hashlib
import sys
from enum import Enum
from pathlib import Path

from rich.console import Console
from rich.tree import Tree


class FileStatus(Enum):
    """Status of a file during upgrade comparison."""
    UNMODIFIED = "unmodified"
    MODIFIED = "modified"
    DELETED = "deleted"
    UNKNOWN = "unknown"


class VersionStatus(Enum):
    """Status of workspace version relative to installed Cortext."""
    LEGACY = "legacy"
    UPGRADE_AVAILABLE = "upgrade_available"
    CURRENT = "current"
    NEWER_WORKSPACE = "newer_workspace"


def compute_sha256(content: str) -> str:
    """Compute SHA-256 hash of string content.

    Args:
        content: String content to hash

    Returns:
        Hash string in format "sha256:{hex_digest}"
    """
    hash_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"sha256:{hash_digest}"


def compute_file_hash(path: Path) -> str:
    """Compute SHA-256 hash of file content.

    Args:
        path: Path to file to hash

    Returns:
        Hash string in format "sha256:{hex_digest}"

    Raises:
        FileNotFoundError: If file does not exist
    """
    content = path.read_text(encoding="utf-8")
    return compute_sha256(content)


def get_file_status(path: Path, original_hash: str | None) -> FileStatus:
    """Determine the modification status of a file.

    Args:
        path: Path to the file to check
        original_hash: The original hash stored during generation, or None

    Returns:
        FileStatus indicating whether file is unmodified, modified, deleted, or unknown
    """
    if original_hash is None:
        return FileStatus.UNKNOWN

    if not path.exists():
        return FileStatus.DELETED

    try:
        current_hash = compute_file_hash(path)
        if current_hash == original_hash:
            return FileStatus.UNMODIFIED
        else:
            return FileStatus.MODIFIED
    except Exception:
        return FileStatus.UNKNOWN

console = Console()


class StepTracker:
    """Track and display progress for multi-step operations."""

    def __init__(self, title: str = "Cortext"):
        self.console = Console()
        self.tree = Tree(f"🧠 {title}")

    def add_step(self, message: str, status: str = "✓"):
        """Add a completed step."""
        self.tree.add(f"[green]{status}[/green] {message}")

    def add_error(self, message: str):
        """Add an error step."""
        self.tree.add(f"[red]✗[/red] {message}")

    def add_warning(self, message: str):
        """Add a warning step."""
        self.tree.add(f"[yellow]⚠[/yellow] {message}")

    def add_info(self, message: str):
        """Add an info step."""
        self.tree.add(f"[cyan]ℹ[/cyan] {message}")

    def display(self):
        """Display the tree."""
        self.console.print(self.tree)


# AI Agent Configuration
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "commands_dir": ".claude/commands",
        "cli_check": "claude",
        "requires_cli": False,
        "install_url": None,
    },
    "opencode": {
        "name": "OpenCode",
        "commands_dir": ".opencode/command",
        "cli_check": "opencode",
        "requires_cli": True,
        "install_url": "https://opencode.ai",
    },
    "gemini": {
        "name": "Gemini CLI",
        "commands_dir": ".gemini/commands",
        "cli_check": "gemini",
        "requires_cli": True,
        "install_url": "https://ai.google.dev/gemini-api/docs/cli",
    },
}


def get_template_dir() -> Path:
    """Get the templates directory from the package."""
    # Try system location first (installed package)
    sys_templates = Path(sys.prefix) / "share" / "cortext" / "templates"
    if sys_templates.exists():
        return sys_templates

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_templates = current_file.parent.parent.parent / "templates"
    if dev_templates.exists():
        return dev_templates

    # Fallback to package directory
    return dev_templates


def get_scripts_dir() -> Path:
    """Get the scripts directory from the package."""
    # Try system location first (installed package)
    sys_scripts = Path(sys.prefix) / "share" / "cortext" / "scripts"
    if sys_scripts.exists():
        return sys_scripts

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_scripts = current_file.parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    return dev_scripts


def get_commands_dir() -> Path:
    """Get the claude_commands directory from the package."""
    # Try system location first (installed package)
    sys_commands = Path(sys.prefix) / "share" / "cortext" / "claude_commands"
    if sys_commands.exists():
        return sys_commands

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_commands = current_file.parent.parent.parent / "claude_commands"
    if dev_commands.exists():
        return dev_commands

    return dev_commands


def get_git_hooks_dir() -> Path:
    """Get the git-hooks directory from the package."""
    # Try system location first (installed package)
    sys_hooks = Path(sys.prefix) / "share" / "cortext" / "scripts" / "git-hooks"
    if sys_hooks.exists():
        return sys_hooks

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_hooks = current_file.parent.parent.parent / "scripts" / "git-hooks"
    if dev_hooks.exists():
        return dev_hooks

    return dev_hooks


def get_hooks_dir() -> Path:
    """Get the hooks directory from the package (for copying to .workspace/hooks)."""
    # Try system location first (installed package)
    sys_hooks = Path(sys.prefix) / "share" / "cortext" / "scripts" / "hooks"
    if sys_hooks.exists():
        return sys_hooks

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_hooks = current_file.parent.parent.parent / "scripts" / "hooks"
    if dev_hooks.exists():
        return dev_hooks

    return dev_hooks
