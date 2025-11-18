# Spec: MCP Install Command

**Capability**: mcp-install-command
**Related To**: mcp-agent-registration, cli-init
**Status**: Proposed

## Overview

Provide a standalone command to add MCP server configuration to existing workspaces, allowing users who skipped MCP during init or have existing workspaces to configure MCP later.

---

## ADDED Requirements

### Requirement: MCP Install Command Exists

The CLI SHALL provide a `cortext mcp install` command to add MCP configuration to the current workspace.

#### Scenario: User Installs MCP in Existing Workspace

```
GIVEN a workspace initialized without MCP configuration
WHEN a user runs `cortext mcp install`
THEN MCP configuration is added for all configured agents
AND the command outputs "MCP server configured for: Claude Code, Gemini CLI"
```

#### Scenario: User Not in Workspace

```
GIVEN a user is NOT in a Cortext workspace directory
WHEN the user runs `cortext mcp install`
THEN the command exits with error: "Not in a Cortext workspace. Run cortext init first."
```

---

### Requirement: MCP Install Detects Configured Agents

The `cortext mcp install` command SHALL detect which agents are configured and create MCP config for each.

#### Scenario: Workspace Has Claude and Gemini

```
GIVEN a workspace with `.claude/commands/` and `.gemini/commands/` directories
WHEN user runs `cortext mcp install`
THEN MCP config is created for both Claude and Gemini
AND the command lists which agents were configured
```

#### Scenario: Workspace Has Only Claude

```
GIVEN a workspace with only `.claude/commands/` directory
WHEN user runs `cortext mcp install`
THEN MCP config is created only for Claude
AND the command outputs "MCP server configured for: Claude Code"
```

---

### Requirement: MCP Install Supports Specific Agent Selection

The command SHALL support `--ai` flag to configure MCP for specific agents only.

#### Scenario: User Installs MCP for Claude Only

```
GIVEN a workspace with Claude and Gemini configured
WHEN user runs `cortext mcp install --ai claude`
THEN MCP config is created only for Claude
AND Gemini config is not modified
```

#### Scenario: User Installs MCP for All Agents

```
GIVEN a workspace with multiple agents
WHEN user runs `cortext mcp install --ai all`
THEN MCP config is created for all configured agents
```

---

### Requirement: MCP Install Preserves Existing Config

The command SHALL NOT overwrite existing MCP configurations by default.

#### Scenario: MCP Already Configured

```
GIVEN a workspace with existing `.claude/mcp_config.json`
WHEN user runs `cortext mcp install`
THEN the existing config is NOT overwritten
AND the command outputs "MCP already configured for: Claude Code"
AND suggests using `--force` to overwrite
```

#### Scenario: Force Overwrite Existing Config

```
GIVEN a workspace with existing MCP config
WHEN user runs `cortext mcp install --force`
THEN existing MCP configs are overwritten
AND the command outputs "MCP server reconfigured for: Claude Code"
```

---

### Requirement: MCP Install Validates MCP Server Available

The command SHALL check if `cortext-mcp` is available before creating configs.

#### Scenario: MCP Server Not in PATH

```
GIVEN `cortext-mcp` is not in PATH
WHEN user runs `cortext mcp install`
THEN the command warns: "cortext-mcp not found in PATH"
AND explains how to install: "Reinstall cortext or ensure cortext-mcp is accessible"
AND still creates config files (for future use)
```

#### Scenario: MCP Server Available

```
GIVEN `cortext-mcp` is in PATH
WHEN user runs `cortext mcp install`
THEN the command confirms: "MCP server available: cortext-mcp"
AND creates config files
```

---

### Requirement: MCP Install Provides Clear Output

The command SHALL provide clear feedback about what was configured.

#### Scenario: Successful Installation

```
GIVEN a workspace without MCP config
WHEN user runs `cortext mcp install`
THEN the output includes:
  "✓ MCP server configured for Claude Code"
  "✓ MCP server configured for Gemini CLI"
  "  Config: ~/.gemini/settings.json"
  "  Config: <workspace>/.claude/mcp_config.json"
AND suggests how to test: "Test with: claude (in this workspace)"
```

---

### Requirement: MCP Install Handles Gemini Settings Merge

When configuring Gemini, the command SHALL merge the MCP config into existing `~/.gemini/settings.json`.

#### Scenario: Gemini Settings File Exists

```
GIVEN `~/.gemini/settings.json` exists with other configuration
WHEN user runs `cortext mcp install --ai gemini`
THEN the existing settings are preserved
AND the mcpServers.cortext entry is added/updated
AND the file remains valid JSON
```

#### Scenario: Gemini Settings File Does Not Exist

```
GIVEN `~/.gemini/settings.json` does not exist
WHEN user runs `cortext mcp install --ai gemini`
THEN `~/.gemini/settings.json` is created
AND contains only the mcpServers.cortext configuration
```

---

## Implementation Notes

### Command Signature

```bash
cortext mcp install [OPTIONS]

Options:
  --ai TEXT        Configure MCP for specific agent (claude, gemini, opencode, all)
  --force          Overwrite existing MCP configurations
  --help           Show this message and exit
```

### Logic Flow

1. Verify in Cortext workspace (check `.workspace/registry.json`)
2. Detect configured agents (check for `.claude/`, `.gemini/`, `.opencode/`)
3. Filter by `--ai` flag if provided
4. Check if `cortext-mcp` is in PATH (warn if not)
5. For each agent:
   - Check if MCP config already exists
   - Skip if exists and `--force` not provided
   - Create/update MCP config
6. Output summary of what was configured

### Code Location

Add to `src/cortext_cli/commands/mcp.py`:
```python
import typer
from pathlib import Path

app = typer.Typer(help="MCP server management commands")

@app.command("install")
def mcp_install(
    ai: str = typer.Option(None, help="Configure for specific agent"),
    force: bool = typer.Option(False, help="Overwrite existing configs"),
):
    """Add MCP server configuration to current workspace."""
    # Implementation here
```

Register in `src/cortext_cli/cli.py`:
```python
from cortext_cli.commands import mcp

app.add_typer(mcp.app, name="mcp")
```

### Testing

Required tests:
- Unit: Test agent detection logic
- Unit: Test Gemini settings.json merge
- Integration: Run `mcp install` in test workspace
- E2E: Install MCP, verify Claude can use tools

### Gemini Settings Merge Logic

```python
def merge_gemini_mcp_config(workspace_path: Path):
    settings_path = Path.home() / ".gemini" / "settings.json"

    # Read existing settings or create new
    if settings_path.exists():
        settings = json.loads(settings_path.read_text())
    else:
        settings = {}

    # Ensure mcpServers exists
    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    # Add/update cortext server
    settings["mcpServers"]["cortext"] = {
        "command": "cortext-mcp",
        "args": [],
        "env": {"WORKSPACE_PATH": str(workspace_path.absolute())},
        "trust": True
    }

    # Write back
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2))
```
