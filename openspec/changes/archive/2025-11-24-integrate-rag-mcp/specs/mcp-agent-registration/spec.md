# Spec: MCP Agent Registration

**Capability**: mcp-agent-registration
**Related To**: cli-init, mcp-server
**Status**: Proposed

## Overview

Automatically configure MCP server registration for supported AI agents during workspace initialization, eliminating manual setup and ensuring agents can access MCP tools immediately.

---

## ADDED Requirements

### Requirement: User Controls MCP Configuration via Flags

The `cortext init` command SHALL support `--mcp` and `--no-mcp` flags to control MCP server configuration.

#### Scenario: User Explicitly Enables MCP

```
GIVEN a user runs `cortext init --ai claude --mcp`
WHEN the initialization completes
THEN MCP configuration is created for Claude
AND no interactive prompt is shown
```

#### Scenario: User Explicitly Disables MCP

```
GIVEN a user runs `cortext init --ai claude --no-mcp`
WHEN the initialization completes
THEN NO MCP configuration is created
AND no interactive prompt is shown
```

#### Scenario: Flags Take Precedence Over Prompts

```
GIVEN a user runs `cortext init --ai claude --no-mcp`
WHEN the initialization runs
THEN the MCP configuration prompt is NOT shown
AND MCP is not configured
```

---

### Requirement: Interactive MCP Configuration Prompt

When MCP flags are NOT provided, the init command SHALL prompt the user to configure MCP.

#### Scenario: User Accepts MCP Prompt

```
GIVEN a user runs `cortext init --ai claude` (no MCP flags)
WHEN the initialization reaches the MCP configuration step
THEN the user is prompted: "Configure MCP server for AI agents? (Y/n)"
WHEN the user responds "Y" or presses Enter
THEN MCP configuration is created
```

#### Scenario: User Declines MCP Prompt

```
GIVEN a user runs `cortext init --ai claude` (no MCP flags)
WHEN the user is prompted for MCP configuration
AND the user responds "n"
THEN NO MCP configuration is created
AND a message explains how to add MCP later with `cortext mcp install`
```

---

### Requirement: Init Creates MCP Config for Selected Agents

The `cortext init` command SHALL create MCP server configuration files for each selected AI agent.

#### Scenario: Initialize Workspace with Claude Code

```
GIVEN a user runs `cortext init --ai claude`
WHEN the initialization completes
THEN a file exists at `<workspace>/.claude/mcp_config.json`
AND the file contains MCP server configuration for "cortext-mcp"
AND the configuration includes the workspace path
```

#### Scenario: Initialize with All Agents

```
GIVEN a user runs `cortext init --ai all`
WHEN the initialization completes
THEN MCP config files exist for Claude, Gemini, and OpenCode
AND each config is in the agent-specific directory
```

#### Scenario: Initialize Without MCP Config

```
GIVEN a user runs `cortext init` in an existing workspace
WHEN the workspace already has MCP config files
THEN the init command does not overwrite existing configs
AND logs that MCP is already configured
```

---

### Requirement: MCP Config Uses Workspace-Local Paths

MCP configuration files SHALL use workspace-relative paths for portability.

#### Scenario: Workspace is Moved

```
GIVEN a workspace initialized at `/home/user/workspace`
AND MCP is configured with workspace path
WHEN the workspace is moved to `/projects/workspace`
AND the MCP server is started
THEN the server correctly resolves paths relative to new location
```

---

### Requirement: Claude Code MCP Configuration

The init command SHALL create Claude Code-compatible MCP configuration.

#### Scenario: Claude Loads MCP Server

```
GIVEN a workspace with `.claude/mcp_config.json` created by init
WHEN Claude Code starts in the workspace
THEN Claude discovers the "cortext-mcp" server
AND the server is available for tool calls
AND tools include both keyword and semantic search
```

**Config Format:**
```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "<absolute_workspace_path>"
      }
    }
  }
}
```

---

### Requirement: Gemini CLI MCP Configuration

The init command SHALL create Gemini CLI-compatible MCP configuration in `~/.gemini/settings.json`.

#### Scenario: Gemini Uses MCP Server

```
GIVEN a workspace initialized with `--ai gemini`
WHEN the initialization completes
THEN `~/.gemini/settings.json` contains an mcpServers entry for "cortext"
AND the entry includes command "cortext-mcp" and workspace environment
WHEN Gemini CLI starts
THEN Gemini can call cortext-mcp tools
```

**Config Format** (merged into existing settings.json):
```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "<absolute_workspace_path>"
      },
      "trust": true
    }
  }
}
```

---

### Requirement: OpenCode MCP Configuration

The init command SHALL create OpenCode-compatible MCP configuration.

#### Scenario: OpenCode Uses MCP Server

```
GIVEN a workspace with `.opencode/mcp_config.json` created by init
WHEN OpenCode starts in the workspace
THEN OpenCode can call cortext-mcp tools via MCP protocol
```

**Config Format**: Similar to Claude, possibly integrated into `AGENT_CONFIG.toml`

---

### Requirement: MCP Config Validation

The init command SHALL validate that `cortext-mcp` command is available before creating config.

#### Scenario: MCP Command Not Found

```
GIVEN cortext-mcp is not in PATH
WHEN user runs `cortext init`
THEN init logs a warning that MCP server is not available
AND creates config files anyway (for future use)
AND informs user how to install cortext-mcp
```

#### Scenario: MCP Command Available

```
GIVEN cortext-mcp is in PATH
WHEN user runs `cortext init`
THEN init confirms MCP server is available
AND creates config files
AND logs success message
```

---

### Requirement: MCP Config Documentation

The init command SHALL provide clear feedback about MCP configuration.

#### Scenario: User is Informed About MCP

```
GIVEN a user runs `cortext init --ai claude`
WHEN the initialization completes
THEN the output includes:
  "MCP server configured for Claude Code"
  "Available tools: search_workspace, search_semantic, embed_document, ..."
AND links to documentation for testing MCP tools
```

---

## Implementation Notes

### Agent Config Paths

| Agent | MCP Config Location | Notes |
|-------|-------------------|-------|
| Claude Code | `<workspace>/.claude/mcp_config.json` | Workspace-local, Claude auto-discovers |
| Gemini CLI | `<workspace>/.gemini/mcp_config.json` | Format TBD - needs research |
| OpenCode | `<workspace>/.opencode/mcp_config.json` | May integrate with AGENT_CONFIG.toml |
| Cursor | N/A | Cursor doesn't support MCP protocol |

### Config Template

Store template at `templates/mcp_config.json`:
```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "{{WORKSPACE_PATH}}"
      }
    }
  }
}
```

Replace `{{WORKSPACE_PATH}}` during init.

### Implementation Steps

1. Add `install_mcp_config()` function to `init.py`
2. Call after `configure_ai_tools()`
3. Check if `cortext-mcp` is in PATH
4. For each agent, copy and populate template
5. Log success/warnings

### Testing

Required tests:
- Unit: Test `install_mcp_config()` creates correct files
- Integration: Run `cortext init`, verify configs exist
- E2E: Start Claude with generated config, verify MCP works

### Backward Compatibility

Existing workspaces:
- Users can re-run `cortext init` to add MCP config
- Existing configs are not overwritten
- No data migration needed
