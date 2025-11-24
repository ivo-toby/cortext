# Proposal: Integrate RAG Tools into MCP Server

**Change ID:** integrate-rag-mcp
**Created:** 2025-11-17
**Status:** Proposed
**Type:** Feature Enhancement

## Problem Statement

The RAG pipeline tools (`embed_document`, `search_semantic`, `get_similar`, `get_embedding_status`) exist in `src/cortext_rag/mcp_tools.py` but are not exposed via the MCP server. Additionally, the MCP server is not automatically configured for supported AI agents (Claude, Gemini, OpenCode) during workspace initialization.

This means:
1. Agents cannot use semantic search capabilities via MCP
2. Users must manually configure MCP server for each agent
3. RAG functionality is only accessible via CLI, not through AI agents

## Proposed Solution

### 1. Expose RAG Tools in MCP Server
Integrate the 5 RAG tools from `cortext_rag/mcp_tools.py` into `cortext_mcp/server.py`:
- `embed_document` - Embed specific files/conversations
- `embed_workspace` - Embed entire workspace
- `search_semantic` - Semantic search across workspace
- `get_similar` - Find similar documents
- `get_embedding_status` - Get embedding statistics

### 2. Auto-Register MCP Server with Agents
During `cortext init`, automatically create MCP configuration files for each selected agent:
- **Claude Code**: `~/.config/claude/mcp_servers.json` or workspace-local config
- **Gemini CLI**: Appropriate Gemini MCP configuration
- **OpenCode**: AGENT_CONFIG.toml MCP settings

## Benefits

1. **Unified Interface**: Agents can access both keyword and semantic search through MCP
2. **Zero Configuration**: MCP server automatically configured during workspace init
3. **Cross-Agent Compatibility**: Same RAG tools available to all supported agents
4. **Better UX**: No manual setup required for semantic search

## Scope

**In Scope:**
- Add 5 RAG tools to MCP server tool list
- Implement tool handlers in MCP server
- Create MCP config templates for Claude, Gemini, OpenCode
- Add MCP registration step to init command
- Update documentation

**Out of Scope:**
- Cursor integration (Cursor doesn't use MCP protocol)
- Advanced RAG features (context injection, timeline queries)
- MCP server authentication/security

## Dependencies

- Existing RAG pipeline (Phase 4 - complete)
- MCP server implementation (exists)
- Agent configuration system (exists in init.py)

## Risks & Mitigations

**Risk**: MCP config location differs per agent/OS
**Mitigation**: Research correct config paths, provide fallback to workspace-local config

**Risk**: Breaking changes to existing MCP server users
**Mitigation**: Additive changes only, existing tools remain unchanged

**Risk**: RAG dependencies not installed
**Mitigation**: RAG is now required dependency, always available

## Success Criteria

1. All 5 RAG tools listed in `tools/list` MCP response
2. Each RAG tool successfully callable via MCP `tools/call`
3. Claude Code can use `search_semantic` tool in a workspace
4. MCP config automatically created for selected agents during init
5. Documentation updated with MCP+RAG examples

## Related Work

- `add-rag-pipeline` - Provides RAG tools (complete)
- Existing MCP server implementation
- Agent configuration in `init.py`
