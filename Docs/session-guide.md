# Session Management Guide

This guide explains how to pause and resume conversations in Cortext with full context preservation.

## Overview

When you have a conversation with an AI agent in Cortext, the session management system allows you to:
- **Pause conversations** and come back later
- **Resume with full context** - the agent remembers what was discussed
- **Track conversation status** - active, paused, or completed

## Quick Start

### Pausing a Conversation

When you want to stop a conversation and save it for later:

```
/workspace.stop-conversation
```

The agent will:
1. Save the current session state
2. Confirm the save with a summary
3. Tell you how to resume

### Resuming a Conversation

To continue a paused conversation:

```
/workspace.resume
```

The agent will:
1. List your resumable conversations
2. Let you select one
3. Load the context and continue where you left off

### Using the CLI

```bash
# List all resumable conversations
cortext resume --list

# Filter by type
cortext resume --list --type brainstorm

# Resume by ID
cortext resume 001-brainstorm-api-design

# Resume by search
cortext resume "api design"
```

## How It Works

### Session Initialization

When you start any conversation (brainstorm, debug, plan, etc.), a session is automatically created:

```
001-brainstorm-api-design/
├── brainstorm.md           # Your conversation content
└── .session/
    ├── session.json        # Metadata and configuration
    └── messages.jsonl      # Chat history
```

### Session Data

**session.json** contains:
```json
{
  "version": "1.0",
  "conversation_id": "001-brainstorm-api-design",
  "conversation_type": "brainstorm",
  "status": "paused",
  "created_at": "2025-11-22T10:30:00Z",
  "last_active": "2025-11-22T11:45:00Z",
  "message_count": 24,
  "agent_config": {
    "command": "/workspace.brainstorm",
    "system_prompt_hash": "sha256:...",
    "model": "claude-sonnet-4-5-20250929",
    "tools": ["mcp__cortext__search_workspace"]
  },
  "context_summary": "Exploring REST vs GraphQL for internal APIs"
}
```

**messages.jsonl** contains chat history (JSON Lines format):
```jsonl
{"role": "user", "content": "Let's brainstorm API design", "timestamp": "2025-11-22T10:30:00Z"}
{"role": "assistant", "content": "Great! What's the core problem...", "timestamp": "2025-11-22T10:30:15Z"}
```

### Resume Flow

When you resume a conversation:

1. **Command loading** - The original slash command is invoked (e.g., `/workspace.brainstorm`)
2. **Context injection** - Session metadata and history are loaded
3. **Continuation** - Agent picks up naturally from where you stopped

## Session Status

Conversations can have three statuses:

| Status | Description |
|--------|-------------|
| `active` | Currently in progress |
| `paused` | Saved and waiting to resume |
| `completed` | Finished (can still resume if needed) |

## Automatic Save Detection

The agent can detect when you want to pause based on phrases like:
- "let's stop here"
- "that's enough for now"
- "I need to go"
- "let's continue later"

When detected, the agent will ask: "Would you like me to save this session?"

## Viewing Session Status

### In Workspace Status

```bash
.workspace/scripts/bash/workspace-status.sh
```

Shows:
- Total resumable sessions
- Count by status (active/paused/completed)
- Most recent sessions

### With CLI

```bash
cortext resume --list
```

Shows a table with:
- Conversation type
- ID
- Last active time
- Status
- Summary

## Troubleshooting

### "No resumable conversations found"

**Cause:** No conversations have session state saved yet.

**Solution:**
1. Start a new conversation
2. Use `/workspace.stop-conversation` to save it
3. Then you can resume it later

### Session not loading correctly

**Cause:** The session.json file may be corrupted or missing fields.

**Solution:**
1. Check the session file exists: `ls <conversation-dir>/.session/`
2. Verify session.json is valid JSON: `jq . <conversation-dir>/.session/session.json`
3. If corrupted, you can still access the conversation markdown file

### Agent doesn't remember context

**Cause:** The message history may not have been saved.

**Solution:**
1. Check messages.jsonl exists and has content
2. Ensure you used `/workspace.stop-conversation` before ending the session
3. The markdown file still contains your documented ideas

### Command changed since last session

**Cause:** The slash command was updated after you paused.

**Note:** This is expected behavior. The agent will use the current version of the command, which may include improvements. The session data tracks the original command hash so you can see if it changed.

## Best Practices

### When to Pause

- Before leaving for a break
- When switching to a different task
- At natural stopping points in the conversation
- When you need to think and come back

### Writing Good Summaries

When you pause, the agent creates a context summary. You can influence this by:
- Clearly stating where you are: "We've decided on REST, now we need to design endpoints"
- Mentioning pending decisions: "Still need to choose between option A and B"

### Managing Many Sessions

- Use `--type` filter to focus on specific conversation types
- Search by topic when you have many sessions
- Consider marking old sessions as "completed" to reduce clutter

## Git Integration

Session data is committed alongside conversation content:

```bash
git add <conversation-dir>/.session/
git commit -m "[session] Pause: API Design Discussion"
```

This means:
- Sessions are version controlled
- You can see session history in git log
- Sessions sync across machines if you push

## Privacy Considerations

Session data includes your full conversation history in plaintext. Consider:
- Adding `.session/` to `.gitignore` if you don't want to track sessions
- Being mindful of sensitive information in conversations
- The data stays local unless you push to a remote repository
