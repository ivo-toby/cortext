# Changelog

All notable changes to Cortext will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Workspace Upgrade System

Cortext now supports safe, incremental workspace upgrades that preserve user customizations while updating built-in files to newer versions.

**Key Features:**
- **Hash-based tracking**: SHA-256 hashes detect file modifications
- **Smart prompts**: Only prompts for files you've actually changed
- **Automatic backups**: Timestamped backups before any overwrite
- **Legacy support**: Graceful migration for pre-v0.3.0 workspaces
- **Multiple upgrade options**: Overwrite, keep, diff, or create .new files

**New Command:**
```bash
cortext upgrade                    # Interactive upgrade
cortext upgrade --yes              # Auto-accept defaults
cortext upgrade --dry-run          # Preview changes
cortext upgrade --regenerate TYPE  # Force regenerate specific type
cortext upgrade --built-in-only    # Skip custom types
```

**Registry Schema v2.0:**
- Added `workspace_meta` with version tracking
- Added `generated_with` metadata to conversation types
- Tracks original file hashes for upgrade detection

**What this means for you:**
- New workspaces: Created with v2.0 schema automatically
- Existing workspaces: Run `cortext upgrade` to migrate
- Custom types: Will be tracked for safe future upgrades

### Changed

#### **BREAKING**: MCP Server Workspace Scope

MCP tools now accept an explicit `workspace_path` parameter instead of relying on the `WORKSPACE_PATH` environment variable. This fixes the issue where MCP tools would search in the wrong workspace after switching between Cortext workspaces.

**What changed:**
- All MCP tools (`search_workspace`, `get_context`, `get_decision_history`) now accept optional `workspace_path` parameter
- MCP registration no longer includes `WORKSPACE_PATH` environment variable
- Server defaults to current working directory when `workspace_path` not provided
- AI agents should pass the current workspace path when calling tools

**New registration format:**
```bash
# Old (deprecated)
claude mcp add --transport stdio --scope local cortext --env WORKSPACE_PATH=/path -- cortext-mcp

# New
claude mcp add --transport stdio --scope local cortext -- cortext-mcp
```

**New tool call format:**
```python
# AI passes workspace explicitly
search_workspace(query="...", workspace_path="/path/to/workspace")

# Or relies on cwd fallback
search_workspace(query="...")
```

#### Upgrade Path

**Existing users - no action required in most cases:**
1. Old registrations with `WORKSPACE_PATH` continue to work
2. The env var is ignored; server uses current working directory
3. When Claude Code spawns MCP from your project, cwd is correct

**For cleanest setup (recommended for multi-workspace users):**
```bash
# Remove old registration
claude mcp remove cortext

# Re-register without WORKSPACE_PATH
cortext init
# or manually: claude mcp add --transport stdio --scope local cortext -- cortext-mcp
```

**Gemini/OpenCode users:**
- Run `cortext mcp install --force` to update configuration
- Or manually remove `env`/`environment` sections from config files

### Added

#### Init Performance Improvements
- **`--quick` flag**: Skip MCP check and registration for faster init in CI/scripts
  - Example: `cortext init --quick /path/to/workspace`
  - Message informs user to run `cortext mcp add` later
- **Existing installation detection**: Checks if MCP is already configured before prompting
  - Claude: Runs `claude mcp list` to check for cortext
  - Gemini: Checks `~/.gemini/settings.json` for cortext entry
  - OpenCode: Checks `opencode.json` for cortext entry
  - Skips prompt and shows "MCP already configured" when detected
- **Progress feedback**: Shows spinner during slow MCP registration operations
  - "Registering MCP server with Claude Code..."
  - "Configuring MCP for Gemini..."
  - "Configuring MCP for OpenCode..."
- **Reduced timeout**: MCP registration timeout reduced from 30s to 10s
  - Clear error message on timeout with manual command to run
- **Cached command checks**: Single `which cortext-mcp` call per init run

#### RAG Tools in MCP Server
- **Semantic Search via MCP**: AI agents can now use semantic search tools through MCP
  - `embed_document` - Embed specific documents/conversations for semantic search
  - `embed_workspace` - Embed entire workspace content
  - `search_semantic` - Semantic search using embeddings (finds conceptually similar content)
  - `get_similar` - Find documents similar to a given source
  - `get_embedding_status` - Get workspace embedding statistics
- **5 new MCP tools** available alongside existing keyword search tools
- **Automatic fallback**: RAG tools gracefully unavailable if dependencies missing

#### Automatic MCP Configuration
- **Interactive MCP setup during init**: Users are prompted to configure MCP server
  - Default: Yes (user can press Enter to accept)
  - Can be skipped with response "n"
  - Explains how to add later with `cortext mcp install`
- **Command-line flags for automation**:
  - `--mcp` flag to explicitly enable MCP configuration
  - `--no-mcp` flag to skip MCP setup
  - Flags take precedence over interactive prompt
- **Multi-agent support**:
  - Claude Code: Workspace-local `.claude/mcp_config.json`
  - Gemini CLI: Global `~/.gemini/settings.json` with merge logic
  - OpenCode: Workspace-local `.opencode/mcp_config.json`
- **Workspace path substitution**: Configs include absolute workspace path in `WORKSPACE_PATH` env var
- **Validation**: Checks if `cortext-mcp` command is available (warns but continues if missing)

#### `cortext mcp install` Command
- **Post-init MCP configuration**: Add MCP to existing workspaces
- **Agent detection**: Automatically detects which agents are configured
- **Selective configuration**: `--ai <agent>` flag to configure specific agent only
- **Force overwrite**: `--force` flag to update existing configurations
- **Gemini settings merge**: Preserves existing settings when adding MCP config
- **Clear output**: Shows which agents were configured and config file paths
- **Error handling**: Validates workspace, checks for agents, warns if MCP command missing

### Changed

#### Claude Code MCP Registration Method
- **Fixed MCP setup for Claude Code**: Changed from config file to CLI registration
  - Claude Code requires servers to be registered via `claude mcp add` command
  - The `cortext init --mcp` and `cortext mcp install` commands now automatically run:
    `claude mcp add --transport stdio --scope local cortext -- cortext-mcp`
  - Falls back to showing manual instructions if Claude CLI not available
  - Updated both `init` and `mcp install` commands
  - Updated all documentation to reflect correct registration method
  - This is the correct approach per Claude Code documentation

#### Updated Documentation
- **mcp-server.md**: Complete documentation of 8 MCP tools (3 keyword + 5 RAG)
  - Automatic vs manual configuration instructions
  - Tool schemas and examples for all RAG tools
  - Troubleshooting section for MCP and RAG issues
- **README.md**: Added MCP Server section with quick setup guide
- **CLI help**: Added `cortext mcp install` to command list

### Fixed

#### Gemini CLI Independent Configuration
- **Fixed `cortext init --ai=gemini` not creating `.gemini/` folder**
  - Gemini configuration now converts directly from source command templates
  - Removed dependency on Claude configuration existing first
  - Each AI tool can now be configured independently
  - `--ai=all` continues to work correctly

### Changed

#### **BREAKING**: Conversation Type Folder Structure
- **Top-level type folders**: Each conversation type now has its own folder at workspace root
  - OLD: `conversations/meeting/YYYY-MM-DD/###-name/`
  - NEW: `meeting/YYYY-MM-DD/###-name/`
- **Cleaner organization**: No more nested `conversations/` parent folder
  - `brainstorm/` - Brainstorm conversations
  - `debug/` - Debug conversations
  - `learn/` - Learning notes
  - `meeting/` - Meeting notes
  - `plan/` - Planning sessions
  - `review/` - Code reviews
- **Pre-created at init**: All type folders created during `cortext init`
- **Git-tracked**: Each folder contains `.gitkeep` for empty folder tracking
- **Registry updated**: Folder paths now use type name directly (e.g., `"meeting"` not `"conversations/meeting"`)
- **MCP server updated**: Searches in top-level type folders
- **Custom types**: Now create top-level folders at workspace root

#### Migration Notes
- **New workspaces**: Will use new top-level structure automatically
- **Existing workspaces**: Old `conversations/{type}/` structure still works
- **MCP server**: Supports both old and new structures for backward compatibility
- **Recommendation**: New workspaces should use new structure; existing workspaces can migrate manually if desired

#### Code Quality
- **Extracted default conversation types to constant**: `DEFAULT_CONVERSATION_TYPES` in MCP server
  - Single source of truth for default types
  - Eliminated duplicate dictionary definitions
  - Improved maintainability

### Fixed

#### Init Command Path Handling
- **Fixed `cortext init .`** now correctly initializes in current directory instead of home directory
- **Added interactive prompt** when no arguments provided - users now explicitly choose workspace location
- **Smart path detection**: Arguments containing `.`, `/`, or `~` are treated as filesystem paths
  - `cortext init .` → current directory
  - `cortext init ..` → parent directory
  - `cortext init /opt/workspace` → absolute path
  - `cortext init ~/projects/ai` → home-relative path
  - `cortext init ./subdir` → relative path
- **Backward compatible**: Simple names still create `~/name`
  - `cortext init myworkspace` → `~/myworkspace`
- **Interactive options** when running `cortext init`:
  1. Current directory (with path shown)
  2. Default location (`~/ai-workspace`)
  3. Custom path (user input)
- **Improved help text** with usage examples in `cortext init --help`

### Changed

#### Conversation Workflows Redesign
- **Conversation-first approach**: Transformed all conversation workflows from template-filling to dialogue-based interaction
  - Conversations now emphasize ongoing dialogue with real-time documentation
  - Claude uses Edit tool frequently during conversation to update documents
  - Natural completion signals replace forced "finalization" steps
  - Users experience collaborative discussion, not form-filling

#### Template Simplification
- **Minimal scaffolding philosophy**: All templates redesigned as flexible frameworks, not prescriptive forms
  - `learning-notes.md`: Reduced from 248 lines to 30 lines
  - `brainstorm.md`: Simplified from 82 lines to 36 lines
  - `debug-session.md`: Simplified from 159 lines to 36 lines
  - `feature-planning.md`: Simplified to 36 lines with open-ended sections
  - `meeting-notes.md`: Simplified to 36 lines for real-time capture
  - `review-template.md`: Simplified to 36 lines for collaborative feedback
  - Removed nested subsections and prescriptive field structures
  - Templates now provide basic structure without dictating content organization
  - White space for organic content growth

#### Slash Command Instructions
- **Rewrote all 6 conversation slash commands** to emphasize dialogue over template generation
  - `workspace_learn.md`: Exploratory conversation with progressive learning
  - `workspace_brainstorm.md`: Iterative ideation with emergent ideas
  - `workspace_debug.md`: Investigative dialogue with real-time findings
  - `workspace_plan.md`: Collaborative planning through iterative refinement
  - `workspace_meeting.md`: Real-time documentation during discussion
  - `workspace_review.md`: Collaborative feedback through back-and-forth
  - All commands now instruct Claude to use Edit tool throughout conversation
  - Removed "completion" mentality - conversations continue naturally
  - Added example dialogue patterns showing natural flow

#### Custom Type Generation
- **Updated `workspace_add.md`** to generate conversation-first custom types
  - Creates minimal templates (under 50 lines) following scaffolding philosophy
  - Generates slash commands with conversation-first instructions
  - Custom types automatically follow dialogue-based pattern
  - Emphasizes real-time documentation during conversation

### Technical Details
- **No breaking changes**: Bash scripts, registry, and data structures unchanged
- **Pure UX improvement**: Only affects templates and slash command instructions
- **Backward compatible**: Existing conversations unaffected
- **Requirements tracked**: 8 new spec requirements added across 2 spec deltas

### Files Changed
- Templates: `learning-notes.md`, `brainstorm.md`, `debug-session.md`, `feature-planning.md`, `meeting-notes.md`, `review-template.md`
- Slash commands: `workspace_learn.md`, `workspace_brainstorm.md`, `workspace_debug.md`, `workspace_plan.md`, `workspace_meeting.md`, `workspace_review.md`
- Custom type generation: `workspace_add.md`

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

%b## [Previous Releases]

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

%b## [0.1.0] - 2025-11-10

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
%b
%b
%b
%b