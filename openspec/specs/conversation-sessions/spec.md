# conversation-sessions Specification

## Purpose
TBD - created by archiving change add-conversation-resumption. Update Purpose after archive.
## Requirements
### Requirement: Session State Persistence
Each conversation SHALL persist its session state to enable resumption with full agent context.

**ID:** `SESS-001` | **Priority:** High

#### Scenario: Session state saved when conversation ends

- **GIVEN** a user is in an active brainstorm conversation
- **WHEN** they indicate the conversation should pause or end
- **THEN** the system MUST save session state to `.session/session.json`
- **AND** the system MUST save message history to `.session/messages.jsonl`
- **AND** the session status MUST be set to "paused" or "completed"

#### Scenario: Session includes agent configuration

- **GIVEN** a conversation session is being saved
- **WHEN** the session state is written
- **THEN** it MUST include the command used (e.g., `/workspace.brainstorm`)
- **AND** it MUST include a hash of the system prompt version
- **AND** it MUST include the model identifier used
- **AND** it MUST include the list of MCP tools available

#### Scenario: Message history format

- **GIVEN** a conversation with multiple exchanges
- **WHEN** message history is persisted
- **THEN** each message MUST be stored as a JSON line with role, content, and timestamp
- **AND** the format MUST be JSON Lines (`.jsonl`)
- **AND** messages MUST be in chronological order

**Example:**
```
conversations/2025-11-22/001-brainstorm-topic/
├── brainstorm.md
└── .session/
    ├── session.json
    └── messages.jsonl
```

---

### Requirement: Stop Conversation Command
Users SHALL be able to explicitly save and pause conversations with clear feedback.

**ID:** `SESS-002` | **Priority:** High

#### Scenario: Explicit stop command

- **GIVEN** a user is in an active conversation
- **WHEN** they run `/workspace.stop-conversation`
- **THEN** the system MUST save the current session state
- **AND** the agent MUST confirm the save was successful
- **AND** the agent MUST inform the user they can resume with `/workspace.resume`

#### Scenario: Stop command feedback

- **GIVEN** a conversation session is saved via stop command
- **WHEN** the agent confirms the save
- **THEN** the confirmation MUST include the conversation title
- **AND** the confirmation MUST mention `/workspace.resume`
- **AND** the agent SHOULD provide a brief summary of where the conversation stopped

**Example:**
```
User: /workspace.stop-conversation

Claude: Session saved.

Conversation "API Design Discussion" has been paused.
You can continue later with /workspace.resume

Summary: We were exploring REST vs GraphQL, leaning toward REST for simplicity.
```

---

### Requirement: Resume Command
Users SHALL be able to resume paused conversations through a dedicated command with full context restoration.

**ID:** `SESS-003` | **Priority:** High

#### Scenario: List resumable conversations

- **GIVEN** a user runs `/workspace.resume`
- **WHEN** resumable conversations exist in the workspace
- **THEN** the agent MUST display a list of conversations with session state
- **AND** each entry MUST show: type, title, last active time, status, and summary
- **AND** conversations MUST be sorted by last activity (most recent first)

#### Scenario: Resume by selection

- **GIVEN** a user is viewing the list of resumable conversations
- **WHEN** they select a conversation by number or search term
- **THEN** the agent MUST load the session state for that conversation
- **AND** the agent MUST inject the conversation context
- **AND** the agent MUST continue the conversation naturally

#### Scenario: Command loading on resume

- **GIVEN** a conversation is being resumed
- **WHEN** the system processes the resume request
- **THEN** it MUST read the original command from session state (e.g., `/workspace.brainstorm`)
- **AND** it MUST invoke that command to load the agent's system prompt
- **AND** it MUST then inject the conversation context and history
- **AND** the agent MUST have the same behavioral instructions as the original conversation

#### Scenario: Context injection on resume

- **GIVEN** a conversation is being resumed
- **WHEN** the agent receives the resume request after command loading
- **THEN** it MUST receive a context block with conversation metadata
- **AND** it MUST receive the full message history
- **AND** it MUST receive a summary of where the conversation left off
- **AND** the agent MUST acknowledge the resumption and continue appropriately

#### Scenario: Command prompt changes since original conversation

- **GIVEN** a conversation was started with a command that has since been updated
- **WHEN** the user resumes that conversation
- **THEN** the system MUST use the current version of the command
- **AND** the system SHOULD detect if the prompt changed (via stored hash)
- **AND** the system MAY warn the user that the agent's instructions have changed

#### Scenario: No resumable conversations

- **GIVEN** a user runs `/workspace.resume`
- **WHEN** no conversations have session state
- **THEN** the agent MUST inform the user that no resumable conversations exist
- **AND** it SHOULD suggest starting a new conversation

**Example interaction:**
```
User: /workspace.resume

Claude: Here are your resumable conversations:

1. [brainstorm] API Design Discussion
   Last active: 2 hours ago | Status: paused
   Summary: Exploring REST vs GraphQL, leaning toward REST

2. [debug] Auth Token Expiry Issue
   Last active: yesterday | Status: active
   Summary: Identified race condition in token refresh

Which conversation would you like to continue? (number or search)

User: 1

Claude: [Resuming "API Design Discussion"]

I see we were discussing REST vs GraphQL for your internal APIs,
and you were leaning toward REST for its simplicity.

Where would you like to pick up? We could:
- Finalize the REST decision and move to endpoint design
- Revisit the GraphQL option with specific concerns
- Something else?
```

---

### Requirement: CLI Resume Support
The Cortext CLI SHALL provide a command to resume conversations directly.

**ID:** `SESS-004` | **Priority:** Medium

#### Scenario: Resume by conversation ID

- **GIVEN** a user knows the conversation ID
- **WHEN** they run `cortext resume 001-brainstorm-topic`
- **THEN** the system MUST locate the conversation
- **AND** the system MUST launch the appropriate AI tool
- **AND** the session context MUST be pre-loaded

#### Scenario: Resume by search

- **GIVEN** a user wants to find a conversation by topic
- **WHEN** they run `cortext resume "api design"`
- **THEN** the system MUST search conversation titles and summaries
- **AND** if one match is found, it MUST resume that conversation
- **AND** if multiple matches are found, it MUST prompt for selection

#### Scenario: List resumable conversations

- **GIVEN** a user wants to see what can be resumed
- **WHEN** they run `cortext resume --list`
- **THEN** the system MUST display all conversations with session state
- **AND** it MUST show ID, type, title, status, and last active time

---

### Requirement: Session Lifecycle Management
The system SHALL track conversation session status and manage transitions appropriately.

**ID:** `SESS-005` | **Priority:** Medium

#### Scenario: Status transitions

- **GIVEN** a conversation has session state
- **WHEN** the session status changes
- **THEN** valid status values MUST be: "active", "paused", "completed"
- **AND** transitions MUST be: active -> paused, active -> completed, paused -> active, paused -> completed

#### Scenario: Auto-pause on inactivity

- **GIVEN** a conversation is in "active" status
- **WHEN** no activity occurs for a configurable period (default: 5 minutes)
- **THEN** the system SHOULD save the session with "paused" status
- **AND** the user SHOULD be informed that the session was auto-saved

#### Scenario: Completed conversations

- **GIVEN** a conversation is marked as "completed"
- **WHEN** a user attempts to resume it
- **THEN** the system SHOULD warn that the conversation was marked complete
- **AND** the user SHOULD be able to override and resume anyway

---

### Requirement: Git Integration for Sessions
Session data SHALL be included in git commits alongside conversation content.

**ID:** `SESS-006` | **Priority:** Low

#### Scenario: Session committed with conversation

- **GIVEN** a conversation is saved with session state
- **WHEN** the conversation is committed to git
- **THEN** the `.session/` directory MUST be included in the commit
- **AND** the commit message SHOULD indicate session state was saved

#### Scenario: Session-only updates

- **GIVEN** a conversation is resumed and then paused again
- **WHEN** only the session state has changed (not the markdown)
- **THEN** the system MAY commit just the session updates
- **AND** the commit message SHOULD indicate "session update"

