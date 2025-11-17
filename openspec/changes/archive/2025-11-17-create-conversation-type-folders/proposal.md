# Proposal: Create Conversation Type Folders During Init

**Change ID:** `create-conversation-type-folders`
**Status:** Proposed
**Created:** 2025-11-16

---

## Why

### Problem Statement

When `cortext init` creates a new workspace, it does NOT create the type-specific conversation folders that are defined in the registry. This causes confusion and inconsistency:

1. **Missing folders at init**: Users expect to see `conversations/meeting/`, `conversations/brainstorm/`, etc. but only `conversations/` exists
2. **First conversation creates folder**: The bash scripts create these folders on-demand, but users don't know where their conversations will go until they create one
3. **Inconsistent user experience**: The registry defines folders but they don't exist in the filesystem

**Current behavior (buggy):**
```
workspace/
├── conversations/              # Wrong! Nested structure
│   └── meeting/               # Created on-demand under conversations/
└── .workspace/
    └── registry.json          # Defines "conversations/meeting" (wrong nesting)
```

**Expected behavior:**
```
workspace/
├── brainstorm/                # Top-level, type-first organization
├── debug/
├── learn/
├── meeting/
├── plan/
├── review/
└── .workspace/
    └── registry.json          # Defines "meeting" (not "conversations/meeting")
```

---

## What Changes

### 1. Change Registry Folder Paths

Update registry to use top-level paths instead of nested under `conversations/`:
- OLD: `"folder": "conversations/meeting"`
- NEW: `"folder": "meeting"`

### 2. Remove `conversations/` Parent Folder

Remove `conversations/` from the directory structure created during init. Each type gets its own top-level folder.

### 3. Pre-create Type Folders in Init

After creating the registry, iterate through all conversation types and create their base folders at workspace root.

### 4. Add .gitkeep Files

Git doesn't track empty directories. Add `.gitkeep` files to ensure the folders are committed.

### 5. Update Documentation

Update all references from `conversations/{type}/` to `{type}/` structure.

### 6. MCP Server Path Updates

Update MCP search paths to look in type folders at root level.

---

## Impact Analysis

### Files Changed
- `src/cortext_cli/commands/init.py` - Registry paths and folder creation
- `src/cortext_mcp/server.py` - Search paths for conversations
- `README.md` - Directory structure examples
- `Docs/user-guide.md` - Workspace structure documentation
- `Docs/spec.md` - Architecture documentation
- `openspec/project.md` - Project conventions

### User Experience
- **Cleaner structure**: Type-first organization at workspace root
- **Less nesting**: `meeting/` vs `conversations/meeting/`
- **More intuitive**: Each type is a top-level domain folder
- **Better discoverability**: Users see all conversation types immediately

### Risk Assessment
- **Breaking change for existing workspaces**: Old workspaces use `conversations/{type}/`
- **Migration required**: Existing workspaces need manual migration OR dual-format support
- **Medium risk**: Significant structural change

### Breaking Change Notes
- **New workspaces**: Will use top-level type folders
- **Existing workspaces**: Will still have `conversations/{type}/` structure
- **Recommendation**: Support both formats in MCP server for backward compatibility

---

## Design Decisions

### Decision 1: Create Folders After Registry
**Choice**: Create folders immediately after registry is created
**Rationale**: Registry defines the folder structure, so create folders based on registry

### Decision 2: Use .gitkeep Files
**Choice**: Add `.gitkeep` to each empty folder
**Rationale**: Ensures empty folders are tracked in git

### Decision 3: Read from Registry
**Choice**: Create folders based on registry entries, not hardcoded list
**Rationale**: Supports custom types and future changes automatically

---

## Acceptance Criteria

1. `cortext init` creates `{type}/` folders at workspace root (NOT under `conversations/`)
2. Registry defines folders as `"meeting"` not `"conversations/meeting"`
3. Each folder contains a `.gitkeep` file
4. Folders are tracked in the initial git commit
5. Folder names match registry keys exactly (singular: `meeting`, not `meetings`)
6. MCP server searches in `{type}/` paths
7. Custom types added via `/workspace.add` use top-level folders
8. Documentation reflects new structure
9. No `conversations/` parent folder is created

---

## Spec Deltas

- `specs/workspace-init/spec.md` - Requirements for workspace initialization
