# Project Context

## Purpose

Cortext is an AI-augmented workspace system for knowledge work. It provides:

- **Persistent Memory**: Git-backed conversation history that builds a searchable knowledge base
- **Structured Workflows**: Template-driven conversation types (brainstorm, debug, plan, learn, meeting, review)
- **Multi-AI Support**: Works seamlessly with Claude Code, Cursor, OpenCode, and Gemini CLI
- **Constitution System**: Personal working principles that ensure consistent AI behavior across all tools
- **Semantic Search**: MCP server for searching past conversations and retrieving context

**Core Philosophy**: Local-first, git-as-database, tool-agnostic, privacy-preserving, structured-yet-flexible.

## Tech Stack

### Core
- **Python 3.11+** - Main implementation language
- **typer** - CLI framework for commands
- **rich** - Terminal UI and formatting
- **bash** - Workflow automation scripts

### Integration
- **MCP (Model Context Protocol)** - AI tool integration for search
- **ripgrep (rg)** - Fast full-text search
- **git** - Version control and workspace database
- **httpx** - HTTP client for future extensions

### AI Tools (Supported)
- Claude Code (full support)
- Cursor (rules-based)
- OpenCode (prompt-based)
- Gemini CLI (TOML commands)

### Packaging
- **hatchling** - Build backend
- **uv** or **pip** - Package installation

## Project Conventions

### Code Style

**Python**:
- PEP 8 compliant with modern Python 3.11+ idioms
- Type hints for all function signatures
- Docstrings for all public functions and classes
- Max line length: 88 characters (Black-compatible)
- Use `pathlib.Path` for all file operations
- Prefer f-strings for string formatting

**Naming Conventions**:
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`
- CLI commands: `kebab-case` (e.g., `cortext check`)

**Bash Scripts**:
- Use `set -e` for error handling
- Source common utilities from `common.sh`
- Provide clear error messages with color coding
- Always check prerequisites before operations

### Architecture Patterns

**CLI Structure**:
```
cortext_cli/
  ├── cli.py          # Main entry point, command routing
  ├── commands/       # Individual commands (init, check, list)
  ├── utils.py        # Shared utilities
  └── converters.py   # AI tool format converters
```

**MCP Server**:
```
cortext_mcp/
  └── server.py       # MCP protocol handler, search tools
```

**Design Patterns**:
- **Command Pattern**: Each CLI command is a separate module
- **Template Method**: Conversation workflows follow template structure
- **Strategy Pattern**: Different AI tool converters
- **Repository Pattern**: Git serves as data repository

**Key Principles**:
- Separation of concerns (CLI, MCP, templates, scripts)
- Single responsibility for each module
- Fail fast with clear error messages
- Progressive enhancement (core works without optional tools)

### Testing Strategy

**Testing Philosophy**:
- Test critical paths (init, template generation, MCP protocol)
- Manual testing for CLI UX
- Integration tests for git workflows
- Smoke tests for each conversation type

**To Implement**:
- Unit tests for core utilities (`utils.py`, `converters.py`)
- Integration tests for MCP server tools
- CLI integration tests (init workflow, check command)
- Template validation tests

**Test Structure** (planned):
```
tests/
  ├── unit/           # Unit tests for utilities
  ├── integration/    # Integration tests for workflows
  └── fixtures/       # Test workspaces and templates
```

### Git Workflow

**Commit Convention**:
```
[type] Brief summary (imperative mood)

Detailed description if needed.

Additional context or metadata.
```

**Commit Types**:
- `[feat]` - New features
- `[fix]` - Bug fixes
- `[docs]` - Documentation changes
- `[refactor]` - Code refactoring
- `[test]` - Test additions/changes
- `[chore]` - Build/config changes
- `[conversation]` - User conversation commits
- `[workspace]` - Workspace structure changes

**Branch Strategy**:
- `main` - All conversation commits go directly to main
- `feature/*` - Development features (for project development)

**Workflow**:
1. All conversations commit directly to main branch
2. Git tags mark conversation start points (`conv/{ID}`)
3. Atomic commits with clear, searchable messages
4. Users can create manual branches for isolation when needed

**Tag Format**:
- `conv/{CONVERSATION_ID}` - e.g., `conv/001-brainstorm-new-feature`
- List tags: `git tag -l "conv/*" --sort=-creatordate`

### File Organization

**Templates**: Markdown files with `[PLACEHOLDER]` syntax
**Scripts**: Executable bash scripts in `scripts/bash/`
**Commands**: Markdown files with YAML frontmatter for Claude Code
**Documentation**: Comprehensive guides in `Docs/`

## Domain Context

### Conversation Types

Cortext organizes knowledge work into conversation types:

1. **Brainstorm** - Free-form ideation, exploration of ideas
2. **Debug** - Systematic troubleshooting with root cause analysis
3. **Plan** - Feature and project planning with requirements
4. **Learn** - Learning documentation with examples and notes
5. **Meeting** - Structured meeting notes with action items
6. **Review** - Code and design reviews with feedback

Each type has:
- Template (`.workspace/templates/{type}.md`)
- Bash script (`.workspace/scripts/bash/{type}.sh`)
- Slash command (`.claude/commands/workspace_{type}.md`)
- Registry entry (`.workspace/registry.json`)

### Constitution System

The constitution (`.workspace/memory/constitution.md`) defines:
- Communication style preferences
- Working principles and methodology
- Technical stack preferences
- Guardrails and boundaries
- Current context and focus areas

**All AI tools read this file** to maintain consistent behavior.

### Workspace Structure

```
workspace/
├── .workspace/             # Core configuration
│   ├── memory/
│   │   ├── constitution.md  # User's working principles
│   │   ├── context.md      # Current focus
│   │   └── decisions.md    # Decision log
│   ├── scripts/            # Automation scripts
│   ├── templates/          # Conversation templates
│   └── registry.json       # Conversation type registry
├── brainstorm/             # Brainstorm conversations ({type}/YYYY-MM-DD/###-type-topic/)
├── debug/                  # Debug conversations
├── learn/                  # Learning notes
├── meeting/                # Meeting notes
├── plan/                   # Planning sessions
├── review/                 # Code reviews
├── .claude/               # Claude Code configuration
├── .cursorrules          # Cursor configuration
├── .opencode/            # OpenCode configuration
└── .gemini/              # Gemini CLI configuration
```

### Registry System

The registry (`registry.json`) tracks:
- Available conversation types (built-in and custom)
- Template paths and script locations
- Command names and descriptions
- Creation dates and metadata
- Usage statistics

### MCP Protocol

Cortext implements MCP for AI tool integration:
- **Tools**: `search_workspace`, `get_context`, `get_decision_history`
- **Protocol**: JSON over stdio
- **Transport**: Process spawning via `cortext-mcp` command

## Important Constraints

### Technical Constraints

1. **Local-First**: All data must stay on user's machine
2. **Privacy**: No data sent to external services (except user-initiated AI conversations)
3. **Git-Required**: Git is mandatory for workspace operation
4. **Python 3.11+**: Modern Python features (type hints, pathlib, etc.)
5. **Cross-Platform**: Must work on Linux, macOS, and Windows (with WSL)

### Design Constraints

1. **Tool-Agnostic**: Cannot depend on specific AI tool being available
2. **Progressive Enhancement**: Core features work without optional dependencies
3. **Backward Compatible**: Workspace format should be stable across versions
4. **Human-Readable**: All data in human-readable formats (markdown, JSON)
5. **No Lock-In**: Users can access all data without Cortext installed

### UX Constraints

1. **Constitution-Driven**: All AI interactions respect user's constitution
2. **Searchable**: All content must be full-text searchable
3. **Versioned**: Every change tracked in git with clear history
4. **Structured**: Templates guide but don't constrain creativity
5. **Portable**: Workspace can be synced across machines

## External Dependencies

### Required Dependencies

- **git** (>= 2.30) - Version control, core to entire system
- **Python** (>= 3.11) - Runtime environment
- **typer** (>= 0.12.0) - CLI framework
- **rich** (>= 13.0.0) - Terminal UI

### Optional Dependencies

- **ripgrep** - Fast search (for MCP server search_workspace tool)
- **ollama** - Local LLM for RAG (Phase 4, future)
- **tmux** - Session management (recommended but not required)

### AI Tool Dependencies (User Choice)

- **Claude Code** - Anthropic's CLI tool
- **Cursor** - AI-powered editor
- **OpenCode** - Open source AI CLI
- **Gemini CLI** - Google's AI CLI

**Important**: Cortext works independently of which AI tool the user chooses.

### External Services

- **None** - Cortext is fully local and offline-capable
- AI tools may require API keys, but that's user-managed

## Development Workflow

### Adding New Features

1. Create feature branch from `main`
2. Implement with tests (when applicable)
3. Update documentation (README, user guide, etc.)
4. Commit with conventional commit message
5. Merge to main when complete

### Adding New Conversation Types (Core)

1. Create template in `templates/{type}.md`
2. Create bash script in `scripts/bash/{type}.sh`
3. Create slash command in `claude_commands/workspace_{type}.md`
4. Update `init.py` to include in default registry
5. Document in user guide

### Release Process

1. Update `CHANGELOG.md` with changes
2. Update version in `pyproject.toml` and `__init__.py`
3. Create git tag: `git tag -a v0.x.0 -m "Release v0.x.0"`
4. Test installation with `uv tool install .`
5. Push tag: `git push origin v0.x.0`

## Notes for AI Assistants

When working on this project:

1. **Always read the spec**: `Docs/spec.md` contains complete architecture
2. **Follow conventions**: Consistent style, naming, and structure
3. **Update docs**: Every feature needs documentation
4. **Test manually**: Run `cortext init` and verify workflows
5. **Think local-first**: No cloud dependencies
6. **Respect privacy**: User data stays private
7. **Be tool-agnostic**: Don't assume specific AI tool
8. **Maintain portability**: Keep everything human-readable

## Future Considerations

### Phase 4 (RAG with Ollama)
- Embedding generation for semantic search
- Vector store integration (ChromaDB/FAISS)
- Automatic context injection
- Related conversation suggestions

### Phase 5 (Advanced Features)
- Template import/export
- Conversation analytics
- Knowledge graph visualization
- Team collaboration (while staying local-first)

### Long-term Vision
- Plugin system for custom tools
- Web UI for visualization
- Community template marketplace
- Integration with more AI tools
