---
description: Save and pause the current conversation for later resumption
tags: [workspace, session, pause, save, conversation]
---

# Workspace Stop Conversation

You are saving the current conversation session so it can be resumed later with full context.

## Your Task

### 1. Identify the Active Conversation

Find the conversation you've been working on in this session:
- Look for the conversation directory you created or have been editing
- The path should be something like: `<type>/YYYY-MM-DD/###-type-topic/`

### 2. Save the Session State

Use the bash utilities to save the session. You need to:

1. **Count the messages exchanged** - Estimate based on conversation turns
2. **Write a context summary** - 1-2 sentences describing where the conversation stopped
3. **Update the session status to "paused"**

Run this command (adjust values for your conversation):
```bash
bash -c 'source .workspace/scripts/bash/common.sh && update_session "<conversation-dir>" "paused" "<message-count>" "<context-summary>"'
```

Example:
```bash
bash -c 'source .workspace/scripts/bash/common.sh && update_session "brainstorm/2025-11-22/001-brainstorm-api-design" "paused" "24" "Exploring REST vs GraphQL for internal APIs, leaning toward REST for simplicity"'
```

### 3. Commit the Session

Stage and commit the session data:
```bash
git add <conversation-dir>/.session/
git commit -m "[session] Pause: <conversation-title>"
```

### 4. Confirm to User

After saving, tell the user:

```
Session saved.

Conversation "<title>" has been paused.
You can continue later with /workspace.resume

Summary: <your context summary>
```

## Important Notes

- **Context summary should capture where things left off** - What was being discussed? What decisions were pending? What was the last topic?
- **Message count is an estimate** - Count major exchanges, not every back-and-forth
- **The .session directory stores**:
  - `session.json` - Metadata and status
  - `messages.jsonl` - Chat history (if you've been appending messages)

## Example Flow

```
User: /workspace.stop-conversation

You: [Find the active conversation - brainstorm/2025-11-22/001-brainstorm-api-design]
     [Run update_session command]
     [Commit the session]

     Session saved.

     Conversation "API Design Discussion" has been paused.
     You can continue later with /workspace.resume

     Summary: We were exploring REST vs GraphQL for internal APIs,
     with a leaning toward REST for its simplicity. Next step was
     to discuss specific endpoint design.
```
