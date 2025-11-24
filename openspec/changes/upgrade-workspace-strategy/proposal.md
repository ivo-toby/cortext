# Proposal: Upgrade Workspace Strategy

**Change ID**: `upgrade-workspace-strategy`
**Status**: Draft
**Created**: 2025-11-24

## Problem Statement

When Cortext is updated, existing workspaces lack a mechanism to:
1. Detect version differences between installed Cortext and workspace
2. Update built-in scripts, templates, and slash commands
3. Handle custom conversation types that users may have modified

The core challenge is **custom conversation types** - they are generated from templates but users may customize them after creation. Blindly overwriting loses customizations; never updating leaves them with outdated scripts that may break.

Currently, users must manually update their workspaces or reinitialize, losing their registry metadata and customizations.

## Proposed Solution

Implement a hash-based tracking system with smart prompts that:
- Records the original state of generated files using SHA-256 hashes
- Detects when files have been modified by users
- Safely upgrades unmodified files while prompting for modified ones
- Provides backup, diff, and manual merge options

## What Changes

### New Capabilities
- **workspace-upgrade**: New `cortext upgrade` command for upgrading workspaces

### Modified Capabilities
- **workspace-init**: Add `workspace_meta` with version tracking to registry
- **conversation-types**: Add `generated_with` metadata to track file origins
- **cli-versioning**: Add workspace version checking logic

## Impact Analysis

### Affected Components
1. **Registry schema** - Extended with version tracking and file hashes
2. **Init command** - Creates version metadata on new workspaces
3. **Add type workflow** - Records generation metadata for custom types
4. **New upgrade command** - Core upgrade logic

### Migration Path
- Existing workspaces detected as "legacy" (no version tracking)
- User prompted to initialize tracking during first upgrade
- Option to treat existing files as modified (safe) or unmodified (fast)

### Risk Mitigation
- All overwrites create timestamped backups in `.workspace/backup/`
- Dry-run mode previews changes without applying
- Users always prompted before overwriting modified files
- Manual escape hatches available (show diff, create .new file)

## Success Criteria

1. **Zero data loss** - Backups always created before overwrite
2. **Unmodified files upgrade seamlessly** - No prompts for unchanged files
3. **Modified files handled safely** - User always chooses action
4. **Clear communication** - User understands what's happening
5. **Escape hatches** - Manual options always available

## Open Questions

1. Should we track hashes for built-in types too, or always overwrite them?
   - *Recommendation*: Track hashes - allows users to customize built-ins too
2. How to handle partial upgrades (user skips some files)?
   - *Recommendation*: Track per-file upgrade status, allow re-running
3. Should `cortext init` in existing workspace trigger upgrade?
   - *Recommendation*: No, provide clear warning and point to `cortext upgrade`
4. How to version the registry schema itself?
   - *Recommendation*: Add `schema_version` field, migrate on upgrade

## Implementation Phases

### Phase 1: Foundation (MVP)
- Registry schema extension with version metadata
- Hash computation utilities
- Basic `cortext upgrade` command skeleton
- Built-in type upgrades (always overwrite)

### Phase 2: Smart Upgrades
- File modification detection (hash comparison)
- Custom type prompts for modified files
- Backup system
- Dry-run mode

### Phase 3: Enhanced UX
- Version check notification on startup
- Show diff option
- Create .new file option
- Breaking change detection

### Phase 4: Future Enhancement
- Separation of concerns (managed/custom sections in scripts)
- Section-aware parsing for upgrades
- Migration tools for existing custom types

## Related Specifications

- `workspace-init` - Will be modified for version tracking
- `conversation-types` - Will track generation metadata
- `cli-versioning` - Will add workspace version checking
- `template-system` - Informs how templates are generated
