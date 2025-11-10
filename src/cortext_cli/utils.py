"""Utility functions and classes for Cortext."""

import sys
from pathlib import Path

from rich.console import Console
from rich.tree import Tree

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
