# Change: Fix MCP workspace scope with tool arguments

## Why

The MCP server's `WORKSPACE_PATH` environment variable persists across workspaces, causing tools to search in the wrong location when users switch between Cortext workspaces. This affects:

1. **Claude Code**: Global MCP registration keeps old path; "already exists" prevents updates
2. **Gemini**: Global `~/.gemini/settings.json` with hardcoded path
3. **Switching without init**: Users moving between existing workspaces without re-running `cortext init`

This is critical for Cortext's core value proposition - the MCP server must operate in the correct workspace to provide accurate search and context.

## What Changes

### Primary Fix: Add workspace_path argument to all MCP tools
- All MCP tools SHALL accept an optional `workspace_path` parameter
- AI agent passes current directory when calling tools
- Fallback to cwd if not provided
- Removes dependency on `WORKSPACE_PATH` environment variable

### Secondary Fix: Simplify MCP registration
- Remove `WORKSPACE_PATH` from all MCP configurations
- Registration becomes workspace-agnostic
- No more "already exists" conflicts when switching workspaces

## Impact

- **Affected specs**: `mcp-server`, `cli-init`
- **Affected code**:
  - `src/cortext_mcp/server.py` (add workspace_path to tool schemas and handlers)
  - `src/cortext_cli/commands/init.py:888-956` (remove WORKSPACE_PATH from registrations)
  - `src/cortext_cli/commands/mcp.py:196-265` (remove WORKSPACE_PATH from registrations)
  - `templates/mcp_config.json` (remove WORKSPACE_PATH)
  - `templates/opencode_config.json` (remove WORKSPACE_PATH)

## Benefits

- **Explicit control**: AI agent determines which workspace to operate in
- **No conflicts**: Registration is workspace-agnostic, no "already exists" issues
- **Simpler config**: No environment variables to manage
- **Consistent**: Matches pattern already used by RAG tools
