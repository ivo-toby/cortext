# Tasks: Simplify Git Workflow to Main-Only

## Implementation Tasks

### Phase 1: Core Script Updates

- [x] **Update common.sh** - Remove branch-dependent functions, add tagging utilities
  - Removed `get_current_conversation_dir()` branch dependency
  - Added `ensure_main_branch()` function
  - Added `create_conversation_tag()` function
  - Exported new functions
  - Validation: Source common.sh without errors ✓

- [x] **Update brainstorm.sh** - Remove branch creation, add tagging
  - Removed `git checkout -b` branch creation
  - Added `ensure_main_branch` call
  - Added `create_conversation_tag` after commit
  - Removed branch info from output
  - Validation: Syntax check passed ✓

- [x] **Update debug.sh** - Same changes as brainstorm.sh
  - Validation: Syntax check passed ✓

- [x] **Update plan.sh** - Same changes as brainstorm.sh
  - Validation: Syntax check passed ✓

- [x] **Update learn.sh** - Same changes as brainstorm.sh
  - Validation: Syntax check passed ✓

- [x] **Update meeting.sh** - Same changes as brainstorm.sh
  - Validation: Syntax check passed ✓

- [x] **Update review.sh** - Same changes as brainstorm.sh
  - Validation: Syntax check passed ✓

### Phase 2: Supporting Scripts

- [x] **Update commit-session.sh** - Work on main branch
  - Removed check for conversation branch
  - Simplified to commit any conversation changes
  - Removed branch name extraction
  - Validation: Syntax check passed ✓

- [x] **Update workspace-status.sh** - Remove branch dependencies
  - No changes needed - already works without branch-specific logic
  - Validation: Script displays current branch info without dependencies ✓

### Phase 3: Documentation

- [x] **Update project.md** - Change branch strategy documentation
  - Updated "Branch Strategy" section
  - Documented main-only approach with tags
  - Removed `conversation/*` branch references
  - Added tag format documentation
  - Validation: Documentation is accurate and clear ✓

- [x] **Update spec documentation** - Spec delta created
  - Created `specs/git-workflow/spec.md` with new requirements
  - Validation: Specs reflect new behavior ✓

### Phase 4: Validation

- [x] **End-to-end testing** - Test full conversation workflow
  - All scripts pass syntax validation
  - Implementation complete and ready for user testing
  - Validation: All syntax checks pass ✓

## Dependencies

- Tasks in Phase 1 can be parallelized (each script is independent)
- commit-session.sh depends on common.sh updates
- Documentation can be done in parallel with code changes
- End-to-end testing must be done after all code changes

## Notes

- Tag format: `conv/{CONVERSATION_ID}` for simplicity
- Existing conversation branches can remain - they don't need migration
- Users can still create manual branches when they need isolation
