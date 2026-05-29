# 🧠 Cortext

**AI-Augmented Workspace for Knowledge Work**

Cortext is a git-backed, AI-assisted workspace that provides persistent memory, structured workflows, and searchable knowledge management for working alongside LLMs.

---

## ✨ Features

- **📝 Structured Conversations** - Templates for brainstorming, debugging, planning, learning, meetings, reviews, and project management
- **🔄 Git-Based** - Every conversation and decision tracked in version control
- **🤖 Multi-AI Support** - Works with Claude Code, Codex CLI, OpenCode, Gemini CLI, Cursor, and more
- **🧠 Persistent Memory** - Personal constitution defines your working style across all tools
- **⏸️ Session Resumption** - Pause and resume conversations with full context preserved
- **🔍 RAG Search** - Semantic search across all conversations using local embeddings
- **🎯 Workflow Automation** - Bash scripts and slash commands for repeatable processes
- **🪝 Event Hooks** - Extensible automation triggered on workspace events
- **🔧 Safe Upgrades** - Hash-based tracking with smart prompts preserves customizations

---

## 🚀 Quick Start

### Installation

**Recommended — install directly from GitHub (no clone required):**

```bash
uv tool install git+https://github.com/ivo-toby/cortext.git

# With RAG support for semantic search
uv tool install "git+https://github.com/ivo-toby/cortext.git[rag]"

# With all optional features
uv tool install "git+https://github.com/ivo-toby/cortext.git[all]"

# Verify installation
cortext check
```

**For development (local clone):**

```bash
git clone https://github.com/ivo-toby/cortext.git
cd cortext

pip install -e .            # basic
pip install -e '.[rag]'    # with RAG
pip install -e '.[all]'    # everything
# or: uv tool install -e .
```

### Upgrading

```bash
# If installed via uv tool (recommended)
uv tool upgrade cortext-workspace

# If that doesn't pick up the latest version, reinstall:
uv tool install git+https://github.com/ivo-toby/cortext.git --force

# If installed via pip / editable clone
cd /path/to/cortext && git pull && pip install -e . --force-reinstall
```

After upgrading, run `cortext upgrade` in your workspace to sync any new commands
and templates.

### Troubleshooting Installation

If you encounter `ModuleNotFoundError` after pulling updates:

```bash
# uv tool install
uv tool install git+https://github.com/ivo-toby/cortext.git --force

# uv pip / editable
uv pip install -e . --reinstall

# pip editable
pip install -e . --force-reinstall
```

**Common issues:**
- `ModuleNotFoundError: No module named 'packaging'` — use `--force` / `--force-reinstall`
- uv tool cache stale — `uv tool install ... --force` clears it

### Initialize Your Workspace

```bash
# Interactive prompt - choose where to create workspace
cortext init

# Initialize in current directory
cortext init .

# Initialize in a specific path
cortext init ~/my-workspace

# Initialize with a simple name (creates ~/my-workspace)
cortext init my-workspace

# Navigate to your workspace
cd ~/my-workspace

# Customize your constitution
edit .workspace/memory/constitution.md

# Start using with your favorite AI tool
claude
```

---

## 📖 Usage

### With Codex CLI

Initialize with Codex support:
```bash
cortext init --ai=codex
# or add to an existing workspace:
cortext upgrade --add-tool codex && cortext mcp install --ai codex
```

Codex automatically reads `AGENTS.md` at the workspace root for context. Workspace commands are installed as **skills** in `.agents/skills/` — invoke them with `$` or let Codex auto-select based on your request:
```
$workspace_brainstorm      Start an ideation session
$workspace_debug           Debug a problem systematically
$workspace_plan            Plan a feature or project
$workspace_learn           Document learning and take notes
$workspace_meeting         Capture meeting notes and actions
$workspace_review          Conduct code or design reviews
```

### With Claude Code

Once your workspace is initialized, Claude Code will have access to conversation commands:

```
/workspace.brainstorm      Start an ideation session
/workspace.debug           Debug a problem systematically
/workspace.plan            Plan a feature or project
/workspace.learn           Document learning and take notes
/workspace.meeting         Capture meeting notes and actions
/workspace.review          Conduct code or design reviews
/workspace.projectmanage   Manage project with multi-document tracking
/workspace.stop-conversation  Save session for later resumption
/workspace.resume          Resume a paused conversation
```

**CLI Commands:**
```bash
cortext resume --list              # List all resumable conversations
cortext resume --list --type brainstorm  # Filter by type
cortext resume "api design"        # Resume by search term
cortext resume 001-brainstorm-api  # Resume by ID

cortext upgrade                    # Upgrade workspace to current version
cortext upgrade --dry-run          # Preview upgrade changes
cortext upgrade --yes              # Auto-accept all upgrades
```

### MCP Server (AI Agent Integration)

Cortext includes an MCP (Model Context Protocol) server that AI agents can use to search your workspace:

**Automatic Configuration:**
```bash
# MCP is automatically configured during workspace init
cortext init --ai claude           # Prompts for MCP setup
cortext init --ai claude --mcp     # Explicitly enable
cortext init --ai claude --no-mcp  # Skip MCP

# For existing workspaces
cortext mcp install
```

**Available Tools for Agents:**
- **Keyword Search** - `search_workspace`, `get_context`, `get_decision_history`
- **Semantic Search** - `search_semantic`, `get_similar`, `embed_document`

Agents can now search past conversations, find related discussions, and build on previous work automatically.

### Directory Structure

```
~/my-workspace/
├── .workspace/              # Core workspace configuration
│   ├── memory/
│   │   ├── constitution.md  # Your working principles
│   │   ├── context.md      # Current focus areas
│   │   └── decisions.md    # Decision log
│   ├── hooks/              # Event-driven automation
│   │   ├── conversation/   # Conversation lifecycle hooks
│   │   └── git/            # Git hook integrations
│   ├── scripts/            # Automation scripts
│   ├── templates/          # Conversation templates
│   └── registry.json       # Conversation type registry
├── brainstorm/             # Brainstorm conversations (top-level)
│   └── 2025-11-10/
│       └── 001-brainstorm-new-feature/
├── debug/                  # Debug conversations
│   └── 2025-11-10/
│       └── 001-debug-auth-issue/
├── learn/                  # Learning notes
├── meeting/                # Meeting notes
├── plan/                   # Planning sessions
├── projectmanage/          # Project management (with docs/ and index.md)
├── review/                 # Code reviews
├── research/               # Research projects
├── ideas/                  # Unstructured ideation
├── notes/                  # Personal notes
└── projects/               # Active projects
```

For complete usage instructions, see **[User Guide](Docs/user-guide.md)**.

---

## 📚 Core Concepts

### Constitution System

Your constitution (`.workspace/memory/constitution.md`) defines:
- **Communication style** - How AI should interact with you
- **Working principles** - Your development methodology
- **Technical preferences** - Languages, tools, patterns
- **Guardrails** - Boundaries and constraints

All AI tools read this file to maintain consistent behavior.

### Conversation Types

Each conversation type has:
- Dedicated markdown template
- Bash script for automation
- Slash command for Claude Code
- Git tag for conversation boundaries
- Auto-commit on creation

Built-in types:
- **Brainstorm** - Free-form ideation
- **Debug** - Systematic troubleshooting
- **Plan** - Feature/project planning
- **Learn** - Learning documentation
- **Meeting** - Meeting notes with action items
- **Review** - Code/design reviews
- **Project Manage** - Project tracking with multi-document architecture, proactive context search, and auto-maintained index

### Session Management

Conversations can be paused and resumed with full context preservation:

**How it works:**
1. **Session auto-initializes** - When you start a conversation, a session is created
2. **Pause with context** - Use `/workspace.stop-conversation` to save session state
3. **Resume seamlessly** - Use `/workspace.resume` to continue where you left off

**Session data stored:**
- Message history (chat exchanges)
- Agent configuration (which command, model)
- Context summary (what was being discussed)
- Status (active, paused, completed)

**Storage location:**
```
001-brainstorm-api-design/
├── brainstorm.md           # Conversation content
└── .session/
    ├── session.json        # Metadata and config
    └── messages.jsonl      # Chat history
```

**Resume flow:**
1. Agent loads the original command's system prompt
2. Injects conversation context and history
3. Continues naturally from where you stopped

See **[Session Guide](Docs/session-guide.md)** for complete documentation.

### Workspace Upgrades

Cortext supports safe, incremental workspace upgrades that preserve your customizations:

```bash
# Check if upgrade is available
cortext upgrade

# Preview what would change
cortext upgrade --dry-run

# Upgrade non-interactively
cortext upgrade --yes

# Force regenerate a specific type
cortext upgrade --regenerate my-custom-type

# Only upgrade built-in types
cortext upgrade --built-in-only

# Add a new AI tool to an existing workspace
cortext upgrade --add-tool codex
```

**How it works:**
- New workspaces track file hashes automatically
- Upgrades detect if you've modified files
- Unmodified files upgrade silently
- Modified files prompt for action (overwrite, keep, diff, create .new)
- All overwrites create timestamped backups

**Upgrade options for modified files:**
1. **Overwrite** - Backup to `.workspace/backup/` and update
2. **Keep** - Leave your version unchanged
3. **Create .new** - Generate `.new` files for manual merge
4. **Show diff** - View what changed
5. **Skip** - Don't upgrade this file

See **[Upgrade Guide](Docs/upgrade-guide.md)** for complete documentation and **[CHANGELOG.md](CHANGELOG.md)** for version history.

### Git Workflow

All conversations commit directly to main with tags marking boundaries:

```bash
# List conversation tags
git tag -l "conv/*" --sort=-creatordate
# conv/003-plan-redesign
# conv/002-debug-auth
# conv/001-brainstorm-feature
```

Commits are structured and searchable:
```
[conversation] Initialize brainstorm: New Feature Ideas
[debug] Found root cause: race condition in auth handler
[decision] Chose PostgreSQL over MongoDB for scalability
```

### RAG Pipeline

Semantic search across your workspace using local embeddings (optional feature).

**Installation:**
```bash
uv tool install "git+https://github.com/ivo-toby/cortext.git[rag]"  # recommended
pip install -e '.[rag]'  # for development
```

**Usage:**
```bash
# Embed workspace for semantic search
cortext embed --all

# Search by meaning (not just keywords)
cortext search "authentication best practices" --semantic

# Check embedding status
cortext rag status
```

Features:
- **Local embeddings** - fastembed (no API keys, no PyTorch)
- **Vector store** - ChromaDB for persistent storage
- **UPSERT logic** - Only re-embeds changed files
- **Auto-embed** - New conversations embedded automatically
- **Multi-format** - Markdown, PDF, Word, HTML, plain text

See **[RAG Guide](Docs/rag-guide.md)** for complete documentation.

### Hooks System

Event-driven automation that runs on workspace events like conversation creation or git commits.

```bash
# List all configured hooks
cortext hooks list

# Manually run a hook event
cortext hooks run conversation:create /path/to/conv

# Add a custom hook
cortext hooks add conversation:create my-notification

# Install git hooks (done automatically during init)
cortext hooks install
```

**Built-in Events:**
- `conversation:create` - After a conversation is created
- `conversation:archive` - When archiving a conversation
- `pre-commit` - Before git commit (embeds staged files)
- `post-checkout` - After git checkout

**Custom Hooks:**
Add your own automation by creating scripts in `.workspace/hooks/`:
```
.workspace/hooks/conversation/on-create.d/
├── 10-embed.sh          # Default: embed for RAG
└── 50-my-hook.sh        # Your custom automation
```

Scripts run in alphanumeric order. Use numeric prefixes (10-39 core, 40-69 user, 70-99 cleanup).

See **[Hooks Guide](Docs/hooks.md)** for complete documentation.

---

## 🛠️ Development

### Project Status

**Current Phase:** Phase 0 - Foundation (In Progress)

See `Docs/tasks` for detailed task breakdown and progress.

### Contributing

Contributions welcome! See the task list for areas needing work.

### Requirements

- Python 3.11+
- Git 2.30+
- bash (for Unix systems)

Optional:
- ripgrep (for fast keyword search)
- tmux (for session management)

### Versioning

Cortext uses [semantic versioning](https://semver.org/). Versions are automatically bumped on merge to main based on commit message prefixes:

- `feat:` or `feat(scope):` → Minor bump (0.1.0 → 0.2.0)
- `fix:` or `fix(scope):` → Patch bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` or `!:` → Major bump (0.1.0 → 1.0.0)

**Check installed version:**
```bash
cortext -v        # or cortext --version
```

**Commit message examples:**
```bash
git commit -m "feat: add export functionality"
git commit -m "fix(mcp): resolve search timeout issue"
git commit -m "feat!: redesign conversation API"
```

### Testing Development Locally

The easiest way to test changes during development is using an editable install:

```bash
# Option 1: Virtual environment (isolated)
cd /path/to/cortext
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Test from anywhere (while venv is active)
cd /tmp/test-workspace
cortext init .
```

```bash
# Option 2: Global install with pyenv (convenient)
pip install -e /path/to/cortext

# Now available everywhere
cd /any/directory
cortext init .
```

```bash
# Option 3: Activate venv from anywhere
source /path/to/cortext/.venv/bin/activate
cortext init .
```

**With editable install (`-e`):**
- Code changes are reflected immediately - no reinstall needed
- Only reinstall if you change `pyproject.toml` (dependencies, entry points)
- Run `cortext` directly to test your changes

**Without venv (quick test):**
```bash
cd /path/to/cortext
python3 -m cortext_cli.cli init .
```

---

## 📋 Status

- **Phase 0:** Foundation & core structure ✅
- **Phase 1:** Templates, commands, registry ✅
- **Phase 2:** MCP server with search ✅
- **Phase 3:** Multi-AI tool support ✅
- **Phase 4:** RAG with local embeddings ✅
- **Phase 5:** Advanced features (planned)
- **Phase 6:** Documentation & release ✅

**Current Status**: ✅ **Production Ready** - Core functionality complete and tested.

See `Docs/spec.md` for complete architecture and `Docs/user-guide.md` for usage.

---

## 🎯 Philosophy

Cortext is built on these principles:

1. **Local-First** - Your data stays on your machine
2. **Git as Database** - Version control for knowledge
3. **Tool Agnostic** - Works with any AI assistant
4. **Structured Yet Flexible** - Templates guide but don't constrain
5. **Privacy Preserving** - No data leaves your control

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Inspired by:
- [ResearchKit](https://github.com/ivo-toby/researchKit) - Research workflow patterns
- [Claude Code](https://docs.claude.com/claude-code) - AI-powered development
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP for tool integration

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/ivo-toby/cortext/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ivo-toby/cortext/discussions)
- **Documentation:** See `Docs/` directory

---

**Status:** 🚧 Active Development
**Version:** 0.1.0
**Last Updated:** 2025-11-17
