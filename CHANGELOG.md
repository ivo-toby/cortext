# Changelog

All notable changes to Cortext will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-10

### Added

#### Core CLI
- `cortext init` - Initialize new workspace with full directory structure
- `cortext check` - Verify required tools (git, ripgrep, ollama, tmux)
- `cortext list` - List all conversation types in workspace
- Constitution system for defining working principles
- Registry system for conversation type management
- Multi-AI tool configuration (Claude Code, Cursor, OpenCode, Gemini CLI)

#### Conversation Types (Templates + Scripts + Commands)
- **Brainstorm** - Ideation and exploration
- **Debug** - Systematic troubleshooting
- **Plan** - Feature and project planning
- **Learn** - Learning documentation
- **Meeting** - Meeting notes with action items
- **Review** - Code and design reviews
- **Add** - Create custom conversation types

#### Bash Scripts
- `common.sh` - Shared utilities for all scripts
- `brainstorm.sh`, `debug.sh`, `plan.sh`, `learn.sh`, `meeting.sh`, `review.sh` - Conversation starters
- `commit-session.sh` - Auto-commit current conversation
- `workspace-status.sh` - Display workspace overview

#### Claude Code Integration
- 7 slash commands: `/workspace.brainstorm`, `/workspace.debug`, `/workspace.plan`, `/workspace.learn`, `/workspace.meeting`, `/workspace.review`, `/workspace.add`
- Comprehensive command documentation with best practices

#### MCP Server
- `cortext-mcp` server with MCP protocol support
- `search_workspace` tool - Search conversations with ripgrep
- `get_context` tool - Retrieve relevant past conversations
- `get_decision_history` tool - Look up decision history
- Date range and type filtering
- JSON-based MCP protocol over stdio

#### Multi-AI Support
- **Claude Code**: Full support with slash commands and MCP
- **Cursor**: .cursorrules with workspace context
- **OpenCode**: Custom prompts and command structure
- **Gemini CLI**: Auto-conversion to TOML format
- Universal `--ai=all` flag for complete setup
- Constitution-based consistency across all tools

#### Documentation
- Comprehensive README with quick start
- Complete user guide (90+ sections)
- MCP server documentation
- Multi-AI support guide
- Detailed specification (1600+ lines)
- Task breakdown and progress tracking

#### Templates
- 6 conversation type templates (markdown)
- Constitution template with examples
- Context and decision log templates
- MCP configuration template
- Cursor rules template

### Infrastructure
- Python 3.11+ package with typer CLI
- Rich library for beautiful terminal output
- Git-based version control for all conversations
- Cross-platform support (Linux, macOS, Windows)
- Editable install support for development

### Philosophy
- Local-first (no data leaves your machine)
- Git as database (full version history)
- Tool agnostic (works with multiple AI tools)
- Constitution-driven (consistent behavior)
- Structured yet flexible (templates guide, don't constrain)

---

## [Unreleased]

### Planned for 0.2.0 (Phase 4 - RAG)
- Ollama integration for local embeddings
- Semantic search with vector store (ChromaDB/FAISS)
- Automatic context injection
- Related conversation suggestions

### Planned for 0.3.0 (Phase 5 - Advanced Features)
- Template import/export system
- Conversation analytics and statistics
- Knowledge graph visualization
- Timeline queries
- PDF export for conversations

### Future Enhancements
- Tmux integration and session management
- Additional AI tool support (Aider, Continue)
- Web interface for visualization
- Team collaboration features
- Community template marketplace

---

## Links

- [GitHub Repository](https://github.com/yourusername/cortext)
- [Documentation](Docs/)
- [User Guide](Docs/user-guide.md)
- [MCP Server Guide](Docs/mcp-server.md)
- [Multi-AI Support](Docs/multi-ai-support.md)
