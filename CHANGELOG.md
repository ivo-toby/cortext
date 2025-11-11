# Changelog

All notable changes to Cortext will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Conversation Folder Organization
- **Type-based subfolder structure**: Conversations now organized by type under `conversations/`
  - Each conversation type has its own subfolder: `conversations/{type}/YYYY-MM-DD/###-type-topic/`
  - Default mappings: `brainstorm/`, `debug/`, `learn/`, `meeting/`, `plan/`, `review/`
  - Custom types automatically use their type name as folder name
  - Provides clear separation between different domains of work
  - Reduces cognitive load with intuitive type-name = folder-name convention

#### Registry System Enhancement
- Added `folder` field to conversation type registry entries
  - Specifies the base folder path for each conversation type
  - Configurable per-type in `.workspace/registry.json`
  - Defaults to `conversations/{type-name}` if not specified or registry unavailable

#### Bash Utilities
- Added `get_conversation_folder()` function to `common.sh`
  - Reads folder path from registry using `jq`
  - Falls back to `conversations/{type}` if registry unavailable
  - Ensures consistent folder resolution across all scripts

### Changed

#### Bash Scripts
- Updated all conversation creation scripts to use registry-based folder resolution
  - `brainstorm.sh`, `debug.sh`, `plan.sh`, `learn.sh`, `meeting.sh`, `review.sh`
  - Now call `get_conversation_folder()` to determine save location
  - Maintains backward compatibility with old flat structure
- Updated `workspace-status.sh` to aggregate across all type subfolders
  - Correctly counts conversations at depth 3 (type/date/conversation)
  - Shows total, today, and monthly statistics across all folders

#### MCP Server
- Enhanced conversation name extraction to support both old and new structures
  - New: `conversations/{type}/YYYY-MM-DD/###-name/` (depth i+3)
  - Old: `conversations/YYYY-MM-DD/###-name/` (depth i+2)
  - Automatically detects and handles both formats

#### Custom Conversation Type Creation
- Updated `workspace_add.md` to include `folder` field in registry entries
  - Generated bash scripts use `get_conversation_folder()` for dynamic resolution
  - Custom types default to `conversations/{custom-type-name}/`

#### Documentation
- Updated directory structure examples in README, project.md, and spec.md
- Changed from flat `conversations/YYYY-MM-DD/` to organized `conversations/{type}/YYYY-MM-DD/`
- Added explanation of folder configuration and customization options

### Migration Notes
- **No migration required**: Old and new structures coexist peacefully
- Old conversations in `conversations/YYYY-MM-DD/` remain accessible
- New conversations automatically use type-based subfolder structure
- MCP server searches and finds conversations in both formats
- Workspace status correctly counts across both formats

---

## [Previous Releases]

### Changed

#### Breaking Changes
- **Conversation Directory Structure**: Changed from `YYYY-MM/###-type-topic/` to `YYYY-MM-DD/###-type-topic/` format
  - All new conversations now use day-level granularity
  - Provides better chronological organization and easier navigation
  - Old `YYYY-MM` format conversations remain accessible and searchable
  - No migration required - formats coexist peacefully

#### Bash Scripts
- Updated all conversation creation scripts to use `YYYY-MM-DD` format
  - `common.sh`, `brainstorm.sh`, `debug.sh`, `plan.sh`, `learn.sh`, `meeting.sh`, `review.sh`
  - `workspace-status.sh` now shows both "Today" and "This month" statistics

#### MCP Server
- Enhanced `search_workspace` date_range parameter to support both formats:
  - `YYYY-MM` format: searches all conversations from that month (backward compatible)
  - `YYYY-MM-DD` format: searches only conversations from that specific day
  - Glob patterns automatically match appropriate directory structures

#### Documentation
- Updated all references from `YYYY-MM` to `YYYY-MM-DD` format
  - `openspec/project.md`, `templates/cursorrules`, `Docs/spec.md`, `Docs/mcp-server.md`

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
