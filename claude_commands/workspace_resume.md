---
description: Resume a previously paused conversation with full context
tags: [workspace, session, resume, continue, conversation]
---

# Workspace Resume

You are helping the user resume a previously paused conversation with full context restoration.

## Your Task

### 1. List Resumable Conversations

Find conversations with session state:
```bash
bash -c 'source .workspace/scripts/bash/common.sh && list_sessions' | jq -s '.'
```

This returns JSON with all sessions. Filter for active/paused status.

### 2. Display Options to User

Present the resumable conversations in a clear format:

```
Here are your resumable conversations:

1. [brainstorm] API Design Discussion
   Last active: 2 hours ago | Status: paused
   Summary: Exploring REST vs GraphQL, leaning toward REST

2. [debug] Auth Token Expiry Issue
   Last active: yesterday | Status: active
   Summary: Identified race condition in token refresh

3. [plan] Q1 Roadmap Planning
   Last active: 3 days ago | Status: paused
   Summary: Prioritized features, discussing resource allocation

Which conversation would you like to continue? (number or search term)
```

**Formatting notes:**
- Sort by last_active (most recent first)
- Show relative time (e.g., "2 hours ago", "yesterday")
- Show status badge
- Keep summaries to one line

### 3. Handle User Selection

When user selects a conversation:

1. **Load the session data**:
   ```bash
   bash -c 'source .workspace/scripts/bash/common.sh && load_session "<conversation-dir>"'
   ```

2. **Get the original command** from `agent_config.command` in the session

3. **Read the message history**:
   ```bash
   cat <conversation-dir>/.session/messages.jsonl
   ```

### 4. Resume with Context (Two-Phase Loading)

**CRITICAL: You must invoke the original command to get the proper system prompt.**

The resume flow:
1. Identify the original command (e.g., `/workspace.brainstorm`)
2. Tell the user you're loading that context
3. The system will load the command's instructions
4. Then inject the conversation context

**Tell the user:**
```
Resuming "[conversation-title]"...

Loading /workspace.brainstorm context...

[RESUMED CONVERSATION]
Conversation: brainstorm / API Design Discussion
Last active: 2 hours ago
Messages: 24 exchanges
Summary: Exploring REST vs GraphQL for internal APIs, leaning toward REST

I'm continuing where we left off. [Pick up the conversation naturally based on the summary and history]
```

### 5. Update Session Status

After loading, mark the session as active again:
```bash
source .workspace/scripts/bash/common.sh
update_session "<conversation-dir>" "active" "<message-count>" "<summary>"
```

### 6. Continue the Conversation

Now behave according to the original command's instructions:
- For brainstorm: Continue ideation, build on ideas
- For debug: Continue investigation
- For plan: Continue planning discussion

**Pick up naturally** - Reference where things left off and ask how to proceed.

## Handling Edge Cases

### No Resumable Conversations
```
No resumable conversations found.

Your conversations don't have session state saved yet. To enable resumption:
1. Start a new conversation (e.g., /workspace.brainstorm)
2. When you want to pause, use /workspace.stop-conversation

This saves your session so you can resume later.
```

### Search Instead of Number
If user types a search term instead of a number:
```bash
list_sessions | jq -s '[.[] | select(.id | contains("search-term") or .summary | contains("search-term"))]'
```

### Multiple Matches
If search returns multiple results, show them and ask user to pick.

### Conversation Not Found
```
I couldn't find a conversation matching "<search>".

Available conversations:
[list them]
```

## Example Complete Flow

```
User: /workspace.resume

You: [Run list_sessions]

     Here are your resumable conversations:

     1. [brainstorm] API Design Discussion
        Last active: 2 hours ago | Status: paused
        Summary: Exploring REST vs GraphQL, leaning toward REST

     2. [debug] Auth Token Expiry Issue
        Last active: yesterday | Status: active
        Summary: Identified race condition in token refresh

     Which conversation would you like to continue?

User: 1

You: [Load session for brainstorm/2025-11-22/001-brainstorm-api-design]
     [Read message history]
     [Update status to active]

     Resuming "API Design Discussion"...

     [RESUMED CONVERSATION]
     Conversation: brainstorm / API Design Discussion
     Last active: 2 hours ago
     Messages: 24 exchanges
     Summary: Exploring REST vs GraphQL for internal APIs, leaning toward REST

     I see we were comparing REST and GraphQL for your internal APIs,
     and you were leaning toward REST for its simplicity.

     Where would you like to pick up? We could:
     - Finalize the REST decision and move to endpoint design
     - Revisit the GraphQL option with specific concerns
     - Something else?

User: Let's finalize REST and start on endpoints

You: [Continue as a brainstorm session, building on the previous discussion]
```

## Technical Notes

- **Message history** is in `.session/messages.jsonl` (JSON Lines format)
- **Each line** is: `{"role": "user|assistant", "content": "...", "timestamp": "..."}`
- **Context summary** is in `session.json` under `context_summary`
- **Original command** is in `session.json` under `agent_config.command`
