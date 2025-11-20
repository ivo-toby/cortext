# Design: Hooks System Architecture

## Context

Cortext needs a systematic way to execute automation on workspace events. The brainstorm document (`Docs/brainstorm-kg-hooks-web.md`) outlines a vision for hooks that will eventually power knowledge graph integration, but we need a solid foundation first.

**Stakeholders:**
- Users who want to customize workspace automation
- Future knowledge graph integration
- RAG embedding system

**Constraints:**
- Must work on Linux, macOS, and Windows (WSL)
- Must not break existing functionality
- Must be simple enough for users to extend
- Must be fast (especially pre-commit)

## Goals / Non-Goals

### Goals
- Provide a dispatcher-based hook system for Cortext events
- Enable git hook integration for embedding on commit
- Support graceful degradation when dependencies missing
- Allow users to add custom hooks easily

### Non-Goals
- User interaction hooks (Tier 3 from brainstorm) - deferred
- Knowledge graph integration - separate proposal
- Complex orchestration or async processing
- GUI for managing hooks

## Decisions

### Decision 1: Dispatcher Pattern

**What:** Single `dispatch.sh` script routes all events to appropriate handlers.

**Why:**
- Simple to understand and debug
- Single point of entry for all automation
- Easy to extend without modifying core scripts

**Alternative considered:** Direct hook calls in each script
- Rejected: Would require editing every script for each new hook type

### Decision 2: Directory-Based Hook Organization with Multi-Hook Support

**What:** Organize hooks by event category with `.d/` directories for multiple hooks per event:
```
.workspace/hooks/
├── dispatch.sh
├── conversation/
│   ├── on-create.d/
│   │   ├── 10-embed.sh        # Default: embed conversation
│   │   ├── 20-index.sh        # Default: update index
│   │   └── 50-user-notify.sh  # User-added custom hook
│   ├── on-update.d/
│   │   └── 10-embed.sh
│   └── on-archive.d/
│       └── 10-cleanup.sh
└── git/
    ├── pre-commit.d/
    │   └── 10-embed-staged.sh
    └── post-checkout.d/
        └── 10-rebuild.sh
```

**Why:**
- Clear organization by domain
- Easy to find and modify hooks
- **Multiple hooks per event** - users add scripts without modifying defaults
- Numeric prefixes control execution order
- Similar to `/etc/profile.d/`, `cron.d/`, familiar Unix pattern

**Alternative considered:** Single script per event
- Rejected: Users would have to modify default hooks to add custom logic

**Alternative considered:** Flat directory with prefixed names
- Rejected: Less organized, harder to manage at scale

### Decision 3: Bash for Hooks

**What:** All hooks are bash scripts.

**Why:**
- Consistent with existing Cortext scripts
- No additional dependencies
- Users are familiar with bash
- Fast startup time (critical for pre-commit)

**Alternative considered:** Python hooks
- Rejected: Slower startup, overkill for simple automation

### Decision 4: Source-of-Truth Pattern for Embeddings

**What:** Never commit embedding data; only source markdown is versioned.

**Why (from brainstorm analysis):**
- Avoids merge conflicts with binary embedding data
- Clean git history
- Deterministic: same content = same embeddings
- First clone is slower but subsequent work is clean

**Implementation:**
- Pre-commit: Embed staged files, but don't commit embedding data
- Post-checkout: Rebuild embeddings for missing files
- `.gitignore`: Continue ignoring `.cortext_rag/`

### Decision 5: Smart Embedding in Pre-commit

**What:** Only embed files that are staged for commit, not `--all`.

**Why:**
- Much faster than full workspace embed
- Atomic: ensures staged files are searchable
- Reduces pre-commit time significantly

**Implementation:**
```bash
# In pre-commit hook
staged_files=$(git diff --cached --name-only --diff-filter=AM '*.md')
for file in $staged_files; do
    cortext embed "$file" 2>/dev/null || true
done
```

### Decision 6: Graceful Degradation

**What:** Hooks fail silently if dependencies are missing.

**Why:**
- Core functionality works without RAG installed
- Users aren't blocked by optional features
- Consistent with existing `auto-embed.sh` pattern

**Implementation:**
```bash
# Check before running
if ! command -v cortext &> /dev/null; then
    exit 0  # Silent exit
fi
```

### Decision 7: Sequential Execution with Fail-Fast

**What:** Dispatcher runs all scripts in `.d/` directory in alphanumeric order, stopping on first failure.

**Why:**
- Predictable execution order via numeric prefixes
- Fail-fast prevents cascading errors
- Easy to reason about dependencies between hooks

**Implementation:**
```bash
# In dispatch.sh
hook_dir=".workspace/hooks/${category}/on-${action}.d"
for script in "$hook_dir"/*.sh; do
    if [ -x "$script" ]; then
        "$script" "$@" || exit $?
    fi
done
```

**Naming convention:**
- `10-*` through `39-*`: Core/default hooks
- `40-*` through `69-*`: User hooks (recommended range)
- `70-*` through `99-*`: Cleanup/finalization hooks

## Risks / Trade-offs

### Risk: Pre-commit Hook Too Slow
- **Mitigation:** Only process staged files, not entire workspace
- **Mitigation:** Heavy operations go to post-commit
- **Fallback:** Users can skip with `git commit --no-verify`

### Risk: Hook Conflicts with User Git Hooks
- **Mitigation:** Installation command merges, not overwrites
- **Mitigation:** Document how to integrate with existing hooks

### Risk: Debugging Difficulty
- **Mitigation:** `cortext hooks run <event>` for manual testing
- **Mitigation:** Verbose mode with `CORTEXT_HOOKS_DEBUG=1`
- **Mitigation:** Clear logging to stderr

### Trade-off: No Async Processing
- **Decision:** Keep it simple; no background jobs
- **Rationale:** Complexity not justified for current use cases
- **Future:** Can add if needed for knowledge graph

## Migration Plan

### For New Workspaces
- `cortext init` creates hooks directory with defaults
- Optional: `--with-git-hooks` flag to install git hooks

### For Existing Workspaces
- Run `cortext hooks install` to setup
- Non-destructive: won't overwrite existing hooks
- Merges with existing git hooks if present

### Rollback
- Remove `.workspace/hooks/` directory
- Remove git hooks or revert to sample versions
- No data loss (hooks are optional automation)

## Open Questions

### Q1: Should hooks be async?
**Current answer:** No. Keep it simple for now.
**Revisit when:** Knowledge graph integration requires heavy processing.

### Q2: Hook configuration file?
**Current answer:** No. Convention over configuration.
**Future:** Could add `.workspace/hooks.json` for advanced users.

### Q3: Should hook failure stop execution?
**Current answer:** Yes, by default. A failing hook stops the chain.
**Rationale:** Predictable behavior; users expect hooks to run in order.
**Future:** Could add `--continue-on-error` flag or per-hook config.

## Implementation Notes

### File Locations

| File | Purpose |
|------|---------|
| `scripts/bash/dispatch.sh` | Copy to `.workspace/hooks/` |
| `scripts/git-hooks/pre-commit` | Template for git hook |
| `cortext_cli/commands/hooks.py` | CLI command implementation |

### Event Names

Use colon-separated names for namespacing:
- `conversation:create`
- `conversation:update`
- `conversation:archive`
- `branch:create`
- `branch:delete`

### Integration Points

1. **common.sh**: Add `dispatch_hook()` function
2. **Conversation scripts**: Call `dispatch_hook "conversation:create" "$dir"`
3. **Init command**: Create hooks directory structure
4. **CLI**: New `hooks` command group
