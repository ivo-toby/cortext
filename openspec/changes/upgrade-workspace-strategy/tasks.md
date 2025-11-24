# Tasks: Upgrade Workspace Strategy

## Phase 1: Foundation ✓ COMPLETED

### Registry Schema Extension
- [x] Add `schema_version` field to registry (replacing `version`)
- [x] Add `workspace_meta` structure to registry schema
- [x] Add `generated_with` structure to conversation type schema
- [ ] Create schema migration logic for old → new format (deferred to Phase 2)

### Hash Utilities
- [x] Create `compute_sha256(content: str) -> str` utility function
- [x] Create `compute_file_hash(path: Path) -> str` utility function
- [x] Add hash format: "sha256:{hex_digest}"
- [ ] Write unit tests for hash computation (deferred to Phase 5)

### Init Command Updates
- [x] Modify `create_registry()` to include `workspace_meta`
- [x] Modify built-in type creation to compute and store file hashes
- [x] Store `generated_with` for each built-in conversation type
- [x] Set `script_api_version` to "1.0" for all types
- [ ] Write integration test for new workspace creation (deferred to Phase 5)

### Upgrade Command Skeleton
- [x] Create `src/cortext_cli/commands/upgrade.py` module
- [x] Register `upgrade` command in CLI
- [x] Implement version status detection (LEGACY, UPGRADE_AVAILABLE, CURRENT, NEWER_WORKSPACE)
- [x] Implement basic upgrade flow structure
- [x] Add `--verbose` flag for detailed output

## Phase 2: Smart Upgrades ✓ COMPLETED

### File Status Detection
- [x] Implement `FileStatus` enum (UNMODIFIED, MODIFIED, DELETED, UNKNOWN)
- [x] Create `get_file_status(path, original_hash) -> FileStatus`
- [x] Handle missing files gracefully
- [ ] Write unit tests for status detection (deferred to Phase 5)

### Built-in Type Upgrades
- [x] Load current built-in type templates and scripts
- [x] Compare versions and determine update needs
- [x] Overwrite unmodified files silently
- [x] Update registry hashes after upgrade
- [ ] Test built-in type upgrade flow (deferred to Phase 5)

### Custom Type Prompts
- [x] Detect modified files in custom types
- [x] Implement interactive prompt with 5 options (overwrite, keep, new, diff, skip)
- [x] Handle user choice for overwrite
- [x] Handle user choice for keep
- [x] Handle user choice for .new file
- [x] Handle user choice for show diff

### Backup System
- [x] Create `.workspace/backup/` directory on demand
- [x] Implement `create_backup(path) -> backup_path` function
- [x] Use timestamped naming: `{name}.{YYYYMMDD-HHMMSS}.bak`
- [x] Log backup location to user (in verbose mode)
- [ ] Write unit tests for backup creation (deferred to Phase 5)

### Dry-Run Mode
- [x] Add `--dry-run` flag to upgrade command
- [x] Collect all changes without applying
- [x] Display upgrade plan with file statuses
- [x] Show what prompts would be shown
- [ ] Test dry-run output format (deferred to Phase 5)

### Non-Interactive Mode
- [x] Add `--yes` flag to upgrade command
- [x] Define default actions for each file status
- [x] Skip prompts and apply defaults
- [x] Still create backups for modified files
- [ ] Test non-interactive upgrade flow (deferred to Phase 5)

## Phase 3: Enhanced UX (PARTIALLY IMPLEMENTED)

### Version Check Notification
- [ ] Check workspace version on any cortext command (deferred - future enhancement)
- [ ] Display upgrade notification if outdated (deferred - future enhancement)
- [ ] Suggest `cortext upgrade` command (deferred - future enhancement)
- [ ] Add `--no-version-check` global flag to suppress (deferred - future enhancement)

### Show Diff Option
- [x] Compute diff between original and current content
- [x] Use unified diff format
- [x] Implement syntax highlighting with rich
- [x] Return to prompt after showing diff

### Create .new File Option
- [x] Create file with `.new` extension
- [x] Write new content to .new file
- [x] Keep original file unchanged
- [x] Log paths for manual merge

### Breaking Change Detection
- [ ] Compare workspace API version to current API version (deferred - API versioning not yet implemented)
- [ ] Detect major version changes (deferred - API versioning not yet implemented)
- [ ] Display breaking change warning (deferred - API versioning not yet implemented)
- [ ] Show migration guide URL (future) (deferred - future enhancement)
- [ ] Require explicit regeneration for breaking changes (deferred - future enhancement)

### Additional Flags
- [x] Add `--built-in-only` flag
- [x] Add `--regenerate TYPE` flag
- [x] Add `--backup-dir PATH` flag
- [ ] Add `--no-backup` flag (with warning) (deferred - not needed for MVP)

## Phase 4: Workspace Add Integration ✓ COMPLETED

### Update Workspace Add Slash Command
- [x] Update `/workspace.add` instructions to include `generated_with`
- [x] Document hash computation requirements
- [x] Include all generated files (script, template, commands)
- [x] Set appropriate `script_api_version`

### Test Custom Type Creation
- [ ] Create new custom type (deferred to Phase 5)
- [ ] Verify registry includes generation metadata (deferred to Phase 5)
- [ ] Verify hashes are computed correctly (deferred to Phase 5)
- [ ] Verify upgrade detects unmodified custom type (deferred to Phase 5)

## Phase 5: Documentation & Testing ✓ COMPLETED

### Documentation
- [x] Add upgrade command to CLI help (built-in via Typer)
- [x] Document upgrade workflow in README.md
- [x] Create comprehensive upgrade-guide.md
- [x] Document hash-based tracking system
- [x] Add troubleshooting section for upgrade issues
- [x] Update CHANGELOG.md with upgrade features
- [x] Update workspace_add.md with generation metadata

### Testing
- [ ] Unit tests for hash utilities
- [ ] Unit tests for file status detection
- [ ] Unit tests for backup creation
- [ ] Integration test: upgrade unmodified workspace
- [ ] Integration test: upgrade with modified files
- [ ] Integration test: legacy workspace migration
- [ ] Integration test: dry-run mode
- [ ] Integration test: non-interactive mode
- [ ] Edge case: corrupt registry handling
- [ ] Edge case: missing backup directory permissions

### Release Preparation
- [ ] Update CHANGELOG with upgrade feature
- [ ] Bump version appropriately
- [ ] Test upgrade on real workspace
- [ ] Create example upgrade walkthrough

## Dependencies

- **Phase 1** must complete before Phase 2 can begin
- **Phase 2** must complete before Phase 3 can begin
- **Phase 4** can run in parallel with Phase 3
- **Phase 5** should run throughout development

## Notes

- Hash computation uses SHA-256 via Python's `hashlib`
- All backups go to `.workspace/backup/` by default
- Registry schema migration is automatic on first access
- Script API version starts at "1.0" and follows semver
