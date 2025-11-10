"""List command to show available conversation types."""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def list_types():
    """List all available conversation types in the workspace."""
    # Find workspace root
    workspace_root = Path.cwd()
    registry_path = workspace_root / ".workspace" / "registry.json"

    if not registry_path.exists():
        console.print(
            "[yellow]⚠ Not in a Cortext workspace or registry not found[/yellow]\n"
            "[dim]Run 'cortext init' to create a workspace[/dim]"
        )
        raise typer.Exit(code=1)

    # Load registry
    registry = json.loads(registry_path.read_text())
    conversation_types = registry.get("conversation_types", {})

    if not conversation_types:
        console.print("[yellow]No conversation types found[/yellow]")
        return

    # Separate built-in and custom types
    built_in = {k: v for k, v in conversation_types.items() if v.get("built_in", False)}
    custom = {k: v for k, v in conversation_types.items() if not v.get("built_in", False)}

    console.print("\n[bold cyan]🧠 Cortext - Available Conversation Types[/bold cyan]\n")

    # Built-in types
    if built_in:
        console.print("[bold]Built-in Types:[/bold]")
        table = Table(show_header=True, header_style="bold cyan", show_lines=False)
        table.add_column("Command", style="green")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="dim")

        for type_id, info in sorted(built_in.items()):
            table.add_row(info["command"], info["name"], info["description"])

        console.print(table)

    # Custom types
    if custom:
        console.print("\n[bold]Custom Types:[/bold]")
        table = Table(show_header=True, header_style="bold cyan", show_lines=False)
        table.add_column("Command", style="green")
        table.add_column("Name", style="cyan")
        table.add_column("Created", style="dim")
        table.add_column("Description", style="dim")

        for type_id, info in sorted(custom.items()):
            created = info.get("created", "Unknown")[:10]  # Just date
            table.add_row(info["command"], info["name"], created, info["description"])

        console.print(table)

    # Statistics
    stats = registry.get("statistics", {})
    total = stats.get("total_conversations", 0)
    if total > 0:
        console.print(f"\n[dim]Total conversations: {total}[/dim]")

    console.print("\n[dim]Use '/workspace.add' to create custom conversation types[/dim]\n")
