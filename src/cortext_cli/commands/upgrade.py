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
    get_builtin_conversation_types,
)
from cortext_cli.utils import (
    FileStatus,
    VersionStatus,
    StepTracker,
    compute_file_hash,
    get_file_status,
    get_commands_dir,
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
):
    """Upgrade workspace to current Cortext version."""

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
    """Check for and add missing slash command files.

    Args:
        workspace_dir: Workspace root directory
        dry_run: If True, don't make changes
        verbose: Show detailed progress

    Returns:
        Number of commands added
    """
    commands_dir = get_commands_dir()
    if not commands_dir.exists():
        return 0

    claude_commands_dir = workspace_dir / ".claude" / "commands"
    if not claude_commands_dir.exists():
        return 0

    # Get all command files from package
    package_commands = {f.name for f in commands_dir.glob("*.md")}

    # Get existing command files in workspace
    workspace_commands = {f.name for f in claude_commands_dir.glob("*.md")}

    # Find missing commands
    missing_commands = package_commands - workspace_commands

    if not missing_commands:
        return 0

    if verbose:
        console.print(f"\n[cyan]ℹ[/cyan]  Found {len(missing_commands)} new slash command(s): {', '.join(missing_commands)}")

    added_count = 0
    for cmd_name in missing_commands:
        if dry_run:
            console.print(f"[dim]Would add command: {cmd_name}[/dim]")
            continue

        try:
            src_file = commands_dir / cmd_name
            dest_file = claude_commands_dir / cmd_name
            shutil.copy2(src_file, dest_file)

            if verbose:
                console.print(f"[green]✓[/green] Added command: {cmd_name}")
            added_count += 1
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to add {cmd_name}: {e}")

    if added_count > 0 and not verbose:
        console.print(f"[green]✓[/green] Added {added_count} new slash command(s)")

    return added_count


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
