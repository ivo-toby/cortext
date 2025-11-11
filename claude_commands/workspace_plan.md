---
description: Start a planning conversation for collaborative feature/project planning
tags: [workspace, planning, features, conversation]
---

# Workspace Plan

You are helping the user plan through conversation in their Cortext workspace.

## Your Task

### 1. Initialize the Planning Session

- Ask: "What are you planning?"
- Run the bash script to create the conversation:
  ```bash
  .workspace/scripts/bash/plan.sh "<feature-name>"
  ```
- This creates a minimal document

### 2. Plan Collaboratively Through Dialogue

**This is iterative planning, not upfront specification.**

- Discuss goals and desired outcomes
- Explore different approaches together
- Break down the work collaboratively
- Surface concerns and trade-offs
- Refine as you discuss

**Keep planning conversational:**
- "What are we trying to achieve?"
- "How might we approach this?"
- "What concerns do you have?"
- "Should we break that down further?"

### 3. Refine the Plan During Conversation

**Use the Edit tool throughout** to update the plan document:

- Add goals as they're clarified
- Document approaches as you explore them
- Break down tasks as you identify them
- Capture decisions and rationale
- Note trade-offs and considerations

**Don't finalize upfront** - let the plan evolve through dialogue.

### 4. Iterate Until Direction is Clear

**Planning is iterative, not one-shot.**

- Refine as you discuss
- It's okay to revise earlier ideas
- Let ambiguity surface through conversation
- Continue until the user feels ready to start

## Planning Approaches

Mix these naturally:

- **Start with why** - What problem are we solving?
- **Think big, start small** - What's the MVP?
- **Consider alternatives** - What other approaches exist?
- **Identify risks** - What could go wrong?
- **Break it down** - What are the concrete steps?

## Best Practices

- **Collaborate, don't dictate** - Plan together
- **Update plan as it evolves** - Living document
- **Surface assumptions** - Make thinking explicit
- **Consider trade-offs** - No perfect solutions
- **Stay flexible** - Plans change, that's normal
