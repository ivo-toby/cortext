# Proposal: Refine Conversation Dating

**Change ID:** `refine-conversation-dating`
**Status:** Draft
**Created:** 2025-11-10
**Author:** System

---

## Why

Currently, conversations are organized in directories using the pattern `[year-month]/[number-title]` (e.g., `2025-11/001-brainstorm-feature`). This creates a single directory per month that can accumulate many conversations, making it harder to:

1. **Navigate conversations chronologically** - All conversations from an entire month are in one flat directory
2. **Quickly identify when a conversation occurred** - The month-level granularity doesn't show the specific day
3. **Organize high-activity periods** - Users with multiple daily conversations have difficulty finding specific ones

Day-level granularity provides better temporal organization, clearer chronology, and easier navigation especially for active users who may have 10+ conversations per day.

## What Changes

Change the conversation directory structure from:
```
conversations/YYYY-MM/###-type-topic/
```

To:
```
conversations/YYYY-MM-DD/###-type-topic/
```

**Example:**
- **Before:** `conversations/2025-11/001-brainstorm-new-feature/`
- **After:** `conversations/2025-11-10/001-brainstorm-new-feature/`

**Benefits:**
- Better temporal organization - conversations grouped by day
- Clearer chronology - directory name shows exact date
- Easier navigation - smaller directories per day
- More precise MCP search - filter by specific days
- Improved UX for active users with many daily conversations

## Impact

### Files Affected

**Bash Scripts (8 files):**
- `scripts/bash/brainstorm.sh`
- `scripts/bash/debug.sh`
- `scripts/bash/plan.sh`
- `scripts/bash/learn.sh`
- `scripts/bash/meeting.sh`
- `scripts/bash/review.sh`
- `scripts/bash/common.sh`
- `scripts/bash/workspace-status.sh`

**Claude Commands (1 file):**
- `claude_commands/workspace_add.md`

**MCP Server (1 file):**
- `src/cortext_mcp/server.py` - Update date_range filter to support `YYYY-MM-DD` format

**Documentation (4 files):**
- `openspec/project.md`
- `templates/cursorrules`
- `Docs/spec.md`
- `Docs/mcp-server.md`

### Backward Compatibility

**Breaking Change:** Yes - Existing workspaces will have conversations in `YYYY-MM/` folders.

**Migration Strategy:**
1. New conversations use `YYYY-MM-DD/` format (forward-only)
2. Old conversations remain in `YYYY-MM/` folders (search still works)
3. Optional migration script (future enhancement if needed)

**Decision:** Accept that old and new formats will coexist. This is acceptable because:
- Search (ripgrep) will find conversations regardless of folder structure
- The workspace_status script will count conversations from both formats
- No data loss or corruption
- Clean break for new behavior

## Non-Goals

- ❌ Migrating existing conversations to new format (can be added later if users request it)
- ❌ Supporting hour/minute granularity (day-level is sufficient)
- ❌ Changing conversation ID numbering scheme

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Users confused by two formats | Low | Document the change clearly |
| Search may need adjustment | Medium | Test MCP server with both formats |
| Documentation becomes outdated | Low | Update all docs in same commit |
| External tools break | Very Low | Only affects Cortext internal scripts |

## Acceptance Criteria

- ✅ All conversation creation scripts use `YYYY-MM-DD` format
- ✅ MCP server accepts `YYYY-MM-DD` in date_range parameter
- ✅ workspace-status.sh shows correct counts for both formats
- ✅ Documentation reflects new format with notes about backward compatibility
- ✅ Manual testing creates conversations with daily folders

## Timeline

**Estimated Effort:** 1-2 hours
**Complexity:** Low

---

## Related Specifications

- `conversation-management` - Core conversation directory structure
- `mcp-search` - Date range filtering in MCP server

## References

- Current implementation: `scripts/bash/common.sh:59`
- Date format used: `date +%Y-%m` → `date +%Y-%m-%d`
- MCP server filter: `src/cortext_mcp/server.py:69`
