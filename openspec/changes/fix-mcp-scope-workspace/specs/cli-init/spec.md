## MODIFIED Requirements

### Requirement: MCP registration SHALL NOT include workspace-specific environment variables

The init command SHALL register MCP servers without workspace-specific environment variables, making registrations workspace-agnostic.

**ID:** `CLI-INIT-MCP-003` | **Priority:** High

#### Scenario: Claude Code MCP registration
- **GIVEN** user runs `cortext init` and selects Claude Code agent
- **WHEN** the command registers cortext-mcp
- **THEN** the registration SHALL NOT include `--env WORKSPACE_PATH`
- **AND** SHALL use `--scope local` for local configuration
- **AND** the command format SHALL be: `claude mcp add --transport stdio --scope local cortext -- cortext-mcp`

#### Scenario: Gemini CLI MCP registration
- **GIVEN** user runs `cortext init` and selects Gemini agent
- **WHEN** the command updates `~/.gemini/settings.json`
- **THEN** the cortext entry SHALL NOT include `env` field
- **AND** SHALL only specify `command`, `args`, and `trust`

#### Scenario: OpenCode MCP registration
- **GIVEN** user runs `cortext init` and selects OpenCode agent
- **WHEN** the command creates/updates `opencode.json`
- **THEN** the cortext entry SHALL NOT include `environment` field
- **AND** SHALL only specify `type`, `command`, and `enabled`

#### Scenario: Re-registration in different workspace
- **GIVEN** cortext MCP is already registered
- **WHEN** user runs `cortext init` in a different workspace
- **THEN** no update is needed since registration is workspace-agnostic
- **AND** the existing registration works for all workspaces

---
