# Tasks: Add Project Management Conversation Type

## Overview

Ordered list of work items to implement the `projectmanage` conversation type with multi-document architecture. Tasks are designed to be small and verifiable, following the established pattern for conversation types.

---

## Tasks

### 1. Create master template file
**File**: `templates/project-management.md`

- [x] Create the master conversation template with sections:
  - Goals
  - Roadmap
  - Tasks (with status markers)
  - Status Updates

**Verification**: File exists with proper placeholder syntax `[PLACEHOLDER]`

---

### 2. Create index template file
**File**: `templates/project-index.md`

- [x] Create the auto-maintained index template with:
  - Project name and metadata
  - Document listing by category
  - Links to documents
  - Last updated timestamps

**Verification**: File exists with proper placeholder syntax

---

### 3. Create bash script
**File**: `scripts/bash/projectmanage.sh`

- [x] Create bash script following pattern from `plan.sh`:
  - Source common utilities
  - Accept project name argument
  - Create conversation directory with proper naming
  - Create `docs/` subfolder structure
  - Copy master template and index template
  - Commit to git
  - Create conversation tag
  - Dispatch conversation:create hook

**Verification**: Script runs successfully, creates directory structure with `docs/` folder, commits to git

---

### 4. Create Claude slash command
**File**: `claude_commands/workspace_projectmanage.md`

- [x] Create Claude command that instructs the AI to:
  - Act as a project management assistant
  - **Proactively search workspace** using MCP tools for relevant context
  - **Create multiple documents** with descriptive filenames in appropriate subfolders
  - **Categorize content flexibly** (requirements, notes, decisions, research, etc.)
  - **Maintain index.md automatically** after every document change
  - Track tasks and status in master document
  - Provide overview and summaries on request
  - Update documents during conversation (not just at start)

**Verification**: Command follows YAML frontmatter format, includes MCP tool usage instructions, categorization guidance is clear

---

### 5. Update registry defaults
**File**: `src/cortext_cli/commands/init.py`

- [x] Add `projectmanage` entry to the `create_registry()` function with:
  - name: "Project Manage"
  - folder: "projectmanage"
  - template: ".workspace/templates/project-management.md"
  - command: "/workspace.projectmanage"
  - script: ".workspace/scripts/bash/projectmanage.sh"
  - built_in: True
  - description: "Project management and tracking"
  - sections: ["goals", "roadmap", "tasks", "status", "index"]

**Verification**: `cortext init` creates the new type in registry.json

---

### 6. Update MCP server default types
**File**: `src/cortext_mcp/server.py`

- [x] Add `projectmanage` to `DEFAULT_CONVERSATION_TYPES` constant for fallback compatibility.

**Verification**: MCP server recognizes `projectmanage` as valid type for search filtering

---

### 7. Update project documentation
**File**: `openspec/project.md`

- [x] Add `projectmanage` to the list of conversation types in Domain Context section with description of multi-document architecture.

**Verification**: Documentation reflects the new type and its unique features

---

### 8. Test end-to-end flow

Manual verification (to be done by user):
1. Run `cortext init` in test directory
2. Verify `projectmanage` folder created
3. Run `/workspace.projectmanage` command
4. Verify conversation directory created with `docs/` subfolder
5. Verify both `project-management.md` and `index.md` created
6. Verify git commit and tag created
7. Test creating a document (agent should categorize and update index)
8. Test MCP search with `type: "projectmanage"` filter
9. Test agent proactively searching for context

**Verification**: Complete workflow works including multi-document creation and index maintenance

---

## Dependencies

- Tasks 1, 2 can be done in parallel (templates)
- Task 3 depends on tasks 1, 2 (script copies both templates)
- Task 4 can be done in parallel with tasks 1, 2, 3
- Task 5 depends on tasks 1, 2, 3 (needs correct paths)
- Task 6 can be done in parallel with task 5
- Task 7 can be done anytime
- Task 8 depends on all previous tasks

## Parallelizable Work

**Wave 1** (no dependencies):
- Task 1: Master template
- Task 2: Index template
- Task 4: Claude command

**Wave 2** (after Wave 1):
- Task 3: Bash script
- Task 5: Registry update
- Task 6: MCP server update
- Task 7: Documentation

**Wave 3** (after Wave 2):
- Task 8: End-to-end testing
