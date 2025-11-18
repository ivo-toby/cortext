# Design: Integrate RAG Tools into MCP Server

## Architecture Overview

```
┌─────────────────┐
│   AI Agent      │ (Claude/Gemini/OpenCode)
│  (MCP Client)   │
└────────┬────────┘
         │ stdio/MCP protocol
         ▼
┌─────────────────┐
│ cortext-mcp     │
│   Server        │
├─────────────────┤
│ Keyword Tools:  │
│ - search_workspace      │
│ - get_context           │
│ - get_decision_history  │
├─────────────────┤
│ RAG Tools:      │  ◄── NEW
│ - embed_document        │
│ - embed_workspace       │
│ - search_semantic       │
│ - get_similar           │
│ - get_embedding_status  │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
 ┌──────┐ ┌──────┐ ┌────┐ ┌─────┐
 │Indexer│ │Embedder│ │Store│ │Retriever│
 └──────┘ └──────┘ └────┘ └─────┘
   (cortext_rag components)
```

## Component Changes

### 1. MCP Server (`src/cortext_mcp/server.py`)

**Changes Required:**
- Add 5 new tool definitions to `list_tools()`
- Add 5 new tool handlers to `call_tool()`
- Import RAG tool functions from `cortext_rag.mcp_tools`
- Handle RAG-specific errors gracefully

**Implementation Pattern:**
```python
from cortext_rag import mcp_tools

def list_tools(self):
    return {
        "tools": [
            # ... existing tools ...
            {
                "name": "search_semantic",
                "description": "Semantic search using embeddings",
                "inputSchema": {...}
            },
            # ... other RAG tools ...
        ]
    }

def call_tool(self, tool_name, arguments):
    if tool_name == "search_semantic":
        return mcp_tools.search_semantic(**arguments)
    # ... etc
```

### 2. Init Command (`src/cortext_cli/commands/init.py`)

**Changes Required:**
- Add MCP configuration step after agent configuration
- Create agent-specific MCP config files
- Handle different config locations per agent

**MCP Config Locations:**

| Agent | Config Path |
|-------|-------------|
| Claude Code | `~/.config/claude/mcp_servers.json` (global)<br>OR `<workspace>/.claude/mcp_config.json` (local) |
| Gemini CLI | `~/.gemini/mcp_servers.json` (TBD - needs research) |
| OpenCode | `<workspace>/.opencode/mcp_config.json` (workspace-local) |

**Decision**: Use workspace-local config for portability
- Easier to share workspaces
- No global config pollution
- Each workspace is self-contained

### 3. Config Templates

**Template Structure:**
```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "<workspace_path>"
      }
    }
  }
}
```

## Tool Specifications

### Tool: `embed_document`
**Purpose**: Embed specific file/conversation for semantic search

**Input:**
```json
{
  "path": "string (relative or absolute path)",
  "workspace_path": "string (optional)"
}
```

**Output:**
```json
{
  "success": true,
  "embedded": 3,
  "skipped": 0,
  "total_files": 3,
  "errors": null
}
```

### Tool: `embed_workspace`
**Purpose**: Embed all workspace content

**Input:**
```json
{
  "workspace_path": "string (optional)"
}
```

**Output:**
```json
{
  "success": true,
  "embedded": 15,
  "skipped": 10
}
```

### Tool: `search_semantic`
**Purpose**: Semantic search across workspace

**Input:**
```json
{
  "query": "string",
  "workspace_path": "string (optional)",
  "n_results": "number (default 10)",
  "conversation_type": "string (optional filter)",
  "date_range": "string (YYYY-MM or YYYY-MM-DD, optional)"
}
```

**Output:**
```json
{
  "success": true,
  "query": "authentication patterns",
  "num_results": 3,
  "results": [
    {
      "conversation": "001-auth-patterns",
      "score": 0.85,
      "text": "JWT tokens for stateless auth...",
      "source_path": "brainstorm/2025-11/001-auth-patterns/conversation.md"
    }
  ]
}
```

### Tool: `get_similar`
**Purpose**: Find documents similar to a given document

**Input:**
```json
{
  "source_path": "string",
  "workspace_path": "string (optional)",
  "n_results": "number (default 5)"
}
```

**Output:**
```json
{
  "success": true,
  "source": "path/to/source.md",
  "num_results": 3,
  "similar": [...]
}
```

### Tool: `get_embedding_status`
**Purpose**: Get workspace embedding statistics

**Input:**
```json
{
  "workspace_path": "string (optional)"
}
```

**Output:**
```json
{
  "success": true,
  "total_chunks": 127,
  "num_documents": 15,
  "db_path": "...",
  "recent_embeddings": [...]
}
```

## Error Handling

**Scenarios to handle:**
1. RAG dependencies not installed (shouldn't happen - now required)
2. Workspace not found
3. Vector store not initialized (no embeddings yet)
4. Document not found for `get_similar`
5. Invalid query parameters

**Strategy**: Return error object instead of throwing
```json
{
  "success": false,
  "error": "Workspace not found: /path/to/workspace"
}
```

## Testing Strategy

### Unit Tests
- Test each RAG tool handler in isolation
- Mock `cortext_rag.mcp_tools` functions
- Verify input schema validation
- Verify error handling

### Integration Tests
- Start MCP server
- Call each RAG tool via MCP protocol
- Verify responses match expected format
- Test with real workspace

### End-to-End Tests
- Configure Claude Code with MCP server
- Have Claude use `search_semantic` tool
- Verify results returned to Claude
- Test with multiple conversation types

## Backward Compatibility

**Existing MCP clients**: No breaking changes
- All existing tools remain unchanged
- New tools are additive only
- Schema version stays 0.1.0

**Existing workspaces**: Compatible
- MCP config can be added retroactively
- Users can run `cortext init` in existing workspace to add MCP config
- No data migration required

## Performance Considerations

1. **Lazy imports**: Import RAG tools only when needed
2. **Workspace context**: Server already tracks workspace path
3. **Connection reuse**: MCP server persistent, vector store cached
4. **UPSERT efficiency**: Content hash checking avoids re-embedding

## Security Considerations

1. **Filesystem access**: MCP server limited to workspace directory
2. **Command injection**: No shell commands executed by RAG tools
3. **Resource limits**: Consider embedding rate limits for large workspaces
4. **Privacy**: All processing local, no external API calls

## Migration Path

**Phase 1** (Current proposal):
- Add RAG tools to MCP server
- Auto-configure for Claude Code
- Document manual setup for other agents

**Phase 2** (Future):
- Research and implement Gemini/OpenCode MCP config
- Add MCP server health check command
- Add MCP server logging/debugging tools

**Phase 3** (Future):
- MCP server authentication
- Multi-workspace support
- Remote MCP server capability
