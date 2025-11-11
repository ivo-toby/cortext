# Cortext: AI-Augmented Workspace Architecture

**Project Name:** Cortext 🧠
**Date:** 2025-11-10
**Status:** Design Phase - Ready to Build
**Based on:** ResearchKit architecture + RAG + Git-based knowledge management

---

## Document Structure

This outline serves as the **single source of truth** for building Cortext. It contains:

1. **Vision & Architecture** (Lines 1-150)
   - Core principles, directory structure, git workflow

2. **Components** (Lines 150-350)
   - Constitution system, conversation types, MCP server design, tmux integration

3. **Implementation Roadmap** (Lines 350-450)
   - 6 phases over 12+ weeks, from foundation to open source release

4. **Technical Reference** (Lines 690-1450)
   - **Critical section**: ResearchKit implementation patterns
   - CLI architecture, slash commands, bash scripts, templates, registry
   - Copy-paste ready code examples

5. **Technical Decisions** (Lines 1450-1550)
   - RAG system, git strategy, embedding models, MCP server language

6. **Success Metrics & Open Questions** (Lines 1550-1644)
   - Usability targets, performance benchmarks, unresolved design questions

**For implementation**: Start with the Technical Reference section which contains all patterns from ResearchKit adapted for Cortext.

---

## Vision

Create a centralized, git-backed workspace for AI-assisted knowledge work that provides:
- Persistent memory across conversations
- Structured workflows for different task types
- Multi-AI tool support (Claude Code, OpenCode, Gemini CLI, etc.)
- Local-first RAG for context retrieval
- Personal constitution (working style, guardrails, preferences)
- Tmux-based dedicated environment

**Goal:** Enable tech-savvy professionals to work alongside LLMs with full conversation history, searchable knowledge base, and consistent working principles across all AI tools.

---

## Core Principles

1. **Git as Database**
   - Every conversation, note, and decision tracked in git
   - Atomic commits for searchability and rollback
   - Branch-based organization for different workstreams

2. **Local-First RAG**
   - Conversations and notes indexed locally
   - Semantic search via MCP server
   - No data leaves your machine (privacy-preserving)

3. **Constitution-Driven Interaction**
   - Define your working style once
   - All AI tools read the same constitution
   - Consistent experience across tools

4. **Tool Agnostic**
   - Works with Claude Code, OpenCode, Gemini CLI, Cursor, etc.
   - Portable configuration
   - Easy switching between tools

5. **Structured Workflows**
   - Templates for common tasks
   - Slash commands for repeatability
   - Hooks for automation

---

## Architecture

### Directory Structure

```
~/ai-workspace/
├── .git/                          # Git repository for version control
├── .workspace/                    # Core workspace configuration
│   ├── memory/
│   │   ├── constitution.md        # Your working principles & preferences
│   │   ├── context.md            # Current focus areas & active projects
│   │   ├── preferences.md        # Communication style & guardrails
│   │   └── decisions.md          # Key decisions log
│   ├── scripts/
│   │   ├── commit-session.sh     # Auto-commit conversation sessions
│   │   ├── index-conversations.sh # Update RAG index
│   │   └── workspace-status.sh   # Show workspace state
│   └── templates/
│       ├── brainstorm.md
│       ├── debug-session.md
│       ├── feature-planning.md
│       ├── learning-notes.md
│       └── meeting-notes.md
├── .claude/                       # Claude Code configuration
│   ├── commands/
│   │   ├── workspace_brainstorm.md
│   │   ├── workspace_debug.md
│   │   ├── workspace_learn.md
│   │   ├── workspace_plan.md
│   │   └── workspace_review.md
│   └── hooks/
│       └── post-conversation.sh
├── conversations/                 # All AI conversations organized by type
│   ├── plan/                     # Planning conversations
│   │   └── 2025-11-10/
│   │       └── 001-plan-feature-planning/
│   │           ├── conversation.md
│   │           ├── decisions.md
│   │           └── artifacts/
│   ├── debug/                    # Debug conversations
│   │   └── 2025-11-10/
│   │       └── 001-debug-session/
│   └── brainstorm/               # Brainstorm conversations
│       └── 2025-11-10/
│           └── 001-brainstorm-architecture/
├── research/                      # Formal research projects (ResearchKit)
│   ├── 001-ai-safety/
│   │   ├── plan.md
│   │   ├── sources.md
│   │   ├── findings.md
│   │   └── synthesis.md
│   └── 002-distributed-systems/
├── ideas/                         # Unstructured ideation
│   ├── product-ideas.md
│   ├── technical-explorations.md
│   └── random-thoughts.md
├── notes/                         # Learning notes & references
│   ├── kubernetes/
│   ├── rust/
│   └── system-design/
├── projects/                      # Active project workspaces
│   ├── project-alpha/
│   └── project-beta/
└── .rag-index/                    # RAG system storage (gitignored)
    ├── embeddings.db
    ├── vector-store/
    └── metadata.json
```

### Git Workflow

**Branch Strategy:**
```
main                              # Clean branch, merged completed work
├── conversation/001-feature-x    # Temporary conversation branches
├── conversation/002-debug-y
├── research/001-topic            # Research branches (ResearchKit pattern)
└── project/alpha-dev             # Project-specific branches
```

**Commit Strategy:**
- Auto-commit after each conversation session
- Structured commit messages: `[type] Brief description`
- Types: `conversation`, `research`, `idea`, `note`, `decision`
- Commits are searchable via `git log --grep`

**Example commits:**
```
[conversation] Feature planning for user authentication
[research] Literature review on distributed consensus
[idea] Microservices architecture exploration
[note] Kubernetes networking deep dive
[decision] Chose PostgreSQL over MongoDB for project-alpha
```

---

## Components

### 1. Constitution System

**File:** `.workspace/memory/constitution.md`

Defines:
- **Communication Style:** How you prefer AI to communicate
  - Tone (formal/casual, verbose/concise)
  - Response length preferences
  - Use of examples, analogies, code snippets
- **Working Principles:** Your methodology
  - Test-first development
  - Documentation standards
  - Code review practices
  - Security considerations
- **Guardrails:** Boundaries and constraints
  - Technologies to prefer/avoid
  - Architectural principles
  - Performance requirements
  - Compliance requirements
- **Context:** Your expertise and focus areas
  - Primary languages/frameworks
  - Domain knowledge
  - Current learning goals

**Usage:** All AI tools read this file to understand your working style and preferences.

### 2. Conversation Types & Workflows

Each conversation type has:
- Dedicated template
- Slash command for quick start
- Git branch naming convention
- Auto-commit hook

**Supported Types:**

| Type | Purpose | Command | Template |
|------|---------|---------|----------|
| **Brainstorm** | Ideation, exploration | `/workspace.brainstorm` | `brainstorm.md` |
| **Debug** | Problem solving, troubleshooting | `/workspace.debug` | `debug-session.md` |
| **Plan** | Feature/project planning | `/workspace.plan` | `feature-planning.md` |
| **Learn** | Learning notes, documentation | `/workspace.learn` | `learning-notes.md` |
| **Research** | Formal research (ResearchKit) | `/researchkit.plan` | `plan-template.md` |
| **Review** | Code/design review | `/workspace.review` | `review-template.md` |
| **Meeting** | Meeting notes & action items | `/workspace.meeting` | `meeting-notes.md` |

### 3. MCP Server for RAG

**Purpose:** Provide semantic search across all workspace content

**Features:**
- Index conversations, notes, decisions, research
- Semantic search via embeddings (local models via Ollama)
- Context injection into new conversations
- Related content suggestions
- Timeline queries ("What did I learn about Kubernetes last month?")

**Implementation Phases:**

**Phase 1: Simple full-text search**
- MCP server wraps ripgrep/grep
- Search conversations by keyword
- No embeddings, just fast text search

**Phase 2: Semantic search**
- Local embeddings via Ollama (e.g., `nomic-embed-text`)
- Vector store (ChromaDB, FAISS, or simple JSON)
- Semantic similarity search

**Phase 3: Advanced features**
- Automatic context injection based on current conversation
- "Similar conversation" suggestions
- Trend analysis (topics over time)
- Knowledge graph visualization

**MCP Server Interface:**
```json
{
  "tools": [
    {
      "name": "search_workspace",
      "description": "Search conversations, notes, and research",
      "parameters": {
        "query": "string",
        "type": ["conversation", "research", "note", "idea", "all"],
        "date_range": "optional",
        "limit": "number"
      }
    },
    {
      "name": "get_context",
      "description": "Get relevant context for current conversation",
      "parameters": {
        "topic": "string",
        "max_results": "number"
      }
    },
    {
      "name": "get_decision_history",
      "description": "Retrieve past decisions on a topic",
      "parameters": {
        "topic": "string"
      }
    }
  ]
}
```

### 4. Tmux Integration

**Session Setup:**
```bash
# ~/.tmux/sessions/ai-workspace.sh
#!/bin/bash

# Create or attach to ai-workspace session
tmux new-session -d -s ai-workspace -n main

# Set working directory
tmux send-keys -t ai-workspace:main "cd ~/ai-workspace" C-m

# Load workspace context
tmux send-keys -t ai-workspace:main "cat .workspace/memory/constitution.md" C-m

# Start Claude Code (or preferred AI tool)
tmux send-keys -t ai-workspace:main "claude" C-m

# Create additional windows
tmux new-window -t ai-workspace -n research "cd ~/ai-workspace/research"
tmux new-window -t ai-workspace -n projects "cd ~/ai-workspace/projects"

# Attach to session
tmux attach-session -t ai-workspace
```

**Hooks:**
```bash
# Auto-commit on tmux detach
set-hook -g client-detached 'run-shell "~/ai-workspace/.workspace/scripts/commit-session.sh"'

# Update RAG index on session end
set-hook -g session-closed 'run-shell "~/ai-workspace/.workspace/scripts/index-conversations.sh"'
```

**Tmux Status Bar:**
- Current workspace branch
- Active conversation count
- Last commit time
- RAG index status

### 5. Multi-AI Tool Support

**Claude Code:**
- Full slash command support
- Hooks for automation
- MCP server integration
- Settings in `.claude/`

**OpenCode:**
- Custom agent configuration in `AGENT_CONFIG.toml`
- Slash commands in `.opencode/commands/`
- Ollama support for local models
- Same workspace constitution

**Gemini CLI:**
- Slash commands in `.gemini/commands/`
- Reads constitution for context
- Shared conversation format

**Cursor:**
- `.cursorrules` reads from constitution
- Shared workspace structure
- Same templates and workflows

**Key:** All tools read `.workspace/memory/constitution.md` and use the same directory structure.

### 6. Extensible Conversation Types

**Philosophy:** The workspace should adapt to your needs, not the other way around.

Users can create custom conversation types beyond the built-in ones (brainstorm, debug, plan, etc.). The AI assists with template creation through a guided interview process.

**Usage:**
```
/workspace.add
```

**Guided Creation Process:**

1. **AI interviews the user:**
   ```
   AI: What would you like to call this conversation type?
   User: hobbies

   AI: What's the primary purpose of a "hobbies" conversation?
   User: Track hobby projects, progress, ideas, and learnings

   AI: What phases or sections should a hobby conversation have?
   User: Current project, goals, progress, challenges, next steps, resources

   AI: What kind of information needs to be captured?
   User: Project details, materials, techniques, time spent, photos/links

   AI: What outputs or artifacts do you expect?
   User: Progress log, photo gallery links, skill progression

   AI: Any special requirements? (citations, code snippets, diagrams, etc.)
   User: Links to resources, embedded images
   ```

2. **AI generates initial template:**
   ```markdown
   # Hobby Project: {project-name}

   **Date:** {date}
   **Category:** {category}
   **Status:** {in-progress|paused|completed}

   ## Current Project

   {Brief description of what you're working on}

   ## Goals

   - [ ] {Goal 1}
   - [ ] {Goal 2}
   - [ ] {Goal 3}

   ## Progress Log

   ### {Date}

   **Time Spent:** {hours}

   {What did you work on? What did you accomplish?}

   **Resources Used:**
   - {Resource 1} - {link}
   - {Resource 2} - {link}

   **Photos/Gallery:**
   - {image link or path}

   ## Challenges & Solutions

   **Challenge:** {What problem did you encounter?}
   **Solution:** {How did you solve it?}
   **Learned:** {Key takeaway}

   ## Skills Acquired

   - {Skill 1}: {Proficiency level}
   - {Skill 2}: {Proficiency level}

   ## Next Steps

   - [ ] {Next action 1}
   - [ ] {Next action 2}

   ## Materials & Tools

   | Item | Quantity | Source | Notes |
   |------|----------|--------|-------|
   | {material} | {qty} | {where} | {notes} |

   ## Resources

   - {Tutorial/Guide} - {link}
   - {Community/Forum} - {link}
   ```

3. **AI creates slash command:**

   Creates `.claude/commands/workspace_hobbies.md`:
   ```markdown
   You are helping the user with a hobby project conversation.

   1. Read the template: `.workspace/templates/hobbies.md`
   2. Ask the user for project details:
      - Project name
      - Category (woodworking, electronics, crafts, etc.)
      - Current status
   3. Create a new conversation in `conversations/hobby/{YYYY-MM-DD}/###-hobby-{project-name}/`
   4. Use the template to create `project.md`
   5. Create `gallery/` folder for images
   6. Create git branch: `hobby/###-{project-name}`
   7. Guide the user through filling in the template
   8. Auto-commit when done

   The user wants to track hobby projects, progress, learnings, and build a personal knowledge base of their hands-on work.
   ```

4. **AI saves and commits:**
   ```bash
   # Files created:
   .workspace/templates/hobbies.md           # The template
   .claude/commands/workspace_hobbies.md     # Claude Code slash command
   .opencode/commands/hobbies.md            # OpenCode command
   .workspace/registry.json                  # Updated registry

   # Git commit:
   git add .workspace/templates/hobbies.md .claude/commands/workspace_hobbies.md
   git commit -m "[workspace] Add 'hobbies' conversation type

   User-defined conversation type for tracking hobby projects.

   Sections: project, goals, progress, challenges, skills, resources
   Purpose: Track hobby projects and learnings"
   ```

5. **AI confirms:**
   ```
   ✅ Created new conversation type: "hobbies"

   Files created:
   - Template: .workspace/templates/hobbies.md
   - Slash command: /workspace.hobbies

   You can now use:
   /workspace.hobbies

   To start tracking a hobby project. The template is in git, so you can
   edit it anytime with:

   Edit .workspace/templates/hobbies.md

   Would you like to start your first hobby conversation now?
   ```

**Registry System:**

`.workspace/registry.json` tracks all conversation types:
```json
{
  "conversation_types": {
    "brainstorm": {
      "name": "Brainstorm",
      "template": ".workspace/templates/brainstorm.md",
      "command": "/workspace.brainstorm",
      "built_in": true,
      "created": "2025-11-10",
      "description": "Ideation and exploration"
    },
    "hobbies": {
      "name": "Hobbies",
      "template": ".workspace/templates/hobbies.md",
      "command": "/workspace.hobbies",
      "built_in": false,
      "created": "2025-11-15",
      "created_by": "user",
      "description": "Track hobby projects, progress, and learnings"
    }
  }
}
```

**Benefits:**

✅ **Personalized:** Workspace adapts to your unique needs
✅ **Iterative:** Templates can be edited and improved over time
✅ **Versioned:** Git tracks evolution of your conversation types
✅ **Shareable:** Export template + command to share with others
✅ **AI-assisted:** Don't need to understand template structure
✅ **Discoverable:** `/workspace.list` shows all available types

**Advanced Features:**

**Clone & Modify:**
```
/workspace.clone brainstorm deep-dive

AI: I'll create a new conversation type based on "brainstorm".
    What should be different in "deep-dive"?

User: Add sections for research sources and detailed analysis

AI: ✅ Created "deep-dive" based on "brainstorm" with additional sections
```

**Import/Export:**
```bash
# Export conversation type
/workspace.export hobbies

AI: Exported to: .workspace/exports/hobbies-conversationtype.tar.gz
    Share this file with others to use your template!

# Import from community
/workspace.import ~/Downloads/book-notes.tar.gz

AI: Imported "book-notes" conversation type
    Use with: /workspace.book-notes
```

**List Available Types:**
```
/workspace.list

AI: Available conversation types:

    Built-in:
    - /workspace.brainstorm - Ideation and exploration
    - /workspace.debug - Problem solving and troubleshooting
    - /workspace.plan - Feature/project planning
    - /workspace.learn - Learning notes and documentation
    - /workspace.review - Code/design review
    - /workspace.meeting - Meeting notes and action items

    Custom:
    - /workspace.hobbies - Track hobby projects (created 2025-11-15)
    - /workspace.book-notes - Reading notes and summaries (imported)

    Use /workspace.add to create a new type
```

---

## Implementation Roadmap

### Phase 0: Foundation (Week 1)

**Goal:** Set up basic workspace structure and test with ResearchKit

- [ ] Install ResearchKit and test current functionality
- [ ] Design workspace directory structure
- [ ] Draft personal constitution
- [ ] Set up git repository with branch strategy
- [ ] Create tmux session configuration

**Deliverables:**
- Working ResearchKit installation
- Workspace structure in `~/ai-workspace/`
- Initial constitution document
- Tmux session script

### Phase 1: Core Workspace (Week 2-3)

**Goal:** Extend ResearchKit patterns to general workspace

- [ ] Create conversation templates (brainstorm, debug, plan, learn, meeting)
- [ ] Write slash commands for Claude Code
- [ ] Implement auto-commit hooks
- [ ] Add workspace status script
- [ ] Test with multiple conversation types
- [ ] **Build `/workspace.add` for extensible conversation types**
- [ ] Create registry system (`.workspace/registry.json`)
- [ ] Add `/workspace.list` to show available types

**Deliverables:**
- 5+ slash commands for different conversation types
- Git hooks for auto-commits
- Templates for each conversation type
- Working workflow for non-research conversations
- **Extensible conversation type system with `/workspace.add`**
- Registry tracking built-in and custom types

### Phase 2: MCP Server - Basic (Week 4-5)

**Goal:** Simple search across workspace content

- [ ] Build basic MCP server wrapping ripgrep
- [ ] Implement keyword search across conversations
- [ ] Add date filtering and conversation type filtering
- [ ] Integrate with Claude Code
- [ ] Test search performance

**Deliverables:**
- Working MCP server with basic search
- Claude Code integration
- Documentation for search commands

### Phase 3: Multi-AI Support (Week 6-7)

**Goal:** Make workspace portable across AI tools

- [ ] Test with OpenCode + Ollama
- [ ] Create Gemini CLI configuration
- [ ] Add Cursor support
- [ ] Document tool-switching workflow
- [ ] Create tool-agnostic templates

**Deliverables:**
- Configuration for 3+ AI tools
- Documentation for each tool
- Verified workflow portability

### Phase 4: MCP Server - RAG (Week 8-10)

**Goal:** Add semantic search with local embeddings

- [ ] Set up Ollama with embedding model (nomic-embed-text)
- [ ] Implement vector store (ChromaDB or FAISS)
- [ ] Add embedding generation for conversations
- [ ] Implement semantic search
- [ ] Add context injection feature
- [ ] Performance optimization

**Deliverables:**
- RAG-enabled MCP server
- Semantic search functionality
- Automatic context injection
- Performance benchmarks

### Phase 5: Advanced Features (Week 11-12)

**Goal:** Polish and add power-user features

- [ ] Knowledge graph visualization
- [ ] Trend analysis (topics over time)
- [ ] Related conversation suggestions
- [ ] Export workflows (PDF, markdown, presentations)
- [ ] Collaboration features (sharing conversations)
- [ ] Analytics dashboard
- [ ] **Conversation type sharing: `/workspace.clone`, `/workspace.export`, `/workspace.import`**
- [ ] Community template marketplace

**Deliverables:**
- Visualization tools
- Export capabilities
- Analytics features
- User documentation
- **Template sharing system**
- Community template repository

### Phase 6: Open Source Release (Week 13+)

**Goal:** Package as reusable tool for others

- [ ] Clean up codebase
- [ ] Write comprehensive documentation
- [ ] Create installation scripts
- [ ] Record demo video
- [ ] Publish to GitHub
- [ ] Write blog post/article
- [ ] Gather community feedback

**Deliverables:**
- Public GitHub repository
- Installation documentation
- Demo video
- Blog post/article
- Community engagement

---

## Technical Reference: ResearchKit Architecture

This section documents the technical implementation patterns from ResearchKit that Cortext will adapt and extend.

### CLI Architecture

**Tool**: Python with Typer + Rich
```python
# Key dependencies
- typer>=0.12.0        # CLI framework
- rich>=13.0.0         # Terminal formatting
- httpx[socks]>=0.27.0 # HTTP client (for future features)
- platformdirs>=4.0.0  # Cross-platform paths
```

**Entry Point Pattern**:
```python
app = typer.Typer(
    name="cortext",
    help="AI-augmented workspace for knowledge work",
    add_completion=False,
    invoke_without_command=True,
)

@app.command()
def init(
    workspace_name: Optional[str] = typer.Argument(None),
    ai: str = typer.Option("claude", help="AI tool to configure"),
):
    """Initialize a new Cortext workspace"""
    pass

@app.command()
def check():
    """Check if required tools are installed"""
    pass

def main():
    """Entry point for the CLI"""
    app()
```

**AI Agent Configuration Pattern**:
```python
AGENT_CONFIG = {
    "claude": {
        "name": "Claude Code",
        "commands_dir": ".claude/commands",
        "cli_check": "claude",
        "requires_cli": False,
        "install_url": None,
    },
    "opencode": {
        "name": "OpenCode",
        "commands_dir": ".opencode/command",
        "cli_check": "opencode",
        "requires_cli": True,
        "install_url": "https://opencode.ai",
    },
    # ... more agents
}
```

### Directory Structure Creation

**Pattern**: Programmatic directory tree creation
```python
def create_workspace_structure(workspace_dir: Path, tracker: StepTracker):
    """Create the .workspace directory structure"""
    workspace_config = workspace_dir / ".workspace"

    directories = [
        workspace_config / "memory",
        workspace_config / "scripts" / "bash",
        workspace_config / "scripts" / "powershell",
        workspace_config / "templates",
        workspace_config / "exports",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    tracker.add_step("Created .workspace directory structure")
```

**Template Copying**:
```python
def get_template_dir() -> Path:
    """Get the templates directory from the package"""
    # Try system location first (installed package)
    sys_templates = Path(sys.prefix) / "share" / "cortext" / "templates"
    if sys_templates.exists():
        return sys_templates

    # Try development location (editable install)
    current_file = Path(__file__).resolve()
    dev_templates = current_file.parent.parent.parent / "templates"
    if dev_templates.exists():
        return dev_templates

    return dev_templates

def copy_template(template_name: str, destination: Path):
    """Copy a template file to destination"""
    template_dir = get_template_dir()
    src = template_dir / template_name
    if src.exists():
        shutil.copy2(src, destination)
    else:
        raise FileNotFoundError(f"Template not found: {template_name}")
```

### Slash Command Format

**Claude Code slash command structure** (`.claude/commands/*.md`):

```markdown
---
description: Brief description (1 sentence)
tags: [tag1, tag2, tag3]
---

# Command Title

Brief introduction paragraph explaining what this command does.

## Your Task

1. **Step 1**: Description
   - Sub-task
   - Sub-task

   Optional code block:
   ```bash
   command to run
   ```

2. **Step 2**: Description
   - More sub-tasks

## Best Practices

Bulleted list of best practices.

## Example

Optional example usage.

## When Complete

What happens after this command finishes.
```

**Gemini CLI format** (`.gemini/commands/*.toml`):

```toml
description = "Brief description"

prompt = """
Full prompt text here.
Multi-line supported.
Escape special chars: \" \\
"""
```

**Conversion function**:
```python
def convert_md_to_toml(md_path: Path) -> tuple[str, str]:
    """Convert markdown command to TOML format"""
    content = md_path.read_text()

    # Parse frontmatter
    description = ""
    prompt_content = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            prompt_content = parts[2].strip()

            for line in frontmatter.split("\n"):
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()

    # Generate command name
    command_name = md_path.stem.replace("cortext_", "")

    # Escape for TOML
    prompt_escaped = prompt_content.replace("\\", "\\\\").replace('"""', r'\"\"\""')
    description_escaped = description.replace('"', '\\"')

    toml_content = f'''description = "{description_escaped}"

prompt = """
{prompt_escaped}
"""
'''

    return toml_content, command_name
```

### Bash Script Patterns

**Common utilities script** (`scripts/bash/common.sh`):

```bash
#!/usr/bin/env bash
# Common utilities for Cortext scripts

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Print functions (output to stderr to avoid interfering with command substitution)
print_success() {
    echo -e "${GREEN}✓ $1${NC}" >&2
}

print_error() {
    echo -e "${RED}✗ $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}" >&2
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}" >&2
}

print_step() {
    echo -e "${BLUE}→ $1${NC}" >&2
}

# Get workspace root
get_workspace_root() {
    if [ -d ".workspace" ]; then
        echo "$(pwd)/.workspace"
    else
        print_error "Not in a Cortext workspace directory"
        print_info "Run 'cortext init' to initialize a workspace"
        exit 1
    fi
}

# Get current conversation from git branch
get_current_conversation_dir() {
    local workspace_root=$(get_workspace_root)
    local branch_name=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    if [ -z "$branch_name" ] || [ "$branch_name" = "main" ]; then
        print_error "Not on a conversation branch"
        print_info "Use /workspace.brainstorm or similar to start"
        exit 1
    fi

    # Extract conversation ID from branch (e.g., conversation/001-topic -> 001-topic)
    local conv_id=$(echo "$branch_name" | sed 's|^conversation/||')
    local conv_dir="${workspace_root}/../conversations/$(date +%Y-%m-%d)/${conv_id}"

    if [ ! -d "$conv_dir" ]; then
        mkdir -p "$conv_dir"
    fi

    echo "$conv_dir"
}

# Get next ID (for auto-incrementing conversation IDs)
get_next_id() {
    local conversations_dir="$1"
    local max_id=0

    for dir in "${conversations_dir}"/*/; do
        if [ -d "$dir" ]; then
            local dir_name=$(basename "$dir")
            local id=$(echo "$dir_name" | grep -oE '^[0-9]+' || echo "0")
            if [ "$id" -gt "$max_id" ]; then
                max_id=$id
            fi
        fi
    done

    printf "%03d" $((max_id + 1))
}

# Copy template
copy_template() {
    local template_name="$1"
    local destination="$2"
    local workspace_root=$(get_workspace_root)
    local template_file="${workspace_root}/templates/${template_name}"

    if [ ! -f "$template_file" ]; then
        print_error "Template not found: ${template_name}"
        exit 1
    fi

    cp "$template_file" "$destination"
    print_success "Created: $(basename $destination)"
}

# Update date placeholders
update_date_in_file() {
    local file="$1"
    local current_date=$(date +%Y-%m-%d)

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\[DATE\]/$current_date/g" "$file"
    else
        sed -i "s/\[DATE\]/$current_date/g" "$file"
    fi
}

# Check git initialized
check_git_initialized() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not a git repository"
        print_info "Initialize git with: git init"
        exit 1
    fi
}

# Display header
show_header() {
    local title="$1"
    echo -e "${CYAN}" >&2
    echo "╔════════════════════════════════════════════════════════════╗" >&2
    echo "║                                                            ║" >&2
    echo "║              🧠 Cortext                                     ║" >&2
    echo "║                                                            ║" >&2
    echo "║              $title" >&2
    echo "║                                                            ║" >&2
    echo "╚════════════════════════════════════════════════════════════╝" >&2
    echo -e "${NC}" >&2
}

# Export functions for use in other scripts
export -f print_success
export -f print_error
export -f print_warning
export -f print_info
export -f print_step
export -f get_workspace_root
export -f get_current_conversation_dir
export -f get_next_id
export -f copy_template
export -f update_date_in_file
export -f check_git_initialized
export -f show_header
```

**Example workflow script** (`scripts/bash/brainstorm.sh`):

```bash
#!/usr/bin/env bash
# Cortext Brainstorm Script

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

show_header "Brainstorming Session"

# Parse arguments
TOPIC="$1"

if [ -z "$TOPIC" ]; then
    print_error "Topic is required"
    echo "Usage: $0 <topic>" >&2
    echo "Example: $0 \"New Feature Ideas\"" >&2
    exit 1
fi

# Check prerequisites
check_git_initialized

# Get next conversation ID
WORKSPACE_ROOT=$(get_workspace_root)
FOLDER=$(get_conversation_folder "brainstorm")
CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../${FOLDER}/$(date +%Y-%m-%d)"
mkdir -p "$CONVERSATIONS_DIR"

CONVERSATION_ID=$(get_next_id "$CONVERSATIONS_DIR")
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
CONVERSATION_NAME="${CONVERSATION_ID}-brainstorm-${TOPIC_SLUG}"
CONVERSATION_DIR="${CONVERSATIONS_DIR}/${CONVERSATION_NAME}"

# Create conversation directory
mkdir -p "$CONVERSATION_DIR"

# Create git branch
BRANCH_NAME="conversation/${CONVERSATION_NAME}"
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"

print_success "Created conversation: ${CONVERSATION_NAME}"
print_info "Branch: ${BRANCH_NAME}"

# Copy template
BRAINSTORM_FILE="${CONVERSATION_DIR}/brainstorm.md"
copy_template "brainstorm.md" "$BRAINSTORM_FILE"

# Update placeholders
update_date_in_file "$BRAINSTORM_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\[TOPIC\]/$TOPIC/g" "$BRAINSTORM_FILE"
    sed -i '' "s/\[ID\]/$CONVERSATION_NAME/g" "$BRAINSTORM_FILE"
else
    sed -i "s/\[TOPIC\]/$TOPIC/g" "$BRAINSTORM_FILE"
    sed -i "s/\[ID\]/$CONVERSATION_NAME/g" "$BRAINSTORM_FILE"
fi

# Initial commit
print_step "Committing brainstorm session..."
git add "$CONVERSATION_DIR"
git commit -m "[conversation] Initialize brainstorm: ${TOPIC}

Created conversation ${CONVERSATION_NAME}.

Type: brainstorm
Purpose: Ideation and exploration
" 2>/dev/null || print_warning "Nothing new to commit"

# Display summary
echo "" >&2
print_success "Brainstorm session created!"
echo "" >&2
print_info "Conversation: ${CONVERSATION_NAME}"
print_info "File: ${BRAINSTORM_FILE}"
echo "" >&2
echo -e "${CYAN}Next steps:${NC}" >&2
echo "  1. Open ${BRAINSTORM_FILE}" >&2
echo "  2. Capture ideas freely" >&2
echo "  3. Commit regularly with git" >&2
echo "" >&2
```

### Git Workflow Implementation

**Branch creation pattern**:
```bash
# Generate branch name
BRANCH_NAME="conversation/${CONVERSATION_ID}-${TYPE}-${TOPIC_SLUG}"

# Create or checkout branch
git checkout -b "$BRANCH_NAME" 2>/dev/null || git checkout "$BRANCH_NAME"
```

**Commit message format**:
```bash
git commit -m "[TYPE] Brief summary

Detailed explanation of what this commit contains.

Metadata:
- Field: value
- Field: value
"
```

**Types**: `conversation`, `research`, `idea`, `note`, `decision`, `workspace`

### Template System

**Template structure** (Markdown with placeholders):

```markdown
# [TITLE]

**ID**: [ID]
**Date**: [DATE]
**Type**: [TYPE]
**Status**: [STATUS]

---

## Section 1

Content with [PLACEHOLDER] values.

## Section 2

More content.

---

## Metadata

- Created: [DATE]
- Last Modified: [DATE]
- Tags: [TAGS]
```

**Placeholder replacement**:
```bash
# Using sed for placeholder replacement
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS requires '' after -i
    sed -i '' "s/\[PLACEHOLDER\]/$VALUE/g" "$FILE"
else
    # Linux
    sed -i "s/\[PLACEHOLDER\]/$VALUE/g" "$FILE"
fi
```

### Registry System

**Registry file** (`.workspace/registry.json`):

```json
{
  "version": "1.0",
  "created": "2025-11-10",
  "conversation_types": {
    "brainstorm": {
      "name": "Brainstorm",
      "template": ".workspace/templates/brainstorm.md",
      "command": "/workspace.brainstorm",
      "script": ".workspace/scripts/bash/brainstorm.sh",
      "built_in": true,
      "created": "2025-11-10",
      "description": "Ideation and exploration",
      "sections": ["goals", "ideas", "themes", "next-steps"]
    }
  },
  "statistics": {
    "total_conversations": 0,
    "by_type": {}
  }
}
```

**Registry update pattern** (Python):
```python
import json
from pathlib import Path
from datetime import datetime

def register_conversation_type(
    workspace_root: Path,
    type_name: str,
    template_path: str,
    description: str,
    sections: list[str],
    built_in: bool = False
):
    """Register a new conversation type in the registry"""
    registry_path = workspace_root / ".workspace" / "registry.json"

    # Load existing registry
    if registry_path.exists():
        registry = json.loads(registry_path.read_text())
    else:
        registry = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "conversation_types": {},
            "statistics": {"total_conversations": 0, "by_type": {}}
        }

    # Add new type
    registry["conversation_types"][type_name] = {
        "name": type_name.title(),
        "template": template_path,
        "command": f"/workspace.{type_name}",
        "script": f".workspace/scripts/bash/{type_name}.sh",
        "built_in": built_in,
        "created": datetime.now().isoformat(),
        "description": description,
        "sections": sections
    }

    # Save registry
    registry_path.write_text(json.dumps(registry, indent=2))
```

### AI Agent-Specific Configuration

**Cursor** (`.cursorrules`):
```markdown
# Cortext Workspace AI Rules

## Project Context
This is a Cortext workspace for AI-augmented knowledge work.

## Workspace Structure
- `.workspace/memory/constitution.md`: User's working principles
- `conversations/`: All AI conversations organized by type
- `research/`: Formal research projects
- `ideas/`: Unstructured ideation
- `notes/`: Learning notes

## Key Principles
- Follow the constitution in `.workspace/memory/constitution.md`
- Maintain structured documentation
- Commit atomically to git
- Cross-reference related conversations

## File Organization
- Conversations in `conversations/{type}/YYYY-MM-DD/###-type-topic/`
- Each conversation has its own git branch
- Templates in `.workspace/templates/`

## When Creating Content
- Use existing templates as guides
- Maintain consistent formatting
- Add proper metadata (date, type, tags)
- Reference related conversations when relevant
```

**OpenCode** (`.opencode/prompts/workspace_assistant.txt`):
```
You are a workspace assistant helping with AI-augmented knowledge work using Cortext.

Your role:
1. Help maintain organized conversations
2. Ensure proper git commits
3. Follow the user's constitution (.workspace/memory/constitution.md)
4. Cross-reference related conversations
5. Suggest relevant past insights from the workspace

Key files:
- constitution.md: User's working principles and preferences
- conversations/: All conversations organized by type and date
- registry.json: Tracks conversation types and metadata

When helping:
- Check the constitution for user preferences
- Maintain structured documentation
- Use templates for new conversations
- Commit work atomically to git
- Search past conversations for relevant context
```

### Package Distribution

**pyproject.toml structure**:
```toml
[project]
name = "cortext-workspace"
version = "0.1.0"
description = "AI-augmented workspace for knowledge work"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [{ name = "Cortext Contributors" }]

dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
    "httpx[socks]>=0.27.0",
    "platformdirs>=4.0.0",
]

[project.scripts]
cortext = "cortext_cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/cortext_cli"]

[tool.hatch.build.targets.wheel.shared-data]
"templates" = "share/cortext/templates"
"claude_commands" = "share/cortext/claude_commands"
"scripts" = "share/cortext/scripts"

[tool.hatch.build.targets.sdist]
include = [
    "src/",
    "templates/",
    "claude_commands/",
    "scripts/",
]
```

### Installation Commands

```bash
# Install from git (for users)
uv tool install cortext-workspace --from git+https://github.com/user/cortext.git

# Verify installation
cortext check

# Development install
git clone https://github.com/user/cortext.git
cd cortext
uv pip install -e .
# or: pip install -e .
```

### Progress Tracking (StepTracker)

```python
from rich.tree import Tree
from rich.console import Console

class StepTracker:
    """Track and display progress for multi-step operations"""

    def __init__(self, title: str = "Cortext"):
        self.console = Console()
        self.tree = Tree(f"🧠 {title}")

    def add_step(self, message: str, status: str = "✓"):
        """Add a completed step"""
        self.tree.add(f"[green]{status}[/green] {message}")

    def add_error(self, message: str):
        """Add an error step"""
        self.tree.add(f"[red]✗[/red] {message}")

    def add_warning(self, message: str):
        """Add a warning step"""
        self.tree.add(f"[yellow]⚠[/yellow] {message}")

    def display(self):
        """Display the tree"""
        self.console.print(self.tree)
```

### Cross-Platform Considerations

**Path handling**:
```python
from pathlib import Path

# Always use Path for cross-platform paths
workspace_dir = Path.cwd() / ".workspace"
workspace_dir.mkdir(parents=True, exist_ok=True)
```

**Script permissions** (Unix):
```python
import os

if os.name != "nt":  # Not Windows
    os.chmod(script_path, 0o755)  # Make executable
```

**Sed commands** (macOS vs Linux):
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS requires empty string after -i
    sed -i '' 's/old/new/g' file.txt
else
    # Linux
    sed -i 's/old/new/g' file.txt
fi
```

---

## Technical Decisions

### RAG System: Local vs Cloud

**Decision:** Local-first with optional cloud fallback

**Rationale:**
- Privacy: Conversations may contain sensitive information
- Cost: No API costs for embeddings and search
- Speed: Local vector search is fast enough for personal use
- Offline: Works without internet connectivity

**Implementation:**
- Ollama for local embeddings (`nomic-embed-text`, `mxbai-embed-large`)
- ChromaDB or FAISS for vector storage
- Simple JSON metadata store
- Optional cloud sync for backup (encrypted)

### Git Strategy: Monorepo vs Multiple Repos

**Decision:** Single monorepo for all workspace content

**Rationale:**
- Simpler search across all content
- Unified git history
- Easier backup and sync
- Cross-conversation references work naturally

**Trade-offs:**
- Repo size may grow large (mitigate with LFS for artifacts)
- Need good .gitignore for binary files

### Embedding Model Selection

**Options:**
1. `nomic-embed-text` (137M params) - Fast, good quality
2. `mxbai-embed-large` (335M params) - Better quality, slower
3. `all-minilm` (33M params) - Very fast, lower quality

**Decision:** Start with `nomic-embed-text`, allow user configuration

**Rationale:**
- Good balance of speed and quality
- Well-supported by Ollama
- Can switch based on user hardware

### MCP Server Language: Python vs TypeScript

**Decision:** Python

**Rationale:**
- Better ecosystem for embeddings and vector stores
- Easier to integrate with Ollama
- Simpler for users to extend/customize
- Rich NLP libraries available

---

## Success Metrics

### Usability
- [ ] Can set up workspace in < 10 minutes
- [ ] All conversation types have working templates
- [ ] Search returns relevant results in < 2 seconds
- [ ] Works with 3+ AI tools
- [ ] **Can create custom conversation type in < 5 minutes with `/workspace.add`**
- [ ] **User creates at least 1 custom conversation type in first week**

### Performance
- [ ] Search 1000+ conversations in < 2 seconds
- [ ] Embedding generation < 1 second per conversation
- [ ] Commit hooks run in < 3 seconds

### Adoption (Open Source)
- [ ] 100+ GitHub stars in first month
- [ ] 10+ community contributions
- [ ] 5+ blog posts/articles written about it
- [ ] Used by 50+ practitioners
- [ ] **20+ community-contributed conversation type templates**
- [ ] **Active template marketplace with ratings/reviews**

---

## Open Questions

### 1. Conversation Capture
**Question:** How to automatically capture conversations?
**Options:**
- Manual: User runs slash command to save conversation
- Hook-based: Post-conversation hook captures automatically
- Log-based: Parse AI tool logs (fragile, tool-specific)

**Recommendation:** Start with hook-based for Claude Code, manual for others

### 2. RAG Chunking Strategy
**Question:** How to chunk conversations for embedding?
**Options:**
- By message (each message is a chunk)
- By conversation (entire conversation is one chunk)
- By topic (split conversations into topic segments)
- Hybrid (messages + metadata about conversation)

**Recommendation:** Start with message-level, add conversation-level metadata

### 3. Privacy & Sync
**Question:** How to sync across machines while preserving privacy?
**Options:**
- Git remote (plaintext, requires trust in host)
- Encrypted git remote (git-crypt, complex setup)
- No sync (pure local, backup via external drive)
- Self-hosted sync (Syncthing, Nextcloud)

**Recommendation:** Start with standard git remote, add encryption as opt-in feature

### 4. Collaboration Features
**Question:** Should workspace support team collaboration?
**Options:**
- Pure single-user (simpler, clearer privacy model)
- Shared workspace (complex permissions, merge conflicts)
- Export/import (share specific conversations)

**Recommendation:** Start single-user, add export/import for selective sharing

### 5. ResearchKit Integration
**Question:** Fork ResearchKit or extend it?
**Options:**
- Fork and modify for general workspace
- Build on top as separate tool that uses ResearchKit
- Contribute features back to ResearchKit

**Recommendation:** Build as extension, contribute MCP features back to ResearchKit

---

## Resources

### Existing Tools & Inspiration
- **ResearchKit:** https://github.com/ivo-toby/researchKit
- **SpecKit:** https://github.com/github/spec-kit
- **Claude Code:** https://docs.claude.com/claude-code
- **MCP Specification:** https://modelcontextprotocol.io
- **Ollama:** https://ollama.ai

### Technical Dependencies
- Python 3.11+
- Git 2.30+
- Ollama (for local embeddings)
- Tmux 3.0+
- ripgrep (for fast search)
- One or more AI tools (Claude Code, OpenCode, etc.)

### Learning Resources
- MCP server development guide
- Vector embeddings tutorial
- Git hooks documentation
- Tmux scripting guide

---

## Next Steps

1. **Validate concept:** Use ResearchKit for 1-2 weeks, identify gaps
2. **Draft constitution:** Write personal constitution document
3. **Design MCP server:** Sketch out API and architecture
4. **Prototype search:** Build simplest possible MCP search server
5. **Test workflow:** Use for real work, gather feedback
6. **Iterate:** Refine based on actual usage patterns

---

## Conclusion

This architecture provides a foundation for "AI-augmented knowledge work" that is:
- **Privacy-preserving:** All data stays local
- **Tool-agnostic:** Works with multiple AI tools
- **Structured:** Clear workflows and templates
- **Searchable:** RAG enables finding past insights
- **Versioned:** Git provides full history
- **Extensible:** MCP servers allow custom functionality

By building on ResearchKit's proven architecture and adding RAG capabilities, this creates a powerful workspace for professionals working alongside AI systems.

The key insight: **Git + Constitution + RAG + Structured Workflows = Persistent AI Collaboration**

---

**Status:** Ready to prototype Phase 0
**Next Action:** Install ResearchKit and create initial workspace structure
**Timeline:** 12-week implementation plan
**Success:** Working system that increases productivity and knowledge retention
