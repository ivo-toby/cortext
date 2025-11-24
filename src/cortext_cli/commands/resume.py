"""Resume command to continue paused conversations."""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def find_sessions(workspace_root: Path, conv_type: Optional[str] = None) -> list[dict]:
    """Find all conversations with session state."""
    sessions = []

    # Search for session.json files
    for session_file in workspace_root.rglob("*/.session/session.json"):
        try:
            session_data = json.loads(session_file.read_text())
            conv_dir = session_file.parent.parent

            # Filter by type if specified
            if conv_type and session_data.get("conversation_type") != conv_type:
                continue

            sessions.append({
                "dir": str(conv_dir),
                "id": session_data.get("conversation_id", "unknown"),
                "type": session_data.get("conversation_type", "unknown"),
                "status": session_data.get("status", "unknown"),
                "last_active": session_data.get("last_active", ""),
                "summary": session_data.get("context_summary", ""),
                "command": session_data.get("agent_config", {}).get("command", ""),
                "message_count": session_data.get("message_count", 0),
            })
        except (json.JSONDecodeError, KeyError):
            continue

    # Sort by last_active (most recent first)
    sessions.sort(key=lambda x: x.get("last_active", ""), reverse=True)

    return sessions


def format_relative_time(iso_time: str) -> str:
    """Format ISO timestamp as relative time."""
    if not iso_time:
        return "unknown"

    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt

        if diff.days > 7:
            return dt.strftime("%Y-%m-%d")
        elif diff.days > 1:
            return f"{diff.days} days ago"
        elif diff.days == 1:
            return "yesterday"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"
    except (ValueError, TypeError):
        return iso_time[:10] if len(iso_time) >= 10 else iso_time


def resume_command(
    query: Optional[str] = typer.Argument(
        None,
        help="Conversation ID or search term to resume"
    ),
    list_all: bool = typer.Option(
        False,
        "--list", "-l",
        help="List all resumable conversations"
    ),
    conv_type: Optional[str] = typer.Option(
        None,
        "--type", "-t",
        help="Filter by conversation type (e.g., brainstorm, debug)"
    ),
    status_filter: Optional[str] = typer.Option(
        None,
        "--status", "-s",
        help="Filter by status (active, paused, completed)"
    ),
):
    """Resume a previously paused conversation.

    Examples:
        cortext resume --list
        cortext resume --list --type brainstorm
        cortext resume 001-brainstorm-api
        cortext resume "api design"
    """
    # Find workspace root
    workspace_root = Path.cwd()
    workspace_dir = workspace_root / ".workspace"

    if not workspace_dir.exists():
        console.print(
            "[yellow]⚠ Not in a Cortext workspace[/yellow]\n"
            "[dim]Run 'cortext init' to create a workspace[/dim]"
        )
        raise typer.Exit(code=1)

    # Find all sessions
    sessions = find_sessions(workspace_root, conv_type)

    # Filter by status if specified
    if status_filter:
        sessions = [s for s in sessions if s["status"] == status_filter]

    # If no sessions found
    if not sessions:
        console.print("[yellow]No resumable conversations found.[/yellow]")
        if conv_type:
            console.print(f"[dim]No {conv_type} conversations with session state.[/dim]")
        console.print("\n[dim]Start a conversation and use /workspace.stop-conversation to save it.[/dim]")
        raise typer.Exit(code=0)

    # List mode
    if list_all or query is None:
        console.print("\n[bold cyan]🧠 Cortext - Resumable Conversations[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold cyan", show_lines=False)
        table.add_column("#", style="dim", width=3)
        table.add_column("Type", style="cyan", width=12)
        table.add_column("ID", style="green")
        table.add_column("Last Active", style="dim", width=14)
        table.add_column("Status", width=10)
        table.add_column("Summary", style="dim", max_width=40)

        for idx, session in enumerate(sessions, 1):
            status_style = {
                "active": "[green]active[/green]",
                "paused": "[yellow]paused[/yellow]",
                "completed": "[dim]completed[/dim]",
            }.get(session["status"], session["status"])

            # Truncate summary
            summary = session["summary"]
            if len(summary) > 40:
                summary = summary[:37] + "..."

            table.add_row(
                str(idx),
                session["type"],
                session["id"],
                format_relative_time(session["last_active"]),
                status_style,
                summary
            )

        console.print(table)
        console.print(f"\n[dim]Total: {len(sessions)} conversation(s)[/dim]")
        console.print("\n[dim]To resume: cortext resume <id> or cortext resume <search-term>[/dim]\n")
        raise typer.Exit(code=0)

    # Search mode - find matching session
    matches = []
    query_lower = query.lower()

    for session in sessions:
        # Match by ID (exact or partial)
        if query_lower in session["id"].lower():
            matches.append(session)
        # Match by summary
        elif query_lower in session["summary"].lower():
            matches.append(session)

    if not matches:
        console.print(f"[yellow]No conversation found matching '{query}'[/yellow]")
        console.print("\n[dim]Available conversations:[/dim]")
        for session in sessions[:5]:
            console.print(f"  - {session['id']}")
        raise typer.Exit(code=1)

    if len(matches) > 1:
        console.print(f"[yellow]Multiple conversations match '{query}':[/yellow]\n")
        for idx, session in enumerate(matches, 1):
            console.print(f"  {idx}. [{session['type']}] {session['id']}")
            if session["summary"]:
                console.print(f"     [dim]{session['summary'][:60]}[/dim]")
        console.print("\n[dim]Please be more specific.[/dim]")
        raise typer.Exit(code=1)

    # Single match - show resume info
    session = matches[0]

    console.print(f"\n[bold cyan]Resuming conversation...[/bold cyan]\n")
    console.print(f"[bold]Conversation:[/bold] {session['id']}")
    console.print(f"[bold]Type:[/bold] {session['type']}")
    console.print(f"[bold]Command:[/bold] {session['command']}")
    console.print(f"[bold]Last active:[/bold] {format_relative_time(session['last_active'])}")
    console.print(f"[bold]Messages:[/bold] {session['message_count']}")
    if session["summary"]:
        console.print(f"[bold]Summary:[/bold] {session['summary']}")

    console.print(f"\n[green]To continue this conversation:[/green]")
    console.print(f"  1. Run: [cyan]{session['command']}[/cyan] in your AI tool")
    console.print(f"  2. Or use: [cyan]/workspace.resume[/cyan] and select this conversation")
    console.print(f"\n[dim]Conversation directory: {session['dir']}[/dim]\n")
