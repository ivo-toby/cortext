## 1. Session Storage Foundation

- [x] 1.1 Define `session.json` schema with TypeScript types
- [x] 1.2 Define `messages.jsonl` format and parser
- [x] 1.3 Create session directory structure in conversation templates
- [x] 1.4 Add session utilities to `scripts/bash/common.sh`
  - `save_session()` - Write session state
  - `load_session()` - Read session state
  - `get_session_path()` - Resolve session directory

## 2. Conversation Command Updates

- [x] 2.1 Update `workspace_brainstorm.md` to save session on conversation end
- [x] 2.2 Update `workspace_debug.md` to save session on conversation end
- [x] 2.3 Update `workspace_plan.md` to save session on conversation end
- [x] 2.4 Update `workspace_learn.md` to save session on conversation end
- [x] 2.5 Update `workspace_meeting.md` to save session on conversation end
- [x] 2.6 Update `workspace_review.md` to save session on conversation end
- [x] 2.7 Add session save behavior to custom conversation type template

## 3. Session Commands Implementation

- [x] 3.1 Create `workspace_stop-conversation.md` slash command
  - Save current session state
  - Confirm save to user
  - Remind user about `/workspace.resume`
- [x] 3.2 Create `workspace_resume.md` slash command
  - List recent conversations with session state
  - Allow selection by number or search
  - Load and inject context on selection
- [x] 3.3 Add context injection template for resumed conversations
- [x] 3.4 Handle "no sessions found" gracefully

## 4. CLI Resume Command

- [x] 4.1 Add `cortext resume` command to CLI
  - Support resume by ID: `cortext resume 001-brainstorm-topic`
  - Support fuzzy search: `cortext resume "api design"`
  - Launch appropriate AI tool with context
- [x] 4.2 Add `--list` flag to show resumable conversations
- [x] 4.3 Add `--type` filter for conversation type
- [x] 4.4 Update CLI help and documentation

## 5. Registry and Status Updates

- [x] 5.1 Add `session_support: true` to conversation types in registry
- [x] 5.2 Update `workspace-status.sh` to show resumable conversations
- [x] 5.3 Add conversation status tracking (active/paused/completed)

## 6. Testing and Validation

- [x] 6.1 Test session save/load cycle for each conversation type
- [x] 6.2 Test resume with various message history sizes
- [x] 6.3 Test resume after system prompt changes
- [x] 6.4 Test `/workspace.resume` command flow
- [x] 6.5 Test `cortext resume` CLI command
- [x] 6.6 Verify git commits include session data correctly

## 7. Documentation

- [x] 7.1 Update README with resume workflow
- [x] 7.2 Document session data format for contributors
- [x] 7.3 Add troubleshooting for common resume issues
