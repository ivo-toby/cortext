# Design: Upgrade Workspace Strategy

## Overview

This document captures architectural decisions for implementing workspace upgrades in Cortext. The design enables safe, incremental upgrades of workspace files while preserving user customizations.

## Architecture

### Core Components

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Version Checker   │────▶│  Upgrade Engine  │────▶│  File Handler   │
│ (detect workspace   │     │ (orchestrate     │     │ (backup, write, │
│  version status)    │     │  upgrade flow)   │     │  diff, merge)   │
└─────────────────────┘     └──────────────────┘     └─────────────────┘
         │                           │                        │
         │                           ▼                        │
         │                  ┌──────────────────┐               │
         └─────────────────▶│    Registry      │◀──────────────┘
                            │ (schema + state) │
                            └──────────────────┘
```

### Data Flow

1. **Invocation**: User runs `cortext upgrade`
2. **Detection**: Load registry, compare workspace version to installed version
3. **Analysis**: For each conversation type, compute file statuses
4. **Presentation**: Display upgrade plan to user
5. **Execution**: Process each file based on status and user choice
6. **Finalization**: Update registry metadata, commit changes

## Key Design Decisions

### Decision 1: SHA-256 for File Hashing

**Choice**: Use SHA-256 hashes to track original file content.

**Rationale**:
- Deterministic and reproducible
- Fast enough for small template/script files (<1KB typically)
- Collision-resistant for integrity checking
- Standard library support (`hashlib`)

**Alternatives Considered**:
- Git blob hashes: Adds git dependency, more complex
- MD5: Weaker, no significant speed benefit for small files
- File modification time: Unreliable across systems

### Decision 2: Registry as Single Source of Truth

**Choice**: Store all upgrade metadata in `.workspace/registry.json`.

**Rationale**:
- Already serves as workspace configuration
- Single file to read/write
- Atomic updates via JSON
- Easy to inspect and debug

**Schema Extension**:
```json
{
  "schema_version": "2.0",
  "workspace_meta": {
    "cortext_version": "0.3.0",
    "initialized": "2025-11-20T10:00:00Z",
    "last_upgraded": "2025-11-24T15:30:00Z"
  },
  "conversation_types": {
    "my-type": {
      "generated_with": {
        "cortext_version": "0.3.0",
        "script_api_version": "1.0",
        "files": {
          "script": {
            "path": ".workspace/scripts/bash/my-type.sh",
            "original_hash": "sha256:..."
          }
        }
      }
    }
  }
}
```

### Decision 3: Four File Statuses

**Choice**: Categorize files into four upgrade statuses.

| Status | Condition | Default Action |
|--------|-----------|----------------|
| `UNMODIFIED` | Current hash = original hash | Overwrite silently |
| `MODIFIED` | Current hash ≠ original hash | Prompt user |
| `DELETED` | File doesn't exist | Skip (warn) |
| `UNKNOWN` | No original hash (legacy) | Treat as modified |

**Rationale**:
- Clear semantics for each case
- Safe defaults (unknown = modified)
- Minimal user interruption for unchanged files

### Decision 4: Backup Before Overwrite

**Choice**: Always create timestamped backup before overwriting modified files.

**Implementation**:
```
.workspace/backup/
  my-type.sh.20251124-153000.bak
  my-type.sh.20251125-091500.bak
```

**Rationale**:
- Zero-risk overwrite policy
- Users can recover any version
- Timestamp provides clear history
- `.workspace/` keeps it organized with other workspace files

### Decision 5: Interactive Prompts for Modified Files

**Choice**: When a file is modified, prompt user with options:
1. Overwrite (with backup)
2. Keep current version
3. Create .new file for manual merge
4. Show diff

**Rationale**:
- User maintains control over customizations
- Multiple escape hatches for different preferences
- Diff helps user understand changes
- .new file enables careful manual merge

### Decision 6: Built-in Types Are Tracked Too

**Choice**: Track hashes for built-in types, not just custom types.

**Rationale**:
- Users may customize built-in types
- Consistent behavior across all types
- Same upgrade flow for everything
- More flexible than hardcoded "always overwrite"

**Exception**: `--force-built-ins` flag to bypass prompts for built-in types.

### Decision 7: Dry-Run Mode

**Choice**: Provide `--dry-run` flag that shows upgrade plan without applying changes.

**Output Example**:
```
$ cortext upgrade --dry-run

Dry Run - No changes will be made

Would upgrade from 0.2.0 → 0.3.0

Built-in types (7):
  brainstorm - would update
  debug - would update
  ...

Custom types (2):
  standup - unmodified, would update
  retro - MODIFIED, would prompt
    - retro.sh (modified)
    - retro.md (unmodified)
```

**Rationale**:
- Safe preview before commitment
- Helps users understand scope
- Useful for CI/automation

### Decision 8: Script API Versioning

**Choice**: Track script API version separately from Cortext version.

```json
"script_api_version": "1.0"
```

**Semantic Versioning**:
- Patch (1.0.1): Bug fixes, no action needed
- Minor (1.1.0): New features, backward compatible
- Major (2.0.0): Breaking changes, regeneration required

**Rationale**:
- Scripts may stay stable across Cortext versions
- Breaking changes need explicit handling
- Users can skip non-breaking upgrades

### Decision 9: Legacy Workspace Detection

**Choice**: Workspaces without `workspace_meta` are detected as "legacy".

**Flow**:
```
$ cortext upgrade

⚠ Legacy workspace detected

Options:
1. Initialize tracking (treat files as potentially modified)
2. Initialize tracking (treat files as unmodified)
3. Cancel

Choice [1]:
```

**Rationale**:
- Graceful migration from pre-versioning workspaces
- User chooses safety vs convenience
- One-time setup, then normal upgrades apply

### Decision 10: Command-Line Interface

**Choice**: Single `cortext upgrade` command with focused flags.

```
cortext upgrade [OPTIONS]

Options:
  --yes, -y              Accept defaults non-interactively
  --dry-run              Preview changes only
  --built-in-only        Skip custom types
  --regenerate TYPE      Force regenerate specific type
  --backup-dir PATH      Custom backup location
  --verbose, -v          Show detailed progress
```

**Rationale**:
- Simple primary use case (just run `cortext upgrade`)
- Flags for advanced scenarios
- Consistent with existing CLI patterns

## Future Considerations

### Separation of Concerns (Phase 4)

Scripts could be structured with managed and user sections:

```bash
# ╔═══════════════════════════════════════════╗
# ║ CORTEXT MANAGED SECTION - DO NOT EDIT     ║
# ╚═══════════════════════════════════════════╝

# [Managed code here - overwritten on upgrade]

# ╔═══════════════════════════════════════════╗
# ║ USER CUSTOMIZATION SECTION                ║
# ╚═══════════════════════════════════════════╝

pre_commit_hook() {
    # User code here - preserved on upgrade
}
```

**Benefits**:
- Clear boundaries for users
- Automatic preservation of customizations
- No prompts needed for most upgrades

**Deferred because**:
- Adds complexity to script templates
- Requires migration of existing custom types
- Current hash-based approach handles immediate need

### Downgrade Support

Not supported in Phase 1-3.

**Rationale**:
- Complex to maintain old versions of files
- Users can restore from git history
- Upgrade path is forward-only like most tools

### Partial Upgrade State

If user cancels mid-upgrade or skips files:
- Registry records what was upgraded
- Next `cortext upgrade` detects remaining work
- Per-file tracking enables resume

## Integration Points

### With Init Command

`cortext init` creates `workspace_meta`:
```python
"workspace_meta": {
    "cortext_version": get_version(),
    "initialized": datetime.utcnow().isoformat() + "Z",
    "last_upgraded": None
}
```

### With Add Type Workflow

`/workspace.add` slash command records generation metadata:
```python
"generated_with": {
    "cortext_version": get_version(),
    "script_api_version": "1.0",
    "files": {
        "script": {
            "path": script_path,
            "original_hash": compute_hash(script_content)
        },
        # ... template, commands
    }
}
```

### With Version Command

`cortext --version` could show workspace version status:
```
Cortext 0.3.2
Workspace: 0.2.0 (upgrade available)
```

## Error Handling

| Scenario | Handling |
|----------|----------|
| Registry not found | "Not a Cortext workspace" error |
| Registry parse error | "Corrupted registry" error with recovery hint |
| Backup dir not writable | Fail with clear message before any changes |
| Hash computation fails | Treat file as UNKNOWN (modified) |
| Git not available | Warn but continue (skip git operations) |

## Testing Strategy

1. **Unit tests**: Hash computation, status detection, file operations
2. **Integration tests**: Full upgrade scenarios with mock workspaces
3. **Edge cases**: Legacy workspaces, missing files, corrupt registry
4. **User journey tests**: Interactive prompts, dry-run, various flags
