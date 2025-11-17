# Tasks: Create Conversation Type Folders During Init

**Change ID:** `create-conversation-type-folders`

---

## Implementation Tasks

### Phase 1: Registry Path Changes

- [x] **Update registry folder paths to top-level**
  - Change `"folder": "conversations/brainstorm"` → `"folder": "brainstorm"`
  - Change `"folder": "conversations/debug"` → `"folder": "debug"`
  - Change `"folder": "conversations/learn"` → `"folder": "learn"`
  - Change `"folder": "conversations/meeting"` → `"folder": "meeting"`
  - Change `"folder": "conversations/plan"` → `"folder": "plan"`
  - Change `"folder": "conversations/review"` → `"folder": "review"`
  - Verify: Registry uses top-level paths

- [x] **Remove conversations/ from init structure**
  - Remove `workspace_dir / "conversations"` from directory list
  - Type folders will be created based on registry
  - Verify: No `conversations/` folder created

### Phase 2: Folder Creation Implementation

- [x] **Add folder creation function**
  - Create `create_conversation_type_folders(workspace_dir, registry, tracker)` function
  - Iterate through `registry["conversation_types"]`
  - Extract "folder" path for each type (now just "meeting", not "conversations/meeting")
  - Create folder at workspace root using `Path.mkdir(parents=True, exist_ok=True)`
  - Add `.gitkeep` file to each folder
  - Track progress with StepTracker
  - Verify: Function creates all type folders at root

- [x] **Integrate into init workflow**
  - Call `create_conversation_type_folders()` after `create_registry()`
  - Pass the registry dict to the function (return it from create_registry)
  - Ensure folders are created before initial git commit
  - Verify: `cortext init` creates type folders at root

- [x] **Update create_registry to return registry**
  - Modify `create_registry()` to return the registry dict
  - Store return value in init() for use by folder creation
  - Verify: Registry is accessible for folder creation

### Phase 3: MCP Server Updates

- [x] **Update MCP search paths**
  - Change search base from `conversations/` to workspace root
  - Update glob patterns to search `{type}/` folders
  - Ensure backward compatibility with old `conversations/{type}/` structure
  - Verify: MCP server finds conversations in new structure

- [x] **Update path detection in MCP server**
  - Adjust conversation name extraction for new depth
  - OLD: `conversations/{type}/YYYY-MM-DD/###-name/` (depth i+3)
  - NEW: `{type}/YYYY-MM-DD/###-name/` (depth i+2)
  - Verify: Correct conversation names extracted

### Phase 4: Custom Type Generation

- [x] **Update workspace_add.md slash command**
  - Change generated folder path from `"conversations/{type}"` to `"{type}"`
  - Update examples to show top-level structure
  - Verify: Custom types use top-level folders

### Phase 5: Error Handling

- [x] **Add error handling for folder creation**
  - Handle permission errors gracefully
  - Skip folder if it already exists
  - Log warnings for failures but don't abort init
  - Verify: Init continues even if folder creation partially fails

### Phase 6: Testing

- [x] **Manual testing of folder creation**
  - Test fresh `cortext init`
  - Verify all 6 type folders created at workspace root
  - Verify NO `conversations/` folder created
  - Verify `.gitkeep` files exist in each type folder
  - Verify folders are in initial git commit
  - Check git status shows clean after init
  - Verify: All acceptance criteria pass

- [x] **Test conversation creation**
  - Run `/workspace.meeting` or bash script
  - Verify conversation created at `meeting/YYYY-MM-DD/###-name/`
  - NOT at `conversations/meeting/YYYY-MM-DD/###-name/`
  - Verify: Correct path structure

- [x] **Test MCP server search**
  - Verify MCP server finds conversations in new structure
  - Test search with date filters
  - Test type filters
  - Verify: Search works correctly

### Phase 7: Documentation Updates

- [x] **Update README directory structure**
  - Show type folders at workspace root
  - Remove `conversations/` from structure
  - Update all path examples
  - Verify: Documentation matches implementation

- [x] **Update project.md**
  - Change workspace structure section
  - Update from `conversations/{type}/` to `{type}/`
  - Verify: Project conventions updated

- [x] **Update spec.md**
  - Update architecture documentation
  - Change all path references
  - Verify: Spec reflects new structure

- [x] **Update CHANGELOG**
  - Document breaking change
  - Explain folder structure reorganization
  - Note backward compatibility considerations
  - Verify: Changes clearly documented

### Phase 8: Finalization

- [x] **Mark all tasks complete**
  - Review all items verified
  - Ensure documentation updated
  - Confirm tests pass

- [x] **Commit changes**
  - Use conventional commit format
  - Include comprehensive description
  - Reference folder creation improvement

---

## Validation Checklist

Before marking complete:

- [x] Registry uses top-level paths ("meeting" not "conversations/meeting")
- [x] All 6 built-in type folders created at workspace root
- [x] NO `conversations/` parent folder created
- [x] Each folder contains `.gitkeep` file
- [x] Folders tracked in initial git commit
- [x] Folder names are singular (meeting, not meetings)
- [x] Conversations saved to `{type}/YYYY-MM-DD/###-name/`
- [x] MCP server searches in `{type}/` paths
- [x] Custom types use top-level folders
- [x] workspace_add.md generates correct paths
- [x] All documentation updated (README, project.md, spec.md)
- [x] CHANGELOG documents the breaking change

---

## Dependencies

- **None** - Self-contained enhancement to init command

## Parallel Work

- Phase 1 tasks must be sequential (function depends on integration)
- Phase 2-3 can be done after Phase 1
- Phase 4 can be done in parallel with Phase 2-3

---

## Rollback Plan

If issues arise:
1. Revert single commit
2. Old behavior restored (folders created on-demand)
3. No data loss - only affects new workspace creation
4. Existing workspaces unaffected
