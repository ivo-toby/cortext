# Tasks: Organize Conversation Folders

**Change ID:** `organize-conversation-folders`

---

## Implementation Tasks

### Phase 1: Registry Updates

- [x] **Update `src/cortext_cli/commands/init.py`**
  - Add `folder` field to all conversation types in `create_registry()` function
  - Brainstorm: `"folder": "conversations/brainstorm"`
  - Debug: `"folder": "conversations/debug"`
  - Plan: `"folder": "conversations/plan"`
  - Learn: `"folder": "conversations/learn"`
  - Meeting: `"folder": "conversations/meeting"`
  - Review: `"folder": "conversations/review"`
  - Verify: Create new workspace and check registry.json has folder fields

### Phase 2: Bash Script Utilities

- [x] **Add folder resolution to `scripts/bash/common.sh`**
  - Create `get_conversation_folder()` function
  - Reads registry.json for conversation type's folder
  - Falls back to `conversations/general` if not found
  - Returns absolute path to folder
  - Verify: Function reads registry correctly

### Phase 3: Update Conversation Scripts

- [x] **Update `scripts/bash/brainstorm.sh`**
  - Replace hardcoded `conversations/$(date +%Y-%m-%d)`
  - Use `get_conversation_folder "brainstorm"`
  - Should resolve to `conversations/brainstorm/YYYY-MM-DD/`
  - Verify: Create brainstorm, check it's in `conversations/brainstorm/`

- [x] **Update `scripts/bash/debug.sh`**
  - Use `get_conversation_folder "debug"`
  - Should resolve to `conversations/debug/YYYY-MM-DD/`
  - Verify: Create debug session, check folder location

- [x] **Update `scripts/bash/plan.sh`**
  - Use `get_conversation_folder "plan"`
  - Should resolve to `conversations/plan/YYYY-MM-DD/`
  - Verify: Create plan, check folder location

- [x] **Update `scripts/bash/learn.sh`**
  - Use `get_conversation_folder "learn"`
  - Should resolve to `conversations/learn/YYYY-MM-DD/`
  - Verify: Create learning notes, check folder location

- [x] **Update `scripts/bash/meeting.sh`**
  - Use `get_conversation_folder "meeting"`
  - Should resolve to `conversations/meeting/YYYY-MM-DD/`
  - Verify: Create meeting notes, check folder location

- [x] **Update `scripts/bash/review.sh`**
  - Use `get_conversation_folder "review"`
  - Should resolve to `conversations/review/YYYY-MM-DD/`
  - Verify: Create review, check folder location

### Phase 4: Supporting Scripts

- [x] **Update `scripts/bash/workspace-status.sh`**
  - Change to search `conversations/` recursively (all subfolders)
  - Update output to show breakdown by subfolder
  - Show: Total, Today, This Month, and optionally by category
  - Verify: Status shows accurate counts across all subfolders

- [x] **Update `scripts/bash/commit-session.sh`**
  - Already uses `CONVERSATIONS_DIR="${WORKSPACE_ROOT}/../conversations"`
  - Verify it still works with subfolder structure (should be fine)

### Phase 5: MCP Server Updates

- [x] **Update `src/cortext_mcp/server.py`**
  - Verify `conversations_dir` path includes all subfolders
  - Current implementation should work (searches recursively)
  - Test search finds conversations in `conversations/ideas/`, `conversations/notes/`, etc.
  - Verify: MCP search returns results from all subfolders

### Phase 6: Custom Conversation Type Support

- [x] **Update `claude_commands/workspace_add.md`**
  - Add prompt asking user which folder to use for custom type
  - Default to `conversations/{custom-type-name}/` if not specified (type name = folder name)
  - Add `folder` field to generated registry entry
  - Update generated bash script to use folder from registry
  - Verify: Create custom type, specify folder, test it saves correctly

### Phase 7: Documentation Updates

- [x] **Update `README.md`**
  - Change directory structure example to show subfolders:
    ```
    conversations/
    ├── brainstorm/   # Brainstorm conversations
    ├── debug/        # Debug conversations
    ├── learn/        # Learn conversations
    ├── meeting/      # Meeting conversations
    ├── plan/         # Plan conversations
    └── review/       # Review conversations
    ```
  - Add note about configurable folders
  - Verify: Documentation is clear

- [x] **Update `Docs/spec.md`**
  - Document `folder` field in registry
  - Explain default folder mappings
  - Show example of overriding folder in registry
  - Verify: Spec is comprehensive

- [x] **Update `Docs/user-guide.md`**
  - Add section on "Organizing Conversations"
  - Explain default folder structure
  - Show how to customize folder in registry.json
  - Provide examples of use cases
  - Verify: Users can understand and customize

- [x] **Update `openspec/project.md`**
  - Update workspace structure to show conversation subfolders
  - Verify: Project context is accurate

### Phase 8: Backward Compatibility

- [x] **Test with existing workspace**
  - Create workspace with old structure (conversations/YYYY-MM-DD/)
  - Verify old conversations still searchable
  - Verify new conversations go to subfolders
  - Verify MCP server finds both old and new conversations
  - Document: Old and new formats coexist peacefully

### Phase 9: Testing & Validation

- [x] **Functional Testing**
  - Create new workspace with `cortext init`
  - Run each conversation type script
  - Verify correct subfolder used
  - Verify conversation IDs increment within each subfolder
  - Test workspace-status shows correct breakdown

- [x] **Registry Customization Testing**
  - Manually edit registry.json, change a folder
  - Run that conversation type script
  - Verify it uses the custom folder
  - Test with invalid folder path (error handling)

- [x] **MCP Server Testing**
  - Create conversations in different subfolders
  - Run searches across all folders
  - Verify all conversations found
  - Test type filtering still works

- [x] **Custom Type Testing**
  - Use /workspace.add to create custom type
  - Specify custom folder
  - Verify custom type uses specified folder
  - Verify custom type in registry has folder field

### Phase 10: Finalization

- [x] **Update CHANGELOG.md**
  - Document new folder organization feature
  - Note backward compatibility
  - Explain migration (optional - old format still works)

- [x] **Commit Changes**
  - Use conventional commit: `[feat] Organize conversations into subfolders`
  - Include description of folder mappings and configuration

---

## Validation Checklist

Before marking complete:

- [x] All conversation scripts use folder from registry
- [x] Registry has folder field for all types
- [x] MCP server searches all subfolders
- [x] Documentation explains configuration
- [x] Backward compatibility verified
- [x] Custom types can specify folder
- [x] Manual testing passed for all conversation types

---

## Dependencies

- **None** - This change is self-contained

## Parallel Work

- Phase 3 (conversation scripts) can be done in parallel (6 independent scripts)
- Phase 7 (documentation) can be done in parallel (4 independent files)

---

## Rollback Plan

If issues arise:
1. Revert single commit containing all changes
2. Old behavior: all conversations go to `conversations/YYYY-MM-DD/`
3. No data loss - only folder organization changes
