# Proposal: Fix Gemini Init Configuration

**Change ID:** `fix-gemini-init-configuration`
**Status:** Proposed
**Created:** 2025-11-17

---

## Why

`cortext init --ai=gemini` fails to create `.gemini/` folder because the Gemini configuration code depends on Claude commands existing first, but Claude is never configured when only Gemini is requested.

**Current (buggy) code:**
```python
elif tool == "gemini":
    gemini_dir = workspace_dir / ".gemini" / "commands"
    claude_dir = workspace_dir / ".claude" / "commands"  # Depends on Claude!
    if claude_dir.exists():  # False when --ai=gemini
        converted = convert_claude_commands_to_gemini(claude_dir, gemini_dir)
```

**Result**: No `.gemini/` folder created, no Gemini commands configured.

---

## What Changes

Convert from source command templates directly instead of depending on Claude configuration.

**After:**
```python
elif tool == "gemini":
    gemini_dir = workspace_dir / ".gemini" / "commands"
    converted = convert_claude_commands_to_gemini(commands_dir, gemini_dir)  # Use source
    if converted:
        configured_tools.append(f"Gemini CLI ({len(converted)} commands)")
```

---

## Impact Analysis

### Files Changed
- `src/cortext_cli/commands/init.py` - Fix Gemini configuration to use source commands

### User Experience
- `cortext init --ai=gemini` now works correctly
- `.gemini/commands/` folder created with TOML files
- All standalone AI tool configurations now independent

### Risk Assessment
- **Very low risk**: Simple bug fix
- **No breaking changes**: Fixes broken functionality
- **Backward compatible**: `--ai=all` still works

---

## Acceptance Criteria

1. `cortext init --ai=gemini` creates `.gemini/commands/` folder
2. Gemini TOML files are generated correctly
3. Each AI tool can be configured independently
4. `--ai=all` still works (configures all tools)

---

## Spec Deltas

- `specs/cli-init/spec.md` - Modify requirement for AI tool independence
