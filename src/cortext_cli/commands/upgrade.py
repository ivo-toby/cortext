"""Upgrade command to migrate workspaces to newer Cortext versions."""

import json
import shutil
from datetime import datetime, timezone
from difflib import unified_diff
from importlib.metadata import version as get_package_version
from pathlib import Path
from typing import Optional

import typer
from packaging.version import Version, parse as parse_version
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from cortext_cli.commands.init import (
    SCRIPT_API_VERSION,
    compute_generated_files_metadata,
    configure_ai_tools,
    get_builtin_conversation_types,
)
from cortext_cli.converters import (
    convert_md_for_codex,
    convert_md_to_toml,
)
from cortext_cli.utils import (
    FileStatus,
    VersionStatus,
    StepTracker,
    compute_file_hash,
    get_file_status,
    get_commands_dir,
    get_hooks_dir,
    get_scripts_dir,
    get_template_dir,
)

console = Console()


def get_cortext_version() -> str:
    """Get the current installed Cortext version."""
    try:
        return get_package_version("cortext-workspace")
    except Exception:
        return "0.0.0"


def check_workspace_version(workspace_dir: Path) -> tuple[VersionStatus, str | None]:
    """Check workspace version against installed Cortext version.

    Args:
        workspace_dir: Workspace root directory

    Returns:
        Tuple of (VersionStatus, workspace_version_string or None)
    """
    registry_path = workspace_dir / ".workspace" / "registry.json"

    if not registry_path.exists():
        console.print("[red]✗[/red] Not a Cortext workspace")
        raise typer.Exit(1)

    try:
        registry = json.loads(registry_path.read_text())
    except json.JSONDecodeError:
        console.print("[red]✗[/red] Corrupted registry file")
        console.print("[dim]Try restoring from git history[/dim]")
        raise typer.Exit(1)

    workspace_meta = registry.get("workspace_meta")
    if workspace_meta is None:
        return (VersionStatus.LEGACY, None)

    workspace_version_str = workspace_meta.get("cortext_version")
    installed_version_str = get_cortext_version()

    if not workspace_version_str:
        return (VersionStatus.LEGACY, None)

    try:
        workspace_version = parse_version(workspace_version_str)
        installed_version = parse_version(installed_version_str)

        if workspace_version < installed_version:
            return (VersionStatus.UPGRADE_AVAILABLE, workspace_version_str)
        elif workspace_version > installed_version:
            return (VersionStatus.NEWER_WORKSPACE, workspace_version_str)
        else:
            return (VersionStatus.CURRENT, workspace_version_str)
    except Exception:
        # If version parsing fails, treat as legacy
        return (VersionStatus.LEGACY, workspace_version_str)


def create_backup(file_path: Path, backup_dir: Path) -> Path:
    """Create a timestamped backup of a file.

    Args:
        file_path: Path to file to backup
        backup_dir: Directory to store backup in

    Returns:
        Path to the created backup file
    """
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"

    shutil.copy2(file_path, backup_path)
    return backup_path


def show_diff(original_content: str, current_content: str, file_path: str):
    """Display a unified diff between original and current content.

    Args:
        original_content: Original file content
        current_content: Current file content
        file_path: Path for display purposes
    """
    diff = unified_diff(
        original_content.splitlines(keepends=True),
        current_content.splitlines(keepends=True),
        fromfile=f"{file_path} (original)",
        tofile=f"{file_path} (current)",
        lineterm=""
    )

    diff_text = "".join(diff)
    if diff_text:
        console.print(Syntax(diff_text, "diff", theme="monokai"))
    else:
        console.print("[dim]No differences found[/dim]")


def _add_tool_to_workspace(workspace_dir: Path, tool: str, verbose: bool):
    """Wire up a new AI tool on an existing workspace non-destructively.

    Creates the tool's command directory (e.g. .codex/prompts/), converts
    and installs all built-in commands plus custom types from the registry,
    and writes AGENTS.md / config files as appropriate.
    """
    supported = {"claude", "codex", "opencode", "gemini", "cursor"}
    if tool not in supported:
        console.print(f"[red]✗[/red] Unknown tool '{tool}'. Supported: {', '.join(sorted(supported))}")
        raise typer.Exit(1)

    tracker = StepTracker(f"Adding {tool.title()} support")

    # Configure built-in AI tool files (commands, AGENTS.md, etc.)
    configure_ai_tools(workspace_dir, tool, tracker)

    # Also sync custom conversation types from registry
    registry_path = workspace_dir / ".workspace" / "registry.json"
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text())
            custom_types = {
                tid: cfg
                for tid, cfg in registry.get("conversation_types", {}).items()
                if not cfg.get("built_in", True)
            }
            if custom_types:
                _sync_custom_types_to_tool(workspace_dir, tool, custom_types, verbose)
                tracker.add_step(f"Synced {len(custom_types)} custom type(s) to {tool}")
        except Exception as e:
            tracker.add_warning(f"Could not sync custom types: {e}")

    tracker.display()
    console.print(
        f"\n[green]✓[/green] {tool.title()} support added.\n"
        f"[dim]Run 'cortext mcp install --ai {tool}' to also configure the MCP server.[/dim]"
    )


def _sync_custom_types_to_tool(
    workspace_dir: Path, tool: str, custom_types: dict, verbose: bool
):
    """Copy/convert custom type command files into the new tool's directory."""
    from cortext_cli.converters import convert_md_for_codex, convert_md_to_toml

    for type_id, type_config in custom_types.items():
        command_name = type_config.get("command", "").lstrip("/").replace(".", "_")
        if not command_name:
            continue

        # Source: Claude command (always present for user-created types)
        claude_src = workspace_dir / ".claude" / "commands" / f"{command_name}.md"
        if not claude_src.exists():
            continue

        try:
            if tool == "codex":
                codex_dir = workspace_dir / ".codex" / "prompts"
                if codex_dir.exists():
                    content, _ = convert_md_for_codex(claude_src)
                    (codex_dir / f"{command_name}.md").write_text(content)
                    user_dir = Path.home() / ".codex" / "prompts"
                    user_dir.mkdir(parents=True, exist_ok=True)
                    (user_dir / f"{command_name}.md").write_text(content)
            elif tool == "opencode":
                opencode_dir = workspace_dir / ".opencode" / "command"
                if opencode_dir.exists():
                    import shutil as _shutil
                    _shutil.copy2(claude_src, opencode_dir / f"{command_name}.md")
            elif tool == "gemini":
                gemini_dir = workspace_dir / ".gemini" / "commands"
                if gemini_dir.exists():
                    content, _ = convert_md_to_toml(claude_src)
                    (gemini_dir / f"{command_name}.toml").write_text(content)
            elif tool == "claude":
                pass  # already the source
            if verbose:
                console.print(f"[green]✓[/green] Synced custom type '{type_id}' for {tool}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Could not sync '{type_id}' for {tool}: {e}")


def upgrade_command(
    workspace_path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Path to workspace (default: current directory)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would change without applying",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Accept all defaults non-interactively",
    ),
    built_in_only: bool = typer.Option(
        False,
        "--built-in-only",
        help="Only upgrade built-in types, skip custom types",
    ),
    regenerate: Optional[str] = typer.Option(
        None,
        "--regenerate",
        help="Force regenerate specific custom type",
    ),
    backup_dir: Optional[Path] = typer.Option(
        None,
        "--backup-dir",
        help="Custom backup directory (default: .workspace/backup/)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed progress",
    ),
    add_tool: Optional[str] = typer.Option(
        None,
        "--add-tool",
        help="Add support for a new AI tool without re-initializing (e.g. codex, opencode, gemini)",
    ),
):
    """Upgrade workspace to current Cortext version.

    To add a new AI tool to an existing workspace without re-initializing:

        cortext upgrade --add-tool codex
    """

    # Determine workspace directory
    if workspace_path is None:
        workspace_dir = Path.cwd()
    else:
        workspace_dir = workspace_path.resolve()

    # Check if workspace exists
    if not (workspace_dir / ".workspace").exists():
        console.print("[red]✗[/red] Not a Cortext workspace")
        console.print(f"[dim]Directory: {workspace_dir}[/dim]")
        raise typer.Exit(1)

    # --add-tool: non-destructively wire up a new AI tool on an existing workspace
    if add_tool:
        _add_tool_to_workspace(workspace_dir, add_tool, verbose)
        return

    # Check workspace version status
    status, workspace_version = check_workspace_version(workspace_dir)

    if status == VersionStatus.CURRENT:
        console.print("[green]✓[/green] Workspace is up to date")
        console.print(f"[dim]Version: {workspace_version}[/dim]")
        return

    if status == VersionStatus.NEWER_WORKSPACE:
        console.print("[yellow]⚠[/yellow] Workspace version is newer than installed Cortext")
        console.print(f"[dim]Workspace: {workspace_version} | Installed: {get_cortext_version()}[/dim]")
        console.print("[dim]Consider upgrading Cortext[/dim]")
        return

    # Display upgrade info
    installed_version = get_cortext_version()
    console.print(Panel.fit(
        f"[bold cyan]🔄 Cortext Workspace Upgrade[/bold cyan]\n\n"
        f"From: [yellow]{workspace_version or 'Legacy'}[/yellow] → To: [green]{installed_version}[/green]",
        border_style="cyan"
    ))

    if dry_run:
        console.print("[dim]Dry run - no changes will be made[/dim]\n")

    if status == VersionStatus.LEGACY:
        if not handle_legacy_workspace(workspace_dir, dry_run, yes, verbose):
            return

    # Set backup directory
    if backup_dir is None:
        backup_dir = workspace_dir / ".workspace" / "backup"

    # Perform the upgrade
    perform_upgrade(
        workspace_dir=workspace_dir,
        dry_run=dry_run,
        yes=yes,
        built_in_only=built_in_only,
        regenerate=regenerate,
        backup_dir=backup_dir,
        verbose=verbose,
    )


def handle_legacy_workspace(workspace_dir: Path, dry_run: bool, yes: bool, verbose: bool) -> bool:
    """Handle upgrade of legacy workspace without version tracking.

    Args:
        workspace_dir: Workspace root directory
        dry_run: If True, don't make any changes
        yes: If True, use default answers
        verbose: Show detailed progress

    Returns:
        True if migration should proceed, False otherwise
    """
    console.print("\n[yellow]⚠ Legacy workspace detected[/yellow]")
    console.print("This workspace was created before Cortext 0.3.0 and doesn't have")
    console.print("version tracking metadata.\n")

    if dry_run:
        console.print("[dim]Would add version metadata to registry[/dim]")
        console.print("[dim]Would compute hashes for all existing files[/dim]")
        return True

    if not yes:
        choice = Prompt.ask(
            "How should existing files be treated?",
            choices=["modified", "unmodified", "cancel"],
            default="modified"
        )

        if choice == "cancel":
            console.print("Upgrade cancelled")
            return False

        treat_as_modified = choice == "modified"
    else:
        treat_as_modified = True  # Safe default

    # Migrate the registry to new schema
    registry_path = workspace_dir / ".workspace" / "registry.json"
    registry = json.loads(registry_path.read_text())

    current_version = get_cortext_version()
    current_time = datetime.now(timezone.utc).isoformat()

    # Add workspace_meta if missing
    if "workspace_meta" not in registry:
        registry["workspace_meta"] = {
            "cortext_version": current_version,
            "initialized": registry.get("created", current_time),
            "last_upgraded": current_time,
        }

    # Update schema version
    if "version" in registry:
        del registry["version"]
    registry["schema_version"] = "2.0"

    # Add generated_with metadata to each conversation type
    for type_id, type_config in registry.get("conversation_types", {}).items():
        if "generated_with" not in type_config:
            try:
                # Compute current file hashes as baseline
                generated_metadata = compute_generated_files_metadata(workspace_dir, type_id, type_config)
                type_config["generated_with"] = generated_metadata

                if treat_as_modified and verbose:
                    console.print(f"[dim]Added tracking for {type_id}[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Could not compute hashes for {type_id}: {e}")

    # Save updated registry
    registry_path.write_text(json.dumps(registry, indent=2))
    console.print("[green]✓[/green] Migrated workspace to schema v2.0\n")

    return True


def add_missing_builtin_types(
    workspace_dir: Path,
    registry: dict,
    dry_run: bool,
    yes: bool,
    verbose: bool,
) -> int:
    """Check for and add missing built-in conversation types.

    Args:
        workspace_dir: Workspace root directory
        registry: Current registry dict
        dry_run: If True, don't make changes
        yes: If True, use default answers
        verbose: Show detailed progress

    Returns:
        Number of types added
    """
    current_builtin_types = get_builtin_conversation_types()
    existing_types = set(registry.get("conversation_types", {}).keys())
    missing_types = set(current_builtin_types.keys()) - existing_types

    if not missing_types:
        return 0

    console.print(f"\n[cyan]ℹ[/cyan]  Found {len(missing_types)} new built-in conversation type(s): {', '.join(missing_types)}")

    if not yes and not dry_run:
        if not Confirm.ask("Would you like to add these new types to your workspace?", default=True):
            console.print("[dim]Skipping new types[/dim]")
            return 0

    added_count = 0
    template_dir = get_template_dir()
    scripts_dir = get_scripts_dir()

    for type_id in missing_types:
        type_config = current_builtin_types[type_id].copy()

        if dry_run:
            console.print(f"[dim]Would add: {type_id}[/dim]")
            continue

        try:
            # Copy template file
            template_name = Path(type_config["template"]).name
            src_template = template_dir / template_name
            dest_template = workspace_dir / type_config["template"]

            if src_template.exists():
                dest_template.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_template, dest_template)
                if verbose:
                    console.print(f"  Copied template: {template_name}")

            # Copy script file
            script_name = Path(type_config["script"]).name
            src_script = scripts_dir / "bash" / script_name
            dest_script = workspace_dir / type_config["script"]

            if src_script.exists():
                dest_script.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_script, dest_script)
                dest_script.chmod(0o755)  # Make executable
                if verbose:
                    console.print(f"  Copied script: {script_name}")

            # Create conversation folder
            folder_path = workspace_dir / type_config["folder"]
            folder_path.mkdir(parents=True, exist_ok=True)
            (folder_path / ".gitkeep").touch()

            # Compute generation metadata
            try:
                generated_metadata = compute_generated_files_metadata(workspace_dir, type_id, type_config)
                type_config["generated_with"] = generated_metadata
            except Exception as e:
                if verbose:
                    console.print(f"[yellow]⚠[/yellow] Could not compute hashes for {type_id}: {e}")

            # Add to registry
            registry["conversation_types"][type_id] = type_config

            console.print(f"[green]✓[/green] Added: {type_id}")
            added_count += 1

        except Exception as e:
            console.print(f"[red]✗[/red] Failed to add {type_id}: {e}")

    return added_count


def add_missing_slash_commands(
    workspace_dir: Path,
    dry_run: bool,
    verbose: bool,
) -> int:
    """Check for and add missing command files across all active AI tool directories.

    Syncs built-in commands to each AI tool directory that exists in the workspace:
    - Claude Code (.claude/commands/)
    - Codex CLI (.codex/prompts/)
    - OpenCode (.opencode/command/)
    - Gemini (.gemini/commands/)

    Returns:
        Number of command files added across all tools
    """
    commands_dir = get_commands_dir()
    if not commands_dir.exists():
        return 0

    package_commands = list(commands_dir.glob("*.md"))
    if not package_commands:
        return 0

    package_names = {f.name for f in package_commands}
    added_count = 0

    # --- Claude Code ---
    claude_dir = workspace_dir / ".claude" / "commands"
    if claude_dir.exists():
        missing = package_names - {f.name for f in claude_dir.glob("*.md")}
        if missing and verbose:
            console.print(f"\n[cyan]ℹ[/cyan]  Claude: {len(missing)} new command(s)")
        for cmd_name in missing:
            if dry_run:
                console.print(f"[dim]Would add Claude command: {cmd_name}[/dim]")
                continue
            try:
                shutil.copy2(commands_dir / cmd_name, claude_dir / cmd_name)
                if verbose:
                    console.print(f"[green]✓[/green] Added Claude command: {cmd_name}")
                added_count += 1
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to add Claude {cmd_name}: {e}")

    # --- Codex CLI ---
    # .codex/prompts/ is the workspace VCS reference; ~/.codex/prompts/ is the
    # only path Codex actually scans. Both must be kept in sync independently:
    # workspace may be complete while the user home is empty (e.g. new machine).
    codex_dir = workspace_dir / ".codex" / "prompts"
    if codex_dir.exists():
        user_codex_dir = Path.home() / ".codex" / "prompts"
        workspace_existing = {f.name for f in codex_dir.glob("*.md")}
        user_existing = {f.name for f in user_codex_dir.glob("*.md")} if user_codex_dir.exists() else set()

        missing_workspace = package_names - workspace_existing
        # Also sync any workspace prompts absent from user home (covers fresh machines)
        missing_user = (package_names | workspace_existing) - user_existing

        all_to_process = missing_workspace | missing_user
        if all_to_process and verbose:
            console.print(f"\n[cyan]ℹ[/cyan]  Codex: {len(missing_workspace)} workspace + "
                          f"{len(missing_user - missing_workspace)} user-home prompt(s) to sync")

        for cmd_name in all_to_process:
            # Prefer the package source; fall back to existing workspace file
            pkg_src = commands_dir / cmd_name
            src = pkg_src if pkg_src.exists() else codex_dir / cmd_name
            if not src.exists():
                continue
            if dry_run:
                console.print(f"[dim]Would sync Codex prompt: {cmd_name}[/dim]")
                continue
            try:
                codex_content, _ = convert_md_for_codex(src)
                if cmd_name in missing_workspace:
                    (codex_dir / cmd_name).write_text(codex_content)
                if cmd_name in missing_user:
                    user_codex_dir.mkdir(parents=True, exist_ok=True)
                    (user_codex_dir / cmd_name).write_text(codex_content)
                if verbose:
                    console.print(f"[green]✓[/green] Synced Codex prompt: {cmd_name}")
                added_count += 1
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to sync Codex {cmd_name}: {e}")

    # --- OpenCode ---
    opencode_dir = workspace_dir / ".opencode" / "command"
    if opencode_dir.exists():
        missing = package_names - {f.name for f in opencode_dir.glob("*.md")}
        if missing and verbose:
            console.print(f"\n[cyan]ℹ[/cyan]  OpenCode: {len(missing)} new command(s)")
        for cmd_name in missing:
            if dry_run:
                console.print(f"[dim]Would add OpenCode command: {cmd_name}[/dim]")
                continue
            try:
                shutil.copy2(commands_dir / cmd_name, opencode_dir / cmd_name)
                if verbose:
                    console.print(f"[green]✓[/green] Added OpenCode command: {cmd_name}")
                added_count += 1
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to add OpenCode {cmd_name}: {e}")

    # --- Gemini ---
    gemini_dir = workspace_dir / ".gemini" / "commands"
    if gemini_dir.exists():
        package_toml_names = {f.stem + ".toml" for f in package_commands}
        existing_toml = {f.name for f in gemini_dir.glob("*.toml")}
        missing_toml = package_toml_names - existing_toml
        if missing_toml and verbose:
            console.print(f"\n[cyan]ℹ[/cyan]  Gemini: {len(missing_toml)} new command(s)")
        for toml_name in missing_toml:
            md_name = toml_name.replace(".toml", ".md")
            src = commands_dir / md_name
            if not src.exists():
                continue
            if dry_run:
                console.print(f"[dim]Would add Gemini command: {toml_name}[/dim]")
                continue
            try:
                toml_content, _ = convert_md_to_toml(src)
                (gemini_dir / toml_name).write_text(toml_content)
                if verbose:
                    console.print(f"[green]✓[/green] Added Gemini command: {toml_name}")
                added_count += 1
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to add Gemini {toml_name}: {e}")

    if added_count > 0 and not verbose:
        console.print(f"[green]✓[/green] Added {added_count} new command file(s) across AI tools")

    return added_count


def upgrade_core_infrastructure(
    workspace_dir: Path,
    dry_run: bool,
    verbose: bool,
) -> int:
    """Upgrade core infrastructure files that users should not modify.

    These files are always overwritten without checking for modifications,
    as they contain core functionality that should stay in sync with Cortext.

    Args:
        workspace_dir: Workspace root directory
        dry_run: If True, don't make changes
        verbose: Show detailed progress

    Returns:
        Number of files upgraded
    """
    scripts_dir = get_scripts_dir()
    hooks_dir = get_hooks_dir()
    template_dir = get_template_dir()

    if not scripts_dir.exists():
        if verbose:
            console.print("[yellow]⚠[/yellow] Scripts directory not found in package")
        return 0

    upgraded_count = 0

    # Upgrade all bash scripts
    bash_src = scripts_dir / "bash"
    bash_dest = workspace_dir / ".workspace" / "scripts" / "bash"

    if bash_src.exists() and bash_dest.exists():
        for script in bash_src.glob("*.sh"):
            dest_file = bash_dest / script.name

            if dry_run:
                if verbose:
                    console.print(f"[dim]Would upgrade: {script.name}[/dim]")
                upgraded_count += 1
            else:
                try:
                    import os
                    shutil.copy2(script, dest_file)
                    # Make executable on Unix systems
                    if os.name != "nt":
                        os.chmod(dest_file, 0o755)

                    if verbose:
                        console.print(f"[green]✓[/green] Updated: {script.name}")
                    upgraded_count += 1
                except Exception as e:
                    console.print(f"[red]✗[/red] Failed to upgrade {script.name}: {e}")

    # Upgrade PowerShell scripts
    ps_src = scripts_dir / "powershell"
    ps_dest = workspace_dir / ".workspace" / "scripts" / "powershell"

    if ps_src.exists() and ps_dest.exists():
        for script in ps_src.glob("*.ps1"):
            dest_file = ps_dest / script.name

            if dry_run:
                if verbose:
                    console.print(f"[dim]Would upgrade: {script.name}[/dim]")
                upgraded_count += 1
            else:
                try:
                    shutil.copy2(script, dest_file)
                    if verbose:
                        console.print(f"[green]✓[/green] Updated: {script.name}")
                    upgraded_count += 1
                except Exception as e:
                    console.print(f"[red]✗[/red] Failed to upgrade {script.name}: {e}")

    # Upgrade hooks dispatcher
    if hooks_dir.exists():
        dispatcher_src = hooks_dir / "dispatch.sh"
        dispatcher_dest = workspace_dir / ".workspace" / "hooks" / "dispatch.sh"

        if dispatcher_src.exists() and dispatcher_dest.parent.exists():
            if dry_run:
                if verbose:
                    console.print(f"[dim]Would upgrade: dispatch.sh[/dim]")
                upgraded_count += 1
            else:
                try:
                    import os
                    shutil.copy2(dispatcher_src, dispatcher_dest)
                    if os.name != "nt":
                        os.chmod(dispatcher_dest, 0o755)

                    if verbose:
                        console.print(f"[green]✓[/green] Updated: dispatch.sh")
                    upgraded_count += 1
                except Exception as e:
                    console.print(f"[red]✗[/red] Failed to upgrade dispatch.sh: {e}")

        # Upgrade hook scripts
        for category in ["conversation", "git"]:
            category_src = hooks_dir / category
            if not category_src.exists():
                continue

            for event_dir in category_src.iterdir():
                if not event_dir.is_dir():
                    continue

                dest_event_dir = workspace_dir / ".workspace" / "hooks" / category / event_dir.name
                if not dest_event_dir.exists():
                    if not dry_run:
                        dest_event_dir.mkdir(parents=True, exist_ok=True)

                for hook in event_dir.glob("*.sh"):
                    dest_hook = dest_event_dir / hook.name

                    if dry_run:
                        if verbose:
                            console.print(f"[dim]Would upgrade: {category}/{event_dir.name}/{hook.name}[/dim]")
                        upgraded_count += 1
                    else:
                        try:
                            import os
                            shutil.copy2(hook, dest_hook)
                            if os.name != "nt":
                                os.chmod(dest_hook, 0o755)

                            if verbose:
                                console.print(f"[green]✓[/green] Updated: {category}/{event_dir.name}/{hook.name}")
                            upgraded_count += 1
                        except Exception as e:
                            console.print(f"[red]✗[/red] Failed to upgrade {hook.name}: {e}")

    # Upgrade hooks documentation
    hooks_doc_src = template_dir / "hooks.md"
    hooks_doc_dest = workspace_dir / ".workspace" / "docs" / "hooks.md"

    if hooks_doc_src.exists() and hooks_doc_dest.parent.exists():
        if dry_run:
            if verbose:
                console.print(f"[dim]Would upgrade: hooks.md documentation[/dim]")
            upgraded_count += 1
        else:
            try:
                shutil.copy2(hooks_doc_src, hooks_doc_dest)
                if verbose:
                    console.print(f"[green]✓[/green] Updated: hooks.md documentation")
                upgraded_count += 1
            except Exception as e:
                console.print(f"[red]✗[/red] Failed to upgrade hooks.md: {e}")

    if upgraded_count > 0 and not verbose and not dry_run:
        console.print(f"[green]✓[/green] Updated {upgraded_count} infrastructure file(s)")

    return upgraded_count


def perform_upgrade(
    workspace_dir: Path,
    dry_run: bool,
    yes: bool,
    built_in_only: bool,
    regenerate: Optional[str],
    backup_dir: Path,
    verbose: bool,
):
    """Perform the workspace upgrade.

    Args:
        workspace_dir: Workspace root directory
        dry_run: If True, don't make changes
        yes: If True, use default answers
        built_in_only: If True, only upgrade built-in types
        regenerate: Type to force regenerate
        backup_dir: Directory for backups
        verbose: Show detailed progress
    """
    # Load registry
    registry_path = workspace_dir / ".workspace" / "registry.json"
    registry = json.loads(registry_path.read_text())

    conversation_types = registry.get("conversation_types", {})
    tracker = StepTracker("Upgrade Progress")

    # Built-in conversation types that ship with Cortext
    built_in_types = {
        "brainstorm", "debug", "plan", "learn", "meeting", "review", "projectmanage"
    }

    upgraded_count = 0
    skipped_count = 0
    prompted_count = 0

    console.print("\nAnalyzing workspace...\n")

    # Check for missing built-in types and add them
    types_added = add_missing_builtin_types(workspace_dir, registry, dry_run, yes, verbose)
    if types_added > 0:
        upgraded_count += types_added
        if not dry_run:
            # Save registry with new types
            registry_path.write_text(json.dumps(registry, indent=2))
            # Reload conversation_types for further processing
            conversation_types = registry.get("conversation_types", {})

    # Check for missing slash commands and add them
    commands_added = add_missing_slash_commands(workspace_dir, dry_run, verbose)
    if commands_added > 0 and not dry_run:
        # Commit the new command files to git if applicable
        pass

    # Upgrade core infrastructure files (scripts, hooks, etc.)
    infrastructure_upgraded = upgrade_core_infrastructure(workspace_dir, dry_run, verbose)
    if infrastructure_upgraded > 0:
        upgraded_count += infrastructure_upgraded

    for type_id, type_config in conversation_types.items():
        is_built_in = type_config.get("built_in", False)

        # Skip custom types if built_in_only is set
        if not is_built_in and built_in_only:
            if verbose:
                console.print(f"[dim]Skipping custom type: {type_id}[/dim]")
            skipped_count += 1
            continue

        # Force regenerate if specified
        if regenerate and type_id == regenerate:
            if upgrade_type_files(
                workspace_dir, type_id, type_config, backup_dir, dry_run, yes, force=True, verbose=verbose
            ):
                upgraded_count += 1
            continue

        # Check if files need upgrading
        generated_with = type_config.get("generated_with", {})
        if not generated_with:
            console.print(f"[yellow]⚠[/yellow] {type_id}: No generation metadata, treating as unmodified")
            if upgrade_type_files(
                workspace_dir, type_id, type_config, backup_dir, dry_run, yes, force=False, verbose=verbose
            ):
                upgraded_count += 1
            continue

        # Check each file's status
        files_metadata = generated_with.get("files", {})
        modified_files = []
        unmodified_files = []

        for file_key, file_info in files_metadata.items():
            file_path = workspace_dir / file_info.get("path", "")
            original_hash = file_info.get("original_hash")

            status = get_file_status(file_path, original_hash)

            if status == FileStatus.MODIFIED:
                modified_files.append((file_key, file_path))
            elif status == FileStatus.UNMODIFIED:
                unmodified_files.append((file_key, file_path))
            elif status == FileStatus.DELETED:
                if verbose:
                    console.print(f"[dim]{type_id}: {file_path.name} was deleted[/dim]")

        # If no modifications, upgrade silently
        if not modified_files:
            if verbose:
                console.print(f"[green]✓[/green] {type_id}: unmodified, will upgrade")
            if upgrade_type_files(
                workspace_dir, type_id, type_config, backup_dir, dry_run, yes, force=False, verbose=verbose
            ):
                upgraded_count += 1
        else:
            # Has modifications - prompt user
            console.print(f"\n[yellow]⚠[/yellow] {type_id}: has modifications")
            for file_key, file_path in modified_files:
                console.print(f"  - {file_path.relative_to(workspace_dir)} (modified)")

            if not dry_run:
                if yes:
                    # Default action: backup and overwrite
                    if upgrade_type_files(
                        workspace_dir, type_id, type_config, backup_dir, dry_run, yes, force=True, verbose=verbose
                    ):
                        upgraded_count += 1
                else:
                    # Interactive prompt
                    choice = Prompt.ask(
                        f"How should {type_id} be handled?",
                        choices=["overwrite", "keep", "new", "diff", "skip"],
                        default="skip"
                    )

                    if choice == "overwrite":
                        if upgrade_type_files(
                            workspace_dir, type_id, type_config, backup_dir, dry_run, yes, force=True, verbose=verbose
                        ):
                            upgraded_count += 1
                    elif choice == "keep":
                        console.print(f"[dim]Keeping current {type_id} files[/dim]")
                        skipped_count += 1
                    elif choice == "new":
                        create_new_files(workspace_dir, type_id, type_config, verbose)
                        skipped_count += 1
                    elif choice == "diff":
                        show_type_diffs(workspace_dir, type_id, modified_files)
                        # Repeat prompt after showing diff
                        skipped_count += 1
                    else:
                        skipped_count += 1

                prompted_count += 1
            else:
                console.print(f"[dim]Would prompt for action[/dim]")

    # Update registry metadata
    if not dry_run:
        registry["workspace_meta"]["last_upgraded"] = datetime.now(timezone.utc).isoformat()
        registry["workspace_meta"]["cortext_version"] = get_cortext_version()
        registry_path.write_text(json.dumps(registry, indent=2))

    # Summary
    console.print(f"\n[bold]Upgrade Summary[/bold]")
    console.print(f"  Upgraded: {upgraded_count}")
    console.print(f"  Skipped: {skipped_count}")
    if prompted_count > 0:
        console.print(f"  Prompted: {prompted_count}")

    if upgraded_count > 0 and not dry_run:
        console.print(f"\n[green]✓[/green] Workspace upgraded to {get_cortext_version()}")
    elif dry_run:
        console.print(f"\n[dim]Dry run complete - no changes made[/dim]")


def upgrade_type_files(
    workspace_dir: Path,
    type_id: str,
    type_config: dict,
    backup_dir: Path,
    dry_run: bool,
    yes: bool,
    force: bool,
    verbose: bool,
) -> bool:
    """Upgrade files for a conversation type.

    Args:
        workspace_dir: Workspace root directory
        type_id: Type identifier
        type_config: Type configuration
        backup_dir: Backup directory
        dry_run: If True, don't make changes
        yes: If True, skip confirmations
        force: If True, backup and overwrite modified files
        verbose: Show detailed progress

    Returns:
        True if files were upgraded
    """
    if dry_run:
        if verbose:
            console.print(f"[dim]Would upgrade {type_id} files[/dim]")
        return True

    # Backup modified files if force is True
    if force:
        generated_with = type_config.get("generated_with", {})
        for file_key, file_info in generated_with.get("files", {}).items():
            file_path = workspace_dir / file_info.get("path", "")
            if file_path.exists():
                backup_path = create_backup(file_path, backup_dir)
                if verbose:
                    console.print(f"[dim]Backed up {file_path.name} to {backup_path.name}[/dim]")

    # Copy new files from package
    try:
        template_dir = get_template_dir()
        scripts_dir = get_scripts_dir()

        # Update script if it exists in package
        script_path = workspace_dir / type_config.get("script", "")
        script_name = script_path.name
        source_script = scripts_dir / "bash" / script_name
        if source_script.exists():
            shutil.copy2(source_script, script_path)
            if verbose:
                console.print(f"[dim]Updated {script_name}[/dim]")

        # Update template if it exists in package
        template_path = workspace_dir / type_config.get("template", "")
        template_name = template_path.name
        source_template = template_dir / template_name
        if source_template.exists():
            shutil.copy2(source_template, template_path)
            if verbose:
                console.print(f"[dim]Updated {template_name}[/dim]")

        # Recompute hashes
        new_metadata = compute_generated_files_metadata(workspace_dir, type_id, type_config)
        type_config["generated_with"] = new_metadata

        return True

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to upgrade {type_id}: {e}")
        return False


def create_new_files(workspace_dir: Path, type_id: str, type_config: dict, verbose: bool):
    """Create .new files for manual merge.

    Args:
        workspace_dir: Workspace root directory
        type_id: Type identifier
        type_config: Type configuration
        verbose: Show detailed progress
    """
    template_dir = get_template_dir()
    scripts_dir = get_scripts_dir()

    # Create .new files
    script_path = workspace_dir / type_config.get("script", "")
    source_script = scripts_dir / "bash" / script_path.name
    if source_script.exists():
        new_path = script_path.parent / f"{script_path.name}.new"
        shutil.copy2(source_script, new_path)
        console.print(f"[cyan]Created {new_path.relative_to(workspace_dir)}[/cyan]")

    template_path = workspace_dir / type_config.get("template", "")
    source_template = template_dir / template_path.name
    if source_template.exists():
        new_path = template_path.parent / f"{template_path.name}.new"
        shutil.copy2(source_template, new_path)
        console.print(f"[cyan]Created {new_path.relative_to(workspace_dir)}[/cyan]")


def show_type_diffs(workspace_dir: Path, type_id: str, modified_files: list):
    """Show diffs for modified files of a type.

    Args:
        workspace_dir: Workspace root directory
        type_id: Type identifier
        modified_files: List of (file_key, file_path) tuples
    """
    for file_key, file_path in modified_files:
        console.print(f"\n[bold]Diff for {file_path.name}:[/bold]")
        # Note: We don't have the original content stored, only the hash
        # So we can't show the actual diff without loading from package
        console.print("[dim]Original content hash differs from current[/dim]")
        console.print("[dim]Use --regenerate to see package version[/dim]")
