# Tasks: Fix Gemini Init Configuration

**Change ID:** `fix-gemini-init-configuration`

---

## Implementation Tasks

### Phase 1: Fix Bug

- [ ] **Update Gemini configuration to use source commands**
  - Change from `claude_dir` to `commands_dir` (source templates)
  - Remove dependency on Claude configuration
  - Remove `if claude_dir.exists()` check
  - Verify: Gemini converts directly from source

### Phase 2: Testing

- [ ] **Test `cortext init --ai=gemini`**
  - Verify `.gemini/commands/` folder created
  - Verify TOML files generated
  - Verify no `.claude/` folder created
  - Verify: Standalone Gemini configuration works

- [ ] **Test `cortext init --ai=all`**
  - Verify all AI tools configured
  - Verify no regressions
  - Verify: All tools work correctly

### Phase 3: Finalization

- [ ] **Update CHANGELOG**
  - Document bug fix
  - Note independent tool configuration
  - Verify: Fix documented

- [ ] **Commit changes**
  - Use conventional commit format
  - Reference the bug
  - Verify: Clean commit

---

## Validation Checklist

- [ ] `cortext init --ai=gemini` creates `.gemini/commands/`
- [ ] Gemini TOML files generated correctly
- [ ] No dependency on Claude configuration
- [ ] `--ai=all` still works
- [ ] Each AI tool independent

---

## Dependencies

- **None** - Simple bug fix

---

## Rollback Plan

If issues arise:
1. Revert single commit
2. Old (broken) behavior restored
3. No data loss
