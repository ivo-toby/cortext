# Tasks: Refine Conversation Dating

**Change ID:** `refine-conversation-dating`

---

## Implementation Tasks

### Phase 1: Core Scripts Update

- [x] **Update `scripts/bash/common.sh`**
  - Change `date +%Y-%m` to `date +%Y-%m-%d` in `get_current_conversation_dir()` function (line ~59)
  - Verify: Create test conversation and check directory structure

- [x] **Update conversation type scripts** (6 files)
  - `scripts/bash/brainstorm.sh` - Line 27: Change date format
  - `scripts/bash/debug.sh` - Line 27: Change date format
  - `scripts/bash/plan.sh` - Line 27: Change date format
  - `scripts/bash/learn.sh` - Line 27: Change date format
  - `scripts/bash/meeting.sh` - Line 27: Change date format
  - `scripts/bash/review.sh` - Line 27: Change date format
  - Verify: Run each script and confirm `YYYY-MM-DD` directory created

- [x] **Update `scripts/bash/workspace-status.sh`**
  - Line 39: Update `CURRENT_MONTH` to use `YYYY-MM-DD` pattern
  - Update display logic to show "This day" instead of "This month"
  - Consider showing "This month" as aggregate of all `YYYY-MM-*` folders
  - Verify: Run status script and check output formatting

### Phase 2: MCP Server Update

- [x] **Update `src/cortext_mcp/server.py`**
  - Line 69: Update description from "YYYY-MM format" to "YYYY-MM or YYYY-MM-DD format"
  - Update search logic to accept both `YYYY-MM` and `YYYY-MM-DD` patterns
  - Test `--glob` parameter with both formats
  - Verify: Search for conversations with both date formats

### Phase 3: Documentation Updates

- [x] **Update `openspec/project.md`**
  - Line 196: Change `conversations/` comment from `YYYY-MM/###-type-topic/` to `YYYY-MM-DD/###-type-topic/`
  - Verify: Documentation is accurate

- [x] **Update `templates/cursorrules`**
  - Line 8: Change conversation directory format in structure description
  - Verify: Template is consistent with new format

- [x] **Update `Docs/spec.md`**
  - Line 458: Update example from `YYYY-MM` to `YYYY-MM-DD`
  - Line 1327: Update conversation path format
  - Line 986: Update example in common.sh function documentation
  - Line 1108: Update CONVERSATIONS_DIR example
  - Verify: All references updated

- [x] **Update `Docs/mcp-server.md`**
  - Line 53: Change `date_range` description to mention both formats
  - Add example: `"2025-11-10"` alongside `"2025-11"`
  - Verify: Documentation shows backward compatibility

- [x] **Update `claude_commands/workspace_add.md`**
  - Line 110: Update date format in generated script template
  - Verify: Custom conversation types use new format

- [x] **Update `Docs/user-guide.md`** (if exists)
  - Search for `YYYY-MM` references and update to `YYYY-MM-DD`
  - Verify: User-facing docs are current

### Phase 4: Testing & Validation

- [x] **Manual Testing**
  - Create test workspace: `cortext init /tmp/test-workspace`
  - Run each conversation type script:
    - `./scripts/bash/brainstorm.sh "Test Topic"`
    - `./scripts/bash/debug.sh "Test Bug"`
    - Verify directory created: `conversations/YYYY-MM-DD/###-type-topic/`
  - Verify conversation ID increments correctly within daily folders
  - Test workspace-status script shows correct information

- [x] **MCP Server Testing**
  - Test search with old format: `date_range: "2025-11"`
  - Test search with new format: `date_range: "2025-11-10"`
  - Verify both return results correctly

- [x] **Backward Compatibility Verification**
  - Create workspace with old-format conversations
  - Verify search still finds old conversations
  - Verify status script counts both old and new formats

### Phase 5: Finalization

- [x] **Update CHANGELOG.md**
  - Add breaking change notice
  - Document new directory format
  - Mention backward compatibility approach

- [x] **Update README.md**
  - Update directory structure example (if present)
  - Note the change in Quick Start section

- [x] **Commit Changes**
  - Use conventional commit: `[breaking] Change conversation directories to daily granularity`
  - Include full description of change and migration notes

---

## Validation Checklist

Before marking complete:

- [x] All bash scripts updated and tested
- [x] MCP server accepts both date formats
- [x] Documentation fully updated
- [x] Manual testing passed for all conversation types
- [x] No regressions in existing functionality
- [x] Git commit includes all changes atomically

---

## Dependencies

- **None** - This change is self-contained

## Parallel Work

All documentation updates (Phase 3) can be done in parallel.

---

## Rollback Plan

If issues arise:
1. Revert single commit containing all changes
2. Users with new-format conversations can manually rename directories back to `YYYY-MM/` if desired
3. No data loss - only directory naming changes
