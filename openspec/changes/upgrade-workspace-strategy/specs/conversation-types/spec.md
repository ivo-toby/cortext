# Specification: conversation-types

## Overview

Modifications to conversation type management to support tracking generation metadata for the upgrade system.

## MODIFIED Requirements

### Requirement: Custom conversation types SHALL record generation metadata
When users create custom conversation types via `/workspace.add`, the system SHALL record metadata about how files were generated. This metadata SHALL include version information and file hashes to enable upgrade detection.

**Priority**: High

#### Scenario: Recording custom type generation metadata
- **GIVEN** a user creates a custom conversation type "standup"
- **WHEN** the type is successfully created
- **THEN** the registry entry includes `generated_with.cortext_version`
- **AND** includes `generated_with.script_api_version` set to "1.0"
- **AND** includes `generated_with.files` with entries for script, template, and commands

#### Scenario: Hashing custom type script
- **GIVEN** a custom type script is generated
- **WHEN** the file is written to disk
- **THEN** its SHA-256 hash is computed immediately after writing
- **AND** stored in `generated_with.files.script.original_hash`

#### Scenario: Hashing custom type template
- **GIVEN** a custom type template is generated
- **WHEN** the file is written to disk
- **THEN** its SHA-256 hash is computed
- **AND** stored in `generated_with.files.template.original_hash`

#### Scenario: Hashing custom type slash commands
- **GIVEN** custom type slash commands are generated
- **WHEN** the Claude command file is written
- **THEN** its SHA-256 hash is stored in `generated_with.files.command_claude.original_hash`
- **AND** if Gemini command is created, stored in `generated_with.files.command_gemini.original_hash`

---

### Requirement: Conversation type registry entries SHALL include file tracking
The conversation type schema SHALL be extended to track individual file metadata including paths and original content hashes. Each generated file SHALL be tracked separately.

**Priority**: High

#### Scenario: Complete file tracking for new type
- **GIVEN** a new conversation type "retro" is created
- **WHEN** the registry entry is created
- **THEN** `generated_with.files` contains entries for:
  - `script` with path and original_hash
  - `template` with path and original_hash
  - `command_claude` with path and original_hash
  - Optionally `command_gemini` with path and original_hash

#### Scenario: File tracking schema structure
- **GIVEN** a conversation type registry entry
- **WHEN** the `generated_with.files` field is accessed
- **THEN** each entry has `path` (string) and `original_hash` (string starting with "sha256:")

---

### Requirement: Conversation types SHALL support API versioning
The system SHALL track script API version separately from Cortext version to detect breaking changes in generated scripts. Major API version changes SHALL require explicit handling during upgrade.

**Priority**: Medium

#### Scenario: Setting initial script API version
- **GIVEN** a conversation type is created with Cortext 0.3.0
- **WHEN** the `generated_with` metadata is recorded
- **THEN** `script_api_version` is set to the current API version (e.g., "1.0")

#### Scenario: Detecting breaking API changes
- **GIVEN** a custom type was created with script API v1.0
- **AND** current Cortext uses script API v2.0
- **WHEN** the upgrade system analyzes the type
- **THEN** it detects a major version change
- **AND** flags the type as requiring regeneration or manual migration
