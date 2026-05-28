# Multi-AI Tool Support

Cortext works with multiple AI coding assistants, providing a consistent workspace experience across tools.

## Supported Tools

### 1. Claude Code ✅ Full Support

**Configuration**: `.claude/commands/`

**Available Commands**:
- `/workspace.brainstorm` - Start brainstorming
- `/workspace.debug` - Debug systematically
- `/workspace.plan` - Plan features
- `/workspace.learn` - Document learning
- `/workspace.meeting` - Capture meetings
- `/workspace.review` - Conduct reviews
- `/workspace.add` - Create custom types

**Setup**:
```bash
cortext init --ai=claude
# or
cortext init --ai=all
```

### 2. Cursor ✅ Full Support

**Configuration**: `.cursorrules`

Cursor automatically reads the `.cursorrules` file which contains:
- Workspace structure understanding
- Constitution integration
- Git workflow guidance
- Conversation type documentation

**Setup**:
```bash
cortext init --ai=cursor
# or
cortext init --ai=all
```

**Usage**:
Just open your workspace in Cursor - it will automatically read the rules.

### 3. OpenCode ✅ Basic Support

**Configuration**: `.opencode/`

**Features**:
- Workspace assistant prompt
- Command directory
- Constitution integration

**Setup**:
```bash
cortext init --ai=opencode
# or
cortext init --ai=all
```

**Usage**:
OpenCode will read the workspace configuration and provide assistance based on your constitution.

### 4. Codex CLI ✅ Full Support

**Configuration**: `.codex/prompts/` (workspace reference) + `~/.codex/prompts/` (active)

Cortext converts commands to Codex prompt format and writes an `AGENTS.md` at the workspace root that Codex reads automatically for context.

**Setup (new workspace)**:
```bash
cortext init --ai=codex
# or
cortext init --ai=all
```

**Setup (existing workspace)**:
```bash
cortext upgrade --add-tool codex
cortext mcp install --ai codex
```

**Available Commands** (via `/` in Codex):
- `/workspace_brainstorm` - Start brainstorming
- `/workspace_debug` - Debug systematically
- `/workspace_plan` - Plan features
- `/workspace_learn` - Document learning
- `/workspace_meeting` - Capture meetings
- `/workspace_review` - Conduct reviews
- `/workspace_add` - Create custom types

**MCP Server**: Configured via `.codex/config.toml`:
```toml
[mcp_servers.cortext]
command = "cortext-mcp"
```

**Notes**:
- Prompts are installed to `~/.codex/prompts/` (the path Codex scans) and also kept in `.codex/prompts/` for version control
- `AGENTS.md` at workspace root is read by Codex automatically — no slash command needed for context
- Custom types created with `/workspace.add` are also available as `/workspace_{type}` in Codex

### 5. Gemini CLI ✅ Basic Support

**Configuration**: `.gemini/commands/` (TOML format)

Cortext automatically converts Claude Code commands to Gemini CLI TOML format.

**Setup**:
```bash
cortext init --ai=gemini
# or
cortext init --ai=all
```

**Available Commands**:
Same as Claude Code commands, but in TOML format:
- `brainstorm.toml`
- `debug.toml`
- `plan.toml`
- `learn.toml`
- `meeting.toml`
- `review.toml`
- `add.toml`

## Configure All Tools at Once

```bash
# Initialize with all AI tool configurations
cortext init --ai=all
```

This creates:
- `.claude/commands/` - Claude Code
- `.cursorrules` - Cursor
- `.opencode/` - OpenCode
- `.codex/prompts/` + `~/.codex/prompts/` + `AGENTS.md` - Codex CLI
- `.gemini/commands/` - Gemini CLI

## Constitution: The Key to Consistency

All tools read from `.workspace/memory/constitution.md`, ensuring:
- Consistent communication style
- Same working principles
- Shared technical preferences
- Unified guardrails

**Update once, applies everywhere**:
```bash
edit .workspace/memory/constitution.md
```

## Switching Between Tools

The workspace is tool-agnostic:

```bash
# Use with Claude Code
cd ~/my-workspace
claude

# Use with Codex CLI
cd ~/my-workspace
codex

# Use with Cursor
cursor ~/my-workspace

# Use with OpenCode
cd ~/my-workspace
opencode

# Use with Gemini CLI
cd ~/my-workspace
gemini
```

All tools:
- Read the same constitution
- Use the same directory structure
- Create conversations in the same format
- Commit to the same git repository

## Tool-Specific Features

### Claude Code
- Rich slash commands (`/workspace.brainstorm` etc.)
- MCP server integration (search workspace)
- Hooks for automation
- Best documentation coverage

### Codex CLI
- Slash commands (`/workspace_brainstorm` etc.)
- `AGENTS.md` for automatic workspace context — no setup needed per session
- MCP server integration (`[mcp_servers.cortext]`)
- Agent-first design; good for multi-agent workflows

### Cursor
- AI-powered code completion
- Rules-based context
- Inline suggestions
- Good for active coding

### OpenCode
- Local model support
- Open source
- Customizable agents
- Privacy-focused

### Gemini CLI
- Google's AI models
- Command-line interface
- TOML-based configuration
- Good for scripting

## Best Practices

### 1. Start with One Tool
Choose the tool you'll use most and start there:
```bash
cortext init --ai=claude  # or codex, cursor, opencode, gemini
```

### 2. Add Others as Needed
Use `--add-tool` on an existing workspace (non-destructive — won't touch your customizations):
```bash
cd ~/my-workspace
cortext upgrade --add-tool codex
cortext mcp install --ai codex
```

### 3. Keep Constitution Updated
The constitution is your single source of truth:
```bash
# Update preferences
edit .workspace/memory/constitution.md

# All tools will use the new preferences
```

### 4. Use Consistent Workflows
Regardless of tool, follow the same patterns:
- Use conversation templates
- Commit atomically
- Cross-reference past work
- Update decision logs

## Comparison Matrix

| Feature | Claude Code | Codex CLI | Cursor | OpenCode | Gemini CLI |
|---------|-------------|-----------|--------|----------|------------|
| Slash Commands | ✅ Full | ✅ Full | ❌ No | ✅ Yes | ✅ Yes |
| Auto Context (AGENTS.md) | ✅ CLAUDE.md | ✅ AGENTS.md | ✅ .cursorrules | ✅ Yes | ✅ Yes |
| MCP Server | ✅ Yes | ✅ Yes | ⚠️ Limited | ⚠️ Coming | ❌ No |
| Local Models | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| Code Completion | ⚠️ Limited | ✅ Good | ✅ Excellent | ⚠️ Basic | ❌ No |
| Conversation Templates | ✅ Yes | ✅ Yes | ⚠️ Via Rules | ✅ Yes | ✅ Yes |
| Git Integration | ✅ Good | ✅ Good | ✅ Good | ✅ Good | ⚠️ Manual |
| Custom Types | ✅ Full | ✅ Full | ⚠️ Via Rules | ✅ Yes | ✅ Yes |

## Troubleshooting

### Commands Not Working

**Claude Code**: Ensure you're in the workspace directory with `.claude/commands/`

**Codex CLI**: Check that `~/.codex/prompts/` has the workspace prompt files. If missing, run `cortext upgrade --add-tool codex` from the workspace directory.

**Cursor**: Check that `.cursorrules` exists

**OpenCode**: Verify `.opencode/command/` directory exists

**Gemini CLI**: Check `.gemini/commands/` has TOML files

### Constitution Not Being Followed

1. Verify constitution exists: `cat .workspace/memory/constitution.md`
2. Update it with clear instructions
3. Restart your AI tool
4. Explicitly reference it in your first message: "Please read my constitution"

### Tool Conflicts

Different tools can coexist peacefully. They all use:
- Same git repository
- Same file structure
- Same constitution

If you get conflicts, ensure all tools commit to git properly.

## Future Enhancements

- Aider support
- Continue support
- Custom tool integration API
- Shared command registry across tools
- Tool-specific optimizations

## Contributing

Want to add support for a new tool? See `src/cortext_cli/converters.py` for the conversion API.
