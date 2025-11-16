# Proposal: Fix Init Path Handling

**Change ID:** `fix-init-path-handling`
**Status:** Proposed
**Created:** 2025-11-16

---

## Problem Statement

The `cortext init` command has incorrect path handling behavior:

1. **`cortext init .`** - Treats `.` as a workspace name appended to `~`, resulting in initialization in home directory instead of current directory
2. **`cortext init`** - Silently defaults to `~/ai-workspace` instead of asking the user where to install

**Current behavior (buggy):**
```bash
$ pwd
/home/user/myproject
$ cortext init .
# Initializes in /home/user (wrong!)

$ cortext init
# Silently uses ~/ai-workspace without asking
```

**Expected behavior:**
```bash
$ pwd
/home/user/myproject
$ cortext init .
# Initializes in /home/user/myproject (correct!)

$ cortext init
# Prompts: "Where would you like to create the workspace?"
```

---

## Solution Approach

### 1. Smart Path Detection
Treat the positional argument as a **path** (not a name) when it contains path characters:
- `.` (current directory)
- `..` (parent directory)
- `/` (absolute or relative path)
- `~` (home directory expansion)

### 2. Interactive Prompt for No Arguments
When no arguments are provided, prompt the user to choose:
- Current directory (`.`)
- Default location (`~/ai-workspace`)
- Custom path (user input)

### 3. Backward Compatibility
- `cortext init myworkspace` still creates `~/myworkspace`
- `cortext init --path /custom/path` still works as before
- Only behavior change: no-arg case now prompts

---

## Impact Analysis

### Files Changed
- `src/cortext_cli/commands/init.py` - Path resolution logic and prompting

### User Experience
- **Improved**: No more silent defaults, clearer path handling
- **More intuitive**: `.` means current directory as expected
- **Interactive**: Users explicitly choose workspace location

### Risk Assessment
- **Low risk**: Only affects initialization, not existing workspaces
- **No data loss**: Only changes where new workspaces are created
- **Easy rollback**: Simple logic change, no schema changes

---

## Design Decisions

### Decision 1: Path Detection Heuristic
**Choice**: Check for path-like characters (`.`, `/`, `~`)
**Rationale**: Simple, intuitive, covers common cases
**Alternative**: Use `--path` flag only - rejected as less user-friendly

### Decision 2: Interactive Default
**Choice**: Prompt user when no arguments given
**Rationale**: Explicit is better than implicit, prevents mistakes
**Alternative**: Keep silent default - rejected as confusing

### Decision 3: Prompt Options
**Choice**: Offer current dir, default location, and custom input
**Rationale**: Covers most use cases with minimal friction
**Alternative**: Always require explicit path - rejected as too verbose

---

## Acceptance Criteria

1. `cortext init .` initializes in current working directory
2. `cortext init ..` initializes in parent directory
3. `cortext init /absolute/path` initializes at that path
4. `cortext init ~/relative` initializes in home-relative path
5. `cortext init myname` still creates `~/myname` (backward compatible)
6. `cortext init` (no args) prompts user for location
7. `cortext init --path /foo` still works (backward compatible)

---

## Spec Deltas

- `specs/cli-init/spec.md` - Requirements for init command behavior
