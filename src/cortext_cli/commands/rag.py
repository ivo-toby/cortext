"""RAG status and management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer(help="RAG pipeline management commands")


@app.command("status")
def rag_status() -> None:
    """Show RAG embedding statistics.

    Displays information about embedded documents, chunks, and storage.

    Example:
        cortext rag status
    """
    try:
        from cortext_rag import mcp_tools
    except ImportError:
        console.print(
            "[red]RAG dependencies not installed.[/red]\n"
            "Install with: [cyan]pip install cortext-workspace[rag][/cyan]"
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

    result = mcp_tools.get_embedding_status(str(workspace_path))

    if "error" in result:
        console.print(f"[red]Error:[/red] {result['error']}")
        raise typer.Exit(1)

    # Display statistics
    console.print("\n[bold]RAG Embedding Status[/bold]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    table.add_row("Total Documents", str(result["num_documents"]))
    table.add_row("Total Chunks", str(result["total_chunks"]))
    table.add_row("Database Path", result["db_path"])

    console.print(table)

    # Show recent embeddings
    if result.get("recent_embeddings"):
        console.print("\n[bold]Recent Embeddings[/bold]\n")

        recent_table = Table()
        recent_table.add_column("Path", style="cyan")
        recent_table.add_column("Chunks", justify="right")
        recent_table.add_column("Embedded At")

        for item in result["recent_embeddings"]:
            # Shorten path for display
            path = item["path"]
            if len(path) > 60:
                path = "..." + path[-57:]

            recent_table.add_row(
                path, str(item["chunks"]), item["embedded_at"][:19]
            )

        console.print(recent_table)
    else:
        console.print("\n[yellow]No embeddings found.[/yellow]")
        console.print("Run [cyan]cortext embed --all[/cyan] to embed workspace.")
