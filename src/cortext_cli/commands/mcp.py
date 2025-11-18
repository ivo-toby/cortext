"""MCP server management commands."""

import json
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from cortext_cli.utils import get_template_dir

console = Console()
app = typer.Typer(help="MCP server management commands")


@app.command("install")
def mcp_install(
    ai: Optional[str] = typer.Option(
        None, help="Configure for specific agent (claude, gemini, opencode, all)"
    ),
    force: bool = typer.Option(False, help="Overwrite existing configs"),
):
    """Add MCP server configuration to current workspace.

    Examples:
        cortext mcp install               # Configure for all detected agents
        cortext mcp install --ai claude   # Configure only for Claude
        cortext mcp install --force       # Overwrite existing configs
    """
    # Verify we're in a Cortext workspace
    workspace_dir = Path.cwd()
    registry_path = workspace_dir / ".workspace" / "registry.json"

    if not registry_path.exists():
        console.print(
            "[red]✗ Not in a Cortext workspace.[/red]\n"
            "[dim]Run 'cortext init' first to create a workspace.[/dim]"
        )
        raise typer.Exit(code=1)

    # Detect configured agents
    detected_agents = _detect_configured_agents(workspace_dir)

    if not detected_agents:
        console.print(
            "[yellow]⚠ No AI agents detected in this workspace.[/yellow]\n"
            "[dim]Run 'cortext init --ai <agent>' to configure an agent first.[/dim]"
        )
        raise typer.Exit()

    # Filter by --ai flag if provided
    if ai:
        if ai == "all":
            agents_to_configure = detected_agents
        elif ai in detected_agents:
            agents_to_configure = [ai]
        else:
            console.print(
                f"[yellow]⚠ Agent '{ai}' not found in workspace.[/yellow]\n"
                f"[dim]Detected agents: {', '.join(detected_agents)}[/dim]"
            )
            raise typer.Exit()
    else:
        agents_to_configure = detected_agents

    # Check if cortext-mcp is available
    mcp_available = _check_mcp_command()
    if not mcp_available:
        console.print(
            "[yellow]⚠ cortext-mcp command not found in PATH[/yellow]\n"
            "[dim]MCP configs will be created but may not work until cortext-mcp is available.[/dim]\n"
        )

    # Install MCP config for each agent
    configured = []
    already_configured = []
    failed = []

    for agent in agents_to_configure:
        config_exists = _check_mcp_config_exists(workspace_dir, agent)

        if config_exists and not force:
            already_configured.append(agent)
            continue

        success = _install_mcp_config_for_agent(workspace_dir, agent)
        if success:
            configured.append(agent)
        else:
            failed.append(agent)

    # Display results
    console.print()
    if configured:
        for agent in configured:
            action = "reconfigured" if force else "configured"
            console.print(f"[green]✓[/green] MCP server {action} for: [cyan]{agent.title()}[/cyan]")
            if agent == "claude":
                console.print(f"  [dim]Registered via: claude mcp add[/dim]")
            else:
                config_path = _get_config_path(workspace_dir, agent)
                console.print(f"  [dim]Config: {config_path}[/dim]")

    if already_configured:
        console.print()
        for agent in already_configured:
            console.print(
                f"[yellow]⚠[/yellow] MCP already configured for: [cyan]{agent.title()}[/cyan]"
            )
        console.print("[dim]Use --force to overwrite existing configurations[/dim]")

    if failed:
        console.print()
        for agent in failed:
            console.print(f"[red]✗[/red] Failed to configure: [cyan]{agent.title()}[/cyan]")

    if configured:
        console.print(
            f"\n[cyan]Test MCP server:[/cyan]\n"
            f"  Run your AI tool in this workspace to verify MCP tools are available\n"
        )


def _detect_configured_agents(workspace_dir: Path) -> list[str]:
    """Detect which agents are configured in the workspace."""
    agents = []

    # Check for Claude
    if (workspace_dir / ".claude" / "commands").exists():
        agents.append("claude")

    # Check for Gemini
    if (workspace_dir / ".gemini" / "commands").exists():
        agents.append("gemini")

    # Check for OpenCode
    if (workspace_dir / ".opencode" / "command").exists():
        agents.append("opencode")

    return agents


def _check_mcp_command() -> bool:
    """Check if cortext-mcp command is available."""
    try:
        result = subprocess.run(
            ["which", "cortext-mcp"], capture_output=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _check_mcp_config_exists(workspace_dir: Path, agent: str) -> bool:
    """Check if MCP config already exists for an agent."""
    if agent == "claude":
        # Check if server is registered with Claude CLI
        try:
            result = subprocess.run(
                ["claude", "mcp", "get", "cortext"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    else:
        config_path = _get_config_path(workspace_dir, agent)
        return config_path.exists() if config_path else False


def _get_config_path(workspace_dir: Path, agent: str) -> Optional[Path]:
    """Get the config path for a specific agent."""
    if agent == "claude":
        # Claude uses CLI registration, not config file
        return None
    elif agent == "gemini":
        return Path.home() / ".gemini" / "settings.json"
    elif agent == "opencode":
        return workspace_dir / ".opencode" / "mcp_config.json"
    return None


def _install_mcp_config_for_agent(workspace_dir: Path, agent: str) -> bool:
    """Install MCP config for a specific agent."""
    if agent == "claude":
        return _install_claude_mcp_config(workspace_dir)
    elif agent == "gemini":
        return _install_gemini_mcp_config(workspace_dir)
    elif agent == "opencode":
        return _install_opencode_mcp_config(workspace_dir)
    return False


def _install_claude_mcp_config(workspace_dir: Path) -> bool:
    """Install MCP config for Claude Code using 'claude mcp add' command."""
    import subprocess

    # Try to register the MCP server using claude CLI
    try:
        # Check if claude CLI is available
        result = subprocess.run(
            ["claude", "mcp", "add", "--transport", "stdio", "--scope", "local",
             "cortext", "--", "cortext-mcp"],
            cwd=workspace_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True
        elif "already exists" in result.stderr.lower():
            # Already registered - still success
            return True
        else:
            console.print(
                f"[yellow]Could not auto-register MCP server.[/yellow]\n"
                f"[dim]Run: claude mcp add --transport stdio --scope local cortext -- cortext-mcp[/dim]"
            )
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        # Claude CLI not available or command failed
        console.print(
            "[yellow]Claude CLI not available.[/yellow]\n"
            "[dim]To enable MCP server, run:[/dim]\n"
            "  claude mcp add --transport stdio --scope local cortext -- cortext-mcp"
        )
        return False


def _install_gemini_mcp_config(workspace_dir: Path) -> bool:
    """Install MCP config for Gemini CLI (global settings.json merge)."""
    # Gemini uses global settings file
    settings_path = Path.home() / ".gemini" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing settings or create new
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            settings = {}
    else:
        settings = {}

    # Ensure mcpServers exists
    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    # Add/update cortext server entry
    settings["mcpServers"]["cortext"] = {
        "command": "cortext-mcp",
        "args": [],
        "env": {"WORKSPACE_PATH": str(workspace_dir.absolute())},
        "trust": True,
    }

    # Write back
    settings_path.write_text(json.dumps(settings, indent=2))
    return True


def _install_opencode_mcp_config(workspace_dir: Path) -> bool:
    """Install MCP config for OpenCode (workspace-local)."""
    template_dir = get_template_dir()
    template_path = template_dir / "mcp_config.json"

    if not template_path.exists():
        return False

    # Read template
    template_content = template_path.read_text()

    # Substitute workspace path
    config_content = template_content.replace(
        "{{WORKSPACE_PATH}}", str(workspace_dir.absolute())
    )

    # Write to OpenCode's workspace-local config
    config_dir = workspace_dir / ".opencode"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "mcp_config.json"

    config_path.write_text(config_content)
    return True
