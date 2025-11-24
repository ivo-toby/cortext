# Specification: workspace-init

## Overview

Modifications to workspace initialization to support version tracking for the upgrade system.

## MODIFIED Requirements

### Requirement: System SHALL create workspace metadata with version tracking
The init command SHALL create `workspace_meta` in the registry with version information to enable upgrade detection. The metadata SHALL include the Cortext version used to create the workspace, initialization timestamp, and upgrade history.

**Priority**: High

#### Scenario: Creating new workspace with version metadata
- **GIVEN** a user runs `cortext init`
- **WHEN** the workspace is initialized successfully
- **THEN** the registry includes `schema_version` set to "2.0"
- **AND** includes `workspace_meta.cortext_version` set to current version
- **AND** includes `workspace_meta.initialized` set to current timestamp
- **AND** includes `workspace_meta.last_upgraded` set to null

#### Scenario: Registry schema version migration
- **GIVEN** a registry with `version` field (old schema)
- **WHEN** the upgrade system processes the registry
- **THEN** the `version` field is migrated to `schema_version`
- **AND** `workspace_meta` is added with version information

---

### Requirement: System SHALL record generation metadata for built-in types
When creating built-in conversation types, the init command SHALL record their generation metadata including version information and file hashes. This metadata SHALL enable the upgrade system to detect modifications.

**Priority**: High

#### Scenario: Recording built-in type generation metadata
- **GIVEN** a user runs `cortext init`
- **WHEN** built-in conversation types are created
- **THEN** each type includes `generated_with.cortext_version`
- **AND** includes `generated_with.script_api_version`
- **AND** includes `generated_with.files` with path and original_hash for each generated file

#### Scenario: Hashing generated files
- **GIVEN** a built-in type is being created
- **WHEN** the script file is generated
- **THEN** its SHA-256 hash is computed
- **AND** stored in `generated_with.files.script.original_hash`
- **AND** the format is "sha256:{hex_digest}"
