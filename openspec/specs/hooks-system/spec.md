# hooks-system Specification

## Purpose
TBD - created by archiving change add-hooks-system. Update Purpose after archive.
## Requirements
### Requirement: Hook Dispatcher

The system SHALL provide a central dispatcher that routes events to appropriate hook scripts.

The dispatcher SHALL be located at `.workspace/hooks/dispatch.sh`.

The dispatcher SHALL accept an event name as the first argument and pass remaining arguments to all hook scripts.

The dispatcher SHALL map event names to hook directories using the pattern `{category}/on-{action}.d/`.

The dispatcher SHALL execute all executable `.sh` scripts in the hook directory in alphanumeric order.

The dispatcher SHALL stop execution and return the exit code if any script fails (non-zero exit).

The dispatcher SHALL exit silently (code 0) if the hook directory does not exist or contains no scripts.

#### Scenario: Successful multi-hook dispatch

- **WHEN** `dispatch.sh` is called with `conversation:create /path/to/conv`
- **AND** `.workspace/hooks/conversation/on-create.d/` contains `10-embed.sh` and `20-index.sh`
- **THEN** it executes `10-embed.sh /path/to/conv` first
- **AND** then executes `20-index.sh /path/to/conv`
- **AND** exits with code 0 if all scripts succeed

#### Scenario: Missing hook directory

- **WHEN** `dispatch.sh` is called with `conversation:create /path/to/conv`
- **AND** `.workspace/hooks/conversation/on-create.d/` does not exist
- **THEN** it exits with code 0
- **AND** produces no output

#### Scenario: Hook script failure stops chain

- **WHEN** `dispatch.sh` is called with an event
- **AND** the second script in the directory exits with non-zero code
- **THEN** the dispatcher stops execution
- **AND** returns that non-zero exit code
- **AND** subsequent scripts do not run

#### Scenario: Alphanumeric execution order

- **WHEN** a hook directory contains `20-second.sh`, `10-first.sh`, `30-third.sh`
- **THEN** scripts execute in order: `10-first.sh`, `20-second.sh`, `30-third.sh`

### Requirement: Hook Directory Structure

The system SHALL organize hooks in a directory structure under `.workspace/hooks/`.

The structure SHALL include the following directories:
- `conversation/` for conversation lifecycle events
- `git/` for git hook scripts (templates)

Each event SHALL have a `.d/` directory containing executable bash scripts with numeric prefixes.

Scripts SHALL use numeric prefixes to control execution order (e.g., `10-embed.sh`, `20-index.sh`).

The recommended prefix ranges are:
- `10-39`: Core/default hooks
- `40-69`: User custom hooks
- `70-99`: Cleanup/finalization hooks

#### Scenario: Default directory structure

- **WHEN** a workspace is initialized with hooks enabled
- **THEN** the following structure is created:
  ```
  .workspace/hooks/
  ├── dispatch.sh
  ├── conversation/
  │   ├── on-create.d/
  │   │   └── 10-embed.sh
  │   └── on-archive.d/
  │       └── 10-cleanup.sh
  └── git/
      ├── pre-commit.d/
      │   └── 10-embed-staged.sh
      └── post-checkout.d/
          └── 10-rebuild.sh
  ```

#### Scenario: User adds custom hook

- **WHEN** user creates `.workspace/hooks/conversation/on-create.d/50-notify.sh`
- **AND** makes it executable
- **THEN** it runs after `10-embed.sh` on every `conversation:create` event
- **AND** receives the same arguments as other hooks

### Requirement: Common Hook Integration

The system SHALL provide a `dispatch_hook` function in `common.sh` that calls the dispatcher.

The function SHALL accept an event name and optional arguments.

The function SHALL silently succeed if the hooks directory or dispatcher does not exist.

#### Scenario: Calling dispatch_hook from script

- **WHEN** a conversation script calls `dispatch_hook "conversation:create" "$dir"`
- **THEN** it invokes `.workspace/hooks/dispatch.sh conversation:create "$dir"`

#### Scenario: Missing hooks directory

- **WHEN** `dispatch_hook` is called
- **AND** `.workspace/hooks/dispatch.sh` does not exist
- **THEN** the function returns 0 without error

### Requirement: Conversation Lifecycle Hooks

The system SHALL invoke hooks at key points in the conversation lifecycle.

The `conversation:create` event SHALL be dispatched after a conversation directory is created and committed.

The `conversation:archive` event SHALL be dispatched when a conversation is archived.

Hook scripts SHALL receive the conversation directory path as the first argument.

#### Scenario: Conversation creation triggers hook

- **WHEN** a conversation is created via any conversation script (brainstorm, debug, etc.)
- **THEN** `conversation:create` event is dispatched with the conversation path
- **AND** this replaces direct calls to `auto-embed.sh`

#### Scenario: Default on-create hook

- **WHEN** `conversation:create` event fires
- **AND** the default `10-embed.sh` hook is present in `on-create.d/`
- **THEN** it calls `cortext embed` on the conversation directory
- **AND** fails silently if `cortext` or RAG is not available

### Requirement: Git Hooks Installation

The system SHALL provide a CLI command to install git hooks.

The command `cortext hooks install` SHALL copy hook templates to `.git/hooks/`.

The installation SHALL preserve existing git hooks by appending, not overwriting.

The installation SHALL make the hooks executable.

#### Scenario: Installing git hooks on fresh repository

- **WHEN** user runs `cortext hooks install`
- **AND** no existing git hooks are present
- **THEN** pre-commit and post-checkout hooks are installed to `.git/hooks/`
- **AND** hooks are made executable
- **AND** success message is displayed

#### Scenario: Installing git hooks with existing hooks

- **WHEN** user runs `cortext hooks install`
- **AND** existing git hooks are present
- **THEN** Cortext hook code is appended to existing hooks
- **AND** existing functionality is preserved

### Requirement: Pre-commit Hook for Embedding

The system SHALL provide a pre-commit git hook that embeds staged markdown files.

The hook SHALL only process files that are staged for commit (not all files).

The hook SHALL run embedding with graceful degradation if dependencies are missing.

The hook SHALL not prevent commits if embedding fails.

#### Scenario: Pre-commit embeds staged files

- **WHEN** user commits files
- **AND** staged files include markdown files
- **THEN** each staged markdown file is embedded individually
- **AND** the commit proceeds regardless of embedding success

#### Scenario: Pre-commit with no cortext

- **WHEN** pre-commit hook runs
- **AND** `cortext` command is not available
- **THEN** hook exits silently with code 0
- **AND** commit proceeds normally

#### Scenario: Pre-commit performance

- **WHEN** pre-commit hook runs
- **THEN** only staged files are processed (not entire workspace)
- **AND** execution completes within reasonable time for typical commits

### Requirement: Post-checkout Hook for Rebuild

The system SHALL provide a post-checkout git hook that rebuilds missing embeddings.

The hook SHALL check if embedding data exists and rebuild if necessary.

The hook SHALL run in the background or be skippable to avoid blocking checkout.

#### Scenario: Post-checkout rebuilds embeddings

- **WHEN** user checks out a branch
- **AND** embedding data is missing for the current content
- **THEN** hook triggers a rebuild of embeddings
- **AND** displays informational message about rebuild

#### Scenario: Post-checkout skips if current

- **WHEN** user checks out a branch
- **AND** embeddings are already up to date
- **THEN** hook completes immediately without rebuild

### Requirement: CLI Hooks Command

The system SHALL provide a `cortext hooks` command group for managing hooks.

The command SHALL support the following subcommands:
- `install`: Install git hooks
- `run <event>`: Manually trigger an event
- `list`: List available hooks and their status
- `add <event> <name>`: Scaffold a new custom hook

#### Scenario: List hooks

- **WHEN** user runs `cortext hooks list`
- **THEN** displays all configured hooks grouped by event
- **AND** shows all scripts in each `.d/` directory with their order
- **AND** shows whether git hooks are installed

#### Scenario: Manual hook execution

- **WHEN** user runs `cortext hooks run conversation:create /path/to/dir`
- **THEN** the dispatcher is invoked with those arguments
- **AND** output from all hooks is displayed

#### Scenario: Add custom hook

- **WHEN** user runs `cortext hooks add conversation:create my-custom-hook`
- **THEN** creates `.workspace/hooks/conversation/on-create.d/50-my-custom-hook.sh`
- **AND** makes it executable
- **AND** includes a template with argument handling and graceful degradation pattern
- **AND** displays path and next steps

### Requirement: Graceful Degradation

All hooks SHALL implement graceful degradation when dependencies are unavailable.

Hooks SHALL check for required commands before executing and exit silently if missing.

Hooks SHALL not produce error output when degrading gracefully.

#### Scenario: RAG not installed

- **WHEN** any hook attempts to run `cortext embed`
- **AND** RAG dependencies are not installed
- **THEN** the operation is skipped silently
- **AND** hook exits with code 0

#### Scenario: Cortext not installed

- **WHEN** a git hook runs
- **AND** `cortext` command is not in PATH
- **THEN** hook exits silently with code 0
- **AND** git operation proceeds normally

### Requirement: Hooks Documentation

The system SHALL provide comprehensive documentation for the hooks system.

The documentation SHALL be located in the workspace at `.workspace/docs/hooks.md` or equivalent user-accessible location.

The documentation SHALL cover:
- All available hook events and their purposes
- How to create custom hooks with the `.d/` directory pattern
- Numeric prefix naming conventions and recommended ranges
- Execution order and fail-fast behavior
- Graceful degradation patterns for hook scripts
- Troubleshooting common issues

#### Scenario: Documentation created during init

- **WHEN** a workspace is initialized with hooks enabled
- **THEN** hooks documentation is created alongside the hooks directory
- **AND** the documentation includes examples for creating custom hooks

#### Scenario: Documentation covers custom hook creation

- **WHEN** a user reads the hooks documentation
- **THEN** they find step-by-step instructions for adding a custom hook
- **AND** the documentation explains the `cortext hooks add` command
- **AND** it provides a complete example hook script with argument handling

#### Scenario: Documentation explains execution model

- **WHEN** a user reads the hooks documentation
- **THEN** they understand that hooks in `.d/` directories run in alphanumeric order
- **AND** they understand that a failing hook stops the execution chain
- **AND** they understand the recommended prefix ranges (10-39 core, 40-69 user, 70-99 cleanup)

