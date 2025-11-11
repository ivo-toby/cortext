# Cortext MCP Server

The Cortext MCP (Model Context Protocol) server provides semantic search and context retrieval across your workspace.

## Features

- **Workspace Search** - Search across all conversations using ripgrep
- **Context Retrieval** - Get relevant past conversations for a topic
- **Decision History** - Look up past decisions

## Installation

The MCP server is installed automatically with Cortext:

```bash
# After installing cortext, the MCP server is available
which cortext-mcp
```

## Configuration

### For Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "cortext": {
      "command": "cortext-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

Claude Code will automatically detect and use the MCP server when in your workspace.

### For Other Tools

The MCP server uses stdio for communication. Any tool supporting the MCP protocol can connect to it.

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

**Search not working:**
- Install ripgrep: `brew install ripgrep` or equivalent
- Verify: `which rg`

**No results:**
- Ensure you're in a Cortext workspace directory
- Check that conversations exist in `conversations/`
- Try a broader query

## Future Enhancements (Phase 4)

- Semantic search with embeddings (Ollama integration)
- Automatic context injection
- Related conversation suggestions
- Timeline queries
