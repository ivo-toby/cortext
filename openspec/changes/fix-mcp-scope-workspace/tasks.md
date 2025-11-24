## 1. MCP Server Tool Arguments

- [ ] 1.1 Add `workspace_path` parameter to `search_workspace` tool schema
  - Type: string, optional
  - Description: "Workspace root path (defaults to current directory)"
- [ ] 1.2 Add `workspace_path` parameter to `get_context` tool schema
- [ ] 1.3 Add `workspace_path` parameter to `get_decision_history` tool schema
- [ ] 1.4 Update `search_workspace` method to accept and use `workspace_path` parameter
- [ ] 1.5 Update `get_context` method to accept and use `workspace_path` parameter
- [ ] 1.6 Update `get_decision_history` method to accept and use `workspace_path` parameter
- [ ] 1.7 Remove `WORKSPACE_PATH` environment variable handling from `main()`
- [ ] 1.8 Update `CortextMCPServer.__init__` to default `workspace_path` to `Path.cwd()`

## 2. Update MCP Registrations

- [ ] 2.1 Update `_install_claude_mcp_config` in `init.py` to remove `--env WORKSPACE_PATH`
- [ ] 2.2 Update `_install_claude_mcp_config` in `mcp.py` to remove `--env WORKSPACE_PATH`
- [ ] 2.3 Update `_install_gemini_mcp_config` in `init.py` to remove `env` from config
- [ ] 2.4 Update `_install_gemini_mcp_config` in `mcp.py` to remove `env` from config
- [ ] 2.5 Update `_install_opencode_mcp_config` in `init.py` to remove `environment` from config
- [ ] 2.6 Update `_install_opencode_mcp_config` in `mcp.py` to remove `environment` from config
- [ ] 2.7 Update `templates/mcp_config.json` to remove WORKSPACE_PATH
- [ ] 2.8 Update `templates/opencode_config.json` to remove WORKSPACE_PATH

## 3. Testing

- [ ] 3.1 Test MCP tools work without workspace_path (uses cwd)
- [ ] 3.2 Test MCP tools work with explicit workspace_path
- [ ] 3.3 Test `cortext init` creates registration without WORKSPACE_PATH
- [ ] 3.4 Test switching between workspaces works correctly
- [ ] 3.5 Test RAG tools still work with their existing workspace_path parameter

## 4. Documentation

- [ ] 4.1 Update MCP server documentation to reflect new tool signatures
- [ ] 4.2 Remove references to WORKSPACE_PATH environment variable
- [ ] 4.3 Update any examples showing MCP registration with env vars
