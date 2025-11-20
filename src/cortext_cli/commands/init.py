"""Init command to create a new Cortext workspace."""

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from cortext_cli.converters import (
    convert_claude_commands_to_gemini,
    create_opencode_config,
)
from cortext_cli.utils import (
    AGENT_CONFIG,
    StepTracker,
    get_commands_dir,
    get_git_hooks_dir,
    get_hooks_dir,
    get_scripts_dir,
    get_template_dir,
)

console = Console()


def is_path_like(value: str) -> bool:
    """Check if a value looks like a filesystem path rather than a simple name.

    Returns True for paths like: '.', '..', '/foo', '~/bar', './baz', '../qux'
    Returns False for simple names like: 'myworkspace', 'ai-project'
    """
    # Check for path-like patterns
    if value.startswith('.') or value.startswith('/') or value.startswith('~'):
        return True
    if '/' in value:
        return True
    return False


def prompt_for_location() -> Path:
    """Interactively prompt user for workspace location.

    Offers choices:
    - Current directory
    - Default location (~/ai-workspace)
    - Custom path
    """
    cwd = Path.cwd()

    console.print("\n[cyan]Where would you like to create the workspace?[/cyan]\n")
    console.print(f"  [dim]1.[/dim] Current directory: [green]{cwd}[/green]")
    console.print(f"  [dim]2.[/dim] Default location: [green]~/ai-workspace[/green]")
    console.print(f"  [dim]3.[/dim] Custom path")

    choice = Prompt.ask(
        "\nSelect option",
        choices=["1", "2", "3"],
        default="1"
    )

    if choice == "1":
        return cwd
    elif choice == "2":
        return Path.home() / "ai-workspace"
    else:  # choice == "3"
        while True:
            custom_path = Prompt.ask("Enter custom path").strip()
            if custom_path:
                path = Path(custom_path).expanduser().resolve()
                return path
            console.print("[yellow]Please enter a valid path[/yellow]")


def init(
    workspace_name: Optional[str] = typer.Argument(
        None, help="Path or name for the workspace (e.g., '.', '/path/to/workspace', or 'myworkspace')"
    ),
    ai: str = typer.Option(
        "claude", help="AI tool to configure (claude, opencode, gemini, all)"
    ),
    path: Optional[str] = typer.Option(
        None, help="Explicit path for workspace (takes precedence over positional argument)"
    ),
    mcp: bool = typer.Option(
        None, help="Enable MCP server configuration for AI agents"
    ),
    no_mcp: bool = typer.Option(
        False, help="Disable MCP server configuration"
    ),
):
    """Initialize a new Cortext workspace.

    Examples:
        cortext init              # Interactive prompt for location
        cortext init .            # Initialize in current directory
        cortext init ..           # Initialize in parent directory
        cortext init ~/mywork     # Initialize in home-relative path
        cortext init /opt/ai      # Initialize in absolute path
        cortext init myworkspace  # Initialize in ~/myworkspace (backward compat)
    """
    console.print(
        Panel.fit(
            "[bold cyan]🧠 Cortext Workspace Initialization[/bold cyan]",
            border_style="cyan",
        )
    )

    # Determine workspace path
    if path:
        # Explicit --path option takes precedence
        workspace_dir = Path(path).expanduser().resolve()
    elif workspace_name:
        # Check if it looks like a path or a simple name
        if is_path_like(workspace_name):
            # Treat as filesystem path
            workspace_dir = Path(workspace_name).expanduser().resolve()
        else:
            # Treat as name appended to home (backward compatible)
            workspace_dir = Path.home() / workspace_name
    else:
        # No arguments - prompt user for location
        workspace_dir = prompt_for_location()

    # Check if directory exists
    if workspace_dir.exists() and any(workspace_dir.iterdir()):
        console.print(
            f"\n[yellow]⚠ Directory already exists:[/yellow] {workspace_dir}"
        )
        if not Confirm.ask("Initialize workspace here anyway?"):
            console.print("[dim]Cancelled.[/dim]")
            raise typer.Exit()

    # Create workspace directory
    workspace_dir.mkdir(parents=True, exist_ok=True)
    tracker = StepTracker("Initializing Workspace")

    try:
        # Initialize git if not already initialized
        git_dir = workspace_dir / ".git"
        if not git_dir.exists():
            subprocess.run(
                ["git", "init"], cwd=workspace_dir, check=True, capture_output=True
            )
            tracker.add_step("Initialized git repository")
        else:
            tracker.add_info("Git repository already exists")

        # Create directory structure
        create_workspace_structure(workspace_dir, tracker)

        # Copy templates
        copy_templates(workspace_dir, tracker)

        # Copy scripts
        copy_scripts(workspace_dir, tracker)

        # Copy hooks
        copy_hooks(workspace_dir, tracker)

        # Configure AI tools
        configure_ai_tools(workspace_dir, ai, tracker)

        # Create initial registry
        registry = create_registry(workspace_dir, tracker)

        # Create conversation type folders based on registry
        create_conversation_type_folders(workspace_dir, registry, tracker)

        # Create initial constitution
        create_constitution(workspace_dir, tracker)

        # Install git hooks
        install_git_hooks(workspace_dir, tracker)

        # Configure MCP server registration
        configure_mcp(workspace_dir, ai, mcp, no_mcp, tracker)

        # Initial git commit
        try:
            subprocess.run(
                ["git", "add", "."], cwd=workspace_dir, check=True, capture_output=True
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "[workspace] Initialize Cortext workspace\n\n"
                    "Created workspace structure with templates, scripts, and configuration.\n"
                    f"AI tools configured: {ai}",
                ],
                cwd=workspace_dir,
                check=True,
                capture_output=True,
            )
            tracker.add_step("Created initial git commit")
        except subprocess.CalledProcessError:
            tracker.add_warning("Git commit failed (may be nothing to commit)")

        # Display results
        tracker.display()
        console.print(
            f"\n[green]✓ Workspace initialized successfully![/green]\n\n"
            f"[cyan]Location:[/cyan] {workspace_dir}\n\n"
            f"[cyan]Next steps:[/cyan]\n"
            f"  1. cd {workspace_dir}\n"
            f"  2. Review and customize .workspace/memory/constitution.md\n"
            f"  3. Start your first conversation with your AI tool\n"
        )

        # Tool-specific instructions
        if ai in ["claude", "all"]:
            console.print(
                f"\n[cyan]Claude Code:[/cyan]\n"
                f"  - Run 'claude' in the workspace directory\n"
                f"  - Available commands: /workspace.brainstorm, /workspace.debug, etc.\n"
            )

    except Exception as e:
        console.print(f"\n[red]✗ Error during initialization:[/red] {e}")
        raise typer.Exit(code=1)


def create_workspace_structure(workspace_dir: Path, tracker: StepTracker):
    """Create the .workspace directory structure."""
    workspace_config = workspace_dir / ".workspace"

    directories = [
        workspace_config / "memory",
        workspace_config / "scripts" / "bash",
        workspace_config / "scripts" / "powershell",
        workspace_config / "templates",
        workspace_config / "exports",
        workspace_config / "hooks" / "conversation" / "on-create.d",
        workspace_config / "hooks" / "conversation" / "on-archive.d",
        workspace_config / "hooks" / "git" / "pre-commit.d",
        workspace_config / "hooks" / "git" / "post-checkout.d",
        workspace_config / "docs",
        workspace_dir / "research",
        workspace_dir / "ideas",
        workspace_dir / "notes",
        workspace_dir / "projects",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # Create .gitignore for workspace
    gitignore_path = workspace_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """# Cortext workspace ignores

# RAG/Embeddings data (regenerated from source)
.cortext_rag/
.workspace/embeddings/

# OS files
.DS_Store
Thumbs.db
"""
        gitignore_path.write_text(gitignore_content)

    tracker.add_step("Created directory structure")


def copy_templates(workspace_dir: Path, tracker: StepTracker):
    """Copy template files to workspace."""
    template_dir = get_template_dir()
    dest_dir = workspace_dir / ".workspace" / "templates"

    if not template_dir.exists():
        tracker.add_warning("Template directory not found, skipping templates")
        return

    # Copy all markdown templates
    templates_copied = 0
    for template_file in template_dir.glob("*.md"):
        dest_file = dest_dir / template_file.name
        shutil.copy2(template_file, dest_file)
        templates_copied += 1

    if templates_copied > 0:
        tracker.add_step(f"Copied {templates_copied} templates")
    else:
        tracker.add_info("No templates found to copy")


def copy_scripts(workspace_dir: Path, tracker: StepTracker):
    """Copy script files to workspace."""
    scripts_dir = get_scripts_dir()
    dest_bash = workspace_dir / ".workspace" / "scripts" / "bash"
    dest_ps = workspace_dir / ".workspace" / "scripts" / "powershell"

    if not scripts_dir.exists():
        tracker.add_warning("Scripts directory not found, skipping scripts")
        return

    scripts_copied = 0

    # Copy bash scripts
    bash_scripts = scripts_dir / "bash"
    if bash_scripts.exists():
        for script_file in bash_scripts.glob("*.sh"):
            dest_file = dest_bash / script_file.name
            shutil.copy2(script_file, dest_file)
            # Make executable on Unix systems
            if os.name != "nt":
                os.chmod(dest_file, 0o755)
            scripts_copied += 1

    # Copy PowerShell scripts
    ps_scripts = scripts_dir / "powershell"
    if ps_scripts.exists():
        for script_file in ps_scripts.glob("*.ps1"):
            dest_file = dest_ps / script_file.name
            shutil.copy2(script_file, dest_file)
            scripts_copied += 1

    if scripts_copied > 0:
        tracker.add_step(f"Copied {scripts_copied} scripts")
    else:
        tracker.add_info("No scripts found to copy")


def copy_hooks(workspace_dir: Path, tracker: StepTracker):
    """Copy hook scripts to workspace."""
    hooks_dir = get_hooks_dir()
    dest_hooks = workspace_dir / ".workspace" / "hooks"

    if not hooks_dir.exists():
        tracker.add_warning("Hooks directory not found, skipping hooks")
        return

    hooks_copied = 0

    # Copy dispatcher
    dispatcher_src = hooks_dir / "dispatch.sh"
    if dispatcher_src.exists():
        dispatcher_dest = dest_hooks / "dispatch.sh"
        shutil.copy2(dispatcher_src, dispatcher_dest)
        if os.name != "nt":
            os.chmod(dispatcher_dest, 0o755)
        hooks_copied += 1

    # Copy hook scripts from subdirectories
    for category in ["conversation", "git"]:
        category_src = hooks_dir / category
        if not category_src.exists():
            continue

        for event_dir in category_src.iterdir():
            if not event_dir.is_dir():
                continue

            dest_event_dir = dest_hooks / category / event_dir.name
            dest_event_dir.mkdir(parents=True, exist_ok=True)

            for script in event_dir.glob("*.sh"):
                dest_script = dest_event_dir / script.name
                shutil.copy2(script, dest_script)
                if os.name != "nt":
                    os.chmod(dest_script, 0o755)
                hooks_copied += 1

    if hooks_copied > 0:
        tracker.add_step(f"Copied {hooks_copied} hook scripts")
    else:
        tracker.add_info("No hooks found to copy")

    # Copy hooks documentation
    template_dir = get_template_dir()
    hooks_doc_src = template_dir / "hooks.md"
    if hooks_doc_src.exists():
        docs_dir = workspace_dir / ".workspace" / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        hooks_doc_dest = docs_dir / "hooks.md"
        shutil.copy2(hooks_doc_src, hooks_doc_dest)
        tracker.add_step("Created hooks documentation")


def configure_ai_tools(workspace_dir: Path, ai: str, tracker: StepTracker):
    """Configure AI tool slash commands."""
    commands_dir = get_commands_dir()

    if not commands_dir.exists():
        tracker.add_warning("Commands directory not found, skipping AI configuration")
        return

    tools_to_configure = ["claude", "opencode", "gemini", "cursor"] if ai == "all" else [ai]
    configured_tools = []

    for tool in tools_to_configure:
        if tool == "claude":
            # Copy Claude commands
            claude_dir = workspace_dir / ".claude" / "commands"
            claude_dir.mkdir(parents=True, exist_ok=True)
            for cmd_file in commands_dir.glob("*.md"):
                dest_file = claude_dir / cmd_file.name
                shutil.copy2(cmd_file, dest_file)
            configured_tools.append("Claude Code")

        elif tool == "gemini":
            # Convert source commands to Gemini TOML (independent of Claude)
            gemini_dir = workspace_dir / ".gemini" / "commands"
            converted = convert_claude_commands_to_gemini(commands_dir, gemini_dir)
            if converted:
                configured_tools.append(f"Gemini CLI ({len(converted)} commands)")

        elif tool == "opencode":
            # Create OpenCode configuration
            create_opencode_config(workspace_dir)
            # Copy commands to OpenCode format (same as Claude for now)
            opencode_dir = workspace_dir / ".opencode" / "command"
            opencode_dir.mkdir(parents=True, exist_ok=True)
            for cmd_file in commands_dir.glob("*.md"):
                dest_file = opencode_dir / cmd_file.name
                shutil.copy2(cmd_file, dest_file)
            configured_tools.append("OpenCode")

        elif tool == "cursor":
            # Copy Cursor rules
            template_dir = get_template_dir()
            cursorrules_src = template_dir / "cursorrules"
            if cursorrules_src.exists():
                cursorrules_dest = workspace_dir / ".cursorrules"
                shutil.copy2(cursorrules_src, cursorrules_dest)
                configured_tools.append("Cursor")

    if configured_tools:
        tracker.add_step(f"Configured: {', '.join(configured_tools)}")
    else:
        tracker.add_info("AI tool directories created")


def create_registry(workspace_dir: Path, tracker: StepTracker):
    """Create the initial conversation type registry."""
    registry_path = workspace_dir / ".workspace" / "registry.json"

    registry = {
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "conversation_types": {
            "brainstorm": {
                "name": "Brainstorm",
                "folder": "brainstorm",
                "template": ".workspace/templates/brainstorm.md",
                "command": "/workspace.brainstorm",
                "script": ".workspace/scripts/bash/brainstorm.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Ideation and exploration",
                "sections": ["goals", "ideas", "themes", "next-steps"],
            },
            "debug": {
                "name": "Debug",
                "folder": "debug",
                "template": ".workspace/templates/debug-session.md",
                "command": "/workspace.debug",
                "script": ".workspace/scripts/bash/debug.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Problem solving and troubleshooting",
                "sections": ["problem", "investigation", "solution", "learnings"],
            },
            "plan": {
                "name": "Plan",
                "folder": "plan",
                "template": ".workspace/templates/feature-planning.md",
                "command": "/workspace.plan",
                "script": ".workspace/scripts/bash/plan.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Feature and project planning",
                "sections": ["goals", "requirements", "approach", "tasks"],
            },
            "learn": {
                "name": "Learn",
                "folder": "learn",
                "template": ".workspace/templates/learning-notes.md",
                "command": "/workspace.learn",
                "script": ".workspace/scripts/bash/learn.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Learning notes and documentation",
                "sections": ["topic", "notes", "examples", "references"],
            },
            "meeting": {
                "name": "Meeting",
                "folder": "meeting",
                "template": ".workspace/templates/meeting-notes.md",
                "command": "/workspace.meeting",
                "script": ".workspace/scripts/bash/meeting.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Meeting notes and action items",
                "sections": ["attendees", "agenda", "notes", "actions"],
            },
            "review": {
                "name": "Review",
                "folder": "review",
                "template": ".workspace/templates/review-template.md",
                "command": "/workspace.review",
                "script": ".workspace/scripts/bash/review.sh",
                "built_in": True,
                "created": datetime.now().isoformat(),
                "description": "Code and design review",
                "sections": ["overview", "feedback", "suggestions", "decision"],
            },
        },
        "statistics": {"total_conversations": 0, "by_type": {}},
    }

    registry_path.write_text(json.dumps(registry, indent=2))
    tracker.add_step("Created conversation type registry")

    return registry


def create_conversation_type_folders(
    workspace_dir: Path, registry: dict, tracker: StepTracker
):
    """Create folders for each conversation type defined in the registry."""
    conversation_types = registry.get("conversation_types", {})
    folders_created = 0

    for type_name, type_config in conversation_types.items():
        folder_path = type_config.get("folder", type_name)
        full_path = workspace_dir / folder_path

        try:
            # Create the folder
            full_path.mkdir(parents=True, exist_ok=True)

            # Add .gitkeep file so git tracks the empty folder
            gitkeep_path = full_path / ".gitkeep"
            if not gitkeep_path.exists():
                gitkeep_path.touch()

            folders_created += 1
        except Exception as e:
            tracker.add_warning(f"Could not create folder {folder_path}: {e}")

    if folders_created > 0:
        tracker.add_step(f"Created {folders_created} conversation type folders")
    else:
        tracker.add_info("No conversation type folders created")


def create_constitution(workspace_dir: Path, tracker: StepTracker):
    """Create initial constitution files."""
    memory_dir = workspace_dir / ".workspace" / "memory"

    # Constitution template
    constitution = """# Personal Constitution

**Last Updated:** {date}

This document defines your working style, principles, and preferences. All AI tools read this file to understand how to work with you effectively.

---

## Communication Style

### Tone & Approach
- **Formality:** [Casual / Professional / Mix]
- **Response Length:** [Concise / Detailed / Varies by context]
- **Thinking Style:** [Step-by-step / Big picture first / Both]

### Preferred Formats
- Code snippets with explanations
- Bullet points for clarity
- Examples when introducing new concepts
- Analogies for complex ideas

---

## Working Principles

### Development Practices
- Write tests [before/after/alongside] implementation
- Prioritize [readability/performance/maintainability]
- Documentation: [Inline comments/Separate docs/Both]
- Error handling: [Explicit/Graceful/Fail-fast]

### Code Review
- Focus on [logic/style/security/all]
- Provide [brief/detailed] feedback
- Suggest alternatives when critiquing

---

## Technical Preferences

### Languages & Frameworks
**Primary:**
- [Your main programming languages]

**Familiar with:**
- [Languages you know but don't use daily]

**Learning:**
- [Technologies you're currently exploring]

### Tools & Environment
- Editor: [VS Code / Vim / etc.]
- Terminal: [Bash / Zsh / Fish / PowerShell]
- Version Control: [Git workflow preferences]

---

## Guardrails & Boundaries

### Technologies to Prefer
- [Specific libraries, frameworks, or tools you like]

### Technologies to Avoid
- [Tools or approaches you prefer not to use, with reasons]

### Architectural Principles
- [SOLID, DRY, KISS, etc. - your priorities]
- [Specific patterns you follow]

### Security & Compliance
- [Security practices you follow]
- [Compliance requirements if any]

---

## Context & Expertise

### Domain Knowledge
- [Your areas of expertise]
- [Industries or domains you work in]

### Current Focus
- [What you're working on right now]
- [Short-term learning goals]

### Long-term Goals
- [Career or skill development objectives]

---

## Notes

This is a living document. Update it as your preferences and context evolve.
"""

    constitution_path = memory_dir / "constitution.md"
    constitution_path.write_text(constitution.format(date=datetime.now().strftime("%Y-%m-%d")))

    # Context file
    context = """# Current Context

**Last Updated:** {date}

## Active Projects

### [Project Name]
- **Status:** [Planning / In Progress / On Hold]
- **Priority:** [High / Medium / Low]
- **Description:** [Brief description]
- **Key Files:** [Important files or directories]

## Current Focus Areas

- [ ] [Task or area of focus]
- [ ] [Another focus area]

## Blockers & Questions

- [Any current blockers or open questions]

---

**Note:** Update this regularly to keep AI assistants informed of your current work.
"""

    context_path = memory_dir / "context.md"
    context_path.write_text(context.format(date=datetime.now().strftime("%Y-%m-%d")))

    # Decisions log
    decisions = """# Decisions Log

**Purpose:** Track important technical and architectural decisions

---

## {date}

### [Decision Title]
**Context:** [What led to this decision]

**Options Considered:**
1. [Option 1] - [Pros/Cons]
2. [Option 2] - [Pros/Cons]

**Decision:** [What was chosen]

**Rationale:** [Why this was the best choice]

**Consequences:** [Impact and trade-offs]

---

Template for new decisions:
```markdown
## YYYY-MM-DD

### [Decision Title]
**Context:**
**Options Considered:**
**Decision:**
**Rationale:**
**Consequences:**
```
"""

    decisions_path = memory_dir / "decisions.md"
    decisions_path.write_text(decisions.format(date=datetime.now().strftime("%Y-%m-%d")))

    tracker.add_step("Created constitution and memory files")


def install_git_hooks(workspace_dir: Path, tracker: StepTracker):
    """Install git hooks that integrate with Cortext hooks system."""
    git_hooks_src = get_git_hooks_dir()
    git_hooks_dest = workspace_dir / ".git" / "hooks"

    if not git_hooks_src.exists():
        tracker.add_info("Git hooks directory not found, skipping")
        return

    if not git_hooks_dest.exists():
        tracker.add_warning("Git hooks directory not found (is git initialized?)")
        return

    hooks_installed = 0
    hooks_to_install = ["pre-commit", "post-checkout"]

    for hook_name in hooks_to_install:
        src_file = git_hooks_src / hook_name
        if not src_file.exists():
            continue

        dest_file = git_hooks_dest / hook_name

        if dest_file.exists():
            # Check if it's already our hook
            content = dest_file.read_text()
            if "Cortext" in content:
                continue  # Already installed

            # Append to existing hook
            with open(dest_file, "a") as f:
                f.write("\n\n# --- Cortext hooks integration ---\n")
                f.write(src_file.read_text())
        else:
            # Copy the hook
            shutil.copy2(src_file, dest_file)

        # Make executable
        if os.name != "nt":
            os.chmod(dest_file, 0o755)
        hooks_installed += 1

    if hooks_installed > 0:
        tracker.add_step(f"Installed {hooks_installed} git hook(s)")
    else:
        tracker.add_info("Git hooks already installed")


def configure_mcp(
    workspace_dir: Path,
    ai: str,
    mcp_flag: Optional[bool],
    no_mcp_flag: bool,
    tracker: StepTracker,
):
    """Configure MCP server registration for AI agents."""
    # Determine if MCP should be configured
    should_configure_mcp = _determine_mcp_preference(mcp_flag, no_mcp_flag)

    if not should_configure_mcp:
        tracker.add_info("MCP server configuration skipped")
        return

    # Check if cortext-mcp is available
    mcp_available = _check_mcp_command()
    if not mcp_available:
        tracker.add_warning(
            "cortext-mcp command not found in PATH. "
            "MCP configs will be created but may not work until cortext-mcp is available."
        )

    # Determine which agents to configure
    agents_to_configure = _get_agents_from_ai_option(ai)

    # Install MCP config for each agent
    configured_agents = []
    for agent in agents_to_configure:
        if _install_mcp_config_for_agent(workspace_dir, agent, tracker):
            configured_agents.append(agent)

    if configured_agents:
        agent_list = ", ".join(configured_agents)
        tracker.add_step(f"Configured MCP server for: {agent_list}")
    else:
        tracker.add_info("No MCP configurations created")


def _determine_mcp_preference(mcp_flag: Optional[bool], no_mcp_flag: bool) -> bool:
    """Determine if MCP should be configured based on flags and user prompt."""
    # Flags take precedence
    if no_mcp_flag:
        return False
    if mcp_flag is not None:
        return mcp_flag

    # Interactive prompt
    return Confirm.ask(
        "\n[cyan]Configure MCP server for AI agents?[/cyan]",
        default=True,
    )


def _check_mcp_command() -> bool:
    """Check if cortext-mcp command is available."""
    try:
        result = subprocess.run(
            ["which", "cortext-mcp"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _get_agents_from_ai_option(ai: str) -> list[str]:
    """Get list of agents to configure from ai option."""
    if ai == "all":
        return ["claude", "gemini", "opencode"]
    else:
        return [ai]


def _install_mcp_config_for_agent(
    workspace_dir: Path, agent: str, tracker: StepTracker
) -> bool:
    """Install MCP config for a specific agent."""
    if agent == "claude":
        return _install_claude_mcp_config(workspace_dir, tracker)
    elif agent == "gemini":
        return _install_gemini_mcp_config(workspace_dir, tracker)
    elif agent == "opencode":
        return _install_opencode_mcp_config(workspace_dir, tracker)
    else:
        # Cursor doesn't support MCP
        return False


def _install_claude_mcp_config(workspace_dir: Path, tracker: StepTracker) -> bool:
    """Install MCP config for Claude Code using 'claude mcp add' command."""
    # Try to register the MCP server using claude CLI
    try:
        # Check if claude CLI is available
        result = subprocess.run(
            ["claude", "mcp", "add", "--transport", "stdio", "--scope", "local",
             "cortext", "--env", f"WORKSPACE_PATH={workspace_dir.absolute()}",
             "--", "cortext-mcp"],
            cwd=workspace_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            tracker.add_step("Registered cortext-mcp with Claude Code")
            return True
        elif "already exists" in result.stderr.lower():
            tracker.add_info("MCP server already registered with Claude Code")
            return True
        else:
            # Fall back to instructions
            tracker.add_warning(
                "Could not auto-register MCP server. "
                f"Run: claude mcp add --transport stdio --scope local cortext --env WORKSPACE_PATH={workspace_dir.absolute()} -- cortext-mcp"
            )
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        # Claude CLI not available or command failed
        tracker.add_warning(
            "Claude CLI not available. To enable MCP server, run:\n"
            f"  claude mcp add --transport stdio --scope local cortext --env WORKSPACE_PATH={workspace_dir.absolute()} -- cortext-mcp"
        )
        return False


def _install_gemini_mcp_config(workspace_dir: Path, tracker: StepTracker) -> bool:
    """Install MCP config for Gemini CLI (global settings.json merge)."""
    import json as json_module

    # Gemini uses global settings file
    settings_path = Path.home() / ".gemini" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing settings or create new
    if settings_path.exists():
        try:
            settings = json_module.loads(settings_path.read_text())
        except json_module.JSONDecodeError:
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
    settings_path.write_text(json_module.dumps(settings, indent=2))
    return True


def _install_opencode_mcp_config(workspace_dir: Path, tracker: StepTracker) -> bool:
    """Install MCP config for OpenCode (workspace root opencode.json)."""
    import json as json_module

    template_dir = get_template_dir()
    template_path = template_dir / "opencode_config.json"

    if not template_path.exists():
        tracker.add_warning("OpenCode MCP config template not found")
        return False

    # Check if opencode.json already exists
    config_path = workspace_dir / "opencode.json"

    if config_path.exists():
        # Merge with existing config
        try:
            existing_config = json_module.loads(config_path.read_text())
            if "mcp" not in existing_config:
                existing_config["mcp"] = {}

            # Add cortext MCP server
            existing_config["mcp"]["cortext"] = {
                "type": "local",
                "command": ["cortext-mcp"],
                "enabled": True,
                "environment": {
                    "WORKSPACE_PATH": str(workspace_dir.absolute())
                }
            }

            config_path.write_text(json_module.dumps(existing_config, indent=2))
            tracker.add_step("Merged MCP config into existing opencode.json")
            return True
        except json_module.JSONDecodeError:
            # If existing file is invalid, backup and create new
            config_path.rename(config_path.with_suffix(".json.bak"))
            tracker.add_warning("Backed up invalid opencode.json")

    # Create new config from template
    template_content = template_path.read_text()
    config_content = template_content.replace(
        "{{WORKSPACE_PATH}}", str(workspace_dir.absolute())
    )

    config_path.write_text(config_content)
    tracker.add_step("Created opencode.json with MCP config")
    return True
