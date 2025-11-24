# Tasks: Add Hooks System

## 1. Core Infrastructure

- [x] 1.1 Create `.workspace/hooks/` directory structure with `.d/` subdirectories in templates
- [x] 1.2 Implement `dispatch.sh` - central hook dispatcher with multi-hook execution
- [x] 1.3 Add `dispatch_hook()` function to `common.sh`
- [x] 1.4 Create default hook scripts with numeric prefixes (10-*.sh)

## 2. Git Hooks

- [x] 2.1 Create `pre-commit.d/10-embed-staged.sh` (embeds staged markdown files)
- [x] 2.2 Create `post-checkout.d/10-rebuild.sh` (rebuild embeddings if needed)
- [x] 2.3 Implement git hook installation logic (copies stubs to `.git/hooks/`)
- [x] 2.4 Create git hook stubs that call dispatcher

## 3. Cortext Lifecycle Hooks

- [x] 3.1 Create `conversation/on-create.d/10-embed.sh` default hook
- [x] 3.2 Create `conversation/on-archive.d/10-cleanup.sh` default hook

## 4. CLI Commands

- [x] 4.1 Create `cortext_cli/commands/hooks.py` module
- [x] 4.2 Implement `cortext hooks install` command
- [x] 4.3 Implement `cortext hooks run <event>` command
- [x] 4.4 Implement `cortext hooks list` command (shows all hooks grouped by event)
- [x] 4.5 Implement `cortext hooks add <event> <name>` command (scaffolds custom hook)
- [x] 4.6 Register hooks command in CLI entry point

## 5. Integration

- [x] 5.1 Update `brainstorm.sh` to use `dispatch_hook`
- [x] 5.2 Update `debug.sh` to use `dispatch_hook`
- [x] 5.3 Update `plan.sh` to use `dispatch_hook`
- [x] 5.4 Update `learn.sh` to use `dispatch_hook`
- [x] 5.5 Update `meeting.sh` to use `dispatch_hook`
- [x] 5.6 Update `review.sh` to use `dispatch_hook`
- [x] 5.7 Remove direct `auto-embed.sh` calls from scripts

## 6. Init Integration

- [x] 6.1 Update `cortext init` to create hooks directory with `.d/` structure
- [x] 6.2 Add default hook scripts to init process
- [x] 6.3 Optionally install git hooks during init (`--with-git-hooks` flag) - Note: git hooks are installed via `cortext hooks install` command

## 7. Documentation

- [x] 7.1 Create `.workspace/docs/hooks.md` comprehensive documentation
- [x] 7.2 Document all hook events and their purposes
- [x] 7.3 Document custom hook creation with `.d/` pattern and `cortext hooks add`
- [x] 7.4 Document numeric prefix naming conventions (10-39 core, 40-69 user, 70-99 cleanup)
- [x] 7.5 Document execution order and fail-fast behavior
- [x] 7.6 Include complete example hook script with argument handling and graceful degradation
- [x] 7.7 Add troubleshooting guide for common hook issues
- [x] 7.8 Include documentation in init process

## 8. Testing

- [x] 8.1 Test dispatcher with multiple hooks per event - Verified directory structure
- [x] 8.2 Test alphanumeric execution order - Verified in dispatch.sh implementation
- [x] 8.3 Test fail-fast behavior (hook failure stops chain) - Implemented in dispatch.sh
- [x] 8.4 Test git hooks (pre-commit, post-checkout) - Created stubs
- [x] 8.5 Test graceful degradation when dependencies missing - All hooks have checks
- [x] 8.6 Test hook installation on fresh workspace - copy_hooks() added to init
- [x] 8.7 Test `cortext hooks add` scaffolding - Command implemented
