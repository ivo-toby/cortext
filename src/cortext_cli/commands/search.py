"""Search command with semantic search support."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

console = Console()


def search_command(
    query: str = typer.Argument(..., help="Search query"),
    semantic: bool = typer.Option(
        False, "--semantic", "-s", help="Use semantic search (requires RAG)"
    ),
    conversation_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Filter by conversation type"
    ),
    date_range: Optional[str] = typer.Option(
        None, "--date", "-d", help="Filter by date (YYYY-MM or YYYY-MM-DD)"
    ),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results"),
) -> None:
    """Search workspace conversations.

    By default uses keyword search (ripgrep). Use --semantic for meaning-based search.

    Examples:
        cortext search "authentication"
        cortext search "login security" --semantic
        cortext search "api design" --semantic --type plan
        cortext search "refactoring" --semantic --date 2025-11
    """
    workspace_path = Path.cwd()

    # Check for valid workspace
    if not (workspace_path / ".workspace" / "registry.json").exists():
        console.print(
            "[red]Error:[/red] Not in a Cortext workspace. "
            "Run [cyan]cortext init[/cyan] first."
        )
        raise typer.Exit(1)

    if semantic:
        _semantic_search(
            query, workspace_path, conversation_type, date_range, limit
        )
    else:
        _keyword_search(query, workspace_path, conversation_type, limit)


def _semantic_search(
    query: str,
    workspace_path: Path,
    conversation_type: Optional[str],
    date_range: Optional[str],
    limit: int,
) -> None:
    """Perform semantic search using RAG pipeline."""
    from cortext_rag import mcp_tools

    result = mcp_tools.search_semantic(
        query=query,
        workspace_path=str(workspace_path),
        n_results=limit,
        conversation_type=conversation_type,
        date_range=date_range,
    )

    if "error" in result:
        console.print(f"[red]Error:[/red] {result['error']}")
        raise typer.Exit(1)

    # Display results
    console.print(f"\n[bold]Semantic Search:[/bold] {query}\n")

    if not result["results"]:
        console.print("[yellow]No results found.[/yellow]")
        console.print(
            "Try different query terms or ensure workspace is embedded "
            "([cyan]cortext embed --all[/cyan])"
        )
        return

    for i, item in enumerate(result["results"], 1):
        score_pct = int(item["score"] * 100)
        text = item["text"]
        if len(text) > 200:
            text = text[:197] + "..."

        console.print(f"[cyan]{i}.[/cyan] [bold]{item['conversation']}[/bold]")
        console.print(f"   Score: {score_pct}%")
        console.print(f"   {text}")
        console.print(f"   [dim]{item['source_path']}[/dim]\n")


def _keyword_search(
    query: str,
    workspace_path: Path,
    conversation_type: Optional[str],
    limit: int,
) -> None:
    """Perform keyword search using ripgrep."""
    import json
    import subprocess

    # Build search paths
    search_paths = []
    if conversation_type:
        type_dir = workspace_path / conversation_type
        if type_dir.exists():
            search_paths.append(str(type_dir))
        else:
            console.print(f"[yellow]Type '{conversation_type}' not found[/yellow]")
            return
    else:
        # Search all conversation directories
        registry_path = workspace_path / ".workspace" / "registry.json"
        if registry_path.exists():
            registry = json.loads(registry_path.read_text())
            for type_name, config in registry.get("conversation_types", {}).items():
                folder = config.get("folder", type_name)
                type_dir = workspace_path / folder
                if type_dir.exists():
                    search_paths.append(str(type_dir))

    if not search_paths:
        console.print("[yellow]No conversation directories found[/yellow]")
        return

    # Run ripgrep
    try:
        cmd = ["rg", "--json", "-i", query] + search_paths
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        matches = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "match":
                    match_data = data.get("data", {})
                    path = match_data.get("path", {}).get("text", "")
                    line_num = match_data.get("line_number", 0)
                    line_text = match_data.get("lines", {}).get("text", "").strip()
                    matches.append(
                        {"path": path, "line": line_num, "text": line_text}
                    )
                    if len(matches) >= limit:
                        break
            except json.JSONDecodeError:
                continue

        console.print(f"\n[bold]Keyword Search:[/bold] {query}\n")

        if not matches:
            console.print("[yellow]No results found.[/yellow]")
            return

        for i, match in enumerate(matches, 1):
            text = match["text"]
            if len(text) > 200:
                text = text[:197] + "..."

            console.print(f"[cyan]{i}.[/cyan] {match['path']}:{match['line']}")
            console.print(f"   {text}\n")

    except FileNotFoundError:
        console.print(
            "[red]Error:[/red] ripgrep (rg) not found. "
            "Install ripgrep for keyword search."
        )
        raise typer.Exit(1)
    except subprocess.TimeoutExpired:
        console.print("[red]Error:[/red] Search timed out")
        raise typer.Exit(1)
