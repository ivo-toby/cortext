"""Embed command for RAG pipeline."""

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def embed_command(
    path: str = typer.Argument(None, help="Path to file or directory to embed"),
    all_workspace: bool = typer.Option(
        False, "--all", help="Embed entire workspace"
    ),
) -> None:
    """Embed documents for semantic search.

    Embeds conversations and documents into the vector store for semantic search.
    Skips files that haven't changed since last embedding (UPSERT logic).

    Examples:
        cortext embed ./brainstorm/2025-11/
        cortext embed ./docs/research.pdf
        cortext embed --all
    """
    try:
        from cortext_rag import mcp_tools
    except ImportError:
        console.print(
            "[red]RAG dependencies not installed.[/red]\n"
            "Install with: [cyan]pip install cortext-workspace[rag][/cyan]"
        )
        raise typer.Exit(1)

    if not path and not all_workspace:
        console.print(
            "[red]Error:[/red] Specify a path or use --all for workspace-wide embedding"
        )
        raise typer.Exit(1)

    workspace_path = Path.cwd()

    # Check for valid workspace
    if not (workspace_path / ".workspace" / "registry.json").exists():
        console.print(
            "[red]Error:[/red] Not in a Cortext workspace. "
            "Run [cyan]cortext init[/cyan] first."
        )
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if all_workspace:
            progress.add_task("Embedding workspace...", total=None)
            result = mcp_tools.embed_workspace(str(workspace_path))
        else:
            progress.add_task(f"Embedding {path}...", total=None)
            result = mcp_tools.embed_document(path, str(workspace_path))

    if "error" in result:
        console.print(f"[red]Error:[/red] {result['error']}")
        raise typer.Exit(1)

    # Show results
    embedded = result.get("embedded", 0)
    skipped = result.get("skipped", 0)
    total = result.get("total_files", embedded + skipped)

    console.print(f"\n[green]✓[/green] Embedding complete")
    console.print(f"  Files embedded: {embedded}")
    console.print(f"  Files skipped (unchanged): {skipped}")
    console.print(f"  Total files processed: {total}")

    if result.get("errors"):
        console.print(f"\n[yellow]Warnings:[/yellow]")
        for error in result["errors"]:
            console.print(f"  • {error}")
