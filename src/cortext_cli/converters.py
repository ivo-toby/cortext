"""Converters for cross-platform AI tool configurations."""

from pathlib import Path

_CODEX_ARGUMENT_HINTS = {
    "workspace_brainstorm": "<topic>",
    "workspace_debug": "<problem>",
    "workspace_plan": "<feature>",
    "workspace_learn": "<subject>",
    "workspace_meeting": "<title>",
    "workspace_review": "<title>",
    "workspace_projectmanage": "<project-name>",
}


def convert_md_to_toml(md_path: Path) -> tuple[str, str]:
    """
    Convert markdown command to TOML format for Gemini CLI.

    Returns:
        tuple: (toml_content, command_name)
    """
    content = md_path.read_text()

    # Parse frontmatter for description
    description = ""
    prompt_content = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            prompt_content = parts[2].strip()

            # Extract description
            for line in frontmatter.split("\n"):
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break

    # Generate command name from filename
    command_name = md_path.stem.replace("workspace_", "")

    # Escape for TOML (handle quotes and backslashes)
    prompt_escaped = prompt_content.replace("\\", "\\\\").replace('"""', r'\"\"\"')
    description_escaped = description.replace('"', '\\"')

    # Generate TOML content
    toml_content = f'''description = "{description_escaped}"

prompt = """
{prompt_escaped}
"""
'''

    return toml_content, command_name


def convert_claude_commands_to_gemini(
    claude_dir: Path, gemini_dir: Path
) -> list[str]:
    """
    Convert all Claude markdown commands to Gemini TOML format.

    Returns:
        list: Names of converted commands
    """
    gemini_dir.mkdir(parents=True, exist_ok=True)
    converted = []

    for md_file in claude_dir.glob("*.md"):
        try:
            toml_content, command_name = convert_md_to_toml(md_file)
            toml_file = gemini_dir / f"{command_name}.toml"
            toml_file.write_text(toml_content)
            converted.append(command_name)
        except Exception as e:
            print(f"Warning: Could not convert {md_file.name}: {e}")

    return converted


def convert_md_for_codex(md_path: Path) -> tuple[str, str]:
    """Convert Claude markdown command to Codex prompt format.

    Strips Claude-specific frontmatter fields (name, tags, category) and
    rewrites frontmatter with only description and argument-hint.

    Returns:
        tuple: (codex_content, command_name)
    """
    content = md_path.read_text()

    description = ""
    prompt_content = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            prompt_content = parts[2].strip()

            for line in frontmatter.split("\n"):
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break

    command_name = md_path.stem
    argument_hint = _CODEX_ARGUMENT_HINTS.get(command_name)

    frontmatter_lines = []
    if description:
        frontmatter_lines.append(f"description: {description}")
    if argument_hint:
        frontmatter_lines.append(f"argument-hint: \"{argument_hint}\"")

    if frontmatter_lines:
        codex_content = f"---\n{chr(10).join(frontmatter_lines)}\n---\n\n{prompt_content}"
    else:
        codex_content = prompt_content

    return codex_content, command_name


def convert_claude_commands_to_codex(commands_dir: Path, codex_prompts_dir: Path) -> list[str]:
    """Convert all Claude markdown commands to Codex prompt format (deprecated).

    Codex custom prompts are deprecated. Prefer install_codex_skills() instead.

    Returns:
        list: Names of converted commands
    """
    codex_prompts_dir.mkdir(parents=True, exist_ok=True)
    converted = []

    for md_file in commands_dir.glob("*.md"):
        try:
            codex_content, command_name = convert_md_for_codex(md_file)
            dest_file = codex_prompts_dir / md_file.name
            dest_file.write_text(codex_content)
            converted.append(command_name)
        except Exception as e:
            print(f"Warning: Could not convert {md_file.name} for Codex: {e}")

    return converted


def convert_md_to_codex_skill(md_path: Path, skills_dir: Path) -> str:
    """Convert a Claude markdown command to a Codex skill directory.

    Creates <skills_dir>/<skill_name>/SKILL.md with name+description frontmatter.
    Codex loads skills from .agents/skills/ in the project and ~/.agents/skills/.

    Returns:
        skill_name (the directory name created)
    """
    content = md_path.read_text()

    description = ""
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            for line in frontmatter.split("\n"):
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break

    skill_name = md_path.stem.replace("_", "-")  # e.g. workspace-brainstorm
    skill_dir = skills_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_content = f"---\nname: {skill_name}\ndescription: {description}\n---\n\n{body}"
    (skill_dir / "SKILL.md").write_text(skill_content)

    return skill_name


def install_codex_skills(commands_dir: Path, skills_dir: Path) -> list[str]:
    """Convert all Claude markdown commands to Codex skills.

    Skills directory layout:
        <skills_dir>/<skill_name>/SKILL.md

    Codex discovers skills from .agents/skills/ at the project root and
    ~/.agents/skills/ for user-level skills.

    Returns:
        list: skill names installed
    """
    skills_dir.mkdir(parents=True, exist_ok=True)
    installed = []

    for md_file in commands_dir.glob("*.md"):
        try:
            skill_name = convert_md_to_codex_skill(md_file, skills_dir)
            installed.append(skill_name)
        except Exception as e:
            print(f"Warning: Could not convert {md_file.name} to Codex skill: {e}")

    return installed


def create_codex_workspace_agents_md(workspace_dir: Path) -> Path:
    """Create an AGENTS.md file for Codex at the workspace root.

    Codex reads AGENTS.md hierarchically for persistent instructions.

    Returns:
        Path to created AGENTS.md file
    """
    agents_content = """# Cortext Workspace — Codex Instructions

This is a Cortext workspace: a git-backed, locally-hosted platform for
AI-augmented knowledge work. All conversations are versioned in git.

## Key Files

- `.workspace/memory/constitution.md` — Read this first. It contains the
  user's working principles, preferences, and guidelines for all AI interactions.
- `.workspace/memory/context.md` — Current focus areas and active projects.
- `.workspace/memory/decisions.md` — Log of important decisions made.
- `.workspace/registry.json` — Tracks all conversation types and their metadata.

Always read `.workspace/memory/constitution.md` before starting any conversation.

## Conversation Types

Start a conversation by running the corresponding script. Each script creates
a structured document and an initial git commit.

| Type | Script | Purpose |
|------|--------|---------|
| Brainstorm | `.workspace/scripts/bash/brainstorm.sh "<topic>"` | Free-form ideation |
| Debug | `.workspace/scripts/bash/debug.sh "<problem>"` | Systematic troubleshooting |
| Plan | `.workspace/scripts/bash/plan.sh "<feature>"` | Feature/project planning |
| Learn | `.workspace/scripts/bash/learn.sh "<subject>"` | Learning documentation |
| Meeting | `.workspace/scripts/bash/meeting.sh "<title>"` | Meeting notes |
| Review | `.workspace/scripts/bash/review.sh "<title>"` | Code/design reviews |
| Project | `.workspace/scripts/bash/projectmanage.sh "<name>"` | Project tracking |

Custom conversation types are listed in `.workspace/registry.json` with their
scripts under `.workspace/scripts/bash/`.

## Workflow

1. Run the script for the desired conversation type to create a document.
2. Edit the document using standard file edit tools as the conversation progresses.
3. Commit work atomically to git with clear `[conversation]` prefix messages.
4. Cross-reference related past conversations when relevant.

## MCP Search

If the Cortext MCP server is running, you have access to `search_workspace`,
`get_context`, and `get_decision_history` tools for semantic search across
all past conversations.

## Git Conventions

- Commit format: `[conversation] <summary>`
- Conversation tags: `conv/{id}` (e.g., `conv/001-brainstorm-api`)
- Always work on the `main` branch unless otherwise specified.
"""

    agents_md_path = workspace_dir / "AGENTS.md"
    agents_md_path.write_text(agents_content)
    return agents_md_path


def create_opencode_config(workspace_dir: Path) -> Path:
    """
    Create OpenCode configuration that reads from constitution.

    Returns:
        Path to created config file
    """
    opencode_dir = workspace_dir / ".opencode"
    opencode_dir.mkdir(parents=True, exist_ok=True)

    # Create prompts directory
    prompts_dir = opencode_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    # Create workspace assistant prompt
    assistant_prompt = """You are a workspace assistant helping with AI-augmented knowledge work using Cortext.

Your role:
1. Help maintain organized conversations
2. Ensure proper git commits
3. Follow the user's constitution (.workspace/memory/constitution.md)
4. Cross-reference related conversations
5. Suggest relevant past insights from the workspace

Key files:
- constitution.md: User's working principles and preferences
- conversations/: All conversations organized chronologically
- registry.json: Tracks conversation types and metadata

When helping:
- ALWAYS read the constitution first to understand user preferences
- Maintain structured documentation using templates
- Use appropriate conversation types
- Commit work atomically to git with clear messages
- Search past conversations for relevant context
- Reference related work when applicable

Available conversation types:
- Brainstorm: Ideation and exploration
- Debug: Problem solving and troubleshooting
- Plan: Feature and project planning
- Learn: Learning notes and documentation
- Meeting: Meeting notes and action items
- Review: Code and design reviews

Be thorough, maintain consistency, and build on the user's existing knowledge base.
"""

    prompt_file = prompts_dir / "workspace_assistant.txt"
    prompt_file.write_text(assistant_prompt)

    # Create command directory
    command_dir = opencode_dir / "command"
    command_dir.mkdir(parents=True, exist_ok=True)

    return opencode_dir
