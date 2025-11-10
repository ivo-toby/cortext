"""Converters for cross-platform AI tool configurations."""

from pathlib import Path


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
