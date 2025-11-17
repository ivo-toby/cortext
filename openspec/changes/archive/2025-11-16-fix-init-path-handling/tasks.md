# Tasks: Fix Init Path Handling

**Change ID:** `fix-init-path-handling`

---

## Implementation Tasks

### Phase 1: Core Logic Fix

- [x] **Add path detection helper function**
  - Create `is_path_like(value: str) -> bool` function
  - Check for: starts with `.`, `/`, `~`, or contains `/`
  - Return True if value looks like a path, False if simple name
  - Add unit test coverage
  - Verify: `.`, `..`, `/foo`, `~/bar`, `./baz` all return True
  - Verify: `myworkspace`, `ai-project` return False

- [x] **Update path resolution logic in init()**
  - Modify conditional to check `is_path_like()` before treating as name
  - When path-like: use `Path(value).expanduser().resolve()`
  - When not path-like: use `Path.home() / value` (backward compatible)
  - Verify: `cortext init .` uses current directory
  - Verify: `cortext init myname` still uses `~/myname`

### Phase 2: Interactive Prompting

- [x] **Add interactive location prompt**
  - Import `Prompt` from `rich.prompt`
  - Create `prompt_for_location() -> Path` function
  - Show current working directory in prompt
  - Offer choices: "Current directory", "Default (~/ai-workspace)", "Custom path"
  - Handle user selection and return resolved Path
  - Verify: Prompt appears when no arguments given

- [x] **Integrate prompt into init() flow**
  - Check if no path and no workspace_name provided
  - Call `prompt_for_location()` to get user's choice
  - Use returned path as workspace_dir
  - Verify: `cortext init` now prompts user
  - Verify: Each option (current, default, custom) works correctly

### Phase 3: Edge Cases & Validation

- [x] **Handle edge cases**
  - Empty custom path input (re-prompt or use default)
  - Invalid path characters (show error, re-prompt)
  - Path with spaces (should work with proper quoting)
  - Relative paths like `./subdir` or `../sibling`
  - Verify: All edge cases handled gracefully

- [x] **Add input validation**
  - Validate custom path is writable (or parent exists)
  - Check path doesn't contain obviously invalid characters
  - Provide clear error messages
  - Verify: Bad input gives helpful feedback

### Phase 4: Testing & Documentation

- [x] **Manual testing of all scenarios**
  - Test `cortext init .` (current directory)
  - Test `cortext init ..` (parent directory)
  - Test `cortext init /absolute/path`
  - Test `cortext init ~/home-relative`
  - Test `cortext init myname` (backward compat)
  - Test `cortext init` (prompts)
  - Test `cortext init --path /foo` (still works)
  - Test `cortext init name --path /foo` (path takes precedence)
  - Verify: All acceptance criteria pass

- [x] **Update help text and docstrings**
  - Update typer argument help text to clarify path vs name
  - Update function docstring to document new behavior
  - Add examples in help text
  - Verify: `cortext init --help` is clear

- [x] **Update user documentation**
  - Update README with new init behavior
  - Update user guide with examples
  - Document the interactive prompt
  - Verify: Documentation matches implementation

### Phase 5: Finalization

- [x] **Update CHANGELOG.md**
  - Document the bug fix
  - Explain new interactive behavior
  - Note backward compatibility maintained
  - Verify: Changes clearly documented

- [x] **Mark all tasks complete**
  - Review all items verified
  - Ensure documentation updated
  - Confirm tests pass

- [x] **Commit changes**
  - Use conventional commit format: `fix: correct init path handling`
  - Include comprehensive description
  - Reference the bug behavior

---

## Validation Checklist

Before marking complete:

- [x] `cortext init .` initializes in current directory
- [x] `cortext init ..` initializes in parent directory
- [x] `cortext init /path` uses absolute path
- [x] `cortext init ~/path` expands home directory
- [x] `cortext init name` still creates `~/name` (backward compat)
- [x] `cortext init` prompts user for location
- [x] Interactive prompt offers current dir, default, and custom options
- [x] `--path` option still works and takes precedence
- [x] Help text is clear and accurate
- [x] Documentation updated

---

## Dependencies

- **None** - Self-contained fix to init command

## Parallel Work

- Phase 1 tasks can be done sequentially (logic depends on helper)
- Phase 2 tasks can be done after Phase 1
- Phase 4 testing should be done after Phases 1-3 complete

---

## Rollback Plan

If issues arise:
1. Revert single commit
2. Old behavior restored immediately
3. No existing workspaces affected
4. Only impacts new workspace creation
