# 🧠 Cortext

**AI-Augmented Workspace for Knowledge Work**

Cortext is a git-backed, AI-assisted workspace that provides persistent memory, structured workflows, and searchable knowledge management for working alongside LLMs.

---

## ✨ Features

- **📝 Structured Conversations** - Templates for brainstorming, debugging, planning, learning, meetings, and reviews
- **🔄 Git-Based** - Every conversation and decision tracked in version control
- **🤖 Multi-AI Support** - Works with Claude Code, OpenCode, Gemini CLI, Cursor, and more
- **🧠 Persistent Memory** - Personal constitution defines your working style across all tools
- **🔍 RAG Search** - Semantic search across all conversations (coming in Phase 4)
- **🎯 Workflow Automation** - Bash scripts and slash commands for repeatable processes

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cortext.git
cd cortext

# Install with uv (recommended)
uv tool install .

# Or with pip
pip install -e .

# Verify installation
cortext check
```

### Initialize Your Workspace

```bash
# Create a new workspace
cortext init ~/my-workspace

# Navigate to your workspace
cd ~/my-workspace

# Customize your constitution
edit .workspace/memory/constitution.md

# Start using with your favorite AI tool
claude
```

---

## 📖 Usage

### With Claude Code

Once your workspace is initialized, Claude Code will have access to conversation commands:

```
/workspace.brainstorm    Start an ideation session
/workspace.debug         Debug a problem systematically
/workspace.plan          Plan a feature or project
/workspace.learn         Document learning and take notes
/workspace.meeting       Capture meeting notes and actions
/workspace.review        Conduct code or design reviews
```

### Directory Structure

```
~/my-workspace/
├── .workspace/              # Core workspace configuration
│   ├── memory/
│   │   ├── constitution.md  # Your working principles
│   │   ├── context.md      # Current focus areas
│   │   └── decisions.md    # Decision log
│   ├── scripts/            # Automation scripts
│   ├── templates/          # Conversation templates
│   └── registry.json       # Conversation type registry
├── conversations/          # All conversations by date
│   └── 2025-11/
│       ├── 001-brainstorm-new-feature/
│       └── 002-debug-auth-issue/
├── research/               # Research projects
├── ideas/                  # Unstructured ideation
├── notes/                  # Learning notes
└── projects/               # Active projects
```

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
- Git branch for isolation
- Auto-commit on creation

Built-in types:
- **Brainstorm** - Free-form ideation
- **Debug** - Systematic troubleshooting
- **Plan** - Feature/project planning
- **Learn** - Learning documentation
- **Meeting** - Meeting notes with action items
- **Review** - Code/design reviews

### Git Workflow

```
main                          # Clean branch
├── conversation/001-brainstorm-feature
├── conversation/002-debug-auth
└── conversation/003-plan-redesign
```

Commits are structured and searchable:
```
[conversation] Initialize brainstorm: New Feature Ideas
[debug] Found root cause: race condition in auth handler
[decision] Chose PostgreSQL over MongoDB for scalability
```

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
- Ollama (for RAG features in Phase 4)
- ripgrep (for fast search in Phase 2)
- tmux (for session management)

---

## 📋 Roadmap

- **Phase 0:** Foundation & core structure ✅
- **Phase 1:** Templates, commands, registry (In Progress)
- **Phase 2:** MCP server with basic search
- **Phase 3:** Multi-AI tool support
- **Phase 4:** RAG with semantic search
- **Phase 5:** Advanced features (analytics, export)
- **Phase 6:** Open source release

See `Docs/spec.md` for complete architecture and roadmap.

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

- **Issues:** [GitHub Issues](https://github.com/yourusername/cortext/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/cortext/discussions)
- **Documentation:** See `Docs/` directory

---

**Status:** 🚧 Active Development
**Version:** 0.1.0
**Last Updated:** 2025-11-10
