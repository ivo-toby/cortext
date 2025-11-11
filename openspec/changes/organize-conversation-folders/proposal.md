# Proposal: Organize Conversation Folders

**Change ID:** `organize-conversation-folders`
**Status:** Draft
**Created:** 2025-11-10
**Author:** System

---

## Why

**Current Bug**: All conversation types (brainstorm, debug, plan, learn, meeting, review) save to a single flat `conversations/` directory. The workspace initialization creates separate top-level folders (`conversations/`, `research/`, `ideas/`, `notes/`, `projects/`) but they are never used by the conversation scripts.

**Problems:**
1. All conversation types mixed together in one directory, making it hard to find specific types of work
2. Top-level folders (`ideas/`, `notes/`, `projects/`, `research/`) are created but never populated
3. No logical separation between different domains of knowledge work
4. Custom conversation types have no way to specify where they should save

**User Expectation**: Different conversation types should save to semantically appropriate folders (e.g., learning notes → `notes/`, brainstorming → `ideas/`)

## What Changes

**Default Behavior**: Use subfolders under `conversations/` where each conversation type has its own folder matching the type name:
```
conversations/
├── brainstorm/     # Brainstorm conversations
├── debug/          # Debug conversations
├── learn/          # Learn conversations
├── meeting/        # Meeting conversations
├── plan/           # Plan conversations
└── review/         # Review conversations
```

**Configurable**: Add `folder` field to registry.json so users can override the default location per conversation type.

**Example Registry Entry**:
```json
"brainstorm": {
  "name": "Brainstorm",
  "folder": "conversations/brainstorm",  // NEW: Configurable folder (defaults to type name)
  "template": ".workspace/templates/brainstorm.md",
  ...
}
```

## Impact

### Files Affected

**Bash Scripts** (7 files):
- `scripts/bash/common.sh` - Add folder resolution logic
- `scripts/bash/brainstorm.sh` - Use folder from registry (default: `conversations/brainstorm/`)
- `scripts/bash/debug.sh` - Use folder from registry (default: `conversations/debug/`)
- `scripts/bash/plan.sh` - Use folder from registry (default: `conversations/plan/`)
- `scripts/bash/learn.sh` - Use folder from registry (default: `conversations/learn/`)
- `scripts/bash/meeting.sh` - Use folder from registry (default: `conversations/meeting/`)
- `scripts/bash/review.sh` - Use folder from registry (default: `conversations/review/`)

**Registry** (1 file):
- `src/cortext_cli/commands/init.py` - Add `folder` field to default registry entries

**MCP Server** (1 file):
- `src/cortext_mcp/server.py` - Update search to look in all subfolders under `conversations/`

**Documentation** (3 files):
- `README.md` - Update directory structure example
- `Docs/spec.md` - Document folder configuration
- `Docs/user-guide.md` - Explain folder organization

### Backward Compatibility

**Breaking Change**: No - this is backward compatible with a migration path.

**Migration Strategy**:
1. Existing workspaces: Conversations in `conversations/YYYY-MM-DD/` continue to work
2. New workspaces: Use subfolder structure from day one
3. Detection: Check if `conversations/YYYY-MM-DD/` exists → old format, use `conversations/general/`
4. Optional migration script (future): Move old conversations to subfolders

## Design Decisions

### Why subfolders under `conversations/` instead of top-level folders?

**Pros of subfolders**:
- All conversation data in one place (`conversations/`)
- Easier to backup/sync/search entire conversation history
- MCP server searches one directory tree
- Simpler git workflow (one `conversations/` directory to add/commit)

**Cons of top-level** (`ideas/`, `notes/`, etc. at workspace root):
- Scattered conversation data across workspace root
- MCP server must search multiple directories
- Git commits more complex (multiple directories)
- User confusion about where things are

**Decision**: Use `conversations/` subfolders for better organization while keeping data consolidated.

### Default Folder Mappings

| Conversation Type | Default Folder | Rationale |
|------------------|----------------|-----------|
| **Brainstorm** | `conversations/brainstorm/` | Type name = folder name (low cognitive load) |
| **Debug** | `conversations/debug/` | Type name = folder name (low cognitive load) |
| **Plan** | `conversations/plan/` | Type name = folder name (low cognitive load) |
| **Learn** | `conversations/learn/` | Type name = folder name (low cognitive load) |
| **Meeting** | `conversations/meeting/` | Type name = folder name (low cognitive load) |
| **Review** | `conversations/review/` | Type name = folder name (low cognitive load) |
| **Custom** | `conversations/{type-name}/` | Custom types use their type name as folder |

Users can override any of these via `folder` field in registry.

---

## Acceptance Criteria

- ✅ Registry has `folder` field for each conversation type
- ✅ Bash scripts read folder from registry (with defaults)
- ✅ New conversations save to appropriate subfolders
- ✅ MCP server searches all conversation subfolders
- ✅ Documentation explains folder configuration
- ✅ Backward compatibility maintained for existing workspaces

## Timeline

**Estimated Effort:** 2-3 hours
**Complexity:** Medium (requires registry reading in bash scripts)

---

## Related Specifications

- `conversation-management` - Core conversation directory structure
- `mcp-search` - Search across conversation folders
- `registry-system` - Conversation type metadata

## References

- Current bug: All scripts use `CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations/$(date +%Y-%m-%d)"`
- Registry structure: `src/cortext_cli/commands/init.py:283` (`create_registry()`)
- Top-level folders created: `src/cortext_cli/commands/init.py:152-158`
