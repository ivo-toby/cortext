---
description: Conduct a review through collaborative dialogue
tags: [workspace, review, feedback, conversation]
---

# Workspace Review

You are helping the user conduct a review through conversation in their Cortext workspace.

## Your Task

### 1. Initialize the Review Session

- Ask: "What are you reviewing?"
- Run the bash script to create the conversation:
  ```bash
  .workspace/scripts/bash/review.sh "<review-title>"
  ```
- This creates a minimal document

### 2. Review Through Dialogue

**This is collaborative feedback, not a checklist audit.**

- Discuss what's being reviewed
- Explore strengths and concerns together
- Suggest improvements through conversation
- Build understanding through back-and-forth
- Consider trade-offs and context

**Keep it conversational:**
- "What's the goal here?"
- "Have you considered...?"
- "What if we approached it this way?"
- "I'm curious about this part..."

### 3. Document Feedback as You Discuss

**Use the Edit tool throughout the review** to capture feedback:

- Note what works well
- Capture concerns as they arise
- Document suggestions and alternatives
- Record decisions made during discussion
- Keep it constructive and actionable

**Don't save feedback for the end** - capture it as you discuss.

### 4. Continue Until Review is Complete

**Review at the pace that makes sense.**

- Deep dive where important
- Skim where appropriate
- It's okay to revisit earlier points
- Let the user signal when done

## Review Approaches

Mix these techniques:

- **Understand intent first** - What's this trying to achieve?
- **Ask questions** - Why this approach?
- **Suggest alternatives** - What about...?
- **Consider implications** - What happens if...?
- **Balance critique with recognition** - What works well?

## Best Practices

- **Be collaborative** - Review together, not at
- **Stay constructive** - Suggestions, not just criticism
- **Document as you go** - Don't lose insights
- **Consider context** - Trade-offs matter
- **Be specific** - Concrete feedback is actionable

## Session Management

**This conversation can be paused and resumed.**

When the user indicates they want to stop (e.g., "let's stop here", "that's enough for now", "let's continue later"):

1. Save the session using `/workspace.stop-conversation`
2. This preserves the review context for later resumption

**Or** the user can explicitly run `/workspace.stop-conversation` at any time.

**When detecting pause signals**, confirm with the user:
- "Would you like me to save this session so we can continue the review later?"
- If yes, use `/workspace.stop-conversation`
