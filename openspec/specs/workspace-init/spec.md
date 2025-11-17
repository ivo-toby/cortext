# workspace-init Specification

## Purpose
TBD - created by archiving change create-conversation-type-folders. Update Purpose after archive.
## Requirements
### Requirement: Init SHALL create conversation type folders at workspace root
When initializing a workspace, the system SHALL create the base folder for each conversation type at the workspace root level (not nested under a parent folder), ensuring a flat, type-first organization.

**ID:** `INIT-FOLDERS-001` | **Priority:** High

#### Scenario: Creating built-in type folders
**Given** cortext init creates a registry with 6 built-in conversation types
**When** the initialization completes
**Then** the following folders SHALL exist at workspace root:
- `brainstorm/`
- `debug/`
- `learn/`
- `meeting/`
- `plan/`
- `review/`
**And** NO `conversations/` parent folder SHALL be created

#### Scenario: Folders match registry exactly
**Given** the registry defines `"meeting"` with folder `"meeting"`
**When** the folder is created
**Then** the folder path SHALL be exactly `meeting/` at workspace root
**And** NOT `meetings/` (plural)
**And** NOT `conversations/meeting/` (nested)
**And** the folder name SHALL match the conversation type key

#### Scenario: Custom type folder creation
**Given** a user creates a custom conversation type "retrospective"
**When** the type is added to the registry with folder "retrospective"
**Then** the folder `retrospective/` SHALL be created at workspace root
**And** the folder name SHALL match the type key exactly

---

### Requirement: Type folders SHALL be tracked in git
Empty conversation type folders SHALL contain a `.gitkeep` file to ensure they are tracked in the git repository and included in the initial commit.

**ID:** `INIT-FOLDERS-002` | **Priority:** Medium

#### Scenario: Gitkeep files in type folders
**Given** cortext init creates conversation type folders
**When** the folders are created
**Then** each folder SHALL contain a `.gitkeep` file
**And** the gitkeep files SHALL be included in the initial git commit

#### Scenario: Empty folders persist after clone
**Given** a workspace is initialized and pushed to remote
**When** another user clones the repository
**Then** all conversation type folders SHALL exist
**And** each folder SHALL contain its `.gitkeep` file

---

### Requirement: Folder creation SHALL occur after registry creation
The conversation type folders SHALL be created immediately after the registry is generated, using the registry as the source of truth for folder paths.

**ID:** `INIT-FOLDERS-003` | **Priority:** Medium

#### Scenario: Registry-driven folder creation
**Given** the registry has been created with conversation_types
**When** folder creation is performed
**Then** folders SHALL be created by iterating through registry entries
**And** each type's "folder" value SHALL be used as the folder path
**And** folders SHALL be resolved relative to workspace root

---

