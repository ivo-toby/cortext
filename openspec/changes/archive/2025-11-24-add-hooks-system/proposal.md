# Change: Add Hooks System for Event-Driven Automation

## Why

Cortext currently lacks a systematic way to trigger automation on workspace events. The only hook-like behavior is `auto-embed.sh` being called manually at the end of conversation scripts. This ad-hoc approach:

1. **Doesn't scale**: Adding new automation requires editing every conversation script
2. **No git hooks integration**: Post-commit embedding is mentioned in brainstorms but not implemented
3. **No extensibility**: Users can't add their own automation without modifying core scripts
4. **Inconsistent execution**: Some scripts call auto-embed, others don't

A proper hooks system enables deterministic, event-driven automation that can power future knowledge graph integration, automatic indexing, and user-defined workflows.

## What Changes

### Core Hooks Infrastructure

- **Dispatcher**: Central bash script that routes events to hook scripts
- **Hook directory structure**: `.workspace/hooks/` with event-based subdirectories
- **Multiple hooks per event**: `.d/` directories allow users to add custom hooks without modifying defaults
- **Event system**: Defined lifecycle events for conversations, branches, and git operations

### Tier 1: Git Hooks (`.git/hooks/`)

| Hook | Purpose |
|------|---------|
| `pre-commit` | Validate metadata, lint markdown, smart embedding |
| `post-commit` | Update indexes (lightweight, non-blocking) |
| `post-checkout` | Rebuild embeddings if needed |

### Tier 2: Cortext Lifecycle Hooks (`.workspace/hooks/`)

| Event | Purpose |
|-------|---------|
| `conversation:create` | Register in index, setup embedding |
| `conversation:update` | Incremental embedding update |
| `conversation:archive` | Clean up indexes, update stats |

### Supporting Features

- **CLI command**: `cortext hooks install` to setup git hooks
- **CLI command**: `cortext hooks run <event>` to manually trigger hooks
- **CLI command**: `cortext hooks add <event> <name>` to scaffold custom hooks
- **Hook templates**: Default hooks for common operations
- **Execution order**: Scripts run in alphanumeric order (use numeric prefixes)
- **Graceful degradation**: Hooks fail silently if dependencies missing

## Impact

### Affected Specs

- **New capability**: `hooks-system` (this proposal)

### Affected Code

- `scripts/bash/common.sh` - Add `dispatch_hook()` function
- `scripts/bash/*.sh` - All conversation scripts call dispatcher
- `cortext_cli/commands/` - New `hooks.py` command module
- `.workspace/hooks/` - New directory with dispatcher and default hooks
- `.git/hooks/` - Git hook scripts (installed via CLI)

### Migration

- Existing workspaces: Run `cortext hooks install` to setup
- Backward compatible: Scripts work without hooks (graceful degradation)
- `auto-embed.sh` calls replaced with `dispatch_hook "conversation:create"`

### Dependencies

- No new external dependencies
- Uses existing bash/Python infrastructure

### Risks

- **Merge conflicts**: Addressed by source-of-truth pattern (embeddings not committed)
- **Performance**: Pre-commit hooks must be fast; heavy work goes to post-commit
- **Complexity**: Mitigated by simple dispatcher pattern and clear documentation
