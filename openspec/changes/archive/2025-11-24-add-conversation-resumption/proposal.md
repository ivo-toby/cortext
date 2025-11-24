# Change: Add Conversation Session Resumption

## Why

When a user has a brainstorm or other conversation with an agent in Cortext, they can save the conversation content as markdown. However, if they want to return to that conversation later, the agent loses all context - it doesn't know what tools it had access to, what the system prompt was, or what was discussed in the conversation. This makes "resuming" conversations effectively impossible, forcing users to re-explain context and losing the continuity of thought that makes extended conversations valuable.

This is a fundamental limitation that undermines the core value proposition of Cortext as a conversation-first workspace.

## What Changes

### New Capability: Session State Persistence
- **Session storage**: Each conversation folder gets a `.session/` directory with structured state
- **Agent config capture**: Persist the system prompt, model, and tool access used during conversation
- **Message history**: Store the actual chat messages, not just the summarized markdown
- **Resume metadata**: Track conversation status, last activity, and continuation tokens

### New UX: Session Commands
- **`/workspace.stop-conversation`**: Explicitly save and pause the current conversation
- **`/workspace.resume`**: List and select conversations to continue
- **`cortext resume`**: CLI command for direct resumption by ID or search
- **Context injection**: When resuming, agent receives full prior context automatically
- **User feedback**: Clear confirmation when session is saved, with instructions to resume

### Updated Workflows
- **Save on exit**: Conversations auto-save session state when ending
- **Status tracking**: Conversations track "active", "paused", "completed" states
- **History pruning**: Optionally trim old message history while preserving key insights

## Impact

- **Affected specs**:
  - New spec: `conversation-sessions` (session state and resumption)
  - Modified: `conversation-workflows` (add resume behavior)

- **Affected code**:
  - `scripts/bash/*.sh` - Add session save/load
  - `claude_commands/workspace_*.md` - Add save behavior to all conversation types
  - `claude_commands/workspace_resume.md` - New resume command
  - `src/cortext_cli/commands/` - Add `resume` CLI command
  - `.workspace/templates/` - Session directory structure
  - Registry - Track session capabilities per conversation type

- **Breaking changes**: None - existing conversations work as before, just without session state
