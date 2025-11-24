# Workspace Upgrade Guide

## Overview

Cortext provides a safe, incremental upgrade system that preserves your customizations while updating built-in files to newer versions.

## Quick Start

### Check for Upgrades

```bash
cortext upgrade
```

This will:
- Check your workspace version
- Display available upgrade
- Show what will change

### Upgrade Non-Interactively

```bash
cortext upgrade --yes
```

Accepts default actions for all files (safe defaults with backups).

### Preview Changes

```bash
cortext upgrade --dry-run
```

Shows what would change without making any modifications.

## How It Works

### Version Tracking

New workspaces (v0.3.0+) include version tracking metadata:

```json
{
  "schema_version": "2.0",
  "workspace_meta": {
    "cortext_version": "0.3.2",
    "initialized": "2025-11-24T10:00:00Z",
    "last_upgraded": null
  }
}
```

### File Hash Tracking

Each conversation type tracks SHA-256 hashes of generated files:

```json
{
  "brainstorm": {
    "generated_with": {
      "cortext_version": "0.3.2",
      "script_api_version": "1.0",
      "files": {
        "script": {
          "path": ".workspace/scripts/bash/brainstorm.sh",
          "original_hash": "sha256:abc123..."
        }
      }
    }
  }
}
```

### File Status Detection

During upgrade, each file is classified:

| Status | Meaning | Action |
|--------|---------|--------|
| **UNMODIFIED** | Hash matches original | Upgrade silently |
| **MODIFIED** | Hash differs from original | Prompt for action |
| **DELETED** | File doesn't exist | Skip with warning |
| **UNKNOWN** | No hash stored (legacy) | Treat as modified |

## Upgrade Scenarios

### Scenario 1: Unmodified Workspace

```bash
$ cortext upgrade

🔄 Cortext Workspace Upgrade
From: 0.2.0 → To: 0.3.2

Analyzing workspace...

✓ brainstorm - unmodified, upgrading
✓ debug - unmodified, upgrading
✓ plan - unmodified, upgrading
...

Upgrade Summary
  Upgraded: 7
  Skipped: 0

✓ Workspace upgraded to 0.3.2
```

### Scenario 2: Modified Custom Type

```bash
$ cortext upgrade

⚠ retro: has modifications
  - .workspace/scripts/bash/retro.sh (modified)

How should retro be handled? [overwrite/keep/new/diff/skip] (skip):
```

**Your options:**

1. **overwrite** - Backup current file and install new version
   ```
   Backed up retro.sh to .workspace/backup/retro.sh.20251124-153000.bak
   Updated retro.sh
   ```

2. **keep** - Leave your version unchanged
   ```
   Keeping current retro files
   ```

3. **new** - Create `.new` files for manual merge
   ```
   Created .workspace/scripts/bash/retro.sh.new
   Created .workspace/templates/retro.md.new
   ```
   Then manually:
   ```bash
   diff retro.sh retro.sh.new
   # Merge changes as needed
   ```

4. **diff** - View what changed
   ```
   Shows unified diff between original and current
   (Note: Shows hash difference, not full diff)
   ```

5. **skip** - Don't upgrade this type
   ```
   Skipping retro
   ```

### Scenario 3: Legacy Workspace

```bash
$ cortext upgrade

⚠ Legacy workspace detected

This workspace was created before Cortext 0.3.0 and doesn't have
version tracking metadata.

How should existing files be treated? [modified/unmodified/cancel] (modified):
```

**modified** (recommended):
- Treats all files as potentially customized
- Prompts for each conversation type
- Safest option

**unmodified**:
- Treats all files as pristine
- Upgrades everything without prompts
- Use only if workspace is unmodified

## Advanced Usage

### Force Regenerate Specific Type

```bash
cortext upgrade --regenerate my-custom-type
```

Useful when:
- File is corrupted
- You want to reset to template defaults
- Breaking changes require regeneration

### Upgrade Only Built-in Types

```bash
cortext upgrade --built-in-only
```

Upgrades only:
- brainstorm, debug, plan, learn, meeting, review, projectmanage

Skips:
- All custom types you've created

### Custom Backup Directory

```bash
cortext upgrade --backup-dir /path/to/backups
```

Default is `.workspace/backup/` - change if you want backups elsewhere.

### Verbose Output

```bash
cortext upgrade --verbose
```

Shows detailed progress:
- Which files are being updated
- Backup locations
- Hash computations

## Backup Management

### Backup Format

Backups are timestamped:
```
.workspace/backup/
├── brainstorm.sh.20251124-153000.bak
├── brainstorm.sh.20251124-160000.bak
└── retro.sh.20251124-153000.bak
```

### Restoring from Backup

```bash
# Find your backup
ls -la .workspace/backup/

# Restore it
cp .workspace/backup/retro.sh.20251124-153000.bak \
   .workspace/scripts/bash/retro.sh
```

### Cleanup Old Backups

Backups are never automatically deleted. Clean up manually:

```bash
# Remove backups older than 30 days
find .workspace/backup -name "*.bak" -mtime +30 -delete
```

## Best Practices

### Before Upgrading

1. **Commit your work**
   ```bash
   git add -A
   git commit -m "Checkpoint before upgrade"
   ```

2. **Check status**
   ```bash
   git status  # Should be clean
   ```

3. **Preview first**
   ```bash
   cortext upgrade --dry-run
   ```

### During Interactive Upgrade

1. **Review modifications carefully** - If you customized a file, decide if you want to:
   - Keep your changes (keep/skip)
   - Get new features (overwrite)
   - Manually merge (new)

2. **Use diff for uncertainty** - If unsure what changed, use "diff" option

3. **Check backups** - After overwrite, verify backup was created

### After Upgrading

1. **Test functionality**
   ```bash
   # Try creating a conversation
   /workspace.brainstorm test-upgrade
   ```

2. **Review changes**
   ```bash
   git diff
   ```

3. **Commit upgrade**
   ```bash
   git add .workspace/
   git commit -m "chore: upgrade workspace to 0.3.2"
   ```

## Troubleshooting

### "Not a Cortext workspace"

```bash
$ cortext upgrade
✗ Not a Cortext workspace
```

**Solution**: Run from workspace root where `.workspace/` exists, or use:
```bash
cortext upgrade --path /path/to/workspace
```

### "Corrupted registry file"

```bash
$ cortext upgrade
✗ Corrupted registry file
Try restoring from git history
```

**Solution**: Restore registry from git:
```bash
git checkout HEAD -- .workspace/registry.json
```

### Upgrade Fails Mid-Process

If upgrade is interrupted:
1. Check git status
2. Restore from backups if needed
3. Re-run upgrade - it's idempotent

### Can't Find Backup

If backup directory is missing:
```bash
mkdir -p .workspace/backup
```

Then re-run upgrade.

## Version History

### Registry Schema Versions

- **v1.0** - Original schema (pre-0.3.0)
  - Basic conversation type tracking
  - No version metadata

- **v2.0** - Current schema (0.3.0+)
  - Workspace version tracking
  - File hash tracking
  - Generation metadata

### Upgrade Compatibility

| Workspace Version | Installed Cortext | Upgrade Path |
|-------------------|-------------------|--------------|
| Legacy (< 0.3.0) | 0.3.0+ | Migrate to v2.0 schema |
| 0.3.0 | 0.3.2 | Standard upgrade |
| 0.3.2 | 0.3.2 | No upgrade needed |
| 0.4.0 | 0.3.2 | Workspace newer - upgrade Cortext |

## Custom Types

### When Creating Custom Types

When you use `/workspace.add`, the new slash command now includes hash tracking:

```json
"my-custom-type": {
  "generated_with": {
    "cortext_version": "0.3.2",
    "script_api_version": "1.0",
    "files": { /* hashes */ }
  }
}
```

This means your custom types will be tracked for future upgrades too!

### Regenerating Custom Types

If you want to reset a custom type to defaults:

```bash
cortext upgrade --regenerate my-custom-type
```

This will:
1. Backup all current files
2. Regenerate from current templates
3. Update hashes to new baseline

## FAQ

**Q: Will upgrade overwrite my customizations?**
A: No - it detects modifications and prompts you for each file.

**Q: What if I modified a built-in type?**
A: Same as custom types - you'll be prompted with options.

**Q: Can I see what changed before deciding?**
A: Yes - use `--dry-run` or select "diff" during interactive upgrade.

**Q: Are backups automatic?**
A: Yes - any overwrite creates a timestamped backup.

**Q: Can I undo an upgrade?**
A: Yes - restore from backups or `git checkout` before upgrade commit.

**Q: What happens to my conversations?**
A: Nothing - only template/script files are updated. Your conversation content is untouched.

**Q: Do I need to upgrade?**
A: Not immediately, but upgrades may include bug fixes and new features.

**Q: How often should I upgrade?**
A: Check release notes (CHANGELOG.md) - upgrade when features/fixes are relevant.

## See Also

- [CHANGELOG.md](../CHANGELOG.md) - What's new in each version
- [User Guide](user-guide.md) - General workspace usage
- [Session Guide](session-guide.md) - Session management
