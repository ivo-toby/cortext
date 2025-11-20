# Cortext Hooks System

The hooks system provides event-driven automation for your Cortext workspace. Hooks are scripts that run automatically when specific events occur, such as creating a conversation or committing changes.

## Overview

Hooks are organized in `.workspace/hooks/` with subdirectories for each event category. Multiple scripts can run for each event, executing in alphanumeric order.

```
.workspace/hooks/
├── dispatch.sh                    # Central dispatcher
├── conversation/
│   ├── on-create.d/
│   │   ├── 10-embed.sh           # Default: embed for RAG
│   │   └── 50-my-hook.sh         # Your custom hook
│   └── on-archive.d/
│       └── 10-cleanup.sh
└── git/
    ├── pre-commit.d/
    │   └── 10-embed-staged.sh
    └── post-checkout.d/
        └── 10-rebuild.sh
```

## Available Events

### Conversation Lifecycle

| Event | When | Arguments |
|-------|------|-----------|
| `conversation:create` | After conversation is created and committed | `$1` = conversation path |
| `conversation:archive` | When conversation is archived | `$1` = conversation path |

### Git Hooks

| Event | When | Arguments |
|-------|------|-----------|
| `pre-commit` | Before git commit | (none) |
| `post-checkout` | After git checkout | `$1` = prev HEAD, `$2` = new HEAD, `$3` = branch flag |

## Creating Custom Hooks

### Using the CLI

The easiest way to create a custom hook:

```bash
cortext hooks add conversation:create my-hook
```

This creates `.workspace/hooks/conversation/on-create.d/50-my-hook.sh` with a template.

### Manual Creation

1. Create a script in the appropriate `.d/` directory
2. Use a numeric prefix to control execution order
3. Make it executable: `chmod +x your-hook.sh`

### Numeric Prefix Convention

Scripts run in alphanumeric order. Use these ranges:

- `10-39`: Core/default hooks (reserved)
- `40-69`: User custom hooks (recommended)
- `70-99`: Cleanup/finalization hooks

### Example Custom Hook

```bash
#!/usr/bin/env bash
# Custom hook: Send Slack notification on conversation create

# Graceful degradation - exit silently if dependencies missing
if ! command -v curl &> /dev/null; then
    exit 0
fi

# Get conversation path
CONVERSATION_PATH="${1:-}"
if [ -z "$CONVERSATION_PATH" ]; then
    exit 0
fi

# Extract conversation name
CONV_NAME=$(basename "$CONVERSATION_PATH")

# Send notification (replace with your webhook URL)
curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"New conversation: $CONV_NAME\"}" \
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" \
    >/dev/null 2>&1 || true

exit 0
```

## Execution Model

### Sequential Execution

Hooks run in alphanumeric order within each `.d/` directory:
- `10-first.sh` runs before `20-second.sh`
- Use numeric prefixes to control order

### Fail-Fast Behavior

If a hook exits with non-zero status:
- Execution stops immediately
- Subsequent hooks do not run
- The exit code is returned to the caller

### Graceful Degradation

Hooks should fail silently when dependencies are missing:

```bash
# Check for required command
if ! command -v my-tool &> /dev/null; then
    exit 0  # Silent exit, don't block
fi

# Check for RAG dependencies
if ! python3 -c "import cortext_rag" 2>/dev/null; then
    exit 0
fi
```

## CLI Commands

### List Hooks

```bash
cortext hooks list
```

Shows all configured hooks, grouped by event.

### Run Hook Manually

```bash
cortext hooks run conversation:create /path/to/conversation
```

Useful for testing hooks. Debug output is enabled automatically.

### Install Git Hooks

```bash
cortext hooks install
```

Installs git hooks to `.git/hooks/` that integrate with the Cortext hooks system.

### Add Custom Hook

```bash
cortext hooks add <event> <name>
```

Creates a new hook script with a template.

## Debugging

### Enable Debug Output

Set `CORTEXT_HOOKS_DEBUG=1` to see which hooks are running:

```bash
CORTEXT_HOOKS_DEBUG=1 cortext hooks run conversation:create /path
```

### Common Issues

**Hook not running:**
- Check if script is executable: `chmod +x script.sh`
- Verify it's in a `.d/` directory
- Check the event name is correct

**Hook fails silently:**
- Run manually with debug mode
- Check script has correct shebang: `#!/usr/bin/env bash`
- Verify dependencies are available

**Wrong execution order:**
- Check numeric prefix (10-39 core, 40-69 user, 70-99 cleanup)
- Remember: alphanumeric order, so `2-` comes before `10-`

## Default Hooks

### conversation/on-create.d/10-embed.sh

Embeds the new conversation for RAG search. Fails silently if RAG is not installed.

### conversation/on-archive.d/10-cleanup.sh

Placeholder for cleanup when archiving conversations. Currently does nothing.

### git/pre-commit.d/10-embed-staged.sh

Embeds staged markdown files before commit for immediate searchability.

### git/post-checkout.d/10-rebuild.sh

Checks if embedding data exists after checkout and suggests rebuilding if missing.

## Integration with RAG

The hooks system integrates with Cortext's RAG (Retrieval-Augmented Generation) system:

- **On conversation create**: Automatically embed for search
- **On pre-commit**: Embed staged markdown files
- **On post-checkout**: Check if embeddings need rebuilding

This ensures your conversations are always searchable immediately after creation or commit.

## Best Practices

1. **Use graceful degradation**: Always check for dependencies
2. **Keep hooks fast**: Especially pre-commit hooks
3. **Use numeric prefixes**: Follow the convention (40-69 for user hooks)
4. **Test manually first**: Use `cortext hooks run` before relying on automatic execution
5. **Log to stderr**: Use `>&2` for debug output to avoid interfering with pipelines
