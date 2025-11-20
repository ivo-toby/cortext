# Cortext User Guide

Complete guide to using Cortext for AI-augmented knowledge work.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Your First Conversation](#your-first-conversation)
3. [Conversation Types](#conversation-types)
4. [The Constitution](#the-constitution)
5. [Searching Your Workspace](#searching-your-workspace)
6. [Git Workflow](#git-workflow)
7. [Custom Conversation Types](#custom-conversation-types)
8. [Multi-AI Support](#multi-ai-support)
9. [Best Practices](#best-practices)
10. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Installation

```bash
# Clone or install Cortext
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
# Create a workspace
cortext init ~/my-workspace

# Or with specific AI tool
cortext init ~/my-workspace --ai=claude

# Or configure all tools
cortext init ~/my-workspace --ai=all

# Navigate to workspace
cd ~/my-workspace
```

### Workspace Structure

After initialization, you'll have:

```
~/my-workspace/
├── .workspace/          # Core configuration
│   ├── memory/
│   │   ├── constitution.md    # Your working style
│   │   ├── context.md        # Current focus
│   │   └── decisions.md      # Decision log
│   ├── scripts/        # Automation scripts
│   ├── templates/      # Conversation templates
│   └── registry.json   # Conversation types
├── conversations/      # All your conversations
├── .claude/           # Claude Code config (if selected)
├── .cursorrules       # Cursor config (if selected)
└── .git/             # Version control
```

---

## Your First Conversation

### Step 1: Customize Your Constitution

```bash
cd ~/my-workspace
edit .workspace/memory/constitution.md
```

Fill in:
- **Communication style**: How you want AI to communicate
- **Working principles**: Your methodology (TDD, documentation standards, etc.)
- **Technical preferences**: Languages, frameworks, tools
- **Guardrails**: What to avoid or prefer

Example:
```markdown
## Communication Style
- Tone: Professional but friendly
- Response Length: Concise with examples
- Thinking Style: Step-by-step explanations

## Technical Preferences
**Primary Languages:**
- Python 3.11+
- TypeScript

**Avoid:**
- JavaScript without TypeScript
- Complex metaprogramming
```

### Step 2: Start a Conversation

**With Claude Code:**
```
cd ~/my-workspace
claude

# Then use slash commands:
/workspace.brainstorm
/workspace.debug
/workspace.plan
```

**With Cursor:**
```
cursor ~/my-workspace
# Cursor will read .cursorrules automatically
```

**Manually (any tool):**
```bash
# Run the bash script directly
.workspace/scripts/bash/brainstorm.sh "My Feature Ideas"
```

### Step 3: Work Through the Template

The conversation template guides you through sections:
- Goals
- Main content
- Insights
- Next steps

Fill them in naturally during your conversation with the AI.

### Step 4: Commit Your Work

```bash
# Auto-commit the session
.workspace/scripts/bash/commit-session.sh

# Or manually
git add conversations/
git commit -m "[conversation] Brainstorm: My Feature Ideas"
```

---

## Conversation Types

### Brainstorm
**Purpose**: Free-form ideation and exploration

**Use when**:
- Exploring new ideas
- Problem-solving creatively
- Planning without constraints

**Sections**: Goals, Ideas, Themes, Next Steps

**Command**: `/workspace.brainstorm` or `.workspace/scripts/bash/brainstorm.sh "Topic"`

### Debug
**Purpose**: Systematic troubleshooting

**Use when**:
- Fixing bugs
- Investigating issues
- Root cause analysis

**Sections**: Problem, Investigation, Root Cause, Solution, Prevention

**Command**: `/workspace.debug` or `.workspace/scripts/bash/debug.sh "Issue"`

### Plan
**Purpose**: Feature and project planning

**Use when**:
- Designing features
- Planning projects
- Making architectural decisions

**Sections**: Overview, Requirements, Approach, Timeline

**Command**: `/workspace.plan` or `.workspace/scripts/bash/plan.sh "Feature"`

### Learn
**Purpose**: Learning documentation

**Use when**:
- Learning new technologies
- Taking notes
- Documenting discoveries

**Sections**: Concepts, Notes, Examples, Resources

**Command**: `/workspace.learn` or `.workspace/scripts/bash/learn.sh "Topic"`

### Meeting
**Purpose**: Meeting notes and action items

**Use when**:
- Documenting meetings
- Capturing decisions
- Tracking action items

**Sections**: Attendees, Discussion, Decisions, Actions

**Command**: `/workspace.meeting` or `.workspace/scripts/bash/meeting.sh "Meeting"`

### Review
**Purpose**: Code and design reviews

**Use when**:
- Reviewing code
- Design critiques
- Providing feedback

**Sections**: Overview, Feedback, Recommendations, Decision

**Command**: `/workspace.review` or `.workspace/scripts/bash/review.sh "Title"`

---

## The Constitution

Your constitution is the **single source of truth** for how AI assistants should work with you.

### What Goes in the Constitution

**Communication Preferences**:
```markdown
- Be concise but include examples
- Use bullet points for clarity
- Explain complex concepts with analogies
```

**Working Principles**:
```markdown
- Write tests first (TDD)
- Document public APIs
- Prioritize readability over cleverness
```

**Technical Stack**:
```markdown
Primary: Python, TypeScript, PostgreSQL
Familiar: Go, React, Docker
Learning: Rust, Kubernetes
```

**Guardrails**:
```markdown
Prefer:
- Strong typing
- Explicit error handling
- Functional approaches

Avoid:
- Magic numbers
- Global state
- Complex inheritance
```

### Updating Your Constitution

```bash
edit .workspace/memory/constitution.md

# All AI tools will use the updated version immediately
```

---

## Searching Your Workspace

### Using the MCP Server (Claude Code)

Claude Code automatically uses the Cortext MCP server for search.

**In conversation**:
```
Search my workspace for "authentication bug"
Get context about API design decisions
Show me decision history for database choices
```

### Manual Search (ripgrep)

```bash
# Search all conversations
rg "authentication" conversations/

# Search specific type
rg "bug" conversations/*/--debug-*/

# Search by date
rg "feature" conversations/2025-11/
```

### Check Workspace Status

```bash
.workspace/scripts/bash/workspace-status.sh
```

Shows:
- Current branch
- Conversation count
- Recent conversations
- Git status

---

## Git Workflow

### Branch Strategy

All conversations commit directly to `main` with tags marking boundaries:

```bash
# List conversation tags
git tag -l "conv/*" --sort=-creatordate
# conv/003-plan-redesign
# conv/002-debug-auth
# conv/001-brainstorm-feature
```

Users can create manual branches when isolation is needed.

### Committing Work

**Auto-commit**:
```bash
.workspace/scripts/bash/commit-session.sh
```

**Manual commit**:
```bash
git add conversations/
git commit -m "[conversation] Update brainstorm: Feature X

Added 5 new ideas and prioritized top 3."
```

### Commit Message Format

```
[type] Brief summary

Detailed description.

Metadata:
- Conversation: 001-brainstorm-feature
- Phase: Implementation
```

**Types**: `[conversation]`, `[research]`, `[decision]`, `[note]`, `[workspace]`

### Working with Tags

```bash
# List all conversation tags
git tag -l "conv/*" --sort=-creatordate

# Show commits for a specific conversation
git log conv/001-brainstorm-feature..HEAD --oneline

# Find the commit for a conversation start
git show conv/001-brainstorm-feature
```

---

## Custom Conversation Types

Create conversation types tailored to your needs!

### Using `/workspace.add` (Claude Code)

```
/workspace.add
```

Claude will interview you:
1. What to call it?
2. What's the purpose?
3. What sections?
4. What information to capture?
5. What outputs?

Then it generates:
- Template markdown file
- Bash script
- Slash command
- Registry entry

### Manual Creation

1. **Create template**: `.workspace/templates/mytype.md`
2. **Create script**: `.workspace/scripts/bash/mytype.sh`
3. **Create command**: `.claude/commands/workspace_mytype.md`
4. **Update registry**: `.workspace/registry.json`

### Example: Book Notes

```markdown
# Book Notes: [TITLE]

## Book Info
- Author: [AUTHOR]
- Published: [YEAR]
- Genre: [GENRE]

## Reading Progress
- Started: [DATE]
- Status: [Reading/Completed]
- Current Page: [PAGE]

## Chapter Notes
### Chapter [N]: [TITLE]
[Your notes]

## Key Insights
- [Insight 1]
- [Insight 2]

## Quotes
> "[Quote]" - Page [N]

## Personal Reflections
[Your thoughts]

## Rating: [X]/5
```

---

## Multi-AI Support

Cortext works with multiple AI tools!

### Supported Tools

- **Claude Code**: Full support, slash commands, MCP server
- **Cursor**: Rules-based, automatic context
- **OpenCode**: Custom prompts, local models
- **Gemini CLI**: TOML commands, Google AI

### Configure All Tools

```bash
cortext init --ai=all
```

Creates configurations for all supported tools.

### Switch Between Tools

```bash
# Use Claude Code
claude

# Use Cursor
cursor .

# Use OpenCode
opencode

# All use the same workspace!
```

See [Multi-AI Support](multi-ai-support.md) for details.

---

## Best Practices

### 1. Update Your Constitution Regularly

As your preferences evolve, update the constitution:
```bash
edit .workspace/memory/constitution.md
```

### 2. Commit Often

Don't lose work! Commit after each significant conversation:
```bash
.workspace/scripts/bash/commit-session.sh
```

### 3. Cross-Reference Past Work

Before starting new conversations, search for related ones:
```
Search workspace for "similar topic"
```

### 4. Use the Right Conversation Type

Match the conversation type to your goal:
- Ideation → Brainstorm
- Bug fixing → Debug
- Planning → Plan
- Learning → Learn

### 5. Document Decisions

When making important decisions, log them:
```bash
edit .workspace/memory/decisions.md
```

### 6. Keep Context Updated

Update your current focus regularly:
```bash
edit .workspace/memory/context.md
```

### 7. Review Past Conversations

Periodically review old conversations to:
- Extract insights
- Identify patterns
- Update documentation

---

## Tips & Tricks

### Quick Status Check

```bash
# Alias this for convenience
alias ws-status='.workspace/scripts/bash/workspace-status.sh'
```

### Search Shortcuts

```bash
# Add to ~/.bashrc or ~/.zshrc
alias ws-search='rg --json'
alias ws-find='find conversations/ -name "*.md"'
```

### View Recent Conversations

```bash
ls -lt conversations/*/ | head -10
```

### Export Conversations

```bash
# Create archive of all conversations
tar -czf workspace-backup-$(date +%Y%m%d).tar.gz conversations/
```

### Templates Customization

Edit templates to match your style:
```bash
edit .workspace/templates/brainstorm.md
```

### Git Log Search

```bash
# Find commits about specific topics
git log --grep="authentication"

# See conversation commits
git log --grep="\\[conversation\\]"
```

### Workspace Portability

Your workspace is just files! Sync across machines:
```bash
# On machine 1
cd ~/my-workspace
git push

# On machine 2
git clone <repo> ~/my-workspace
```

---

## Troubleshooting

**"Not in a Cortext workspace"**
→ Run `cortext init` or `cd` to your workspace directory

**Slash commands not working**
→ Ensure `.claude/commands/` exists and you're in workspace root

**Search not finding anything**
→ Check ripgrep is installed: `brew install ripgrep`

**Git conflicts**
→ All conversations commit to main; use `git revert` to undo changes

**MCP server not working**
→ Reinstall: `pip install -e .` and verify: `which cortext-mcp`

---

## Next Steps

Now that you understand Cortext:

1. ✅ **Customize your constitution**
2. ✅ **Start your first conversation**
3. ✅ **Explore different conversation types**
4. ✅ **Create a custom conversation type**
5. ✅ **Search your growing knowledge base**

Happy knowledge work! 🧠
