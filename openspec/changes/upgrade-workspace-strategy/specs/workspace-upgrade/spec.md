# Specification: workspace-upgrade

## Overview

This specification defines the workspace upgrade system that enables safe migration of Cortext workspaces to newer versions while preserving user customizations.

## ADDED Requirements

### Requirement: System SHALL provide a cortext upgrade command
The system SHALL provide a CLI command to upgrade workspaces from older Cortext versions to the currently installed version. The command SHALL handle both interactive and non-interactive modes.

**Priority**: High

#### Scenario: Upgrading a workspace with unmodified files
- **GIVEN** a workspace created with Cortext 0.2.0
- **AND** the user has Cortext 0.3.0 installed
- **AND** no conversation type files have been modified
- **WHEN** the user runs `cortext upgrade`
- **THEN** all built-in and custom type files are updated silently
- **AND** the registry `workspace_meta.cortext_version` is updated to "0.3.0"
- **AND** `workspace_meta.last_upgraded` is set to the current timestamp

#### Scenario: Upgrading a workspace with modified custom type
- **GIVEN** a workspace with a custom "retro" conversation type
- **AND** the user has modified `.workspace/scripts/bash/retro.sh`
- **WHEN** the user runs `cortext upgrade`
- **THEN** the system detects the modification via hash comparison
- **AND** prompts the user with options: overwrite, keep, create .new, show diff
- **AND** respects the user's choice for that file

#### Scenario: Running upgrade with --dry-run flag
- **GIVEN** a workspace that needs upgrading
- **WHEN** the user runs `cortext upgrade --dry-run`
- **THEN** the system displays what would change without modifying any files
- **AND** shows the status of each conversation type (unmodified/modified)
- **AND** lists specific files that would be updated

#### Scenario: Running upgrade with --yes flag
- **GIVEN** a workspace with modified files
- **WHEN** the user runs `cortext upgrade --yes`
- **THEN** the system accepts default actions for all prompts
- **AND** creates backups of overwritten modified files
- **AND** completes without requiring user input

#### Scenario: Running upgrade on current workspace
- **GIVEN** a workspace already at the installed Cortext version
- **WHEN** the user runs `cortext upgrade`
- **THEN** the system displays "Workspace is up to date"
- **AND** exits without making changes

---

### Requirement: System SHALL detect file modification status
The system SHALL compare current file content against stored original hashes to determine if users have made customizations. Files SHALL be classified into four statuses: UNMODIFIED, MODIFIED, DELETED, or UNKNOWN.

**Priority**: High

#### Scenario: Detecting unmodified file
- **GIVEN** a file with stored original hash
- **AND** the file content matches the original hash
- **WHEN** the upgrade system checks the file status
- **THEN** the file is classified as UNMODIFIED

#### Scenario: Detecting modified file
- **GIVEN** a file with stored original hash
- **AND** the file content differs from the original hash
- **WHEN** the upgrade system checks the file status
- **THEN** the file is classified as MODIFIED

#### Scenario: Detecting deleted file
- **GIVEN** a file with stored original hash
- **AND** the file no longer exists on disk
- **WHEN** the upgrade system checks the file status
- **THEN** the file is classified as DELETED

#### Scenario: Handling unknown file (legacy)
- **GIVEN** a conversation type without stored hashes (legacy workspace)
- **WHEN** the upgrade system checks the file status
- **THEN** the file is classified as UNKNOWN
- **AND** is treated as MODIFIED for safety

---

### Requirement: System SHALL backup modified files before overwrite
When overwriting a modified file, the system SHALL create a timestamped backup to enable recovery. Backups SHALL be stored in `.workspace/backup/` with timestamped filenames.

**Priority**: High

#### Scenario: Creating backup on overwrite
- **GIVEN** a modified file the user chooses to overwrite
- **WHEN** the upgrade system overwrites the file
- **THEN** a backup is created at `.workspace/backup/{filename}.{timestamp}.bak`
- **AND** the timestamp format is YYYYMMDD-HHMMSS
- **AND** the backup contains the original modified content

#### Scenario: Multiple backups of same file
- **GIVEN** a file that has been backed up before
- **WHEN** the user overwrites it again during another upgrade
- **THEN** a new backup with current timestamp is created
- **AND** previous backups are preserved

---

### Requirement: System SHALL handle legacy workspaces
Workspaces created before version tracking SHALL be detected as "legacy" and migrated to the new schema on first upgrade. The system SHALL prompt users to choose how to treat existing files.

**Priority**: Medium

#### Scenario: Upgrading legacy workspace (safe mode)
- **GIVEN** a workspace without `workspace_meta` in registry
- **WHEN** the user runs `cortext upgrade`
- **AND** chooses "treat files as potentially modified"
- **THEN** the system adds version metadata to registry
- **AND** all files are treated as MODIFIED (prompts for each)
- **AND** current file hashes become the new baseline

#### Scenario: Upgrading legacy workspace (fast mode)
- **GIVEN** a workspace without `workspace_meta` in registry
- **WHEN** the user runs `cortext upgrade`
- **AND** chooses "treat files as unmodified"
- **THEN** the system adds version metadata to registry
- **AND** all files are updated without prompts
- **AND** new file hashes become the baseline

---

### Requirement: System SHALL provide regeneration option for custom types
Users SHALL be able to force regeneration of specific custom types to reset them to template defaults using the `--regenerate TYPE` flag.

**Priority**: Medium

#### Scenario: Regenerating a custom type
- **GIVEN** a custom "retro" conversation type with modifications
- **WHEN** the user runs `cortext upgrade --regenerate retro`
- **THEN** the system regenerates retro from its template
- **AND** backs up all current files
- **AND** updates hashes to new baseline

#### Scenario: Regenerating non-existent type
- **GIVEN** no "foobar" conversation type exists
- **WHEN** the user runs `cortext upgrade --regenerate foobar`
- **THEN** the system displays error "Conversation type 'foobar' not found"

---

### Requirement: System SHALL provide diff viewing for modified files
Users SHALL be able to see what they changed before deciding how to handle a modified file by selecting a "Show diff" option during interactive upgrade.

**Priority**: Low

#### Scenario: Viewing diff of modified file
- **GIVEN** a modified file during upgrade
- **WHEN** the user selects "Show diff" option
- **THEN** the system displays a unified diff
- **AND** shows user changes from original to current
- **AND** returns to the options prompt

---

### Requirement: System SHALL support creating .new files for manual merge
Users SHALL be able to create side-by-side files to merge changes manually by selecting a "Create .new file" option during interactive upgrade.

**Priority**: Low

#### Scenario: Creating .new file
- **GIVEN** a modified file during upgrade
- **WHEN** the user selects "Create .new file" option
- **THEN** the system creates `{filename}.new` with the new version
- **AND** leaves the original modified file unchanged
- **AND** logs the path for manual merge

---

### Requirement: System SHALL support built-in-only upgrades
Users SHALL be able to upgrade only built-in types and skip all custom types using the `--built-in-only` flag.

**Priority**: Low

#### Scenario: Upgrading built-in types only
- **GIVEN** a workspace with built-in and custom types
- **WHEN** the user runs `cortext upgrade --built-in-only`
- **THEN** only built-in conversation types are upgraded
- **AND** custom types are completely skipped
- **AND** the registry version is still updated
