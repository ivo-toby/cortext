# Cortext MCP Server

The Cortext MCP (Model Context Protocol) server provides semantic search and context retrieval across your workspace.

## Features

**Keyword Search:**
- **Workspace Search** - Search across all conversations using ripgrep
- **Context Retrieval** - Get relevant past conversations for a topic
- **Decision History** - Look up past decisions

**Semantic Search (RAG):**
- **Semantic Search** - Find conceptually similar content using embeddings
- **Document Embedding** - Embed conversations for semantic search
- **Similar Documents** - Find documents similar to a given source
- **Embedding Status** - View embedding statistics

## Installation

The MCP server is installed automatically with Cortext:

```bash
# After installing cortext, the MCP server is available
which cortext-mcp
```

## Configuration

### Automatic Configuration (Recommended)

When you initialize a workspace, Cortext automatically configures the MCP server for your selected AI agents:

```bash
# Initialize with MCP auto-configuration
cortext init --ai claude           # Prompts for MCP setup
cortext init --ai claude --mcp     # Explicitly enable MCP
cortext init --ai claude --no-mcp  # Skip MCP configuration

# Configure for all agents
cortext init --ai all --mcp
```

The MCP server is configured at:
- **Claude Code**: `.claude/mcp_config.json` (workspace-local)
- **Gemini CLI**: `~/.gemini/settings.json` (global)
- **OpenCode**: `.opencode/mcp_config.json` (workspace-local)

### Manual Configuration

If you skipped MCP during init or have an existing workspace:

```bash
# Add MCP configuration to current workspace
cortext mcp install

# Configure for specific agent only
cortext mcp install --ai claude

# Overwrite existing configurations
cortext mcp install --force
```

### Configuration Format

For workspace-local configs (Claude, OpenCode):

```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "/absolute/path/to/workspace"
      }
    }
  }
}
```

For Gemini CLI (`~/.gemini/settings.json`):

```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {
        "WORKSPACE_PATH": "/absolute/path/to/workspace"
      },
      "trust": true
    }
  }
}
```

## Available Tools

### 1. search_workspace

Search across conversations, notes, and research.

**Parameters:**
- `query` (required): Search query (supports regex)
- `type` (optional): Filter by conversation type (brainstorm, debug, plan, learn, meeting, review, all)
- `date_range` (optional): Filter by date. Supports YYYY-MM (month) or YYYY-MM-DD (day) format
- `limit` (optional): Maximum results (default: 10)

**Examples:**
```
Search workspace for "authentication bug" in debug conversations
Filter by specific day: date_range="2025-11-10"
Filter by month: date_range="2025-11"
```

### 2. get_context

Get relevant context for a topic from past conversations.

**Parameters:**
- `topic` (required): Topic to search for
- `max_results` (optional): Maximum conversations to return (default: 5)

**Example:**
```
Get context about "API design decisions"
```

### 3. get_decision_history

Retrieve past decisions on a topic.

**Parameters:**
- `topic` (required): Topic or decision area

**Example:**
```
Get decision history for "database choice"
```

---

## RAG Tools

The following semantic search tools are available when RAG dependencies are installed (included by default).

### 4. embed_document

Embed a specific document or conversation for semantic search.

**Parameters:**
- `path` (required): Path to file or directory (relative or absolute)
- `workspace_path` (optional): Workspace root path (defaults to current directory)

**Example:**
```
Embed the conversation at brainstorm/2025-11-17/001-auth-patterns
```

### 5. embed_workspace

Embed all unembedded content in the workspace.

**Parameters:**
- `workspace_path` (optional): Workspace root path

**Example:**
```
Embed entire workspace for semantic search
```

### 6. search_semantic

Semantic search across workspace using embeddings. Finds conceptually similar content, not just keyword matches.

**Parameters:**
- `query` (required): Search query text
- `workspace_path` (optional): Workspace root path
- `n_results` (optional): Maximum results (default: 10)
- `conversation_type` (optional): Filter by type (brainstorm, debug, plan, etc.)
- `date_range` (optional): Filter by date (YYYY-MM or YYYY-MM-DD)

**Examples:**
```
Search for "authentication patterns" (finds related concepts like OAuth, JWT, sessions)
Filter by conversation type: conversation_type="plan"
Filter by date: date_range="2025-11"
```

**When to use semantic vs keyword search:**
- Use `search_semantic` when you want conceptually similar content
- Use `search_workspace` for exact keyword/regex matches

### 7. get_similar

Find documents similar to a given source document.

**Parameters:**
- `source_path` (required): Path to source document
- `workspace_path` (optional): Workspace root path
- `n_results` (optional): Number of similar documents (default: 5)

**Example:**
```
Find conversations similar to brainstorm/2025-11-17/001-auth-patterns
```

### 8. get_embedding_status

Get workspace embedding statistics and status.

**Parameters:**
- `workspace_path` (optional): Workspace root path

**Returns:**
- Total chunks embedded
- Number of documents
- Recent embedding activity

**Example:**
```
Check embedding status to see how many documents are searchable
```

## Requirements

- **ripgrep** - Fast search tool (install with package manager)
  - macOS: `brew install ripgrep`
  - Ubuntu/Debian: `apt install ripgrep`
  - Fedora: `dnf install ripgrep`

Check with: `cortext check`

## Testing

Test the MCP server directly:

```bash
# Start the server (it reads from stdin)
cortext-mcp

# Send a request (in another terminal or as JSON input)
echo '{"method":"tools/list","params":{}}' | cortext-mcp
```

## Troubleshooting

**Server not found:**
- Ensure Cortext is installed: `pip install -e .`
- Check PATH includes the installation bin directory

**MCP not connecting:**
- Verify configuration: Check `.claude/mcp_config.json` or equivalent
- Run `cortext mcp install` to reconfigure
- Check `cortext-mcp` is in PATH: `which cortext-mcp`

**Keyword search not working:**
- Install ripgrep: `brew install ripgrep` or equivalent
- Verify: `which rg`

**Semantic search not working:**
- First embed your workspace: Use `embed_workspace` tool or `cortext embed --all`
- Check embedding status: Use `get_embedding_status` tool
- RAG dependencies should be installed by default (fastembed, chromadb)

**No search results:**
- Ensure you're in a Cortext workspace directory
- Check that conversations exist
- For semantic search: Ensure documents are embedded
- Try a broader query

## Current Features (Phase 4 Complete)

- Semantic search with embeddings (fastembed - no PyTorch required)
- Automatic embedding via git post-commit hook
- Related conversation suggestions via `get_similar` tool
- See `Docs/rag-guide.md` for complete RAG documentation

## Future Enhancements (Phase 5)

- Automatic context injection
- Timeline queries
- Knowledge graph visualization
