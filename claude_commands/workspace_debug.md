---
description: Start a debugging conversation with investigative dialogue
tags: [workspace, debug, troubleshooting, conversation]
---

# Workspace Debug

You are helping the user debug through conversation in their Cortext workspace.

## Your Task

### 1. Initialize the Debug Session

- Ask: "What issue are you debugging?"
- Run the bash script to create the conversation:
  ```bash
  .workspace/scripts/bash/debug.sh "<issue>"
  ```
- This creates a minimal document

### 2. Investigate Through Dialogue

**This is collaborative investigation, not a checklist.**

- Ask about symptoms and context
- Help gather relevant information
- Suggest debugging approaches
- Work through hypotheses together
- Follow the investigation where it leads

**Keep investigating:**
- "What happens if we try...?"
- "Can you show me the error?"
- "When did this start happening?"
- "What changed recently?"

### 3. Document Findings in Real-Time

**Use the Edit tool as you investigate** to update the debug document:

- Add symptoms and context as discovered
- Document tests and their results
- Capture hypotheses (even ones ruled out)
- Note the solution when found
- Record insights for future reference

**Don't wait until solved** - document the investigation process as it happens.

### 4. Continue Until Resolved or Next Steps Clear

**Don't force premature conclusions.**

- Keep investigating as long as productive
- It's okay to not solve it in one session
- Document what was tried for next time
- Let the user decide when to pause

## Debugging Approaches

Use these techniques naturally:

- **Reproduce first** - Can we make it happen consistently?
- **Isolate** - What's the minimal case that shows the issue?
- **Binary search** - What changed between working and broken?
- **Compare** - How does this differ from what works?
- **Logs and errors** - What do they tell us?
- **Hypothesis testing** - Let's try X to see if Y

## Best Practices

- **Ask before assuming** - Get the full picture
- **Document as you go** - Don't lose investigation progress
- **Test one thing at a time** - Isolate variables
- **Consider simple causes first** - Occam's razor
- **Be methodical** - Track what's been tried
- **Capture learnings** - Even failed approaches teach us

## Session Management

**This conversation can be paused and resumed.**

When the user indicates they want to stop (e.g., "let's stop here", "I need to take a break", "let's pick this up later"):

1. Save the session using `/workspace.stop-conversation`
2. This preserves the investigation context for later resumption

**Or** the user can explicitly run `/workspace.stop-conversation` at any time.

**When detecting pause signals**, confirm with the user:
- "Would you like me to save this session so we can continue the investigation later?"
- If yes, use `/workspace.stop-conversation`
