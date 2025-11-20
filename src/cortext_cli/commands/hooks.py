"""Hooks command to manage Cortext event hooks."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cortext_cli.utils import get_git_hooks_dir

console = Console()

app = typer.Typer(
    name="hooks",
    help="Manage Cortext event hooks",
    add_completion=False,
)


def get_workspace_hooks_dir() -> Optional[Path]:
    """Get the .workspace/hooks directory if it exists."""
    cwd = Path.cwd()
    workspace_dir = cwd / ".workspace" / "hooks"
    if workspace_dir.exists():
        return workspace_dir
    return None


def get_hooks_source_dir() -> Path:
    """Get the source hooks directory from the package."""
    # Navigate from this file to scripts/hooks
    package_root = Path(__file__).parent.parent.parent.parent
    return package_root / "scripts" / "hooks"


@app.command()
def install(
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing git hooks"
    ),
):
    """Install git hooks for automatic embedding.

    Installs pre-commit and post-checkout hooks that integrate with
    the Cortext hooks system.
    """
    # Check if we're in a git repo
    git_dir = Path.cwd() / ".git"
    if not git_dir.exists():
        console.print("[red]Error:[/red] Not a git repository")
        raise typer.Exit(code=1)

    git_hooks_dest = git_dir / "hooks"
    git_hooks_src = get_git_hooks_dir()

    if not git_hooks_src.exists():
        console.print("[red]Error:[/red] Git hooks source directory not found")
        raise typer.Exit(code=1)

    hooks_to_install = ["pre-commit", "post-checkout"]
    installed = []

    for hook_name in hooks_to_install:
        src_file = git_hooks_src / hook_name
        if not src_file.exists():
            continue

        dest_file = git_hooks_dest / hook_name

        if dest_file.exists() and not force:
            # Check if it's already our hook
            content = dest_file.read_text()
            if "Cortext" in content:
                console.print(f"[dim]Hook '{hook_name}' already installed[/dim]")
                continue

            # Append to existing hook
            console.print(f"[yellow]Appending to existing '{hook_name}' hook[/yellow]")
            with open(dest_file, "a") as f:
                f.write("\n\n# --- Cortext hooks integration ---\n")
                f.write(src_file.read_text())
        else:
            # Copy or overwrite
            shutil.copy2(src_file, dest_file)

        # Make executable
        if os.name != "nt":
            os.chmod(dest_file, 0o755)

        installed.append(hook_name)

    if installed:
        console.print(f"[green]Installed git hooks:[/green] {', '.join(installed)}")
    else:
        console.print("[dim]No hooks to install[/dim]")


@app.command()
def run(
    event: str = typer.Argument(..., help="Event to trigger (e.g., conversation:create)"),
    args: list[str] = typer.Argument(None, help="Arguments to pass to hooks"),
):
    """Manually trigger a hook event.

    Example:
        cortext hooks run conversation:create /path/to/conversation
    """
    hooks_dir = get_workspace_hooks_dir()
    if not hooks_dir:
        console.print("[red]Error:[/red] No .workspace/hooks directory found")
        console.print("[dim]Run 'cortext init' to create a workspace with hooks[/dim]")
        raise typer.Exit(code=1)

    dispatcher = hooks_dir / "dispatch.sh"
    if not dispatcher.exists():
        console.print("[red]Error:[/red] Dispatcher not found")
        raise typer.Exit(code=1)

    # Build command
    cmd = [str(dispatcher), event]
    if args:
        cmd.extend(args)

    # Set debug mode for manual runs
    env = os.environ.copy()
    env["CORTEXT_HOOKS_DEBUG"] = "1"

    console.print(f"[cyan]Running event:[/cyan] {event}")

    try:
        result = subprocess.run(cmd, env=env)
        if result.returncode != 0:
            console.print(f"[red]Hook failed with exit code {result.returncode}[/red]")
            raise typer.Exit(code=result.returncode)
        else:
            console.print("[green]Hooks completed successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error running hooks:[/red] {e}")
        raise typer.Exit(code=1)


@app.command(name="list")
def list_hooks():
    """List all configured hooks and their status."""
    hooks_dir = get_workspace_hooks_dir()

    if not hooks_dir:
        console.print("[yellow]No hooks directory found[/yellow]")
        console.print("[dim]Run 'cortext init' to create a workspace with hooks[/dim]")
        return

    console.print(Panel.fit("[bold]Cortext Hooks[/bold]", border_style="cyan"))

    # Find all hook events
    events = {}

    for category_dir in hooks_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name == "__pycache__":
            continue

        category = category_dir.name

        for event_dir in category_dir.iterdir():
            if not event_dir.is_dir():
                continue

            # Parse event name from directory
            dir_name = event_dir.name
            if dir_name.startswith("on-") and dir_name.endswith(".d"):
                action = dir_name[3:-2]  # Remove "on-" prefix and ".d" suffix
                event_name = f"{category}:{action}"
            elif dir_name.endswith(".d"):
                # Git hooks like "pre-commit.d"
                event_name = dir_name[:-2]
            else:
                continue

            # Get scripts in this event directory
            scripts = []
            for script in sorted(event_dir.glob("*.sh")):
                is_executable = os.access(script, os.X_OK)
                scripts.append((script.name, is_executable))

            if scripts:
                events[event_name] = scripts

    if not events:
        console.print("[dim]No hooks configured[/dim]")
        return

    # Display hooks in a table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Event")
    table.add_column("Scripts")
    table.add_column("Status")

    for event_name in sorted(events.keys()):
        scripts = events[event_name]
        script_names = []
        all_executable = True

        for name, is_exec in scripts:
            if is_exec:
                script_names.append(f"[green]{name}[/green]")
            else:
                script_names.append(f"[yellow]{name}[/yellow] (not executable)")
                all_executable = False

        status = "[green]Ready[/green]" if all_executable else "[yellow]Check permissions[/yellow]"
        table.add_row(event_name, "\n".join(script_names), status)

    console.print(table)

    # Check git hooks status
    git_hooks_dir = Path.cwd() / ".git" / "hooks"
    if git_hooks_dir.exists():
        console.print("\n[bold]Git Hooks:[/bold]")
        for hook_name in ["pre-commit", "post-checkout"]:
            hook_path = git_hooks_dir / hook_name
            if hook_path.exists():
                content = hook_path.read_text()
                if "Cortext" in content:
                    console.print(f"  [green]{hook_name}[/green]: Installed")
                else:
                    console.print(f"  [yellow]{hook_name}[/yellow]: Exists (not Cortext)")
            else:
                console.print(f"  [dim]{hook_name}[/dim]: Not installed")


@app.command()
def add(
    event: str = typer.Argument(..., help="Event to add hook for (e.g., conversation:create)"),
    name: str = typer.Argument(..., help="Name for the hook (will be prefixed with 50-)"),
):
    """Add a custom hook script for an event.

    Creates a new hook script with a template that includes
    argument handling and graceful degradation patterns.

    Example:
        cortext hooks add conversation:create notify-slack
    """
    hooks_dir = get_workspace_hooks_dir()
    if not hooks_dir:
        console.print("[red]Error:[/red] No .workspace/hooks directory found")
        console.print("[dim]Run 'cortext init' to create a workspace with hooks[/dim]")
        raise typer.Exit(code=1)

    # Parse event
    if ":" in event:
        category, action = event.split(":", 1)
        event_dir = hooks_dir / category / f"on-{action}.d"
    else:
        # Git hook
        event_dir = hooks_dir / "git" / f"{event}.d"

    # Create directory if needed
    event_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize hook name
    hook_name = name.lower().replace(" ", "-").replace("_", "-")
    script_name = f"50-{hook_name}.sh"
    script_path = event_dir / script_name

    if script_path.exists():
        console.print(f"[red]Error:[/red] Hook already exists: {script_path}")
        raise typer.Exit(code=1)

    # Create template
    template = f'''#!/usr/bin/env bash
# Custom hook: {name}
# Event: {event}
#
# This hook runs as part of the {event} event.
# Modify this template to add your custom logic.

# Graceful degradation pattern - exit silently if dependencies missing
# Uncomment and modify as needed:
# if ! command -v your-command &> /dev/null; then
#     exit 0
# fi

# Get arguments passed to the hook
# For conversation events: $1 is the conversation path
# For git hooks: arguments vary by hook type
ARG1="${{1:-}}"

# Debug output (shown when CORTEXT_HOOKS_DEBUG=1)
if [ "${{CORTEXT_HOOKS_DEBUG:-0}}" = "1" ]; then
    echo "[{hook_name}] Running with arg: $ARG1" >&2
fi

# --- Your custom logic here ---



# Exit successfully
exit 0
'''

    script_path.write_text(template)
    os.chmod(script_path, 0o755)

    console.print(f"[green]Created hook:[/green] {script_path}")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print(f"  1. Edit {script_path}")
    console.print(f"  2. Add your custom logic")
    console.print(f"  3. Test with: cortext hooks run {event} [args]")
