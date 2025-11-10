"""Check command to verify required tools are installed."""

import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def check():
    """Check if required tools are installed."""
    console.print("\n[bold cyan]🧠 Cortext - System Check[/bold cyan]\n")

    # Tools to check
    tools = {
        "git": {
            "name": "Git",
            "required": True,
            "check_cmd": ["git", "--version"],
            "install": "https://git-scm.com/downloads",
        },
        "ollama": {
            "name": "Ollama",
            "required": False,
            "check_cmd": ["ollama", "--version"],
            "install": "https://ollama.ai",
            "note": "Required for RAG features (Phase 4)",
        },
        "tmux": {
            "name": "Tmux",
            "required": False,
            "check_cmd": ["tmux", "-V"],
            "install": "https://github.com/tmux/tmux/wiki/Installing",
            "note": "Recommended for workspace session management",
        },
        "rg": {
            "name": "ripgrep",
            "required": False,
            "check_cmd": ["rg", "--version"],
            "install": "https://github.com/BurntSushi/ripgrep",
            "note": "Required for fast search (Phase 2)",
        },
    }

    # Check Python version
    import sys

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    console.print(f"[green]✓[/green] Python {python_version} (requires >=3.11)")

    # Create results table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Version", style="dim")
    table.add_column("Notes", style="dim")

    all_required_ok = True

    for tool_id, tool_info in tools.items():
        # Check if tool is installed
        if shutil.which(tool_id):
            try:
                result = subprocess.run(
                    tool_info["check_cmd"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                version = result.stdout.strip().split("\n")[0]
                status = "[green]✓ Installed[/green]"
                table.add_row(
                    tool_info["name"],
                    status,
                    version,
                    tool_info.get("note", ""),
                )
            except Exception:
                status = "[yellow]⚠ Found but version check failed[/yellow]"
                table.add_row(
                    tool_info["name"], status, "Unknown", tool_info.get("note", "")
                )
        else:
            if tool_info["required"]:
                status = "[red]✗ Not installed (required)[/red]"
                all_required_ok = False
            else:
                status = "[yellow]⚠ Not installed (optional)[/yellow]"

            table.add_row(
                tool_info["name"],
                status,
                f"Install: {tool_info['install']}",
                tool_info.get("note", ""),
            )

    console.print(table)

    # Final message
    if all_required_ok:
        console.print(
            "\n[green]✓ All required tools are installed![/green]\n"
            "[dim]You're ready to run: cortext init[/dim]\n"
        )
    else:
        console.print(
            "\n[red]✗ Some required tools are missing.[/red]\n"
            "[dim]Please install them before continuing.[/dim]\n"
        )
        raise typer.Exit(code=1)
