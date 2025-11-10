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

### 4. Gemini CLI ✅ Basic Support

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
- Rich slash commands
- MCP server integration (search workspace)
- Hooks for automation
- Best documentation coverage

### Cursor
- AI-powered code completion
- Rules-based context
- Inline suggestions
- Good for active coding

### OpenCode
- Local model support (Ollama)
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
cortext init --ai=claude  # or cursor, opencode, gemini
```

### 2. Add Others as Needed
Re-run init with a different tool:
```bash
cd ~/my-workspace
cortext init --ai=cursor
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

| Feature | Claude Code | Cursor | OpenCode | Gemini CLI |
|---------|-------------|--------|----------|------------|
| Slash Commands | ✅ Full | ❌ No | ✅ Yes | ✅ Yes |
| Rules/Context | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| MCP Server | ✅ Yes | ⚠️ Limited | ⚠️ Coming | ❌ No |
| Local Models | ❌ No | ❌ No | ✅ Yes | ❌ No |
| Code Completion | ⚠️ Limited | ✅ Excellent | ⚠️ Basic | ❌ No |
| Conversation Templates | ✅ Yes | ⚠️ Via Rules | ✅ Yes | ✅ Yes |
| Git Integration | ✅ Good | ✅ Good | ✅ Good | ⚠️ Manual |

## Troubleshooting

### Commands Not Working

**Claude Code**: Ensure you're in the workspace directory with `.claude/commands/`

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
